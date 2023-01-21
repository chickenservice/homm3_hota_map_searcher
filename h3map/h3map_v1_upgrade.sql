PRAGMA foreign_keys = ON;

CREATE TABLE config
(
    id            INTEGER,
    maps_location VARCHAR(256),
    PRIMARY KEY (id)
);

CREATE TABLE version
(
    version INTEGER,
    name    VARCHAR(22),
    PRIMARY KEY (version)
);

CREATE TABLE difficulty
(
    difficulty INTEGER,
    name       VARCHAR(10),
    PRIMARY KEY (difficulty)
);

CREATE TABLE map_size
(
    size INTEGER,
    name VARCHAR(2),
    PRIMARY KEY (size)
);

CREATE TABLE player_color
(
    color VARCHAR(6),
    PRIMARY KEY (color)
);

CREATE TABLE faction
(
    name VARCHAR(10),
    PRIMARY KEY (name)
);

CREATE TABLE team
(
    id INTEGER(8),
    PRIMARY KEY (id)
);

CREATE TABLE victory_condition
(
    name VARCHAR(26),
    PRIMARY KEY (name)
);

CREATE TABLE loss_condition
(
    name VARCHAR(13),
    PRIMARY KEY (name)
);

CREATE TABLE map
(
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    name              VARCHAR(100),
    description       VARCHAR,
    version           INTEGER,
    map_size          INTEGER,
    difficulty        INTEGER,
    victory_condition VARCHAR(26),
    loss_condition    VARCHAR(13),
    FOREIGN KEY (version)
        REFERENCES version (version),
    FOREIGN KEY (map_size)
        REFERENCES map_size (size),
    FOREIGN KEY (difficulty)
        REFERENCES difficulty (difficulty),
    FOREIGN KEY (victory_condition)
        REFERENCES victory_condition (name),
    FOREIGN KEY (loss_condition)
        REFERENCES loss_condition (name)
);

CREATE TABLE player
(
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    can_computer_play INTEGER(1),
    can_human_play    INTEGER(1),
    map               INTEGER,
    player_color      VARCHAR(6),
    team              INTEGER(8),
    FOREIGN KEY (map)
        REFERENCES map (id)
        ON DELETE CASCADE,
    FOREIGN KEY (player_color)
        REFERENCES player_color (color),
    FOREIGN KEY (team)
        REFERENCES team (id),
    UNIQUE (map, player_color, team)
);

CREATE TABLE player_town
(
    player  INTEGER,
    faction INTEGER,
    FOREIGN KEY (player)
        REFERENCES player (id)
        ON DELETE CASCADE,
    FOREIGN KEY (faction)
        REFERENCES faction (name),
    PRIMARY KEY (player, faction)
);

INSERT INTO version (version, name)
VALUES (14, 'Restoration of Erathia'),
       (21, 'Shadow of Death'),
       (28, 'Shadow of Death'),
       (30, 'Horn of the abyss'),
       (31, 'Horn of the abyss'),
       (32, 'Horn of the abyss'),
       (51, 'Wake of Gods');

INSERT INTO difficulty (difficulty, name)
VALUES (0, 'Easy'),
       (1, 'Normal'),
       (2, 'Hard'),
       (3, 'Expert'),
       (4, 'Impossible');

INSERT INTO map_size (size, name)
VALUES (36, 'S'),
       (72, 'M'),
       (108, 'L'),
       (144, 'XL'),
       (180, 'H'),
       (216, 'XH'),
       (252, 'G');

INSERT INTO faction (name)
VALUES ('castle'),
       ('rampart'),
       ('tower'),
       ('necropolis'),
       ('inferno'),
       ('dungeon'),
       ('stronghold'),
       ('fortress'),
       ('conflux'),
       ('neutral');

INSERT INTO player_color (color)
VALUES ('Red'),
       ('Blue'),
       ('Tan'),
       ('Green'),
       ('Orange'),
       ('Purple'),
       ('Teal'),
       ('Pink');

INSERT INTO team (id)
VALUES (1),
       (2),
       (3),
       (4),
       (5),
       (6),
       (7),
       (8);

INSERT INTO victory_condition (name)
VALUES ('Standard win'),
       ('Acquire specific artifact'),
       ('Accumulate creatures'),
       ('Accumulate resources'),
       ('Upgrade specific town'),
       ('Build grail structure'),
       ('Defeat specific hero'),
       ('Capture specific town'),
       ('Defeat specific monster'),
       ('Flag all creatures'),
       ('Flag all mines'),
       ('Transport specific artifact'),
       ('Eliminate all monsters'),
       ('Survive for certain time');

INSERT INTO loss_condition (name)
VALUES ('Standard loss'),
       ('Lose specific town'),
       ('Lose specific hero'),
       ('Time expires');