alter table puma_2000_5_poly add column puma_2000_id text;
update puma_2000_5_poly set puma_2000_id=state_fips||puma5;

drop table if exists puma_2000_to_2010;
create table puma_2000_to_2010(
	puma_2000_id text,
	puma_id text,
	joint double precision,
	weight1 double precision,
	weight2 double precision,
	primary key(puma_2000_id, puma_id)
);

insert into puma_2000_to_2010(puma_2000_id, puma_id, joint)
	select puma_2000_id, puma_id, ST_Area(geography(ST_Intersection(a.geom, b.geom)))
	from
		(
			select puma_2000_id, ST_Union(geom) as geom
			from puma_2000_5_poly
			group by puma_2000_id
		) a,
		puma_poly b
	where ST_Intersects(a.geom, b.geom);

-- select max(joint) from
-- (select joint, rank*100/(select count(*) from puma_2000_to_2010) as pct
-- from (
-- 	select joint, rank() over(order by joint) as rank
-- 	from puma_2000_to_2010 order by joint desc
-- ) a
-- ) b
-- group by pct order by pct;

update puma_2000_to_2010 set weight1=joint/weight_total
from (
	select puma_2000_id, sum(joint) weight_total
	from puma_2000_to_2010
	group by puma_2000_id
) a
where a.puma_2000_id=puma_2000_to_2010.puma_2000_id;

update puma_2000_to_2010 set weight2=joint/weight_total
from (
	select puma_id, sum(joint) weight_total
	from puma_2000_to_2010
	group by puma_id
) a
where a.puma_id=puma_2000_to_2010.puma_id;

delete from puma_2000_to_2010 where weight1 < 0.05 and weight2 < 0.05;

update puma_2000_to_2010 set weight1=joint/weight_total
from (
	select puma_2000_id, sum(joint) weight_total
	from puma_2000_to_2010
	group by puma_2000_id
) a
where a.puma_2000_id=puma_2000_to_2010.puma_2000_id;

update puma_2000_to_2010 set weight2=joint/weight_total
from (
	select puma_id, sum(joint) weight_total
	from puma_2000_to_2010
	group by puma_id
) a
where a.puma_id=puma_2000_to_2010.puma_id;
