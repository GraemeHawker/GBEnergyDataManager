SELECT bmu_id, bmra_fpnlevel.ts, vp
	FROM public.bmra_fpnlevel
	left join bmra_fpn
	on bmra_fpnlevel.fpn_id = bmra_fpn.id
	where bmra_fpnlevel.ts='2019-08-09 17:00'
	and sp=34
	and vp!=0
	order by bmu_id;
