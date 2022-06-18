# (c) PKY 2020
import pandas as pd
import statistics as st

class Student:
    def __init__(this, first, second, third, fourth, fifth, sixth, grade, email, gender):
        this.choices = [first, second, third, fourth, fifth, sixth]
        this.grade = grade
        this.email = email
        this.gender = gender

class Session:
    def __init__(this, capacity):
        this.capacity = capacity
        this.students = []
        this.ge_imbalance = [0, ""]
        this.gr_imbalance = [0, 0]

    def getGenderBalance(this):
        num_males = 0
        num_females = 0
        for student in this.students:
            if student.gender == "Male":
                num_males += 1
            else:
                num_females += 1
        dominant = "Male" if num_males > num_females else "Female"
        st_dev = st.stdev([num_males, num_females])*0.75
        this.ge_imbalance = [st_dev, dominant]

    def getGradeBalance(this):
        grades = [0, 0, 0, 0]
        for student in this.students:
            if student.grade == 9:
                grades[0] += 1
            if student.grade == 10:
                grades[1] += 1
            if student.grade == 11:
                grades[2] += 1
            if student.grade == 12:
                grades[3] += 1
        dominant = max(grades)
        dominant = grades.index(dominant)
        dominant += 9
        this.gr_imbalance = [st.stdev(grades), dominant]

    def addStudent(this, student):
        this.students.append(student)
        this.getGenderBalance()
        this.getGradeBalance()


def buildStudentArray(filepath):
    column_headers = ["email", "grade", "gender", "participation", "first", "second", "third", "fourth", "fifth", "sixth"]
    columns=[1, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    form_frame = pd.read_csv(filepath, header=0, names=column_headers, usecols=columns)
    form_frame = form_frame[form_frame.participation == "Yes, I would like to be scheduled into a SAiL session for May."]
    form_frame = form_frame.drop(columns="participation")

    students = []
    for index, row in form_frame.iterrows():
        students.append(Student(row["first"], row["second"], row["third"], row["fourth"], row["fifth"], row["sixth"], row["grade"], row["email"], row["gender"]))
    return students

def buildSessionArray(filepath):
    session_frame = pd.read_csv(filepath, names=["id", "capacity"])

    sessions = {}
    for index, row in session_frame.iterrows():
        sessions[row.id] = Session(row.capacity)
    return sessions

def computeBalances(sessions):
    balances = {}
    for key in sessions:
        balances[key] = max(sessions[key].gr_imbalance[0], sessions[key].ge_imbalance[0])
    #    print(str(sessions[key].gr_imbalance[0]) + "  " + str(sessions[key].ge_imbalance[0]) + "  " + str(balances[key][0]))
    return balances

def assignStudents(students, sessions):
    not_according_to_preferences = []

    for column in range(0, 3):
        if len(students) == 0:
            break
        sorted = []
        for i in range(0, len(students)):
            pref_session_id = students[i].choices[column]
            if sessions[pref_session_id].capacity > 0:
                sessions[pref_session_id].capacity -= 1
                sessions[pref_session_id].addStudent(students[i])
                sorted.append(students[i])
        for student in sorted:
            students.remove(student)
        print(len(students))

    balances = computeBalances(sessions)
   # print(balances)

    sorted = []
    for student in students:
        bottom_ids = student.choices[3:6]
       # print(str(student.email) + str(bottom_ids))
        bottom_sessions = {bottom_ids[i] : balances[bottom_ids[i]] for i in range(0, 3)}
     #   print(bottom_sessions)

        would_worsen_balance = False
        for i in range(0, 3):
            if len(bottom_sessions) == 0:
                print(student.email)
                not_according_to_preferences.append(student)
                break

            key = max(bottom_sessions, key=bottom_sessions.get)
            session = sessions[key]
            if session.capacity > 0:
                if student.gender != session.ge_imbalance[1] or student.grade != session.gr_imbalance[1]:
                    sorted.append(student)
                    session.capacity -= 1
                    session.addStudent(student)
                    balances[key] = max(sessions[key].gr_imbalance[0], sessions[key].ge_imbalance[0])
                    break
                else:
                    would_worsen_balance = True
            else:
                del bottom_sessions[key]
        else:
            if would_worsen_balance:
                key = min(bottom_sessions, key=bottom_sessions.get)
                session = sessions[key]
                sorted.append(student)
                session.capacity -= 1
                session.addStudent(student)
                balances[key] = max(sessions[key].gr_imbalance[0], sessions[key].ge_imbalance[0])

    print([index.email for index in sorted])
    for student in sorted:
        students.remove(student)
    print(len(students))

    for student in students:
        not_according_to_preferences.append(student)

    return not_according_to_preferences

   # print("\n\nSTARTS HERE\n\n")
   # print(balances)

def refactor(sessions, min):
    deleted_students = []
    for key in sessions:
        if len(sessions[key].students) < min:
            deleted_students += sessions[key].students

    not_according_to_preferences = assignStudents(deleted_students, sessions)
    return sessions

def buildOutput(students, sessions, prefs_array):
    output_frame = pd.DataFrame(columns=["Email", "Session", "Assigned According to Prefs?"])
    for key in sessions:
        for student in sessions[key].students:
            prefs = "No" if student in prefs_array else "Yes"
            row = [student.email, key, prefs]
            output_frame.loc[len(output_frame.index)] = row

    for student in students:
        row = [student.email, "Couldn't Be Assigned", "No"]
        output_frame.loc[len(output_frame.index)] = row
    return output_frame



if __name__ == '__main__':
    students = buildStudentArray("input.csv")
    sessions = buildSessionArray("capacity.csv")
    notPrefs = assignStudents(students, sessions)
    resultFrame = buildOutput(sessions, notPrefs)
    resultFrame.to_csv("results.csv")
