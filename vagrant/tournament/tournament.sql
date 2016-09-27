-- Table definitions for the tournament project.
--
-- These tables have to be created for the tournament.py functions to work

CREATE DATABASE tournament;

CREATE TABLE Players (
    Id SERIAL PRIMARY KEY,
    Name TEXT
);


CREATE TABLE Matches (
    Id SERIAL PRIMARY KEY,
    Winner INTEGER REFERENCES Players(Id) ON DELETE CASCADE,
    Loser INTEGER REFERENCES Players(Id)  ON DELETE CASCADE
);

-- Below are some test records and the SQL queries used to develop the functions in tournament.py

-- Insert 8 players
-- INSERT INTO Players (Name) VALUES ('A');
-- INSERT INTO Players (Name) VALUES ('B');
-- INSERT INTO Players (Name) VALUES ('C');
-- INSERT INTO Players (Name) VALUES ('D');
-- INSERT INTO Players (Name) VALUES ('E');
-- INSERT INTO Players (Name) VALUES ('F');
-- INSERT INTO Players (Name) VALUES ('G');
-- INSERT INTO Players (Name) VALUES ('H');

-- -- Insert round 1
-- INSERT INTO Matches (Winner, Loser) VALUES (1, 2);
-- INSERT INTO Matches (Winner, Loser) VALUES (3, 4);
-- INSERT INTO Matches (Winner, Loser) VALUES (5, 6);
-- INSERT INTO Matches (Winner, Loser) VALUES (7, 8);

-- -- INSERT ROUND 2
-- INSERT INTO Matches (Winner, Loser) VALUES (1, 3);
-- INSERT INTO Matches (Winner, Loser) VALUES (5, 7);
-- INSERT INTO Matches (Winner, Loser) VALUES (2, 4);
-- INSERT INTO Matches (Winner, Loser) VALUES (6, 8);

-- -- Won group by
-- (SELECT WINNER AS Id, Name, COUNT(Id) AS WON FROM Matches
-- GROUP BY WINNER);

-- -- Lost group by
-- SELECT LOSER  AS Id, COUNT(Id) AS LOST FROM Matches 
-- GROUP BY LOSER;

-- -- FULL OUTER JOIN THE 2 TABLES ABOVE TO GET SCORECARD,
-- -- then INNER JOIN with Players for name

-- SELECT Name, Players.ID, 
-- coalesce(SCORECARD.WON,0) as WON, coalesce(SCORECARD.LOST,0) AS LOST 
-- FROM 
-- (SELECT coalesce(WON_GB.ID, LOST_GB.ID) AS ID,
-- coalesce(WON, 0) AS WON, coalesce(LOST, 0) AS LOST
-- FROM 
-- (SELECT WINNER AS Id, COUNT(Id) AS WON FROM Matches 
-- GROUP BY WINNER) AS WON_GB 
-- FULL OUTER JOIN
-- (SELECT LOSER  AS Id, COUNT(Id) AS LOST FROM Matches 
-- GROUP BY LOSER) AS LOST_GB
-- ON WON_GB.ID = LOST_GB.ID) AS SCORECARD
-- RIGHT OUTER JOIN 
-- Players
-- on SCORECARD.ID = Players.Id
-- ORDER BY WON DESC;


