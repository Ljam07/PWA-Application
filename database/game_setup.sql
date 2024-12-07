CREATE TABLE Games (
    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    image_path TEXT,
    release_date DATE,
    developer TEXT,
    publisher TEXT
);

CREATE TABLE Reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INT,
    reviewer_name TEXT,
    review_date DATE,
    rating INT CHECK (rating >= 0 AND rating <= 10),
    review_text TEXT,
    FOREIGN KEY (game_id) REFERENCES Games(game_id)
);

INSERT INTO Games (title, description, image_path, release_date, developer, publisher)
VALUES
    ('GTA V', 'Online Game', 'GTA_V.png', '2013-09-17', 'Rockstar North', 'Rockstar Games'),
    ('Minecraft', 'Survival Game', 'Minecraft.jpg', '2009-05-17', 'Notch', 'Mojang');

INSERT INTO Reviews (game_id, reviewer_name, review_date, rating)
VALUES
    (1, 'test', '2024-11-21', 9),
    (1, 'johndoe', '2024-11-23', 10);

--
-- CREATE TABLE Reviewers (
--     reviewer_id INTEGER PRIMARY KEY AUTOINCREMENT,
--     reviewer_name TEXT NOT NULL,
--     email TEXT UNIQUE
-- );
