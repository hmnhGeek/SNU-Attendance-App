from Tkinter import *
import os
import subprocess as sub
import threading
import sys
import tkMessageBox as mbox
import pickle
import base64
import ttk
from PIL import Image, ImageTk
import winsound

# center a window
def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


# colors
tan = "tan"

root = Tk()

# add a chrome logo
img = ImageTk.PhotoImage(Image.open('chromeicon.ico'))

# add app icon
img1 = ImageTk.PhotoImage(Image.open('iconic.ico'))

# add disclaimer.png
img2 = ImageTk.PhotoImage(Image.open('disclaimer.png'))

root.config(background = tan)
root.title("SNU Attendance App")
root.geometry('800x650')
root.resizable(height=0, width =0)
root.iconbitmap(r'iconic.ico')

def dev():
    '''
        function for menubar. not for other purposes.
    '''
    f = open("about.txt", 'r')
    abt = f.read()
    f.close()

    erase()
    insert_in_area(abt, blue_tag)
    
    area.configure(state = "normal")
    area.image_create(END, image = img)
    area.insert(END, "Powered by Chrome", "p4")
    area.tag_config("p4", foreground="purple4", font = ("verdana", 20))
    area.configure(state = "disabled")

def disclaimer():
    erase()

    area.configure(state = "normal")
    area.image_create(END, image = img2)
    area.insert(END, "\n\nThe app is subjected to change in website\'s interface.\n\n", "r2")
    area.tag_config("r2", foreground="red2", font = ("verdana", 15))
    area.configure(state = "disabled")
    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)

def about():

    erase()
    
    area.configure(state = "normal")
    area.image_create(END, image = img1)
    area.insert(END, "\nSNU Attendance App!\nVersion 1.0", "p4")
    area.tag_config("p4", foreground="purple4", font = ("verdana", 20))
    area.configure(state = "disabled")

    insert_in_area("\nDeveloped in Python, for SNUites, by Himanshu Sharma.", special_tag)
    
menubar = Menu(root)
filemenu = Menu(root, tearoff=0)
filemenu.add_command(label="Developer", command=dev)
filemenu.add_command(label="About", command=about)
filemenu.add_command(label="Disclaimer", command=disclaimer)
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="About", menu=filemenu)
root.config(menu=menubar)

# linux commands.
mark_cmd = "mark.exe -m"
record_cmd = "mark.exe -r"

# fonts
majestic = ('timesnewroman', 15)

var = IntVar()

# create a label for subprocess
subprocess_label = Label(root, text = "SUBPROCESS STDOUT", font = majestic, background = tan).pack()

# define subprocess stdout font.
console_font = ('Arial', 12)

# create the text area
scrollbar = Scrollbar(root)
scrollbar.pack(side = RIGHT, fill = Y)
area = Text(root, yscrollcommand = scrollbar.set, width = 100, height = 25, font = console_font)
area.pack(padx = 5, pady = 5)

scrollbar.config(command = area.yview)
area.configure(state ="disabled")

# define some tags
error_tag = ["RED", 'red']
output_tag = ['GREEN', 'brown']
blue_tag = ["BLUE", 'blue']

special_tag = ["dgrod", "dark goldenrod"]

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
    area.delete("1.0", END)
    area.configure(state = "disabled")

def Attendance_mark():
    erase()
    insert_in_area("Process is starting. Please wait for few seconds...\n\n")

    if var.get() == 1:

        process = sub.Popen(mark_cmd+" --off",stdout=sub.PIPE,stderr=sub.PIPE,
        universal_newlines=True, shell = True, bufsize = 1)

        output = process.communicate()[0]
        insert_in_area("Output of the script...\n\n", blue_tag)
        insert_in_area(output, output_tag)

    else:

        process = sub.Popen(mark_cmd,stdout=sub.PIPE,stderr=sub.PIPE,
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
        process = sub.Popen(record_cmd+" --off",stdout=sub.PIPE,stderr=sub.PIPE,
        universal_newlines=True, shell = True, bufsize = 1)

        output = process.communicate()[0]
        insert_in_area("Output of the script...\n\n", blue_tag)
        insert_in_area(output, output_tag)

    else:
        process = sub.Popen(record_cmd, stdout=sub.PIPE,stderr=sub.PIPE,
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

    process = sub.Popen("reseter.exe", stdout=sub.PIPE,stderr=sub.PIPE,
    universal_newlines=True, shell = True, bufsize = 1)

    output, errors = process.communicate()

    insert_in_area("Done reset!!\n\n")
    mbox.showinfo("Alert", "To update the changes, the app will shutdown. You can restart it again.")

    root.destroy()


def newac():
    small_win = Toplevel()
    center(small_win)
    small_win.config(background = tan)
    small_win.iconbitmap(r'iconic.ico')
    small_win.geometry('300x200')
    small_win.resizable(height = 0, width = 0)

    netid_label = Label(small_win, text = "SNU Net ID", background = tan).pack()
    netid = ttk.Entry(small_win)
    netid.pack(pady = 10)

    password_label = Label(small_win, text = "Password", background = tan).pack()
    password = ttk.Entry(small_win, show = "*")
    password.pack(pady = 10)

    def register(event = None):

        f = open('credentials.dat', 'wb')
        d = {}
        user = base64.b64encode(netid.get(), 'utf-8')
        passw = base64.b64encode(password.get(), 'utf-8')

        d.update({'username':user, 'password': passw})
        pickle.dump(d, f)

        f.close()

        mbox.showinfo("Alert", "Registered!! To update the changes, the app will shutdown. You can restart it again.")

        root.destroy()


    submit = ttk.Button(small_win, text = "Submit", command = register)
    submit.pack(pady = 10, padx = 10)

    small_win.bind("<Return>", register)

    small_win.mainloop()

def marking_thread():

    mark_thread = threading.Thread(target=Attendance_mark)
    mark_thread.daemon = True
    mark_thread.start()


def records_thread():
    rec_thread = threading.Thread(target=records)
    rec_thread.daemon = True
    rec_thread.start()


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
                 width = 20, background = tan, activebackground = tan)
C1.pack()

mark_button = ttk.Button(root, text = "Mark Attendance", command = marking_thread)
mark_button.pack()
mark_button.place(x = 200, y = 540)

records_button = ttk.Button(root, text = "Attendance Record", command = records_thread)
records_button.pack()
records_button.place(x = 450, y = 540)

resetb = ttk.Button(root, text = "Remove Net ID", command = set_reset, width = 15)
resetb.pack()
resetb.place(x = 200, y = 590)

new = ttk.Button(root, text = "New Net ID", command = newac, width = 17)
new.pack()
new.place(x = 450, y = 590)

if d == {}:
    C1.config(state = "disabled")
    mark_button.config(state = "disabled")
    records_button.config(state = "disabled")
    resetb.config(state = "disabled")

else:
    new.config(state = "disabled")

root.mainloop()
