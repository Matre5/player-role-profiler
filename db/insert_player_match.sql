-- NOTE:
-- This data is synthetic and used only to validate the pipeline.
-- It does not represent real match statistics.


INSERT INTO player_match_usage (
    match_id,
    player,
    team,
    minutes_played,
    avg_position_x,
    avg_position_y,
    touches,
    touches_wide,
    touches_half_space,
    touches_central,
    progressive_carries,
    carries_into_final_third,
    carries_into_box,
    pressures,
    final_third_pressures,
    shots,
    xg
)
VALUES (
    'FACUP_2025_CITY_X',
    'Antoine Semenyo',
    'Manchester City',
    73,
    78.2,
    34.6,
    41,
    18,
    14,
    9,
    6,
    4,
    1,
    15,
    7,
    1,
    0.08
);
