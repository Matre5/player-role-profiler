-- NOTE:
-- This data is synthetic and used only to validate the pipeline.
-- It does not represent real match statistics.


INSERT INTO matches (
    match_id,
    competition,
    season,
    match_date,
    team,
    opponent,
    home_away,
    opponent_strength,
    team_possession_pct,
    game_state,
    result
)
VALUES (
    'FACUP_2025_CITY_X',
    'FA Cup',
    '2024/25',
    '2025-01-11',
    'Manchester City',
    'Opponent FC',
    'H',
    0.45,
    68.2,
    'drawing',
    'W'
);

