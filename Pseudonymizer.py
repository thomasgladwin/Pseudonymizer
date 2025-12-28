import os
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
import E17
import depseudon
import sys
# To use styling:
from tkinter import *
from tkinter.ttk import *
from ttkthemes import ThemedTk

files_to_process = ()
file_map = ""
initial_dir = os.path.dirname(sys.argv[0])
print(initial_dir)

def f_pseudon():
    if len(files_to_process) == 0:
        label_info.configure(text="Select files to process.")
        return
    label_info.configure(text="Pseudonymizing...")
    window.update()
    window.update_idletasks()
    print(files_to_process)
    out_dir = E17.E17(files_to_process)
    label_info.configure(text="Complete.")

def f_depseudon():
    if len(file_map) == 0 or len(files_to_process) == 0:
        label_info.configure(text="Select both files to process and the mapping file.")
        return
    label_info.configure(text="Depseudonymizing...")
    window.update()
    window.update_idletasks()
    depseudon.depseudon(files_to_process, file_map)
    label_info.configure(text="Complete.")

def browseFiles():
    global files_to_process
    global initial_dir
    files_to_process = fd.askopenfilenames(initialdir=initial_dir,
                                          title="Select a File",
                                          filetypes=(("Documents",
                                                      "*.txt *.docx"),
                                                     ("all files",
                                                      "*.*")))
    basenames = [os.path.basename(fn) for fn in files_to_process]
    text_files['state'] = 'normal'
    text_files.delete(1.0, tk.END)
    for fn in basenames:
        print(fn)
        text_files.insert('end', fn + "\n")
        initial_dir = os.path.dirname(fn)
    text_files['state'] = 'disabled'

def browseFiles_deps():
    global files_to_process
    global initial_dir
    files_to_process = fd.askopenfilenames(initialdir=initial_dir,
                                          title="Select a File",
                                          filetypes=(("Documents",
                                                      "*.txt *.docx"),
                                                     ("all files",
                                                      "*.*")))
    basenames = [os.path.basename(fn) for fn in files_to_process]
    text_files_deps['state'] = 'normal'
    text_files_deps.delete(1.0, tk.END)
    for fn in basenames:
        print(fn)
        text_files_deps.insert('end', fn + "\n")
        initial_dir = os.path.dirname(fn)
    text_files_deps['state'] = 'disabled'

def browseFile():
    global file_map
    global initial_dir
    file_map = fd.askopenfilename(initialdir=initial_dir,
                                          title="Select a File",
                                          filetypes=(("Text",
                                                      "*.txt"),
                                                     ("all files",
                                                      "*.*")))
    # Change label contents
    basename = os.path.basename(file_map)
    label_file_deps.configure(text="File selected: " + basename)
    initial_dir = os.path.dirname(basename)

# Create the window
# window = Tk()
window = ThemedTk(theme="arc")
window.title('File Explorer')
w = window.winfo_screenwidth() / 4
h = window.winfo_screenheight() / 2
# window.geometry("%dx%d" % (w, h))
# window.config(background="black")

tabControl = ttk.Notebook(window)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text ='Pseudonymize')
tabControl.add(tab2, text ='Depseudonymize')
tabControl.pack(expand = 1, fill ="both")

# Pseudon tab
frame_top = Frame(tab1)
label_info = Label(frame_top, text="Pseudonymize", justify="center")

frame_text_files = Frame(tab1)
text_files = Text(frame_text_files, width=40, height=10, fg="blue")
text_files.insert(1.0, "No files selected yet.")
yscroll = Scrollbar(frame_text_files, orient = 'vertical', command = text_files.yview)
text_files['yscrollcommand'] = yscroll.set
text_files['state'] = 'disabled'

button_files = Button(tab1,
                        text="Select files to process",
                        command=browseFiles)
button_pseud = Button(tab1,
                        text="Pseudonymize",
                        command=f_pseudon)
button_exit = Button(tab1,
                     text="Exit",
                     command=sys.exit)

iRow = 1
frame_top.grid(column=0, row=iRow, pady=(0, 0), sticky="ew"); iRow += 1
frame_top.grid_rowconfigure(0, weight=1)
frame_top.grid_columnconfigure(0, weight=1)
label_info.grid(column=0, row=0, pady=(20, 20))

button_files.grid(column=0, row=iRow, pady=(20, 0)); iRow += 1
frame_text_files.grid(column=0, row=iRow, padx=(5, 5)); iRow += 1
text_files.grid(column=0, row=0)
yscroll.grid(column=1, row=0, sticky = 'ns')
button_pseud.grid(column=0, row=iRow, pady=(20, 0)); iRow += 1
button_exit.grid(column=0, row=iRow, pady=(20, 20)); iRow += 1
nRows = iRow

#window.grid_columnconfigure(0,weight=1)
#for iRow in range(nRows):
#    window.grid_rowconfigure(iRow,weight=1)
#frame_text_files.grid_columnconfigure(0,weight=1)
#frame_text_files.grid_columnconfigure(1,weight=1)
#frame_text_files.grid_rowconfigure(0,weight=1)

# Despeudon tab
frame_top_deps = Frame(tab2)
label_info_deps = Label(frame_top_deps, text="Depseudonymize", justify="center")

frame_text_files_deps = Frame(tab2)
text_files_deps = Text(frame_text_files_deps, width=40, height=10, fg="blue")
text_files_deps.insert(1.0, "No files selected yet.")
yscroll_deps = Scrollbar(frame_text_files_deps, orient = 'vertical', command = text_files_deps.yview)
text_files_deps['yscrollcommand'] = yscroll_deps.set
text_files_deps['state'] = 'disabled'

label_file_deps = Label(tab2, text="No mapping file selected yet")

button_files_deps = Button(tab2,
                        text="Select files to process",
                        command=browseFiles_deps)
button_file_map = Button(tab2,
                        text="Select mapping file",
                        command=browseFile)
button_depseud = Button(tab2,
                        text="Depseudonymize",
                        command=f_depseudon)
button_exit_deps = Button(tab2,
                     text="Exit",
                     command=sys.exit)

iRow = 1
frame_top_deps.grid(column=0, row=iRow, pady=(0, 0), sticky="ew"); iRow += 1
frame_top_deps.grid_rowconfigure(0, weight=1)
frame_top_deps.grid_columnconfigure(0, weight=1)
label_info_deps.grid(column=0, row=0, pady=(20, 20))

button_files_deps.grid(column=0, row=iRow, pady=(20, 0)); iRow += 1
frame_text_files_deps.grid(column=0, row=iRow, padx=(5, 5)); iRow += 1
text_files_deps.grid(column=0, row=0)
yscroll_deps.grid(column=1, row=0, sticky = 'ns')
button_file_map.grid(column=0, row=iRow, pady=(20, 0)); iRow += 1
label_file_deps.grid(column=0, row=iRow, columnspan=1); iRow += 1
button_depseud.grid(column=0, row=iRow, pady=(10, 0)); iRow += 1
button_exit_deps.grid(column=0, row=iRow, pady=(20, 20)); iRow += 1
nRows = iRow

#window.grid_columnconfigure(0,weight=1)
#for iRow in range(nRows):
#    window.grid_rowconfigure(iRow,weight=1)
#frame_text_files.grid_columnconfigure(0,weight=1)
#frame_text_files.grid_columnconfigure(1,weight=1)
#frame_text_files.grid_rowconfigure(0,weight=1)

#style = ttk.Style(window)
#style.theme_use('clam')  # put the theme name here, that you want to use
window.mainloop()
