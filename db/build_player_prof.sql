-- NOTE:
-- This data is synthetic and used only to validate the pipeline.
-- It does not represent real match statistics.

INSERT INTO player_role_profile
SELECT
    pmu.player,
    pmu.team,
    m.season,
    SUM(pmu.minutes_played) AS minutes,

    -- usage volume
    SUM(pmu.touches) * 90.0 / SUM(pmu.minutes_played) AS touches_p90,

    -- spatial distribution
    SUM(pmu.touches_wide) * 1.0 / NULLIF(SUM(pmu.touches), 0) AS touches_wide_pct,
    SUM(pmu.touches_half_space) * 1.0 / NULLIF(SUM(pmu.touches), 0) AS touches_half_space_pct,
    SUM(pmu.touches_central) * 1.0 / NULLIF(SUM(pmu.touches), 0) AS touches_central_pct,

    -- ball progression
    SUM(pmu.progressive_carries) * 90.0 / SUM(pmu.minutes_played) AS progressive_carries_p90,
    SUM(pmu.carries_into_box) * 90.0 / SUM(pmu.minutes_played) AS carries_into_box_p90,

    -- defensive work
    SUM(pmu.pressures) * 90.0 / SUM(pmu.minutes_played) AS pressures_p90,
    SUM(pmu.final_third_pressures) * 90.0 / SUM(pmu.minutes_played) AS final_third_pressures_p90,

    -- shooting profile
    SUM(pmu.shots) * 90.0 / SUM(pmu.minutes_played) AS shots_p90,
    SUM(pmu.xg) * 1.0 / NULLIF(SUM(pmu.shots), 0) AS xg_per_shot,

    -- placeholders (future)
    NULL AS passes_final_third_p90,
    NULL AS receptions_between_lines_p90

FROM player_match_usage pmu
JOIN matches m
  ON pmu.match_id = m.match_id

GROUP BY pmu.player, pmu.team, m.season;


