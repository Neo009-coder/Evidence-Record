-- ==============================================================
--  FORENSIC EVIDENCE AND CUSTODY VAULT
--  SQL COMMANDS FILE (Class 12 Computer Science Project)
--
--  My Python program makes all this automatically, but these
--  commands are written here also because -
--     1. they are needed in the practical file
--     2. they can be run directly in MySQL Command Line Client
--        or MySQL Workbench also
--
--  HOW TO RUN THIS FILE
--  --------------------
--  Way 1 (Command Line) : open MySQL Command Line Client, type your
--          password, then type ->
--          SOURCE C:/forensic_setup.sql
--          (write the full path where you saved this file)
--  Way 2 (Workbench)    : open MySQL Workbench, connect, then
--          File > Open SQL Script > choose this file > click the
--          lightning icon to run it.
--  Note : run this file only ONE time, otherwise the sample data
--         will be inserted again.
-- ==============================================================

-- Step 1 : Create the database
CREATE DATABASE IF NOT EXISTS FORENSIC_VAULT;
USE FORENSIC_VAULT;

-- Step 2 : Create the three tables
CREATE TABLE IF NOT EXISTS CASES (
    CASE_ID     VARCHAR(10) PRIMARY KEY,
    CASE_TITLE  VARCHAR(50),
    OFFICER     VARCHAR(30),
    FILED_ON    DATE,
    STATUS      VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS EVIDENCE (
    EV_ID        VARCHAR(10) PRIMARY KEY,
    CASE_ID      VARCHAR(10),
    EV_TYPE      VARCHAR(25),
    DETAILS      VARCHAR(100),
    FOUND_ON     DATE,
    COLLECTED_BY VARCHAR(30),
    STORAGE      VARCHAR(40),
    HOLDER       VARCHAR(30),
    STATUS       VARCHAR(20),
    FOREIGN KEY (CASE_ID) REFERENCES CASES(CASE_ID)
);

CREATE TABLE IF NOT EXISTS CUSTODY (
    TRANS_ID    INT AUTO_INCREMENT PRIMARY KEY,
    EV_ID       VARCHAR(10),
    FROM_PERSON VARCHAR(30),
    TO_PERSON   VARCHAR(30),
    TRANS_DATE  DATE,
    PURPOSE     VARCHAR(100),
    FOREIGN KEY (EV_ID) REFERENCES EVIDENCE(EV_ID)
);

-- Step 3 : Some sample records for testing the project
INSERT INTO CASES VALUES
('C101', 'Bank Locker Robbery',     'Inspector R. Sharma', '2026-07-12', 'Open'),
('C102', 'Missing Person Case',     'SI A. Verma',         '2026-08-02', 'Open'),
('C103', 'Hit and Run Accident',    'Inspector K. Singh',  '2026-08-20', 'Closed');

INSERT INTO EVIDENCE VALUES
('E001', 'C101', 'Fingerprints', 'Prints lifted from locker number 44', '2026-07-12', 'HC Suresh',  'Locker Room B', 'HC Suresh',      'In Storage'),
('E002', 'C101', 'CCTV DVR',     'DVR of bank entrance camera',         '2026-07-12', 'HC Suresh',  'Electronics Rack', 'FSL Rohtak',  'Sent for Test'),
('E003', 'C102', 'Hair Strand',  'Hair found near the last seen spot',  '2026-08-03', 'WC Neelam',  'Locker A-2',    'WC Neelam',      'In Storage'),
('E004', 'C103', 'Paint Sample', 'Paint scraped from damaged scooter',  '2026-08-20', 'SI Dahiya',  'Shelf 5',       'Court Record',   'Released to Court');

INSERT INTO CUSTODY (EV_ID, FROM_PERSON, TO_PERSON, TRANS_DATE, PURPOSE) VALUES
('E001', 'Crime Scene',  'HC Suresh',   '2026-07-12', 'First collection from crime scene'),
('E002', 'Crime Scene',  'HC Suresh',   '2026-07-12', 'First collection from crime scene'),
('E002', 'HC Suresh',    'FSL Rohtak',  '2026-07-18', 'Sent for video enhancement test'),
('E003', 'Crime Scene',  'WC Neelam',   '2026-08-03', 'First collection from crime scene'),
('E004', 'Crime Scene',  'SI Dahiya',   '2026-08-20', 'First collection from crime scene'),
('E004', 'SI Dahiya',    'Court Record','2026-08-25', 'Produced before the court');

-- ==============================================================
--  SOME PRACTICE QUERIES (good for viva / practical exam)
-- ==============================================================

-- show all cases
SELECT * FROM CASES;

-- show all evidence of one case only
SELECT * FROM EVIDENCE WHERE CASE_ID = 'C101';

-- search evidence by type using LIKE
SELECT EV_ID, EV_TYPE, STORAGE FROM EVIDENCE WHERE EV_TYPE LIKE '%hair%';

-- count of evidence in each case using GROUP BY
SELECT CASE_ID, COUNT(*) FROM EVIDENCE GROUP BY CASE_ID;

-- equi join -> evidence list along with case title
SELECT E.EV_ID, C.CASE_TITLE, E.EV_TYPE, E.HOLDER
FROM EVIDENCE E, CASES C
WHERE E.CASE_ID = C.CASE_ID;

-- full custody chain of one evidence item
SELECT * FROM CUSTODY WHERE EV_ID = 'E002' ORDER BY TRANS_ID;

-- evidence which is not in storage
SELECT EV_ID, HOLDER, STATUS FROM EVIDENCE WHERE STATUS <> 'In Storage';
