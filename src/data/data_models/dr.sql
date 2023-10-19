with registered_users as ( 
	select 
		e.game_day,
		u.location,
		count(distinct u.user_number) as num_users
	from events e, users u 
	where date_trunc('day', u.registration_timestamp) <= e.game_day
	group by 1, 2
),
handle_per_matchup as ( 
	select 
		event_id,
		sum(wager_amount) as handle
	from wagers 
	group by 1
),
teams as ( 
	select distinct 
		home_team as team
	from events
),
last_5_handle_prep as ( 
	select 
		date_trunc('year', e.game_start_time) as game_year,
		e.week_of_season,
		t.team,
		sum(w.wager_amount) as handle_per_match
	from events e 
	left join teams t 
		on (e.home_team = t.team or e.away_team = t.team)
	left join wagers w 
		on w.event_id = e.event_id 	
	group by 1, 2, 3
),
last_5_handle as (
	select 
		l.game_year,
		l.week_of_season,
		l.team,
		sum(l.handle_per_match) over (partition by l.team order by l.week_of_season asc rows between 6 preceding and 1 preceding) as last_5_handle_sum
	from last_5_handle_prep l
),
last_5_handle_all as ( 
	select 
		l.game_year,
		l.week_of_season,
		sum(sum(l.handle_per_match)) over (order by l.week_of_season asc rows between 6 preceding and current row) as last_5_handle
	from last_5_handle_prep l
	group by 1, 2
),
concurrent as ( 
	select 
		e.game_day,
		e.time_slot,
		count(distinct event_id) as concurrent_games
	from events e 
	group by 1, 2
),
all_registered as ( 
	select 
		e.game_day,
		count(distinct u.user_number) as num_users 
	from events e, users u 
	where date_trunc('day', u.registration_timestamp) <= e.game_day
	group by 1
),
everything as (
select 
	e.home_team,
	e.away_team,
	e.time_slot,
    date_part('year', e.game_day) as year,
	e.week_of_season,
	coalesce(r_home.num_users, 0) as home_users,
	coalesce(r_away.num_users, 0) as away_users,
	coalesce(r_home.num_users, 0) + coalesce(r_away.num_users, 0) as all_users,
	c.concurrent_games,
	l_all.last_5_handle as last_5_handle_all,
	l_home.last_5_handle_sum as last_5_handle_home,
	l_away.last_5_handle_sum as last_5_handle_away,
	a.num_users as all_registered,
    case when date_part('year', e.game_day::timestamp) = 2020 and e.week_of_season = 11 then True else False end as is_faux_future,
	h.handle
from events e 
left join registered_users r_home 
	on r_home.game_day = e.game_day and e.home_team_location = r_home.location
left join registered_users r_away 
	on r_away.game_day = e.game_day and e.away_team_location = r_away.location
left join handle_per_matchup h 
	on h.event_id = e.event_id
left join concurrent c 
	on c.game_day = e.game_day and c.time_slot = e.time_slot
left join last_5_handle l_home
	on e.home_team = l_home.team and date_trunc('year', game_start_time) = l_home.game_year and e.week_of_season = l_home.week_of_season
left join last_5_handle l_away
	on e.away_team = l_away.team and date_trunc('year', game_start_time) = l_away.game_year and e.week_of_season = l_away.week_of_season
left join last_5_handle_all as l_all 
	on date_trunc('year', e.game_start_time) = l_all.game_year and e.week_of_season = l_all.week_of_season
left join all_registered a 
	on e.game_day = a.game_day 
where l_all.last_5_handle is not null and handle is not null
)
select * from everything
where is_faux_future is False