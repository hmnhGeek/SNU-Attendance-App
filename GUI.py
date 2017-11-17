from Tkinter import *
import os
import subprocess as sub
import threading
import sys
import tkMessageBox as mbox
import pickle
import base64

root = Tk()
root.title("SNU Attendance App")
root.geometry('800x600')
root.resizable(height=0, width =0)

def about():
    '''
        function for menubar. not for other purposes.
    '''
    f = open("about.txt", 'r')
    abt = f.read()
    f.close()

    erase()
    insert_in_area(abt, blue_tag)

menubar = Menu(root)
filemenu = Menu(root, tearoff=0)
filemenu.add_command(label="About", command=about)
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="About", menu=filemenu)
root.config(menu=menubar)

# linux commands.
mark_cmd = "mark.py -m"
record_cmd = "mark.py -r"

# fonts
majestic = ('timesnewroman', 15)

var = IntVar()

# create a label for subprocess
subprocess_label = Label(root, text = "SUBPROCESS STDOUT", font = majestic).pack()

# create the text area
scrollbar = Scrollbar(root)
scrollbar.pack(side = RIGHT, fill = Y)
area = Text(root, yscrollcommand = scrollbar.set, width = 100, height = 30)
area.pack(padx = 5, pady = 5)

scrollbar.config(command = area.yview)
area.configure(state ="disabled")

# define some tags
error_tag = ["RED", 'red']
output_tag = ['GREEN', 'green']
blue_tag = ["BLUE", 'blue']

def insert_in_area(text,color = None):
    if color == None:
        area.configure(state = "normal")
        area.insert(END, text)
        area.configure(state = "disabled")
    else:
        area.configure(state = "normal")
        area.insert(END, text, color[0])
        area.tag_config(color[0], foreground=color[1])
        area.configure(state = "disabled")

def erase():
    area.configure(state = "normal")
    area.delete('1.0', END)
    area.configure(state = "disabled")

def Attendance_mark():
    erase()
    insert_in_area("Process is starting. Please wait for few seconds...\n\n")

    if var.get() == 1:

        process = sub.Popen("python "+mark_cmd+" --off",stdout=sub.PIPE,stderr=sub.PIPE,
        universal_newlines=True, shell = True, bufsize = 1)

        output = process.communicate()[0]
        insert_in_area("Output of the script...\n\n", blue_tag)
        insert_in_area(output, output_tag)

    else:

        process = sub.Popen("python "+mark_cmd,stdout=sub.PIPE,stderr=sub.PIPE,
        universal_newlines=True, shell = True, bufsize = 1)

        output, errors = process.communicate()
        insert_in_area("Output of the script...\n\n", ['BLUE', 'blue'])
        insert_in_area(output, output_tag)

        if errors != '':
            insert_in_area("\nYou are on Unix. Issue this 'sudo modprobe pcspkr' to use beep or use Windows.\n\nAbort\n\n"
            , error_tag)
            insert_in_area("The following errors caused the beep to malfunction...\n\n")
            insert_in_area(errors, error_tag)
            insert_in_area("\nYour attendance is not affected by this error. This error is just to notify the user about beep malfunction.\n\n",
            blue_tag)

def records():
    erase()
    insert_in_area("Process is starting. Please wait for few seconds...\n\n")

    if var.get() == 1:
        process = sub.Popen("python "+record_cmd+" --off",stdout=sub.PIPE,stderr=sub.PIPE,
        universal_newlines=True, shell = True, bufsize = 1)

        output = process.communicate()[0]
        insert_in_area("Output of the script...\n\n", blue_tag)
        insert_in_area(output, output_tag)

    else:
        process = sub.Popen("python "+record_cmd, stdout=sub.PIPE,stderr=sub.PIPE,
        universal_newlines=True, shell = True, bufsize = 1)

        output, errors = process.communicate()
        insert_in_area("Output of the script...\n\n", ['BLUE', 'blue'])
        insert_in_area(output, output_tag)

        if errors != '':
            insert_in_area("\nYou are on Unix. Issue this 'sudo modprobe pcspkr' to use beep or use Windows.\n\nAbort\n\n"
            , error_tag)
            insert_in_area("The following errors caused the beep to malfunction...\n\n")
            insert_in_area(errors, error_tag)

def set_reset():

    process = sub.Popen("python reseter.py", stdout=sub.PIPE,stderr=sub.PIPE,
    universal_newlines=True, shell = True, bufsize = 1)

    output, errors = process.communicate()

    if errors != '':
        process = sub.Popen("reseter.py", stdout=sub.PIPE,stderr=sub.PIPE,
        universal_newlines=True, shell = True, bufsize = 1)

        output, errors = process.communicate()

    insert_in_area("Done reset!!\n\n")
    mbox.showinfo("Alert", "To update the changes, the app will shutdown. You can restart it again.")

    root.destroy()


def newac():
    small_win = Toplevel()
    small_win.geometry('300x300')
    small_win.resizable(height = 0, width = 0)

    netid_label = Label(small_win, text = "SNU Net ID").pack()
    netid = Entry(small_win)
    netid.pack(pady = 10)

    password_label = Label(small_win, text = "Password").pack()
    password = Entry(small_win, show = "*")
    password.pack(pady = 10)

    def register():

        f = open('credentials.dat', 'wb')
        d = {}
        user = base64.b64encode(netid.get(), 'utf-8')
        passw = base64.b64encode(password.get(), 'utf-8')

        d.update({'username':user, 'password': passw})
        pickle.dump(d, f)

        f.close()

        mbox.showinfo("Alert", "Registered!! To update the changes, the app will shutdown. You can restart it again.")

        root.destroy()


    submit = Button(small_win, text = "Submit", command = register)
    submit.pack(pady = 10, padx = 10)

    small_win.mainloop()

def marking_thread():

    mark_thread = threading.Thread(target=Attendance_mark)
    mark_thread.daemon = True
    mark_thread.start()


def records_thread():
    rec_thread = threading.Thread(target=records)
    rec_thread.daemon = True
    rec_thread.start()

def RESET_thread():
    res_thread = threading.Thread(target = set_reset)
    res_thread.daemon = True
    res_thread.start()


# allow these to be normal only if account is present.
binfile = open('credentials.dat', 'rb')
d = {}
try:
    while True:
        d = pickle.load(binfile)
except:
    binfile.close()

# lets handle buttons now.
C1 = Checkbutton(root, text = "Turn Off Beep", variable = var,
                 onvalue = 1, offvalue = 0, height=2,
                 width = 20)
C1.pack()

mark_button = Button(root, text = "Mark Attendance", command = marking_thread)
mark_button.pack()
mark_button.place(x = 200, y = 500)

records_button = Button(root, text = "Attendance Record", command = records_thread)
records_button.pack()
records_button.place(x = 450, y = 500)

resetb = Button(root, text = "Remove Net ID", command = RESET_thread, width = 13)
resetb.pack()
resetb.place(x = 200, y = 550)

new = Button(root, text = "New Net ID", command = newac, width = 15)
new.pack()
new.place(x = 450, y = 550)

if d == {}:
    C1.config(state = "disabled")
    mark_button.config(state = "disabled")
    records_button.config(state = "disabled")
    resetb.config(state = "disabled")

else:
    new.config(state = "disabled")

root.mainloop()
