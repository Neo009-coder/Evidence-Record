# ==============================================================
#  PROJECT     : FORENSIC EVIDENCE AND CUSTODY VAULT
#  MADE BY     : (PRIYANSHU DAS)
#  CLASS       : XII - (B)
#  ROLL NO     : (02)
#  SCHOOL      : (BENGALI SENIOR SECONDARY SCHOOL)
#  SESSION     : 2026-27
# ==============================================================
#
#  ABOUT MY PROJECT
#  ----------------
#  In every police case, the proof (evidence) has to be kept
#  very safely. If anyone changes or loses the evidence then
#  the court does not accept it. So whenever evidence goes
#  from one officer to another officer, it is written in a
#  register. This record is called the CHAIN OF CUSTODY.
#
#  My program is a small database system for this work. It
#  keeps three tables in MySQL ->
#     CASES    : details of each case
#     EVIDENCE : items collected in each case
#     CUSTODY  : who gave the evidence to whom and when
#
#  SOFTWARE I USED
#  ---------------
#     1. Thonny IDE (Python 3)
#     2. MySQL Community Server 8.0 (database server)
#     3. mysql-connector-python (bridge between Python and MySQL)
#
#  BEFORE RUNNING
#  --------------
#     1. MySQL runs as a Windows service, so it starts with the
#        computer by itself. (If needed, start it from the
#        Services window.)
#     2. Install the connector -> in Thonny go to
#        Tools > Manage Packages > search "mysql-connector-python"
#        > Install  (or type this in cmd ->
#        pip install mysql-connector-python)
#     3. MySQL made me set a root password at the time of
#        installation. That password is written below in the
#        PASSWORD line.
#     4. Press F5 and the database and tables get made by themselves
# ==============================================================

import mysql.connector
import datetime

# ---------- my MySQL settings (change password if you have one) ----------
HOST     = "localhost"
USER     = "root"
PASSWORD = "Rupiee_das0090"        # my MySQL root password goes here inside the quotes
DATABASE = "Forensic_vaultt"


# ==============================================================
#  PART 1 : ONE TIME SETUP (makes the database and tables)
# ==============================================================

def setup_database():
    """Runs automatically when the program starts. Creates the
    database and the three tables if they are not there already."""
    con = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD)
    cur = con.cursor()

    cur.execute("CREATE DATABASE IF NOT EXISTS " + DATABASE)
    cur.execute("USE " + DATABASE)

    cur.execute("""CREATE TABLE IF NOT EXISTS CASES (
                   CASE_ID     VARCHAR(10) PRIMARY KEY,
                   CASE_TITLE  VARCHAR(50),
                   OFFICER     VARCHAR(30),
                   FILED_ON    DATE,
                   STATUS      VARCHAR(10))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS EVIDENCE (
                   EV_ID        VARCHAR(10) PRIMARY KEY,
                   CASE_ID      VARCHAR(10),
                   EV_TYPE      VARCHAR(25),
                   DETAILS      VARCHAR(100),
                   FOUND_ON     DATE,
                   COLLECTED_BY VARCHAR(30),
                   STORAGE      VARCHAR(40),
                   HOLDER       VARCHAR(30),
                   STATUS       VARCHAR(20),
                   FOREIGN KEY (CASE_ID) REFERENCES CASES(CASE_ID))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS CUSTODY (
                   TRANS_ID    INT AUTO_INCREMENT PRIMARY KEY,
                   EV_ID       VARCHAR(10),
                   FROM_PERSON VARCHAR(30),
                   TO_PERSON   VARCHAR(30),
                   TRANS_DATE  DATE,
                   PURPOSE     VARCHAR(100),
                   FOREIGN KEY (EV_ID) REFERENCES EVIDENCE(EV_ID))""")

    con.commit()
    con.close()


# ==============================================================
#  PART 2 : SMALL HELPER FUNCTIONS (used again and again)
# ==============================================================

