import webbrowser
from tkinter import *
import os
from tkinter import filedialog, colorchooser, font, Toplevel
import _tkinter
import win32api
from time import *


def wordwrap():
    global wrap
    if wrap.get():
        text.config(wrap='word')
    if not wrap.get():
        text.config(wrap='none')

def underline_it(*args):
    our_font.config(underline=bool(1))


def cut(*args):
    text.event_generate("<<Cut>>")


def copy(*args):
    text.event_generate("<<Copy>>")


def paste(*args):
    text.event_generate("<<Paste>>")


def font_type(*args):
    def font_size_chooser(e):
        our_font.config(size=font_size_listbox.get(font_size_listbox.curselection()))
        text.configure(font=our_font)

    # Change Font Style
    def font_style_chooser(e):
        style = font_style_listbox.get(font_style_listbox.curselection()).lower()

        if style == "bold":
            our_font.config(weight=style)
        if style == "regular":
            our_font.config(weight="normal", slant="roman", underline=True, overstrike=1)
        if style == "italic":
            our_font.config(slant=style)
        if style == "bold/italic":
            our_font.config(weight="bold", slant="italic")
        if style == "underline":
            our_font.config(underline=1)
        if style == "strike":
            our_font.config(overstrike=1)

        text.configure(font=our_font)

    # Create font chooser function
    def font_chooser(e):
        our_font.config(family=my_listbox.get(my_listbox.curselection()))
        text.configure(font=our_font)

    font_window = Tk()
    font_window.configure(bg='White')
    font_window.resizable(False, False)
    our_font = font.Font(family="Calibri", size=int("33"))

    # Add Frame
    my_frame = Frame(font_window, width=510, height=275, bg='White')
    my_frame.pack(pady=10)
    # Freeze Frame in place
    my_frame.grid_propagate(False)
    my_frame.columnconfigure(0, weight=10)
    # Add Labels
    font_label = Label(my_frame, text="Choose Font", font=("Calibri", 14))
    font_label.grid(row=0, column=0, padx=10, sticky=W)

    size_label = Label(my_frame, text="Font Size", font=("Calibri", 14))
    size_label.grid(row=0, column=1, sticky=W)

    style_label = Label(my_frame, text="Font Style", font=("Calibri", 14))
    style_label.grid(row=0, column=2, padx=10, sticky=W)

    # Add Listbox
    my_listbox = Listbox(my_frame, selectmode=SINGLE, width=40)
    my_listbox.grid(row=1, column=0, padx=10)

    # Size Listbox
    font_size_listbox = Listbox(my_frame, selectmode=SINGLE, width=20)
    font_size_listbox.grid(row=1, column=1)

    # Style Listbox
    font_style_listbox = Listbox(my_frame, selectmode=SINGLE, width=20)
    font_style_listbox.grid(row=1, column=2, padx=10)

    # Add Font Families To Listbox
    for f in font.families():
        my_listbox.insert('end', f)

    # Add Sizes to Size Listbox
    font_sizes = [8, 10, 12, 14, 16, 18, 20, 36, 48]
    for size in font_sizes:
        font_size_listbox.insert('end', size)

    # Add Styles To Style Listbox
    font_styles = ["Regular", "Bold", "Italic", "Bold/Italic", "Underline", "Strike"]
    for style in font_styles:
        font_style_listbox.insert('end', style)

    # Bind The Listbox
    my_listbox.bind('<ButtonRelease-1>', font_chooser)
    font_size_listbox.bind('<ButtonRelease-1>', font_size_chooser)
    font_style_listbox.bind('<ButtonRelease-1>', font_style_chooser)
    font_window.mainloop()


def right_click(e):
    right_menu.tk_popup(x=e.x_root, y=e.y_root)


def select_all(*args):
    text.tag_add('sel', '1.0', 'end')
    return "break"


def undo(*args):
    try:
        text.event_generate("<<Undo>>")

    except _tkinter.TclError:
        pass


