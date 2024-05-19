CREATE TABLE IF NOT EXISTS us (
    study_id varchar(50) primary key NOT NULL
    study_title text NOT NULL
    conditions text NOT NULL
    sponsor text NOT NULL
)

CREATE TABLE IF NOT EXISTS eu (
    study_id varchar(50) primary key NOT NULL
    study_title text NOT NULL
    conditions text NOT NULL
    sponsor text NOT NULL
)

CREATE TABLE IF NOT EXISTS combined (
    study_id varchar(50) primary key NOT NULL
    study_title text NOT NULL
    conditions text NOT NULL
    sponsor text NOT NULL
)