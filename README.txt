==============================================================
   FORENSIC EVIDENCE AND CUSTODY VAULT
   Class 12 Computer Science Project (Python + MySQL)
==============================================================
Made by : (WRITE YOUR NAME HERE)
Class   : XII - (SECTION)
Roll No : (ROLL NUMBER)
School  : (SCHOOL NAME)
Session : 2026-27
==============================================================

FILES IN THIS FOLDER
--------------------
1. forensic_vault.py   -> the main program (menu driven,
                          runs in Thonny shell, no GUI)
2. forensic_setup.sql  -> all SQL commands (CREATE TABLE,
                          INSERT sample data, practice queries)
3. viva_questions.txt  -> viva questions with answers,
                          read this before the practical exam
4. sample_output.txt   -> output of one full run of the
                          program (for the practical file)
5. evidence_report.txt -> sample report file made by menu
                          option 9 (file handling output)
6. README.txt          -> this file

SOFTWARE NEEDED
---------------
1. Python 3 with Thonny IDE
2. MySQL Community Server 8.0
3. mysql-connector-python (the bridge module)

HOW TO RUN (STEP BY STEP)
-------------------------
Step 1 : Install MySQL Community Server 8.0 from mysql.com.
         Remember the root password you set during install.

Step 2 : Open Thonny -> Tools > Manage Packages ->
         search "mysql-connector-python" > Install.
         (or in cmd -> pip install mysql-connector-python)

Step 3 : Open forensic_vault.py and write your MySQL root
         password in the PASSWORD line near the top ->
         PASSWORD = "your_password_here"

Step 4 : Fill your name, class and roll number in the
         comment block at the top of the file.

Step 5 : Press F5. The database FORENSIC_VAULT and all three
         tables get created automatically on first run.

Step 6 : (optional) To fill sample records, run
         forensic_setup.sql one time in MySQL Command Line
         Client (SOURCE command) or MySQL Workbench.

THE THREE TABLES
----------------
CASES    : one row per case (case id, title, officer, date)
EVIDENCE : items collected in each case (linked by CASE_ID)
CUSTODY  : transfer history of each evidence item
           (linked by EV_ID, chain of custody)

One case has many evidence items, one evidence item has many
custody transfers. Both are one-to-many relations.
==============================================================
