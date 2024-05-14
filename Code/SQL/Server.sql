-- CREATE A NEW DATABASE

START TRANSACTION;

-- DROP TABLE IF EXISTS
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS crew;
DROP TABLE IF EXISTS cast;
DROP TABLE IF EXISTS links;
DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS movieLanguage;
DROP TABLE IF EXISTS boxOfficeGross;
DROP TABLE IF EXISTS genre;
DROP TABLE IF EXISTS keywords;
DROP TABLE IF EXISTS movieClientReview;


-- ENTITIES FROM THE ER MODEL
CREATE TABLE movies (
    movieID VARCHAR(10),
    title VARCHAR(128), 
    movieDescription TEXT,
    mpaa VARCHAR(16),
    releaseDate VARCHAR(32),
    duration VARCHAR(1000),
    budget FLOAT,
    PRIMARY KEY (movieID)
);

CREATE TABLE people (
    personID VARCHAR(10),
    PRIMARY KEY (personID)
);

CREATE TABLE crew (
    crewID VARCHAR(10),
    director VARCHAR(64),
    writer VARCHAR(64),
    producer VARCHAR(64),
    composer VARCHAR(64),
    cinematographer VARCHAR(64),
    PRIMARY KEY (crewID)
);

CREATE TABLE cast (
    castID VARCHAR(10),
    main_actor_1 VARCHAR(64),
    main_actor_2 VARCHAR(64),
    main_actor_3 VARCHAR(64),
    main_actor_4 VARCHAR(64),
    PRIMARY KEY (castID)
);

CREATE TABLE links (
    movieID VARCHAR(10),
    html TEXT,
    PRIMARY KEY (movieID)
);

CREATE TABLE country (
    country VARCHAR(256),
    PRIMARY KEY (country)
);

CREATE TABLE movieLanguage (
    movieLanguage VARCHAR(10),
    originalLanguage VARCHAR(2),
    PRIMARY KEY (movieLanguage)
);

CREATE TABLE boxOfficeGross (
    boxOfficeGross VARCHAR(64),
    domesticGross INT,
    internationalGross INT,
    worldWideGross INT,
    domesticAverageMoviePrice FLOAT,
    PRIMARY KEY (boxOfficeGross)
);

CREATE TABLE genre (
    genreID VARCHAR(10),
    genre_1 TEXT,
    genre_2 TEXT,
    genre_3 TEXT,
    genre_4 TEXT,
    PRIMARY KEY (genreID)
);

CREATE TABLE keywords (
    keywordID VARCHAR(64),
    keywords VARCHAR(256),
    PRIMARY KEY (keywordID)
);

CREATE TABLE movieClientReview (
    movieID VARCHAR(10),
    title VARCHAR(128),
    customRating FLOAT,
    customReview TEXT,
    PRIMARY KEY (movieID)
);

-- LOAD DATA 

-- MOVIES 
LOAD DATA INFILE '/var/lib/mysql-files/03-Movies/Mojo_budget_update.csv'
    INTO TABLE movies
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (movieID,
    title,
    @dummy,
    movieDescription,
    mpaa,
    releaseDate,
    duration,
    @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy,
    budget,
    @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy);

-- PEOPLE
-- LOAD DATA INFILE '' 
--     INTO TABLE people
--     FIELDS TERMINATED BY ',' 
--     OPTIONALLY ENCLOSED BY '"'
--     LINES TERMINATED BY '\r\n'
--     IGNORE 1 LINES

-- CREW
LOAD DATA INFILE '/var/lib/mysql-files/03-Movies/Mojo_budget_update.csv' 
    INTO TABLE crew
    FIELDS TERMINATED BY ',' 
    OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES 
    (crewID,
    @dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,
    director,
    writer,
    producer,
    composer,
    cinematographer,
    @dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy);

-- CAST
LOAD DATA INFILE '/var/lib/mysql-files/03-Movies/Mojo_budget_update.csv' 
    INTO TABLE cast
    FIELDS TERMINATED BY ',' 
    OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (castID,
    @dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,
    main_actor_1,
    main_actor_2,
    main_actor_3,
    main_actor_4,
    @dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy);

-- CLIENT INFO (couldnt find client info or forgot what client info was)
LOAD DATA INFILE '/var/lib/mysql-files/03-Movies/Mojo_budget_update.csv' 
    INTO TABLE links
    FIELDS TERMINATED BY ',' 
    OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (movieID,
    @dummy,@dummy,@dummy,@dummy,@dummy,@dummy,
    @dummy,@dummy,@dummy,@dummy,@dummy,@dummy,
    @dummy,@dummy,@dummy,@dummy,@dummy,@dummy,
    @dummy,@dummy,@dummy,@dummy,@dummy,@dummy,
    html);

-- COUNTRY 
-- LOAD DATA INFILE '' 
--     INTO TABLE country
--     FIELDS TERMINATED BY ',' 
--     OPTIONALLY ENCLOSED BY '"'
--     LINES TERMINATED BY '\r\n'
--     IGNORE 1 LINES

-- LANGUAGE 
LOAD DATA INFILE '/var/lib/mysql-files/03-Movies/movies_metadata.csv' 
    INTO TABLE movieLanguage
    FIELDS TERMINATED BY ',' 
    OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (@dummy,@dummy,@dummy,@dummy,@dummy,
    movieLanguage,originalLanguage,@dummy,@dummy,@dummy,
    @dummy,@dummy,@dummy,@dummy,@dummy,
    @dummy,@dummy,@dummy,@dummy,@dummy,
    @dummy,@dummy,@dummy,@dummy,@dummy);

-- 
LOAD DATA INFILE '/var/lib/mysql-files/03-Movies/hsx_bomojo_data/boxofficemojo_releases.csv' 
    INTO TABLE boxOfficeGross
    FIELDS TERMINATED BY ',' 
    OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (boxOfficeGross,
    @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, 
    domesticGross, internationalGross, worldwideGross,
    @dummy,@dummy,@dummy,@dummy,@dummy,
    @dummy,@dummy,@dummy,@dummy,@dummy,@dummy);

-- GENRE 
LOAD DATA INFILE '/var/lib/mysql-files/03-Movies/Mojo_budget_update.csv' 
    INTO TABLE genre
    FIELDS TERMINATED BY ',' 
    OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (genreID,
    @dummy,@dummy,@dummy,@dummy,@dummy,@dummy,
    @dummy,@dummy,@dummy,@dummy,@dummy,@dummy,
    @dummy,@dummy,@dummy,@dummy,@dummy,@dummy,
    @dummy,@dummy,
    genre_1,
    genre_2,
    genre_3,
    genre_4,
    @dummy);

-- KEYWORDS
LOAD DATA INFILE '/var/lib/mysql-files/03-Movies/keywords.csv' 
    INTO TABLE keywords
    FIELDS TERMINATED BY ',' 
    OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (keywordID, 
    keywords);

