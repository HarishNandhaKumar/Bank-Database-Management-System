USE bank_db_project;

INSERT INTO bank_branch 
(bankname, branchname, b_st_number, b_street, b_town, b_city, b_state, b_zip, b_ph_number) 
VALUES ('Boston Bank', 'Downtown', 123, 'Main Street', 'Old Town', 'Springfield', 'Illinois', 62701, 2175551234),
('Boston Bank', 'Uptown', 456, 'Market Avenue', 'West Side', 'Chicago', 'Illinois', 60616, 3125555678),
('Boston Bank', 'Northside', 789, 'Elm Drive', 'North Village', 'Peoria', 'Illinois', 61614, 3095557890),
('Boston Bank', 'Eastside', 101, 'Oak Lane', 'East Point', 'Decatur', 'Illinois', 62522, 2175554567);

DELETE from loan;
SET SQL_SAFE_UPDATES = 0;
SET SQL_SAFE_UPDATES = 1;

ALTER TABLE loan AUTO_INCREMENT = 1;

DELETE from transactions;
SET SQL_SAFE_UPDATES = 0;
SET SQL_SAFE_UPDATES = 1;

ALTER TABLE transactions AUTO_INCREMENT = 1;