def search(*args):
    chrome = webbrowser.Chrome(r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    ans = text.get(1.0, END)
    chrome.open("http://google.com/search?q=" + ans)


def find_and_replace(*args):
    def find():

        text.tag_remove('found', '1.0', END)

        s = find_ask_entry.get()

        if s:
            idx = '1.0'
            while 1:
                idx = text.search(s, idx, nocase=1,
                                  stopindex=END)

                if not idx:
                    break
                lastidx = '% s+% dc' % (idx, len(s))

                text.tag_add('found', idx, lastidx)
                idx = lastidx
            text.tag_config('found', foreground='red')
        find_ask_entry.focus_set()

    def find_replace():

        text.tag_remove('found', '1.0', END)

        s = find_ask_entry.get()
        r = replace_ask_entry.get()

        if s and r:
            idx = '1.0'
            while 1:
                idx = text.search(s, idx, nocase=1,
                                  stopindex=END)
                if not idx:
                    break
                lastidx = '% s+% dc' % (idx, len(s))

                text.delete(idx, lastidx)
                text.insert(idx, r)

                lastidx = '% s+% dc' % (idx, len(r))

                text.tag_add('found', idx, lastidx)
                idx = lastidx

            text.tag_config('found', foreground='green', background='yellow')
        find_ask_entry.focus_set()

    find_window = Toplevel()
    find_window.configure(bg="White")
    find_window.title("Find And Replace")
    find_window.iconphoto(False, photo)
    find_window.geometry('320x200')
    find_window.resizable(height=False, width=False)
    find_title_label = Label(find_window, text="Find And Replace", font=("Calibri Bold", 18), bg='White')
    find_title_label.place(x=60, y=0)
    find_ask_label = Label(find_window, text="Find :", bg='White', font=('Calibri', 13))
    find_ask_label.place(x=10, y=50)
    find_ask_entry = Entry(find_window, bg='White')
    find_ask_entry.place(x=55, y=53)
    replace_ask_label = Label(find_window, text='Replace With :', bg='White', font=('Calibri', 13))
    replace_ask_label.place(x=10, y=100)
    replace_ask_entry = Entry(find_window, bg='White')
    replace_ask_entry.place(x=115, y=104)
    find_btn = Button(find_window, text='Find', bg='White', height=1, width=8, command=find)
    find_btn.place(x=190, y=50)
    replace_btn = Button(find_window, text='Replace', bg='White', height=1, width=8, command=find_replace)
    replace_btn.place(x=240, y=100)
    find_window.mainloop()


def new_file():
    text.delete("1.0", END)
    window.title('*Untitled')
    status_bar.config(text="New File        ")

    global file
    file = False


def now(*args):
    now_time = strftime("%I:%M %p %m-%d-%y")
    text.insert(END, now_time)


def italics_it(*args):
    italics_font = font.Font(text, text.cget("font"))
    italics_font.configure(slant="italic")
    text.tag_configure("italic", font=italics_font)

    current_tags = text.tag_names("sel.first")

    if "italic" in current_tags:
        text.tag_remove("italic", "sel.first", "sel.last")
    else:
        text.tag_add("italic", "sel.first", "sel.last")


def bold_it(*args):
    try:
        bold_font = font.Font(text, text.cget("font"))
        bold_font.configure(weight="bold")

        text.tag_configure("bold", font=bold_font)

        current_tags = text.tag_names("sel.first")

        if "bold" in current_tags:
            text.tag_remove("bold", "sel.first", "sel.last")
        else:
            text.tag_add("bold", "sel.first", "sel.last")

    except Exception:
        return


def printer():
    file_print = filedialog.asksaveasfilename(initialdir="G:/",
                                              defaultextension='.txt',
                                              filetypes=[("Text Document", '.txt'),
                                                         ("Python File", '.py'),
                                                         ("Html File", '.html'),
                                                         "All Files"])

    if file_print:
        win32api.ShellExecute(0, "print", file_print, None, ".", 0)

    elif file_print == "":
        return

'''
def zoom(event):
    global font_size_current
    if event.delta > 1:
        current_font_size = int(font_size_current.get())
        new_font_size = current_font_size + 1
        font_size_current.set(str(new_font_size))
        text.config(font=("TkDefaultFont", new_font_size))

    else:
        current_font_size = int(font_size_current.get())
        new_font_size = current_font_size - 1
        font_size_current.set(str(new_font_size))
        text.config(font=("TkDefaultFont", new_font_size))
'''

def shortcuts(*args):
    shortcuts_window = Toplevel()
    shortcuts_window.iconphoto(False, photo)
    shortcuts_window.title("Keyboard Shortcuts")
    shortcuts_window.geometry("600x460")
    shortcuts_window.resizable(height=False, width=False)
    title_label = Label(shortcuts_window, text="Keyboard Shortcuts", font=('Calibri bold', 20))
    title_label.place(x=160, y=0)
    shortcut_1_1 = Label(shortcuts_window, text='Cut : ', font=('Calibri', 15))
    shortcut_1_1.place(x=5, y=50)
    shortcut_1_2 = Label(shortcuts_window, text="Ctrl", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_1_2.place(x=110, y=50)
    shortcut_1_3 = Label(shortcuts_window, text="+", font=('Calibri', 15))
    shortcut_1_3.place(x=160, y=50)
    shortcut_1_4 = Label(shortcuts_window, text="X", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_1_4.place(x=190, y=50)

    shortcut_2_1 = Label(shortcuts_window, text='Copy : ', font=('Calibri', 15))
    shortcut_2_1.place(x=5, y=90)
    shortcut_2_2 = Label(shortcuts_window, text="Ctrl", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_2_2.place(x=110, y=90)
    shortcut_2_3 = Label(shortcuts_window, text="+", font=('Calibri', 15))
    shortcut_2_3.place(x=160, y=90)
    shortcut_2_4 = Label(shortcuts_window, text="C", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_2_4.place(x=190, y=90)

    shortcut_3_1 = Label(shortcuts_window, text='Paste : ', font=('Calibri', 15))
    shortcut_3_1.place(x=5, y=130)
    shortcut_3_2 = Label(shortcuts_window, text="Ctrl", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_3_2.place(x=110, y=130)
    shortcut_3_3 = Label(shortcuts_window, text="+", font=('Calibri', 15))
    shortcut_3_3.place(x=160, y=130)
    shortcut_3_4 = Label(shortcuts_window, text="V", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_3_4.place(x=190, y=130)

    shortcut_4_1 = Label(shortcuts_window, text='Select All : ', font=('Calibri', 15))
    shortcut_4_1.place(x=5, y=170)
    shortcut_4_2 = Label(shortcuts_window, text="Ctrl", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_4_2.place(x=110, y=170)
    shortcut_4_3 = Label(shortcuts_window, text="+", font=('Calibri', 15))
    shortcut_4_3.place(x=160, y=170)
    shortcut_4_4 = Label(shortcuts_window, text="A", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_4_4.place(x=190, y=170)

    shortcut_5_1 = Label(shortcuts_window, text='Open File : ', font=('Calibri', 15))
    shortcut_5_1.place(x=5, y=210)
    shortcut_5_2 = Label(shortcuts_window, text="Ctrl", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_5_2.place(x=110, y=210)
    shortcut_5_3 = Label(shortcuts_window, text="+", font=('Calibri', 15))
    shortcut_5_3.place(x=160, y=210)
    shortcut_5_4 = Label(shortcuts_window, text="O", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_5_4.place(x=190, y=210)

    shortcut_6_1 = Label(shortcuts_window, text='Save File : ', font=('Calibri', 15))
    shortcut_6_1.place(x=5, y=250)
    shortcut_6_2 = Label(shortcuts_window, text="Ctrl", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_6_2.place(x=110, y=250)
    shortcut_6_3 = Label(shortcuts_window, text="+", font=('Calibri', 15))
    shortcut_6_3.place(x=160, y=250)
    shortcut_6_4 = Label(shortcuts_window, text="S ", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_6_4.place(x=190, y=250)

    shortcut_7_1 = Label(shortcuts_window, text='Undo : ', font=('Calibri', 15))
    shortcut_7_1.place(x=5, y=290)
    shortcut_7_2 = Label(shortcuts_window, text="Ctrl", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_7_2.place(x=110, y=290)
    shortcut_7_3 = Label(shortcuts_window, text="+", font=('Calibri', 15))
    shortcut_7_3.place(x=160, y=290)
    shortcut_7_4 = Label(shortcuts_window, text="Z ", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_7_4.place(x=190, y=290)

    shortcut_8_1 = Label(shortcuts_window, text='Font Color : ', font=('Calibri', 15))
    shortcut_8_1.place(x=5, y=330)
    shortcut_8_2 = Label(shortcuts_window, text="Ctrl", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_8_2.place(x=110, y=330)
    shortcut_8_3 = Label(shortcuts_window, text="+", font=('Calibri', 15))
    shortcut_8_3.place(x=160, y=330)
    shortcut_8_4 = Label(shortcuts_window, text="F ", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_8_4.place(x=190, y=330)

    shortcut_9_1 = Label(shortcuts_window, text='Font Type : ', font=('Calibri', 15))
    shortcut_9_1.place(x=5, y=370)
    shortcut_9_2 = Label(shortcuts_window, text="Ctrl", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_9_2.place(x=110, y=370)
    shortcut_9_3 = Label(shortcuts_window, text="+", font=('Calibri', 15))
    shortcut_9_3.place(x=160, y=370)
    shortcut_9_4 = Label(shortcuts_window, text="G", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_9_4.place(x=190, y=370)

    shortcut_14_1 = Label(shortcuts_window, text='Find And Replace : ', font=('Calibri', 15))
    shortcut_14_1.place(x=250, y=50)
    shortcut_14_2 = Label(shortcuts_window, text="F3", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_14_2.place(x=430, y=50)

    shortcut_15_1 = Label(shortcuts_window, text='Save as : ', font=('Calibri', 15))
    shortcut_15_1.place(x=250, y=90)
    shortcut_15_2 = Label(shortcuts_window, text="Ctrl", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_15_2.place(x=380, y=90)
    shortcut_15_3 = Label(shortcuts_window, text="+", font=('Calibri', 15))
    shortcut_15_3.place(x=430, y=90)
    shortcut_15_4 = Label(shortcuts_window, text="Shift ", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_15_4.place(x=460, y=90)
    shortcut_15_5 = Label(shortcuts_window, text="+", font=('Calibri', 15))
    shortcut_15_5.place(x=510, y=90)
    shortcut_15_6 = Label(shortcuts_window, text="S ", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_15_6.place(x=540, y=90)

    shortcut_16_1 = Label(shortcuts_window, text='Print : ', font=('Calibri', 15))
    shortcut_16_1.place(x=250, y=130)
    shortcut_16_2 = Label(shortcuts_window, text="Ctrl", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_16_2.place(x=380, y=130)
    shortcut_16_3 = Label(shortcuts_window, text="+", font=('Calibri', 15))
    shortcut_16_3.place(x=430, y=130)
    shortcut_16_4 = Label(shortcuts_window, text="P ", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_16_4.place(x=460, y=130)

    shortcut_17_1 = Label(shortcuts_window, text='Bold  :', font=('Calibri', 15))
    shortcut_17_1.place(x=250, y=170)
    shortcut_17_2 = Label(shortcuts_window, text="Ctrl", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_17_2.place(x=380, y=170)
    shortcut_17_3 = Label(shortcuts_window, text="+", font=('Calibri', 15))
    shortcut_17_3.place(x=430, y=170)
    shortcut_17_4 = Label(shortcuts_window, text="B ", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_17_4.place(x=460, y=170)

    shortcut_18_1 = Label(shortcuts_window, text='Underline  :', font=('Calibri', 15))
    shortcut_18_1.place(x=250, y=210)
    shortcut_18_2 = Label(shortcuts_window, text="Ctrl", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_18_2.place(x=380, y=210)
    shortcut_18_3 = Label(shortcuts_window, text="+", font=('Calibri', 15))
    shortcut_18_3.place(x=430, y=210)
    shortcut_18_4 = Label(shortcuts_window, text="U ", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_18_4.place(x=460, y=210)

    shortcut_19_1 = Label(shortcuts_window, text='Italics  :', font=('Calibri', 15))
    shortcut_19_1.place(x=250, y=250)
    shortcut_19_2 = Label(shortcuts_window, text="Ctrl", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_19_2.place(x=380, y=250)
    shortcut_19_3 = Label(shortcuts_window, text="+", font=('Calibri', 15))
    shortcut_19_3.place(x=430, y=250)
    shortcut_19_4 = Label(shortcuts_window, text="Shift ", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_19_4.place(x=460, y=250)
    shortcut_19_5 = Label(shortcuts_window, text="+", font=('Calibri', 15))
    shortcut_19_5.place(x=510, y=250)
    shortcut_19_6 = Label(shortcuts_window, text="I ", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_19_6.place(x=540, y=250)

    shortcut_20_1 = Label(shortcuts_window, text='Current  :', font=('Calibri', 15))
    shortcut_20_1.place(x=250, y=290)
    shortcut_20_2 = Label(shortcuts_window, text="F5", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_20_2.place(x=380, y=290)

    shortcut_21_1 = Label(shortcuts_window, text='New File  :', font=('Calibri', 15))
    shortcut_21_1.place(x=250, y=330)
    shortcut_21_2 = Label(shortcuts_window, text="Ctrl", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_21_2.place(x=380, y=330)
    shortcut_21_3 = Label(shortcuts_window, text="+", font=('Calibri', 15))
    shortcut_21_3.place(x=430, y=330)
    shortcut_21_4 = Label(shortcuts_window, text="N ", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_21_4.place(x=460, y=330)

    shortcut_21_1 = Label(shortcuts_window, text='Zoom  :', font=('Calibri', 15))
    shortcut_21_1.place(x=250, y=370)
    shortcut_21_2 = Label(shortcuts_window, text="Ctrl", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_21_2.place(x=380, y=370)
    shortcut_21_3 = Label(shortcuts_window, text="+", font=('Calibri', 15))
    shortcut_21_3.place(x=430, y=370)
    shortcut_21_4 = Label(shortcuts_window, text="MouseWheel ", borderwidth=2, bg='Grey', font=('Calibri', 15))
    shortcut_21_4.place(x=460, y=370)

    shortcuts_window.mainloop()


def about_scribbler(*args):
    creator_window = Toplevel()
    creator_window.resizable(height=False, width=False)
    creator_window.iconphoto(False, photo)
    creator_window.configure(background="White")
    new_photo = PhotoImage(file='Photos/new_icon.png')
    creator_window.geometry("520x320")
    creator_text = "Scribbler is a free and open source text editor created by Aarif.\n " \
                   "This is a inspiration and copy of many text editors like Notepad and \nThe Ubuntu Text Editor.\n " \
                   "Some might say that it is a 'COPY' or 'BAD COPY' of Notepad"
    copyright_text = "-By Aarif Ahmed \n © Aarif Corporation. All Rights Reserved"
    creator_window.title("About Scribbler")
    scribbler_label = Label(creator_window, image=new_photo, background="White")
    scribbler_label.place(x=0, y=0)
    copyright_label = Label(creator_window, text=copyright_text, font=('Calibri', 13), bg="White")
    copyright_label.place(x=130, y=50)
    about_label = Label(creator_window, text=creator_text, font=('Calibri', 13), bg="White")
    about_label.place(x=0, y=150)
    ok_button = Button(creator_window, text="Ok", command=creator_window.destroy, height=1, width=8, bg="white")
    ok_button.place(x=400, y=270)
    creator_window.mainloop()


def about(*args):
    window_aarif = Toplevel()
    about_text = "Scribbler is developed by a Solo Python Developer Aarif.\n" \
                 "He is a Python Developer and a Gamer. \nHe loves programming and knows programming languages \n" \
                 "like Python, HTML and is learning C, C++, Java, CSS, Javascript."

    window_aarif.iconphoto(False, photo)
    window_aarif.configure(bg='White')
    window_aarif.resizable(height=False, width=False)
    window_aarif.title("About The Developer")
    window_aarif.geometry("430x330")
    new_photo = PhotoImage(file='Photos/new_icon.png')
    scribbler_photo = Label(window_aarif, image=new_photo, bg='White')
    scribbler_photo.place(x=0, y=0)
    copyright_text = "-By Aarif Ahmed \n © Aarif Corporation. All Rights Reserved"
    copyright_label = Label(window_aarif, text=copyright_text, font=('Calibri', 13), bg="White")
    copyright_label.place(x=130, y=50)
    aarif_label = Label(window_aarif, bg='White', text=about_text, font=('Calibri', 13))
    aarif_label.place(x=0, y=170)
    ok_button = Button(window_aarif, text="Ok", command=window_aarif.destroy, height=1, width=8, bg="white")
    ok_button.place(x=350, y=300)
    window_aarif.mainloop()


def color_chooser(*args):
    color = colorchooser.askcolor(title="Select Color")
    text.config(fg=color[1])


def open_file(*args):
    file_path = filedialog.askopenfilename(initialdir="G:/",
                                           title="Select File",
                                           filetypes=[("Text Document", '.txt'),
                                                      ("HTML", '.html'),
                                                      ("Python File", '.py'),
                                                      ("All Files", '.*')])

    if file_path is None:
        return

    else:
        try:
            window.title(os.path.basename(file_path))
            text.delete(1.0, END)

            nds_file = open(file_path, "r")

            text.insert(1.0, nds_file.read())

        except Exception:
            return

        finally:
            nds_file.close()
            set_file_path(file_path)


def save_file(*args):
    global file
    if file == '':
        ns_file = filedialog.asksaveasfilename(initialdir="G:/",
                                               defaultextension='.txt',
                                               filetypes=[("Text Document", '.txt'),
                                                          ("Python File", '.py'),
                                                          ("Html File", '.html'),
                                                          "All Files"])
        if ns_file is None:
            return
    else:
        ns_file = file
        if ns_file == '':
            return
    with open(ns_file, 'w') as nd_file:
        code = text.get('1.0', END)
        nd_file.write(code)
        set_file_path(ns_file)


def set_file_path(ns_file):
    global file
    file = ns_file


def exit_app(*args):
    def n_save():
        save_file()
        exit_window.destroy()
        window.destroy()

    def close():
        pass

    def n_exit():
        exit_window.destroy()
        window.destroy()

    def cancel():
        exit_window.destroy()

    if len(text.get('1.0', END)) == 1:
        window.destroy()

    else:
        exit_window = Toplevel()
        screen_width = exit_window.winfo_screenwidth()
        screen_height = exit_window.winfo_screenheight()
        app_width = 330
        app_height = 157
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        exit_window.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
        exit_window.protocol("WM_DELETE_WINDOW", close)
        exit_window.title("Do You Want To Save ?")
        exit_window.resizable(height=False, width=False)
        exit_window.configure(bg='White')
        ask_label = Label(exit_window, text="Do You Want To Exit Without Saving ?", bg='White', font=('Calibri', 13))
        ask_label.pack(pady=10)
        save_btn = Button(exit_window, text='Save', font=('Calibri', 10), height=1, width=9, bg='white',
                          command=n_save)
        save_btn.place(x=40, y=70)
        d_save_btn = Button(exit_window, text="Don't Save", font=('Calibri', 10), height=1, width=9, bg='White',
                            command=n_exit)
        d_save_btn.place(x=130, y=70)
        cancel_btn = Button(exit_window, text="Cancel", font=("Calibri", 10), bg='White', height=1, width=9,
                            command=cancel)
        cancel_btn.place(x=220, y=70)
        exit_window.mainloop()


def save_as(*args):
    save_as_file = filedialog.asksaveasfilename(initialdir="G:/",
                                                defaultextension='.txt',
                                                filetypes=[("Text Document", '.txt'),
                                                           ("Python File", '.py'),
                                                           ("Html File", '.html'),
                                                           "All Files"
                                                           ])
    if save_as_file is None:
        return
    else:
        ns_file = file
        if ns_file == '':
            return
    with open(ns_file, 'w') as nd_file:
        code = text.get('1.0', END)
        nd_file.write(code)
        set_file_path(ns_file)


window = Tk()

file = ''

window.geometry("1000x500")

window.title("Scribbler")
photo = PhotoImage(file='Photos/icon.png')
window.iconphoto(False, photo)

window.protocol('WM_DELETE_WINDOW', exit_app)

window.bind("<Control_L>s", save_file)
window.bind("<Control_R>s", save_file)
window.bind("<Control_L>o", open_file)
window.bind("<Control_R>o", open_file)
window.bind("<Button-3>", right_click)
window.bind("<Control_L>a", select_all)
window.bind("<Control_R>a", select_all)
window.bind("<Control_L>z", undo)
window.bind("<Control_R>z", undo)
window.bind("<Control_L>f", font_type)
window.bind("<Control_R>f", font_type)
window.bind("<Control_L>g", color_chooser)
window.bind("<Control_R>g", color_chooser)
window.bind("<Control-S>", save_as)
window.bind("<F3>", find_and_replace)
# window.bind("<Control-MouseWheel>", zoom)
window.bind("<F5>", now)
window.bind('<Control-I>', italics_it)
window.bind('<Control-b>', bold_it)
window.bind('<Control-u>', underline_it)
window.bind('<Control-n>', new_file)

our_font = font.Font(family="calibri", size=int("25"))

text = Text(window, font=our_font, undo=True, wrap='word')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
text.grid(sticky=N + E + S + W)
scroll_bar = Scrollbar(text)
scroll_bar.pack(side=RIGHT, fill=Y)
text.config(yscrollcommand=scroll_bar.set)

status_bar = Label(window, text="Ready", bd=1, relief=SUNKEN, anchor=W)

# Add the Label widget to the bottom of the window
status_bar.grid(row=1, column=0, columnspan=3, sticky=W + E)

menu_bar = Menu(window)
window.configure(menu=menu_bar)
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New..", command=new_file, accelerator='Ctrl + N')
file_menu.add_command(label="Open", command=open_file, accelerator='Ctrl + O')
file_menu.add_command(label="Save..", command=save_file, accelerator='Ctrl + S')
file_menu.add_command(label="Save as", command=save_as, accelerator='Ctrl + Shift + S')
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app, accelerator='Alt + F4')

edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=cut, accelerator='Ctrl + X')
edit_menu.add_command(label="Copy", command=copy, accelerator='Ctrl + C')
edit_menu.add_command(label="Paste", command=paste, accelerator='Ctrl + V')
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command=undo, accelerator='Ctrl + Z')
edit_menu.add_separator()
edit_menu.add_command(label="Search With Chrome", command=search, accelerator="Ctrl + D")
edit_menu.add_separator()
edit_menu.add_command(label="Find And Replace", command=find_and_replace, accelerator='F3')
edit_menu.add_separator()
edit_menu.add_command(label="Time/Date", command=now, accelerator='F5')

format_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Format", menu=format_menu)
format_menu.add_command(label="Font", command=font_type, accelerator='Ctrl + F')
format_menu.add_command(label="Font Color", command=color_chooser, accelerator='Ctrl + G')
wrap = BooleanVar(value=bool(1))
format_menu.add_checkbutton(label='Word Wrap', command=wordwrap, onvalue=True, offvalue=False,
                            variable=wrap)

about_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=about_menu)
about_menu.add_command(label="About The Developer", command=about)
about_menu.add_command(label="About Scribbler", command=about_scribbler)
about_menu.add_separator()
about_menu.add_command(label="Keyboard Shortcuts", command=shortcuts)

right_menu = Menu(window, tearoff=0)
right_menu.add_command(label="Cut", command=cut, accelerator='Ctrl + X')
right_menu.add_command(label="Copy", command=copy, accelerator='Ctrl + C')
right_menu.add_command(label="Paste", command=paste, accelerator='Ctrl + V')
right_menu.add_command(label="Delete", command=lambda: text.event_generate("<Delete>"), accelerator='Delete')
right_menu.add_separator()
right_menu.add_command(label="Select All", command=select_all, accelerator='Ctrl + A')
right_menu.add_separator()
right_menu.add_command(label="Undo", command=undo, accelerator='Ctrl + Z')

window.mainloop()
