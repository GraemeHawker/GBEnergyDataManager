SELECT bmu_id, bmra_fpnlevel.ts, vp
	FROM public.bmra_fpnlevel
	left join bmra_fpn
	on bmra_fpnlevel.fpn_id = bmra_fpn.id
	where bmra_fpnlevel.ts='2019-08-09 17:00'
	and sp=34
	and vp!=0
	order by bmu_id;

select p114_abv.sd, p114_abp.sp, vol
	from p114_abv
		left join p114_abp
			on p114_abv.id = p114_abp.abv_id
		left join p114_sr_type
			on p114_abv.sr_type_id = p114_sr_type.id
		inner join
			(SELECT sd, sp, max(p114_sr_type.order) as ordinal
				FROM p114_abv
				left join p114_abp
					on p114_abv.id = p114_abp.abv_id
				left join p114_sr_type
					on p114_abv.sr_type_id = p114_sr_type.id
				where bmu_id='T_CRYRW-2'
			 		and p114_abv.sd>='2017-01-01'
					and p114_abv.sd<'2019-08-01'
				group by sd, sp
				order by sd, sp) as inner_query
			on inner_query.sd = p114_abv.sd
				and inner_query.sp = p114_abp.sp
				and inner_query.ordinal = p114_sr_type.order
		where bmu_id='T_CRYRW-2'
	order by sd, sp;
