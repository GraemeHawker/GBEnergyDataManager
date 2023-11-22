# -*- coding: utf-8 -*-
"""
command to generate annual datafiles for given data subsets
"""
import datetime as dt
import pandas as pd
import numpy as np
import pytz
import psycopg2
from sqlalchemy import create_engine
import os
from tqdm import tqdm
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from GBEnergyDataManager.settings import BASE_DIR, DATABASES, NETA_USER, NETA_PWD, NETA_BMU_LIST_URL, DATA_SUMMARY_LOCS


def email_log(log_dict):
    pass


class Command(BaseCommand):
    help = 'downloads BMRA data for specific date range, expected 2 arguments of form yyyy-m-d'

    def add_arguments(self, parser):
        parser.add_argument('subset', nargs=1, type=str)
        parser.add_argument('year', nargs=1, type=int)

    def handle(self, *args, **options):
        log = {}
        self.stdout.write('{:%Y-%m-%d %H:%M:%S} Started'.format(dt.datetime.now()))
        log['{:%Y-%m-%d %H:%M:%S}'.format(dt.datetime.now())] = 'Started'

        # set up start and end dates
        # if fetching data for current year, then set end date to yesterday
        # a value of 0 means current year
        year = options['year'][0]
        if year == 0:
            year = dt.date.today().year
        start_date = dt.date(year, 1, 1)
        if year == (dt.date.today() - dt.timedelta(days=1)).year:
            end_date = dt.date.today() - dt.timedelta(days=1)
        else:
            end_date = dt.date(year, 12, 31)

        # check if year folder exists, if not create it
        save_path = os.path.join(DATA_SUMMARY_LOCS[options['subset'][0]], str(year))
        self.stdout.write('{:%Y-%m-%d %H:%M:%S} saving to {}'.format(dt.datetime.now(),
                                                                     save_path))
        log['{:%Y-%m-%d %H:%M:%S}'.format(dt.datetime.now())] = 'Saving to {}'.format(save_path)
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        # set up blank DataFrame
        self.stdout.write('{:%Y-%m-%d %H:%M:%S} Creating blank dataframe'.format(dt.datetime.now()))
        log['{:%Y-%m-%d %H:%M:%S}'.format(dt.datetime.now())] = 'Creating blank dataframe'

        # create list of clock change dates
        transition_days = [dt.date(x.year, x.month, x.day) for x in
                           pytz.timezone('Europe/London')._utc_transition_times]

        # set up blank dataframe, with settlement periods as index
        # and subset BMUIDs as columns
        if options['subset'][0] == 'scotland':
            #bmus_df = pd.read_csv(os.path.join(BASE_DIR, 'Physical/unit_data/scottish_BMUs_190731.csv'))
            #BMU_types = pd.read_csv(os.path.join(BASE_DIR, 'Physical/unit_data/scottish_BMUs_190731.csv'), index_col=0)
            #bmu_ids = bmus_df['BMU ID'].values
            bmus_df = pd.read_csv(os.path.join(BASE_DIR, 'Physical/unit_data/Generators.csv'))
            BMU_types = pd.read_csv(os.path.join(BASE_DIR, 'Physical/unit_data/Generators.csv'), index_col=1)
            bmu_ids = bmus_df[((bmus_df['GSP region']=='South Scotland')
                               |(bmus_df['GSP region']=='North Scotland'))
                              &(bmus_df.Type != 'Unknown')
                              &((bmus_df.BMU.str.startswith('E'))
                                |(bmus_df.BMU.str.startswith('M'))
                                |(bmus_df.BMU.str.startswith('T')))].BMU.values
        elif options['subset'][0] == 'wind':
            bmus_df = pd.read_csv(os.path.join(BASE_DIR, 'Physical/unit_data/Generators.csv'))
            BMU_types = pd.read_csv(os.path.join(BASE_DIR, 'Physical/unit_data/Generators.csv'), index_col=1)
            bmu_ids = bmus_df[((bmus_df.Type == 'Wind (Offshore)')
                               | (bmus_df.Type == 'Wind (Onshore)'))
                              & ((bmus_df.BMU.str.startswith('E'))
                                 | (bmus_df.BMU.str.startswith('M'))
                                 | (bmus_df.BMU.str.startswith('T')))].BMU.values
        else:
            log['{:%Y-%m-%d %H:%M:%S}'.format(dt.datetime.now())] = 'FAILED: subset {} not recognised'.format(
                options['subset'][0])
            raise ValueError('subset {} not recognised'.format(options['subset'][0]))

        blank_df = pd.DataFrame(columns=['sd', 'sp'])
        curr_date = start_date
        while curr_date <= end_date:
            curr_sp = 1
            if curr_date in [x for x in transition_days if x.month < 6]:  # clocks go forward
                max_sp = 46
            elif curr_date in [x for x in transition_days if x.month > 6]:  # clocks go back
                max_sp = 50
            else:
                max_sp = 48
            while curr_sp <= max_sp:
                new_data = pd.DataFrame([[pd.to_datetime(curr_date), curr_sp]], columns=['sd', 'sp'])
                #blank_df = blank_df.append(new_data)
                blank_df = pd.concat([blank_df, new_data])
                curr_sp += 1
            curr_date += dt.timedelta(days=1)
        blank_df = blank_df.set_index(['sd', 'sp'])
        for bmu_id in bmu_ids:
            blank_df[bmu_id] = np.nan

        # connect to DB
        # --TODO: convert to ORM
        conn = create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(DATABASES['default']['USER'],
                                                                                       DATABASES['default']['PASSWORD'],
                                                                                        DATABASES['default']['HOST'],
                                                                                        DATABASES['default']['PORT'],
                                                                                        DATABASES['default']['NAME'],
                                                                                         )) 
        #conn = psycopg2.connect("dbname='ElexonData' user={} host={} password={}".format(DATABASES['default']['USER'],
        #                                                                                 DATABASES['default']['HOST'],
        #                                                                                 DATABASES['default'][
        #                                                                                     'PASSWORD']))
        #cur = conn.cursor()

        # generate bid acceptance values
        self.stdout.write('{:%Y-%m-%d %H:%M:%S} Generating BAVs'.format(dt.datetime.now()))
        combined_BAVs = blank_df.copy()

        bav_query = 'SELECT sd, sp, sum(bmra_boav.bv) \
        FROM public.bmra_boav \
        where bmra_boav.bmu_id=\'{}\' \
        and sd>=\'{:%Y-%m-%d}\' \
        and sd<=\'{:%Y-%m-%d}\' \
        group by sd, sp \
        order by sd, sp'

        for bmu_id in tqdm(bmu_ids, desc='total'):
            sql_df = pd.read_sql(bav_query.format(bmu_id, start_date, end_date), conn)
            sql_df = sql_df.set_index(['sd', 'sp'])
            combined_BAVs[bmu_id] = sql_df

        combined_BAVs.to_csv(os.path.join(save_path, 'BAVs.csv'))

        # generate offer acceptance values
        self.stdout.write('{:%Y-%m-%d %H:%M:%S} Generating OAVs'.format(dt.datetime.now()))
        combined_OAVs = blank_df.copy()

        oav_query = 'SELECT sd, sp, sum(bmra_boav.ov) \
        FROM public.bmra_boav \
        where bmra_boav.bmu_id=\'{}\' \
        and sd>=\'{:%Y-%m-%d}\' \
        and sd<=\'{:%Y-%m-%d}\' \
        group by sd, sp \
        order by sd, sp'

        for bmu_id in tqdm(bmu_ids, desc='total'):
            sql_df = pd.read_sql(oav_query.format(bmu_id, start_date, end_date), conn)
            sql_df = sql_df.set_index(['sd', 'sp'])
            combined_OAVs[bmu_id] = sql_df

        combined_OAVs.to_csv(os.path.join(save_path, 'OAVs.csv'))

        # generate FPN values
        self.stdout.write('{:%Y-%m-%d %H:%M:%S} Generating FPNs'.format(dt.datetime.now()))
        combined_FPNs = blank_df.copy()

        query = 'SELECT sd, sp, bmra_fpnlevel.ts, vp \
        FROM public.bmra_fpnlevel \
        left join public.bmra_fpn \
        on bmra_fpnlevel.fpn_id = bmra_fpn.id \
        where bmra_fpn.bmu_id=\'{}\' \
        and sd>=\'{:%Y-%m-%d}\' \
        and sd<=\'{:%Y-%m-%d}\' \
        order by sd, sp, bmra_fpnlevel.ts'

        for bmu_id in tqdm(bmu_ids, desc='total'):
            bmu_fpns = []
            df = pd.read_sql(query.format(bmu_id,
                                          start_date - dt.timedelta(days=1),
                                          end_date + dt.timedelta(days=1)),
                             conn)
            prev_SD, prev_SP, prev_VP, prev_TS = None, None, None, None
            total_mwh = 0.0
            for key, values in df.iterrows():
                SD, SP, TS, VP = values['sd'], values['sp'], values['ts'], values['vp']
                if SD == prev_SD and SP == prev_SP:
                    time_diff = (TS - prev_TS).total_seconds() / 3600.0
                    total_mwh += (prev_VP * time_diff + (0.5 * (VP - prev_VP) * time_diff))
                elif prev_SD is not None and prev_SP is not None:
                    bmu_fpns.append([dt.date(prev_SD.year, prev_SD.month, prev_SD.day), prev_SP, total_mwh])
                    #bmu_fpns = pd.concat([bmu_fpns, pd.DataFrame([dt.date(prev_SD.year, prev_SD.month, prev_SD.day), prev_SP, total_mwh])])
                    total_mwh = 0.0
                prev_SD, prev_SP, prev_VP, prev_TS = SD, SP, VP, TS
            new_data = pd.DataFrame(bmu_fpns, columns=['sd', 'sp', bmu_id])
            new_data = new_data.set_index(['sd', 'sp'])
            combined_FPNs.update(new_data)

        combined_FPNs.to_csv(os.path.join(save_path, 'FPNs.csv'))

        # generate MELvalues
        self.stdout.write('{:%Y-%m-%d %H:%M:%S} Generating MELs'.format(dt.datetime.now()))
        combined_MELs = blank_df.copy()

        query = 'SELECT bmra_mel.ts as tsr, sd, sp, bmra_mellevel.ts, ve \
        FROM public.bmra_mellevel \
        left join public.bmra_mel \
        on bmra_mellevel.mel_id = bmra_mel.id \
        where bmra_mel.bmu_id=\'{}\' \
        and sd>=\'{:%Y-%m-%d}\' \
        and sd<=\'{:%Y-%m-%d}\' \
        order by sd, sp, bmra_mel.ts desc, bmra_mellevel.ts'

        for bmu_id in tqdm(bmu_ids, desc='total'):
            bmu_mels = []
            df = pd.read_sql(query.format(bmu_id,
                                          start_date - dt.timedelta(days=1),
                                          end_date + dt.timedelta(days=1)),
                             conn)
            prev_SD, prev_SP, prev_VP, prev_TS, prev_TSR, last_msg_time = None, None, None, None, None, None
            total_mwh, total_time = 0.0, 0.0
            for key, values in df.iterrows():
                SD, SP, TS, VP, TSR = values['sd'], values['sp'], values['ts'], values['ve'], values['tsr']
                if SD == prev_SD and SP == prev_SP:
                    if TSR == last_msg_time:
                        time_diff = (TS - prev_TS).total_seconds() / 3600.0
                        total_mwh += (prev_VP * time_diff + (0.5 * (VP - prev_VP) * time_diff))
                        total_time += time_diff
                elif prev_SD is not None and prev_SP is not None:
                    bmu_mels.append([dt.date(prev_SD.year, prev_SD.month, prev_SD.day), prev_SP, total_mwh])
                    #bmu_mels = pd.concat([bmu_mels, pd.DataFrame([dt.date(prev_SD.year, prev_SD.month, prev_SD.day), prev_SP, total_mwh])])
                    # if not math.isclose(0.5, total_time, rel_tol=1e-5):
                    #    print(prev_SD, prev_SP)
                    #    print('total time duration: {:+06.2f}'.format(total_time))
                    total_mwh, total_time = 0.0, 0.0
                    last_msg_time = values['tsr']
                prev_SD, prev_SP, prev_VP, prev_TS = SD, SP, VP, TS
            new_data = pd.DataFrame(bmu_mels, columns=['sd', 'sp', bmu_id])
            new_data = new_data.set_index(['sd', 'sp'])
            combined_MELs.update(new_data)

        combined_MELs.to_csv(os.path.join(save_path, 'MELs.csv'))

        # calculate cashflow by settlement period
        self.stdout.write('{:%Y-%m-%d %H:%M:%S} Generating cashflows'.format(dt.datetime.now()))
        combined_cashflows = blank_df.copy()

        query = 'SELECT sd, sp, sum(oc) as cashflow \
        FROM public.bmra_ebocf \
        where bmu_id=\'{}\' \
        and sd>=\'{:%Y-%m-%d}\' \
        and sd<=\'{:%Y-%m-%d}\' \
        group by sd, sp \
        order by sd, sp;'

        for bmu_id in tqdm(bmu_ids, desc='total'):
            sql_df = pd.read_sql(query.format(bmu_id,
                                              start_date,
                                              end_date),
                                 conn)
            sql_df = sql_df.set_index(['sd', 'sp'])
            sql_df.rename(columns={'cashflow': bmu_id}, inplace=True)
            combined_cashflows.update(sql_df)

        combined_cashflows.to_csv(os.path.join(save_path, 'offer_cashflows.csv'))

        combined_cashflows = blank_df.copy()

        query = 'SELECT sd, sp, sum(bc) as cashflow \
                FROM public.bmra_ebocf \
                where bmu_id=\'{}\' \
                and sd>=\'{:%Y-%m-%d}\' \
                and sd<=\'{:%Y-%m-%d}\' \
                group by sd, sp \
                order by sd, sp;'

        for bmu_id in tqdm(bmu_ids, desc='total'):
            sql_df = pd.read_sql(query.format(bmu_id,
                                              start_date,
                                              end_date),
                                 conn)
            sql_df = sql_df.set_index(['sd', 'sp'])
            sql_df.rename(columns={'cashflow': bmu_id}, inplace=True)
            combined_cashflows.update(sql_df)

        combined_cashflows.to_csv(os.path.join(save_path, 'bid_cashflows.csv'))

        # calculate P114 metered values by settlement period
        self.stdout.write('{:%Y-%m-%d %H:%M:%S} Generating metered values'.format(dt.datetime.now()))
        combined_metered = blank_df.copy()

        P114_query = 'select distinct p114_abv.sd as sd, p114_abp.sp as sp, vol \
        from p114_abv \
        left join p114_abp \
        on p114_abv.id = p114_abp.abv_id \
        left join p114_sr_type \
        on p114_abv.sr_type_id = p114_sr_type.id \
        inner join \
        (SELECT sd, sp, max(p114_sr_type.order) as ordinal \
        FROM p114_abv \
        left join p114_abp \
        on p114_abv.id = p114_abp.abv_id \
        left join p114_sr_type \
        on p114_abv.sr_type_id = p114_sr_type.id \
        where bmu_id=\'{}\' \
        and p114_abv.sd>=\'{}\' \
        and p114_abv.sd<=\'{}\' \
        group by sd, sp \
        order by sd, sp) as inner_query \
        on inner_query.sd = p114_abv.sd \
        and inner_query.sp = p114_abp.sp \
        and inner_query.ordinal = p114_sr_type.order \
        where bmu_id=\'{}\' \
        and p114_abv.sd>=\'{}\' \
        and p114_abv.sd<=\'{}\' \
        order by sd, sp;'

        for bmu_id in tqdm(bmu_ids, desc='total'):
            sql_df = pd.read_sql(P114_query.format(bmu_id,
                                                   start_date.strftime('%Y-%m-%d'),
                                                   end_date.strftime('%Y-%m-%d'),
                                                   bmu_id,
                                                   start_date.strftime('%Y-%m-%d'),
                                                   end_date.strftime('%Y-%m-%d')), conn)
            sql_df = sql_df.set_index(['sd', 'sp'])
            sql_df.rename(columns={'vol': bmu_id}, inplace=True)
            combined_metered[bmu_id] = sql_df

        combined_metered.to_csv(os.path.join(save_path, 'metered.csv'))

        # generate monthly summaries by BMU
        self.stdout.write('{:%Y-%m-%d %H:%M:%S} Generating monthly BMU aggregate values'.format(dt.datetime.now()))
        combined_BAVs.groupby(level=0).sum().groupby(pd.Grouper(freq='M')).sum().to_csv(
            os.path.join(save_path, 'monthly_BAVs.csv'))
        combined_OAVs.groupby(level=0).sum().groupby(pd.Grouper(freq='M')).sum().to_csv(
            os.path.join(save_path, 'monthly_OAVs.csv'))
        combined_FPNs.groupby(level=0).sum().groupby(pd.Grouper(freq='M')).sum().to_csv(
            os.path.join(save_path, 'monthly_FPNs.csv'))
        combined_MELs.groupby(level=0).sum().groupby(pd.Grouper(freq='M')).sum().to_csv(
            os.path.join(save_path, 'monthly_MELs.csv'))
        combined_cashflows.groupby(level=0).sum().groupby(pd.Grouper(freq='M')).sum().to_csv(
            os.path.join(save_path, 'monthly_cashflows.csv'))
        combined_metered.groupby(level=0).sum().groupby(pd.Grouper(freq='M')).sum().to_csv(
            os.path.join(save_path, 'monthly_metered.csv'))

        # generate daily summaries by BMU
        self.stdout.write('{:%Y-%m-%d %H:%M:%S} Generating daily BMU aggregate values'.format(dt.datetime.now()))
        combined_BAVs.groupby(level=0).sum().groupby(pd.Grouper(freq='D')).sum().to_csv(
            os.path.join(save_path, 'daily_BAVs.csv'))
        combined_OAVs.groupby(level=0).sum().groupby(pd.Grouper(freq='D')).sum().to_csv(
            os.path.join(save_path, 'daily_OAVs.csv'))
        combined_FPNs.groupby(level=0).sum().groupby(pd.Grouper(freq='D')).sum().to_csv(
            os.path.join(save_path, 'daily_FPNs.csv'))
        combined_MELs.groupby(level=0).sum().groupby(pd.Grouper(freq='D')).sum().to_csv(
            os.path.join(save_path, 'daily_MELs.csv'))
        combined_cashflows.groupby(level=0).sum().groupby(pd.Grouper(freq='D')).sum().to_csv(
            os.path.join(save_path, 'daily_cashflows.csv'))
        combined_metered.groupby(level=0).sum().groupby(pd.Grouper(freq='D')).sum().to_csv(
            os.path.join(save_path, 'daily_metered.csv'))

        # generate monthly summaries by BMU Type
        self.stdout.write('{:%Y-%m-%d %H:%M:%S} Generating monthly BMU Type aggregate values'.format(dt.datetime.now()))
        combined_BAVs.groupby(level=0).sum().groupby(pd.Grouper(freq='M')).sum().T.groupby(BMU_types.Type.to_dict()).sum().to_csv(
            os.path.join(save_path, 'monthly_BAVs_bytype.csv'))
        combined_OAVs.groupby(level=0).sum().groupby(pd.Grouper(freq='M')).sum().T.groupby(BMU_types.Type.to_dict()).sum().to_csv(
            os.path.join(save_path, 'monthly_OAVs_bytype.csv'))
        combined_FPNs.groupby(level=0).sum().groupby(pd.Grouper(freq='M')).sum().T.groupby(BMU_types.Type.to_dict()).sum().to_csv(
            os.path.join(save_path, 'monthly_FPNs_bytype.csv'))
        combined_MELs.groupby(level=0).sum().groupby(pd.Grouper(freq='M')).sum().T.groupby(BMU_types.Type.to_dict()).sum().to_csv(
            os.path.join(save_path, 'monthly_MELs_bytype.csv'))
        combined_cashflows.groupby(level=0).sum().groupby(pd.Grouper(freq='M')).sum().T.groupby(BMU_types.Type.to_dict()).sum().to_csv(
            os.path.join(save_path, 'monthly_cashflows_bytype.csv'))
        combined_metered.groupby(level=0).sum().groupby(pd.Grouper(freq='M')).sum().T.groupby(BMU_types.Type.to_dict()).sum().to_csv(
            os.path.join(save_path, 'monthly_metered_bytype.csv'))

        # generate daily summaries by BMU
        self.stdout.write('{:%Y-%m-%d %H:%M:%S} Generating daily BMU Type aggregate values'.format(dt.datetime.now()))
        combined_BAVs.groupby(level=0).sum().groupby(pd.Grouper(freq='D')).sum().T.groupby(BMU_types.Type.to_dict()).sum().to_csv(
            os.path.join(save_path, 'daily_BAVs_bytype.csv'))
        combined_OAVs.groupby(level=0).sum().groupby(pd.Grouper(freq='D')).sum().T.groupby(BMU_types.Type.to_dict()).sum().to_csv(
            os.path.join(save_path, 'daily_OAVs_bytype.csv'))
        combined_FPNs.groupby(level=0).sum().groupby(pd.Grouper(freq='D')).sum().T.groupby(BMU_types.Type.to_dict()).sum().to_csv(
            os.path.join(save_path, 'daily_FPNs_bytype.csv'))
        combined_MELs.groupby(level=0).sum().groupby(pd.Grouper(freq='D')).sum().T.groupby(BMU_types.Type.to_dict()).sum().to_csv(
            os.path.join(save_path, 'daily_MELs_bytype.csv'))
        combined_cashflows.groupby(level=0).sum().groupby(pd.Grouper(freq='D')).sum().T.groupby(BMU_types.Type.to_dict()).sum().to_csv(
            os.path.join(save_path, 'daily_cashflows_bytype.csv'))
        combined_metered.groupby(level=0).sum().groupby(pd.Grouper(freq='D')).sum().T.groupby(BMU_types.Type.to_dict()).sum().to_csv(
            os.path.join(save_path, 'daily_metered_bytype.csv'))

        # generate summaries by BMU Type
        self.stdout.write('{:%Y-%m-%d %H:%M:%S} Generating BMU Type aggregate values'.format(dt.datetime.now()))
        combined_BAVs.T.groupby(BMU_types.Type.to_dict()).sum().to_csv(os.path.join(save_path, 'BAVs_bytype.csv'))
        combined_OAVs.T.groupby(BMU_types.Type.to_dict()).sum().to_csv(os.path.join(save_path, 'OAVs_bytype.csv'))
        combined_FPNs.T.groupby(BMU_types.Type.to_dict()).sum().to_csv(os.path.join(save_path, 'FPNs_bytype.csv'))
        combined_MELs.T.groupby(BMU_types.Type.to_dict()).sum().to_csv(os.path.join(save_path, 'MELs_bytype.csv'))
        combined_cashflows.T.groupby(BMU_types.Type.to_dict()).sum().to_csv(os.path.join(save_path, 'cashflows_bytype.csv'))
        combined_metered.T.groupby(BMU_types.Type.to_dict()).sum().to_csv(os.path.join(save_path, 'metered_bytype.csv'))

        self.stdout.write('{:%Y-%m-%d %H:%M:%S} Finished'.format(dt.datetime.now()))
