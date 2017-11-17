import cx_Freeze

executables = [cx_Freeze.Executable('GUI.py', icon = "iconic.ico"),
               cx_Freeze.Executable('mark.py'),
               cx_Freeze.Executable('reseter.py')]

cx_Freeze.setup(
    name='SNU Attendance App',
    options={"build_exe": {"packages":["selenium",
                                       "Tkinter",
                                       "os","subprocess",
                                       "threading",
                                       "sys","tkMessageBox",
                                       "pickle",
                                       "base64", "sys", "ttk", "PIL",
                                       "winsound"], "include_files":["credentials.dat",
                                                                   "about.txt",
                                                                   "chromedriver.exe",
                                                                   "iconic.ico", "chromeicon.ico",
                                                                                        "disclaimer.png"]}},

    description="Mark your attendance and view your records.",
    executables = executables
    )
