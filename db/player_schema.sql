CREATE TABLE MATCHES(
    match_id VARCHAR(50) PRIMARY KEY,
    competition VARCHAR(50),
    season VARCHAR(20),
    match_date DATE,
    team VARCHAR(50),
    opponent VARCHAR(50),
    home_away CHAR(1),
    opponent_strength FLOAT,
    team_possession_pct FLOAT,
    game_state VARCHAR(20),
    result CHAR(1)

);

CREATE TABLE player_match_usage (
    match_id VARCHAR(50),
    player VARCHAR(100),
    team VARCHAR(50),
    minutes_played INT,

    avg_position_x FLOAT(53),
    avg_position_y FLOAT(53),

    touches INT,
    touches_wide INT,
    touches_half_space INT,
    touches_central INT,

    progressive_carries INT,
    carries_into_final_third INT,
    carries_into_box INT,

    pressures INT,
    final_third_pressures INT,

    shots INT,
    xg FLOAT(53),

    FOREIGN KEY (match_id) REFERENCES MATCHES(match_id)
);

CREATE TABLE player_role_profile (
    player VARCHAR(100),
    team VARCHAR(50),
    season VARCHAR(50),
    minutes INT,

    touches_p90 FLOAT(53),
    touches_wide_pct FLOAT(53),
    touches_half_space_pct FLOAT(53),
    touches_central_pct FLOAT(53),

    progressive_carries_p90 FLOAT(53),
    carries_into_box_p90 FLOAT(53),

    pressures_p90 FLOAT(53),
    final_third_pressures_p90 FLOAT(53),

    shots_p90 FLOAT(53),
    xg_per_shot FLOAT(53),

    passes_final_third_p90 FLOAT(53),
    receptions_between_lines_p90 FLOAT(53)
);

