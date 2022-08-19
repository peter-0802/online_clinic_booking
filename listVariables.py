import sqlite3 as sql

def getOffenseTitle():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select offense_code from offenses order by id")
    rows = cur.fetchall()
    return rows

def getMinorOffense():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select offense_code from offenses where type = 'Minor' order by id")
    rows = cur.fetchall()
    return rows

def getMajorOffense():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select offense_code from offenses where type = 'Major' order by id")
    rows = cur.fetchall()
    return rows

def getStudentID():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select id_no || ' ' || surname || ' ' || firstname || ', ' || middlename from students order by id")
    rows = cur.fetchall()
    return rows

def getCivilStatus():
    civilStatus = ["Single", "Married", "Widowed", "Separated/Divorced", "Religious"]
    return civilStatus

def getSex():
    sex = ["Male", "Female"]
    return sex

def getYearLevel():
    grade = ["Grade 7", "Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12"]
    return grade

def getSection():
    grade = ["Section A", "Section B", "Section C", "Section D", "Section E", "Section F"]
    return grade