def ask_text(msg):
    """Keeps asking until the user types something (not blank)."""
    while True:
        t = input(msg).strip()
        if t != "":
            return t
        print("  This cannot be left blank!")


def ask_date(msg):
    """Keeps asking until the date is typed in yyyy-mm-dd format."""
    while True:
        d = input(msg).strip()
        parts = d.split("-")
        if (len(parts) == 3 and len(parts[0]) == 4 and
            len(parts[1]) == 2 and len(parts[2]) == 2 and
            parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit()):
            return d
        print("  Wrong format! Type the date like 2026-01-15")


def show_evidence_card(r):
    """Prints one evidence record in a simple block form."""
    print("-" * 45)
    print(" Evidence ID :", r[0])
    print(" Case ID     :", r[1])
    print(" Type        :", r[2])
    print(" Details     :", r[3])
    print(" Found on    :", r[4])
    print(" Collected by:", r[5])
    print(" Storage     :", r[6])
    print(" Holder      :", r[7])
    print(" Status      :", r[8])


# ==============================================================
#  PART 3 : MENU OPTION FUNCTIONS
# ==============================================================

def add_case(cur, con):
    print("\n----- ADD NEW CASE -----")
    cid = ask_text("Enter Case ID (example C101) : ")
    cur.execute("SELECT * FROM CASES WHERE CASE_ID=%s", (cid,))
    if cur.fetchone() is not None:
        print("This Case ID already exists!")
        return
    title   = ask_text("Enter case title            : ")
    officer = ask_text("Officer in charge           : ")
    fdate   = ask_date("Date case was filed (yyyy-mm-dd) : ")
    cur.execute("INSERT INTO CASES VALUES (%s,%s,%s,%s,'Open')",
                (cid, title, officer, fdate))
    con.commit()
    print("Case", cid, "has been saved successfully.")


