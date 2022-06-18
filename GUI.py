# (c) PKY 2020
from backend import *
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb

class GUI(tk.Frame):
    def __init__(this, parent):
        this.students = ""
        this.sessions = ""

        tk.Frame.__init__(this, parent)
        this.pack()
        this.defineWidgets()


    def defineWidgets(this):
        this.info = tk.Label(this, text="Select a students csv and a capacity csv")
        chooseStudents = tk.Button(this, text="select students", command=this.chooseStudents)
        this.studentsField = tk.Entry(this, width=30)
        chooseCapacity = tk.Button(this, text="select capacity", command=this.chooseSessions)
        this.capacityField = tk.Entry(this, width=30)
        minimum=tk.Label(this, text="minimum session size (default=3): ")
        this.min_cap = tk.Entry(this, width=10)
        execute = tk.Button(this, text="execute", command=this.executeSorter)

        this.info.grid(row=0, column=0, columnspan=2)
        chooseStudents.grid(row=1, column=0)
        this.studentsField.grid(row=1, column=1)
        chooseCapacity.grid(row=2, column=0)
        this.capacityField.grid(row=2, column=1)
        minimum.grid(row=3, column=0)
        this.min_cap.grid(row=3, column=1)
        execute.grid(row=4, column=0, columnspan=2)

    def executeSorter(this):
        if (this.students == "" or this.sessions == ""):
            mb.showwarning(title="Attention!", message="You must select a students file and a capacity file.")
        else:
            try :
                min_cap_arg = int(this.min_cap.get()) if this.min_cap.get() != "" else 3
                try:
                    studentArray = buildStudentArray(this.students)
                    sessionArray = buildSessionArray(this.sessions)
                    notPrefs = assignStudents(studentArray, sessionArray)
                    resultFrame = buildOutput(studentArray, sessionArray, notPrefs)
                    resultFrame.to_csv("results.csv")
                    this.info.config(text="Execution successfull! Output stored in results.csv")
                except Exception as e:
                    mb.showwarning(title="Warning!", message=str(e))
                    this.info.config(text="The program failed to execute due to an exception!")
            except ValueError as v:
                message = "You must enter a number as capacity. '" + this.min_cap.get() + "' is not a number."
                mb.showwarning(title="Warning!", message=message)
                this.info.config(text="The program failed to execute due to a ValueError!")


    def chooseStudents(this):
        this.students = fd.askopenfilename()
        this.studentsField.insert(0, this.students)
        if this.sessions != "":
            this.info.config(text="You may now execute")

    def chooseSessions(this):
        this.sessions = fd.askopenfilename()
        this.capacityField.insert(0, this.sessions)
        if this.sessions != "":
            this.info.config(text="You may now execute")



if __name__ == '__main__':
    window = tk.Tk()
    window.title("SAiL Sorter")

    mainFrame = GUI(window)

    window.mainloop()
