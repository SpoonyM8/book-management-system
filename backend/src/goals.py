import sqlite3
import datetime
from uuid import uuid4
from ..config import db
from .error import InputError, AccessError, DatabaseError

#-------------------- Helper functions 

def goal_valid(month, year):
    currMonth = datetime.datetime.now().month
    currYear = datetime.datetime.now().year
    if year > currYear:
        return True
    elif year < currYear or month < currMonth:
        return False
    return True

def goal_exists(username, month, year):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"""select goalID from UserGoals where username="{username}" 
                            and numMonth="{month}" and numYear="{year}";""")
        goalID = cur.fetchone()
        if goalID != None:
            goalID = goalID[0]
        else:
            goalID = False
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()
    return goalID

def goalID_exists(goalID):
    exists = True
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"""select * from UserGoals where goalID="{goalID}";""")
        exists = cur.fetchone()
        if not exists:
            goalID = False
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()
    return exists

def curr_month_reads(username):
    timeNow = datetime.datetime.now()
    currMonth = timeNow.month
    currYear = timeNow.year
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"""select count(*) from hasRead where numMonth="{currMonth}" and numYear="{currYear}"
                                                            and username="{username}";""")
        numRead = cur.fetchone()
        if not numRead:
            numRead = 0
        else:
            numRead = numRead[0]
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()
    return numRead   



#------------------- Main functions 

def create_goal(username, reqJson):
    if 'target' not in reqJson.keys():
        raise InputError("new goal must have a target")
    if 'month' not in reqJson.keys():
        raise InputError("new goal must have a month")
    if 'year' not in reqJson.keys():
        raise InputError("new goal must have a year")
    target, month, year = reqJson['target'], reqJson['month'], reqJson['year']
    if target <= 0:
        raise InputError("target outside range")
    if not goal_valid(month, year):
        raise InputError("Cannot make goal for past months")
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        goalID = goal_exists(username, month, year)
        if not goalID:
            timeNow = datetime.datetime.now()
            currMonth = timeNow.month
            currYear = timeNow.year
            if currMonth == month and currYear == year:
                numRead = curr_month_reads(username)
            else: 
                numRead = 0
            goalID = str(uuid4())
            cur.execute(f"""
                insert into UserGoals values ("{goalID}", "{username}", "{numRead}", "{target}", "{month}", "{year}");
            """)
            conn.commit()
        else:
            update_goal(goalID, reqJson)
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()
    return {"goalID": goalID}

def update_goal(goalID, reqJson):
    if 'target' not in reqJson.keys():
        raise InputError("update must have new target")
    target = reqJson['target']
    if target < 0:
        raise InputError("target outside range")
    if not goalID_exists(goalID):
        raise InputError("goal does not exist")
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        cur.execute(f"""update UserGoals set numTarget="{target}"
                                where goalID="{goalID}";""")
        conn.commit()        
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

def remove_goal(goalID):
    if not goalID_exists(goalID):
        raise InputError("Goal does not exist")
    try: 
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"""
                delete from UserGoals where goalID="{goalID}";
        """)
        conn.commit()
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

def get_user_goals(username):
    try: 
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        goalList = []

        cur.execute(f"""select * from UserGoals where username="{username}";""")
        for goal in cur.fetchall():
            goalDetails = {
                "goalID": goal[0],
                "username": goal[1],
                "numRead": goal[2],
                "numTarget": goal[3], 
                "numMonth": goal[4],
                "numYear": goal[5],
                "isCompleted": goal[2] >= goal[3],
            }
            goalList.append(goalDetails)
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()
    return {"goals": goalList}

def update_monthly_goal(username):
    timeNow = datetime.datetime.now()
    currMonth = timeNow.month
    currYear = timeNow.year
    
    goalID = goal_exists(username, currMonth, currYear)
    if not goalID:
        return
    else:
        try:
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute(f"""select numRead from UserGoals where username="{username}";""")
            newNumRead = int(cur.fetchone()[0]) + 1
            cur.execute(f"""update UserGoals set numRead="{newNumRead}"
                                    where username="{username}" and numMonth="{currMonth}" and numYear="{currYear}";""")
            conn.commit()
        except sqlite3.Error:
            raise DatabaseError(description="database error")
        finally:
            cur.close()
            conn.close()