def add_evidence(cur, con):
    print("\n----- ADD NEW EVIDENCE -----")
    eid = ask_text("Enter Evidence ID (example E001) : ")
    cur.execute("SELECT * FROM EVIDENCE WHERE EV_ID=%s", (eid,))
    if cur.fetchone() is not None:
        print("This Evidence ID already exists!")
        return
    cid = ask_text("Case ID it belongs to        : ")
    cur.execute("SELECT * FROM CASES WHERE CASE_ID=%s", (cid,))
    if cur.fetchone() is None:
        print("No case found with ID", cid, ". Add the case first.")
        return
    evtype   = ask_text("Type (knife/hair/CCTV/blood) : ")
    details  = ask_text("Short description       : ")
    fdate    = ask_date("Date found (yyyy-mm-dd) : ")
    officer  = ask_text("Collected by (officer name)  : ")
    storage  = ask_text("Storage place (eg Locker A-3) : ")
    # the officer who collected it becomes the first holder
    cur.execute("""INSERT INTO EVIDENCE VALUES
                   (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (eid, cid, evtype, details, fdate, officer,
                 storage, officer, "In Storage"))
    # first line of the custody chain is written automatically
    cur.execute("""INSERT INTO CUSTODY
                   (EV_ID, FROM_PERSON, TO_PERSON, TRANS_DATE, PURPOSE)
                   VALUES (%s,'Crime Scene',%s,%s,'First collection from crime scene')""",
                (eid, officer, fdate))
    con.commit()
    print("Evidence", eid, "saved. Its custody chain has also been started.")


def view_cases(cur):
    print("\n----- ALL CASES -----")
    cur.execute("SELECT * FROM CASES ORDER BY CASE_ID")
    rows = cur.fetchall()
    if len(rows) == 0:
        print("No cases in the record yet.")
        return
    print("-" * 78)
    print("CASE ID   TITLE                              OFFICER           FILED ON     STATUS")
    print("-" * 78)
    for r in rows:
        print(r[0].ljust(10), r[1][:32].ljust(34), r[2][:16].ljust(18),
              str(r[3]).ljust(13), r[4])
    print("-" * 78)
    print("Total cases :", len(rows))


def view_evidence(cur):
    print("\n----- ALL EVIDENCE (joined with case title) -----")
    # this is an equi join between EVIDENCE and CASES
    cur.execute("""SELECT E.EV_ID, E.CASE_ID, C.CASE_TITLE, E.EV_TYPE,
                          E.STORAGE, E.HOLDER, E.STATUS
                   FROM EVIDENCE E, CASES C
                   WHERE E.CASE_ID = C.CASE_ID
                   ORDER BY E.EV_ID""")
    rows = cur.fetchall()
    if len(rows) == 0:
        print("No evidence in the record yet.")
        return
    print("-" * 92)
    print("EV ID     CASE     CASE TITLE                    TYPE          STORAGE           HOLDER            STATUS")
    print("-" * 92)
    for r in rows:
        print(r[0].ljust(10), r[1].ljust(9), r[2][:26].ljust(28),
              r[3][:12].ljust(14), r[4][:16].ljust(18), r[5][:16].ljust(18), r[6])
    print("-" * 92)
    print("Total evidence items :", len(rows))


def search_evidence(cur):
    print("\n----- SEARCH EVIDENCE -----")
    print(" 1. Search by Evidence ID")
    print(" 2. Search by Case ID")
    print(" 3. Search by Type (part name is also ok)")
    print(" 4. Search by Status")
    ch = input("Enter your choice : ").strip()
    if ch == "1":
        key = ask_text("Enter Evidence ID : ")
        cur.execute("SELECT * FROM EVIDENCE WHERE EV_ID=%s", (key,))
    elif ch == "2":
        key = ask_text("Enter Case ID : ")
        cur.execute("SELECT * FROM EVIDENCE WHERE CASE_ID=%s ORDER BY EV_ID", (key,))
    elif ch == "3":
        key = ask_text("Enter type (example - hair) : ")
        cur.execute("SELECT * FROM EVIDENCE WHERE EV_TYPE LIKE %s ORDER BY EV_ID",
                    ("%" + key + "%",))
    elif ch == "4":
        key = ask_text("Enter status (In Storage / Released to Court / Destroyed) : ")
        cur.execute("SELECT * FROM EVIDENCE WHERE STATUS=%s", (key,))
    else:
        print("Wrong choice!")
        return
    rows = cur.fetchall()
    if len(rows) == 0:
        print("No matching evidence found.")
        return
    print("\nTotal records found :", len(rows))
    for r in rows:
        show_evidence_card(r)


def transfer_custody(cur, con):
    print("\n----- TRANSFER CUSTODY OF EVIDENCE -----")
    eid = input("Enter Evidence ID : ").strip()
    cur.execute("SELECT HOLDER FROM EVIDENCE WHERE EV_ID=%s", (eid,))
    row = cur.fetchone()
    if row is None:
        print("No evidence found with this ID.")
        return
    print("Current holder of this evidence :", row[0])
    from_p = input("Transferred by [" + row[0] + "] (press Enter for same) : ").strip()
    if from_p == "":
        from_p = row[0]
    to_p    = ask_text("Transferred to (officer / lab name) : ")
    tdate   = ask_date("Transfer date (yyyy-mm-dd) : ")
    purpose = ask_text("Reason (lab test / court hearing etc) : ")
    cur.execute("""INSERT INTO CUSTODY
                   (EV_ID, FROM_PERSON, TO_PERSON, TRANS_DATE, PURPOSE)
                   VALUES (%s,%s,%s,%s,%s)""",
                (eid, from_p, to_p, tdate, purpose))
    # the current holder column of EVIDENCE also has to be updated
    cur.execute("UPDATE EVIDENCE SET HOLDER=%s WHERE EV_ID=%s", (to_p, eid))
    con.commit()
    print("Custody transferred from", from_p, "to", to_p, ".")


def view_chain(cur):
    print("\n----- CUSTODY CHAIN OF AN EVIDENCE -----")
    eid = input("Enter Evidence ID : ").strip()
    cur.execute("SELECT EV_ID FROM EVIDENCE WHERE EV_ID=%s", (eid,))
    if cur.fetchone() is None:
        print("No evidence found with this ID.")
        return
    cur.execute("""SELECT TRANS_ID, FROM_PERSON, TO_PERSON, TRANS_DATE, PURPOSE
                   FROM CUSTODY WHERE EV_ID=%s ORDER BY TRANS_ID""", (eid,))
    rows = cur.fetchall()
    print("Custody history of evidence", eid, "->", len(rows), "record(s)")
    print("-" * 88)
    print("SR   FROM                TO                  DATE        PURPOSE")
    print("-" * 88)
    for r in rows:
        print(str(r[0]).ljust(5), str(r[1])[:18].ljust(20),
              str(r[2])[:18].ljust(20), str(r[3]).ljust(11), str(r[4])[:28])
    print("-" * 88)


def update_evidence(cur, con):
    print("\n----- UPDATE EVIDENCE DETAILS -----")
    eid = input("Enter Evidence ID : ").strip()
    cur.execute("SELECT * FROM EVIDENCE WHERE EV_ID=%s", (eid,))
    if cur.fetchone() is None:
        print("No evidence found with this ID.")
        return
    print(" 1. Change storage place")
    print(" 2. Change status (In Storage / Released to Court / Destroyed)")
    ch = input("What do you want to update : ").strip()
    if ch == "1":
        new = ask_text("New storage place : ")
        cur.execute("UPDATE EVIDENCE SET STORAGE=%s WHERE EV_ID=%s", (new, eid))
    elif ch == "2":
        new = ask_text("New status : ")
        cur.execute("UPDATE EVIDENCE SET STATUS=%s WHERE EV_ID=%s", (new, eid))
    else:
        print("Wrong choice, nothing was updated.")
        return
    con.commit()
    print("Record of", eid, "updated.")


def case_report(cur):
    print("\n----- CASE WISE EVIDENCE REPORT -----")
    cur.execute("SELECT COUNT(*) FROM CASES")
    total_cases = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM EVIDENCE")
    total_ev = cur.fetchone()[0]
    print("Total number of cases    :", total_cases)
    print("Total evidence items     :", total_ev)
    print()
    # LEFT JOIN is used so that cases having zero evidence also come in the list
    cur.execute("""SELECT C.CASE_ID, C.CASE_TITLE, COUNT(E.EV_ID)
                   FROM CASES C LEFT JOIN EVIDENCE E ON C.CASE_ID = E.CASE_ID
                   GROUP BY C.CASE_ID, C.CASE_TITLE""")
    rows = cur.fetchall()
    print("CASE ID   TITLE                              EVIDENCE COUNT")
    print("-" * 60)
    for r in rows:
        print(r[0].ljust(10), r[1][:32].ljust(34), r[2])
    print("-" * 60)

    save = input("\nDo you want to save this report in a text file? (y/n) : ")
    if save.lower() == "y":
        f = open("evidence_report.txt", "w")        # "w" mode makes a new file
        f.write("FORENSIC EVIDENCE AND CUSTODY VAULT - REPORT\n")
        f.write("Generated on : " + str(datetime.datetime.now()) + "\n")
        f.write("=" * 60 + "\n")
        f.write("Total cases : " + str(total_cases) + "\n")
        f.write("Total evidence items : " + str(total_ev) + "\n")
        f.write("=" * 60 + "\n")
        f.write("CASE ID   TITLE                              EVIDENCE COUNT\n")
        f.write("-" * 60 + "\n")
        for r in rows:
            f.write(str(r[0]).ljust(10) + str(r[1])[:32].ljust(34) + str(r[2]) + "\n")
        f.write("-" * 60 + "\n")
        f.close()
        print("Report saved in file -> evidence_report.txt")


def delete_record(cur, con):
    print("\n----- DELETE A RECORD -----")
    print(" 1. Delete an evidence item")
    print(" 2. Delete a case")
    ch = input("Enter your choice : ").strip()
    if ch == "1":
        eid = input("Evidence ID to delete : ").strip()
        cur.execute("SELECT EV_ID FROM EVIDENCE WHERE EV_ID=%s", (eid,))
        if cur.fetchone() is None:
            print("No evidence found with this ID.")
            return
        sure = input("Are you 100 percent sure? Type YES in capitals : ")
        if sure == "YES":
            # custody records are deleted first because of the foreign key
            cur.execute("DELETE FROM CUSTODY WHERE EV_ID=%s", (eid,))
            cur.execute("DELETE FROM EVIDENCE WHERE EV_ID=%s", (eid,))
            con.commit()
            print("Evidence", eid, "and its custody records are deleted.")
        else:
            print("Cancelled. Nothing was deleted.")
    elif ch == "2":
        cid = input("Case ID to delete : ").strip()
        cur.execute("SELECT COUNT(*) FROM EVIDENCE WHERE CASE_ID=%s", (cid,))
        n = cur.fetchone()[0]
        if n > 0:
            print("Cannot delete! This case still has", n, "evidence record(s).")
            print("Delete its evidence first.")
            return
        cur.execute("DELETE FROM CASES WHERE CASE_ID=%s", (cid,))
        con.commit()
        print("Case", cid, "deleted.")
    else:
        print("Wrong choice!")


# ==============================================================
#  PART 4 : MAIN PROGRAM (menu runs again and again till exit)
# ==============================================================

def main():
    print("=" * 60)
    print("          FORENSIC EVIDENCE AND CUSTODY VAULT")
    print("             Class 12 Computer Science Project")
    print("=" * 60)
    try:
        setup_database()
        print("[OK] Connected to MySQL. Database is ready.")
    except mysql.connector.Error:
        print("[ERROR] Could not connect to MySQL server!")
        print("        Check that the MySQL service is running and the")
        print("        PASSWORD written at the top of the program is correct.")
        return

    con = mysql.connector.connect(host=HOST, user=USER,
                                  password=PASSWORD, database=DATABASE)
    cur = con.cursor()

    while True:
        print()
        print("=" * 46)
        print(" MAIN MENU")
        print("=" * 46)
        print("  1. Add New Case")
        print("  2. Add New Evidence")
        print("  3. View All Cases")
        print("  4. View All Evidence")
        print("  5. Search Evidence")
        print("  6. Transfer Custody of Evidence")
        print("  7. View Custody Chain of an Evidence")
        print("  8. Update Evidence (storage / status)")
        print("  9. Case Wise Report (can save in text file)")
        print(" 10. Delete a Record")
        print("  0. Exit")
        print("=" * 46)
        choice = input("Enter your choice (0 to exit) : ").strip()

        if choice == "0":
            print("\nThank you. All data is safely stored in MySQL.")
            con.close()
            break
        elif choice == "1":
            add_case(cur, con)
        elif choice == "2":
            add_evidence(cur, con)
        elif choice == "3":
            view_cases(cur)
        elif choice == "4":
            view_evidence(cur)
        elif choice == "5":
            search_evidence(cur)
        elif choice == "6":
            transfer_custody(cur, con)
        elif choice == "7":
            view_chain(cur)
        elif choice == "8":
            update_evidence(cur, con)
        elif choice == "9":
            case_report(cur)
        elif choice == "10":
            delete_record(cur, con)
        else:
            print("Wrong choice! Enter a number from 0 to 10.")

        input("\nPress Enter to show the menu again...")


# program execution starts from here
main()
