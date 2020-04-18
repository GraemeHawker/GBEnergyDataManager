# -*- coding: utf-8 -*-
"""
command to generate annual datafiles for given data subsets
"""
import datetime as dt
import pandas as pd
import numpy as np
import pytz
import psycopg2
import os
from tqdm import tqdm
from django.core.management.base import BaseCommand, CommandError
from GBEnergyDataManager.settings import BASE_DIR, DATABASES, NETA_USER, NETA_PWD, NETA_BMU_LIST_URL, DATA_SUMMARY_LOCS

class Command(BaseCommand):
    help = 'downloads BMRA data for specific date range, expected 2 arguments of form yyyy-m-d'

    def add_arguments(self, parser):
        parser.add_argument('subset', nargs=1, type=str)
        parser.add_argument('year', nargs=1, type=int)

    def handle(self, *args, **options):
        self.stdout.write('{:%Y-%m-%d %H:%M:%S} Started'.format(dt.datetime.now()))

        # set up start and end dates
        # if fetching data for current year, then set end date to yesterday
        start_date = dt.date(options['year'][0],1,1)
        if options['year'] == (dt.date.today()-dt.timedelta(days=1)).year:
            end_date = dt.date.today()-dt.timedelta(days=1)
        else:
            end_date = dt.date(options['year'][0],12,31)

        # check if year folder exists, if not create it
        save_path = os.path.join(DATA_SUMMARY_LOCS[options['subset'][0]], str(options['year'][0]))
        self.stdout.write('{:%Y-%m-%d %H:%M:%S} saving to {}'.format(dt.datetime.now(),
                                                                     save_path))
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        # set up blank DataFrame
        self.stdout.write('{:%Y-%m-%d %H:%M:%S} Creating blank dataframe'.format(dt.datetime.now()))

        # create list of clock change dates
        transition_days = [dt.date(x.year, x.month, x.day) for x in pytz.timezone('Europe/London')._utc_transition_times]

        # set up blank dataframe, with settlement periods as index
        # and subset BMUIDs as columns
        if options['subset'][0] == 'scotland':
            bmus_df = pd.read_csv(os.path.join(BASE_DIR, 'Physical/unit_data/scottish_BMUs_190731.csv'))
            bmu_ids = bmus_df['BMU ID'].values
        else:
            raise ValueError('subset {} not recognised'.format(options['subset'][0]))

        blank_df = pd.DataFrame(columns = ['sd', 'sp'])
        curr_date = start_date
        while curr_date <= end_date:
            curr_sp = 1
            if curr_date in transition_days[::2]:
                max_sp = 46
            elif curr_date in transition_days[1::2]:
                max_sp = 50
            else:
                max_sp = 48
            while curr_sp <= max_sp:
                new_data = pd.DataFrame([[curr_date, curr_sp]], columns = ['sd', 'sp'])
                blank_df = blank_df.append(new_data)
                curr_sp += 1
            curr_date += dt.timedelta(days=1)
        blank_df = blank_df.set_index(['sd', 'sp'])
        for bmu_id in bmu_ids:
            blank_df[bmu_id] = np.nan

        # connect to DB
        # --TODO: convert to ORM
        conn = psycopg2.connect("dbname='ElexonData' user={} host={} password={}".format(DATABASES['default']['USER'],
                                                                                DATABASES['default']['HOST'],
                                                                                DATABASES['default']['PASSWORD']))
        cur = conn.cursor()
        
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
            sql_df = pd.read_sql(bav_query .format(bmu_id, start_date, end_date), conn)
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
                                          start_date-dt.timedelta(days=1),
                                          end_date+dt.timedelta(days=1)),
                             conn)
            prev_SD, prev_SP, prev_VP, prev_TS = None, None, None, None
            total_mwh = 0.0
            for key, values in df.iterrows():
                SD, SP, TS, VP = values['sd'], values['sp'], values['ts'], values['vp']
                if SD==prev_SD and SP==prev_SP:
                    time_diff = (TS - prev_TS).total_seconds() / 3600.0
                    total_mwh += (prev_VP * time_diff + (0.5 * (VP - prev_VP) * time_diff))
                elif prev_SD is not None and prev_SP is not None:
                    bmu_fpns.append([dt.date(prev_SD.year,prev_SD.month,prev_SD.day),prev_SP,total_mwh])
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
                                          start_date-dt.timedelta(days=1),
                                          end_date+dt.timedelta(days=1)),
                             conn)
            prev_SD, prev_SP, prev_VP, prev_TS, prev_TSR, last_msg_time = None, None, None, None, None, None
            total_mwh, total_time = 0.0, 0.0
            for key, values in df.iterrows():
                SD, SP, TS, VP, TSR = values['sd'], values['sp'], values['ts'], values['ve'], values['tsr']
                if SD==prev_SD and SP==prev_SP:
                    if TSR==last_msg_time:
                        time_diff = (TS - prev_TS).total_seconds() / 3600.0
                        total_mwh += (prev_VP * time_diff + (0.5 * (VP - prev_VP) * time_diff))
                        total_time += time_diff
                elif prev_SD is not None and prev_SP is not None:
                    bmu_mels.append([dt.date(prev_SD.year,prev_SD.month,prev_SD.day),prev_SP,total_mwh])
                    #if not math.isclose(0.5, total_time, rel_tol=1e-5):
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

        query = 'SELECT sd, sp, sum(oc)-sum(bc) as cashflow \
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

        combined_cashflows.to_csv(os.path.join(save_path, 'cashflows.csv'))

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

        self.stdout.write('{:%Y-%m-%d %H:%M:%S} Finished'.format(dt.datetime.now()))
