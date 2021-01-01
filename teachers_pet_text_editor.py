from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror, askokcancel
from tkinter.colorchooser import askcolor
from tkinter.scrolledtext import ScrolledText
from tkinter import *
from tkinter.ttk import *
import time
import os
import string
import math

class SimpleTextEditor:
    """set up text edit program with __init__ and callback functions"""
    def __init__(self):
        # window root
        self.root = Tk()
        self.root.title('Teacher\'s Pet')
        self.root.rowconfigure(1, weight=1, minsize=500,)
        self.root.rowconfigure([0, 2], weight=0, minsize=3,)
        self.root.columnconfigure(1, weight=1, minsize=500,)
        # set the window background color
        self.root.config(background='#BDD4E2',)
        self._frame_style = Style()
        self._frame_style.configure('TFrame', relief='sunken', background='#BDD4E2',
                                    borderwidth=1, highlightthickness=1,
                                    highlightbackground='#BDD4E2', highlightcolor='#BDD4E2',)
        self._frame_style_nested = Style()
        self._frame_style_nested.configure('Nested.TFrame', relief='flat', background='#BDD4E2',
                                    highlightbackground='#BDD4E2', highlightcolor='#BDD4E2',)
        self._btn_style = Style()
        self._btn_style.configure('TButton', relief='groove', font=('BOLD', 14),)                         
        self._lbl_style = Style()
        self._lbl_style.configure('TLabel', highlightbackground='pink', background='pink',)
        # frame timer 
        self.frm_timer = Frame(self.root, style='TFrame',)
        self.frm_timer.grid(row=0, column=0, columnspan=2, sticky='EW', padx=10, pady=8,)
        self.frm_timer.columnconfigure([1, 2, 3, 4, 5], weight=1, minsize=85,)
        # label timer
        self.lbl_timer = Label(self.frm_timer, text='\N{STOPWATCH}', font=('BOLD', 36), anchor=('center'), width=6,
                           style='TLabel', )
        self.lbl_timer.grid(row=0, column=0, padx=3, pady=3, sticky='NEWS',)
        # frame scale_hr
        self.frm_scale_hr = Frame(self.frm_timer, style='Nested.TFrame',)
        self.frm_scale_hr.grid(row=0, column=1, sticky='NEWS',pady=5, )
        self.frm_scale_hr.rowconfigure([0, 1], weight=0,)
        self.frm_scale_hr.columnconfigure(0, weight=1,)
        # label scale_hr
        self.lbl_scale_hr = Label(self.frm_scale_hr, text=f"Hours", style='TLabel',)
        self.lbl_scale_hr.grid(row=0, column=0, pady=3,)
        # scale hour(s)
        self.scale_hr = Scale(self.frm_scale_hr, from_=0, to=4, orient='horizontal', length=85, command=self.verify_scale_hr,)
        self.scale_hr.grid(row=1, column=0, sticky='WE', pady=5, padx=15, ipadx=3,)
        # frame scale_min
        self.frm_scale_min = Frame(self.frm_timer, style='Nested.TFrame', )
        self.frm_scale_min.grid(row=0, column=2, sticky='NEWS', pady=5, )
        self.frm_scale_min.rowconfigure([0, 1], weight=0,)
        self.frm_scale_min.columnconfigure(0, weight=1,)
        # label scale_min
        self.lbl_scale_min = Label(self.frm_scale_min, text=f"Minutes", anchor=('center'), style='TLabel',)
        self.lbl_scale_min.grid(row=0, column=0, pady=3,)
        # scale minute(s)
        self.scale_min = Scale(self.frm_scale_min, from_=0, to=59, command=self.verify_scale_min,
                                  orient='horizontal', length=85,)
        self.scale_min.grid(row=1, column=0, sticky='WE', pady=5, padx=15, ipadx=3,)
        # button start
        self.btn_start = Button(self.frm_timer, text='start', style='TButton',
                                   command=self.start_timer,)
        self.btn_start.grid(row=0, column=3, sticky='E', pady=5, padx=15, ipadx=3,)
        # button stop
        self.btn_stop = Button(self.frm_timer, text='stop', style='TButton', command=self.stop_timer, state='disabled',)
        self.btn_stop.grid(row=0, column=4, sticky='E', pady=5, padx=15, ipadx=3,)
        # timer stop btn switch
        self.timer_stop = False
        # label remaining_time
        self.remaining_hr = 0
        self.remaining_min = 0
        self.remaining_sec = 0
        self.timer_label = Label(self.frm_timer, font=('BOLD', 14,), anchor=('center'), width=30, text = f"remaining time",)
        self.timer_label.grid(row=0, column=5, sticky='WE', pady=5, padx=15, ipadx=3,)
        # frame at left with 5 buttons(open, new file, save, save as, theme)
        # set the left frame background color
        self.frm_btn = Frame(self.root, height=4,) 
        self.frm_btn.grid(row=1, column=0, sticky='NS', padx=10, pady=8,)
        self.frm_btn.rowconfigure([0, 1, 2, 3 ], weight=0, minsize=3,)
        self.frm_btn.rowconfigure(4, weight=1, minsize=3,)
        # button Open 
        self.btn_open = Button(self.frm_btn, text='open', style='TButton', command=self.open_file,)
        self.btn_open.grid(row=0, column=0, sticky='EW', padx=7, pady=7, ipadx=3, ipady=3,)
        # button new file 
        self.btn_new_file = Button(self.frm_btn, text='new file', style='TButton', command=self.new_file,)
        self.btn_new_file.grid(row=1, column=0, sticky='EW', padx=7, pady=7, ipadx=3, ipady=3,)
        # button save 
        self.btn_save = Button(self.frm_btn, text='save',style='TButton',  command=self.save,)
        self.btn_save.grid(row=2, column=0, sticky='EW', padx=7, pady=7, ipadx=3, ipady=3,)
        # button save as 
        self.btn_save_as = Button(self.frm_btn, text='save as', style='TButton', command=self.save_as,)
        self.btn_save_as.grid(row=3, column=0, sticky='EW', padx=7, pady=7, ipadx=3, ipady=3,)
        # button theme 
        self.btn_theme = Button(self.frm_btn, text='theme', style='TButton', command=self.color_change,)
        self.btn_theme.grid(row=4, column=0, sticky='EWS', padx=7, pady=4, ipadx=3,)
        # scrolled text (comes with a frame automatically)
        self.edit_text = ScrolledText(self.root, font=('Menlo', 14), wrap='word', undo=True,
                                      highlightbackground='#D3DEE5', highlightcolor='#D3DEE5',
                                      selectbackground='#E2EDBB',)
        # frame scrolled text
        self.edit_text.frame.config(borderwidth=3, relief='ridge', highlightthickness=3,
                                    highlightbackground='#D3DEE5', highlightcolor='#D3DEE5',)
        # text silver bg outliner 
        self.edit_text.grid(row=1, column=1, sticky='NEWS', padx=8, pady=5, ipadx=5, ipady=2,)
        # variable text to store content of open_file object in case of error, it's needed to rollback
        self.text = None
        # varibale to pause the word count
        self.pause_word_count = False
        # label word_count 
        self.word_count = 0
        self.word_count_label = Label(self.root, text=f"word count  {self.word_count} ", font=('BOLD', 14,),
                                         anchor=('ne'), style='TLabel',)
        self.word_count_label.grid(row=2, column=1, sticky='E', pady=10, padx=10, ipadx=3, ipady=2,)
        # mainloop protocol 
        self.root.protocol("WM_DELETE_WINDOW", self.close_window,)
        # place cursor in the edit_text area
        self.edit_text.focus()
        # start count_words()
        self.count_words()
        # mainloop
        self.root.mainloop()
        

    def verify_scale_hr(self,e =None):
        adjusted = round(self.scale_hr.get())
        self.lbl_scale_hr['text'] = f"Hour(s): {adjusted}"
        self.remaining_hr = adjusted


    def verify_scale_min(self,e=None):
        adjusted = round(self.scale_min.get())
        self.lbl_scale_min['text'] = f"Minutes: {adjusted}"
        self.remaining_min = adjusted


    def start_timer(self):
        """set the timer, call self.timer"""
        if self.remaining_hr == 0 and self.remaining_min == 0:
            self.timer_label['text'] = "Invalid Timer Setting"
        else:
            # disable all buttons
            self.btn_stop.state(['!disabled'])
            self.scale_hr.state(['disabled'])
            self.scale_min.state(['disabled'])
            self.btn_start.state(['disabled'])
            self.btn_open.state(['disabled'])
            self.btn_new_file.state(['disabled'])
            self.btn_save.state(['disabled'])
            self.btn_save_as.state(['disabled'])
            self.btn_theme.state(['disabled'])
            # call timer 
            self.timer()
            

    def stop_timer(self):
        self.btn_stop['state'] = 'disabled'
        self.btn_save.state(['!disabled'])
        self.btn_save_as.state(['!disabled'])
        self.timer_stop = True
        
    
    def open_file(self):
        """open file for editing"""
        file = askopenfilename(title='Choose A File ',)
        if not file:
            pass
        else:
            try:
                with open(file) as input:
                    self.text = input.read()
                self.edit_text.delete('1.0', END)
                self.edit_text.insert(END, self.text)
                self.root.title(f'Teacher\'s Pet - {file}')
            except:
                showerror(title='ERROR', master=self.edit_text, message='An Error Occurs\nTry Again',)
    
    
    def new_file(self):
        """create a new window to start a new file"""
        SimpleTextEditor()


    def save(self):
        """update saved file"""
        self.pause_word_count = True
        outfile = self.edit_text.get('1.0', END)
        if self.root.title() == 'Teacher\'s Pet':
            file = asksaveasfilename(
                title='Save',
                defaultextension='txt',
                initialdir=os.getcwd()
                )
            if not file:
                return
            else:
                try:
                    with open(file, 'w') as output:
                        output.write(outfile)
                    self.root.title(f'Teacher\'s Pet - {file}')
                    self.text = outfile
                except:
                    showerror(title='ERROR', master=self.edit_text, message='An Error Occurs:\nFile Not Saved',)
                    os.system(f"rm {file}")
                    self.pause_word_count = False
                    return
        else:
            filename = self.root.title().lstrip('Teacher\'s Pet - ')
            try:
                with open(filename, 'w') as output:
                    output.write(outfile)
                    self.text = outfile
            except:
                showerror(title='ERROR', master=self.edit_text, message='An Error Occurs:\nFile Not Saved',)
                # rollback to original text file version when initially opened
                with open(filename, 'w') as output:
                    output.write(self.text)
                    self.pause_word_count = False
                return
        lbl_status = Label(self.root, text='file saved', font=('BOLD', 14,))
        lbl_status.grid(row=2, column=0, sticky='sw',)
        lbl_status.after(1000, lbl_status.destroy)
        self.pause_word_count = False
                    

    def save_as(self):
        """save as file"""
        outfile = self.edit_text.get('1.0', END)
        self.pause_word_count = True
        if self.root.title() == 'Teacher\'s Pet':
            file = asksaveasfilename(
                title='Save As',
                defaultextension='txt',
                initialdir=os.getcwd()
                )
            if not file:
                return
            else:
                try:
                    with open(file, 'w') as output:
                        time.sleep(1)
                        output.write(outfile)
                    self.root.title(f'Teacher\'s Pet - {file}')
                    self.text = outfile
                except:
                    showerror(title='ERROR', master=self.edit_text, message='An Error Occurs:\nFile Not Saved',)
                    os.system(f"rm {file}")
                    self.pause_word_count = False
                    return
        else:
            current_fileName = self.root.title().lstrip('Teacher\'s Pet - ')
            file = asksaveasfilename(
                title='Save As',
                defaultextension='txt',
                initialdir=os.getcwd(),
                )
            if not file:
                return
            else:
                try:
                    with open(file, 'w') as output:
                        output.write(outfile)
                        self.root.title(f'Teacher\'s Pet - {file}')
                        self.text = outfile
                except:
                    showerror(title='ERROR', master=self.edit_text, message='An Error Occurs:\nFile Not Saved',)
                    # rollback to original text file version when initially opened
                    os.system(f"rm {file}")
                    self.pause_word_count = False
                    return
        lbl_status = Label(self.root, text='file saved', font=('BOLD', 14,),)
        lbl_status.grid(row=2, column=0, sticky='sw',)
        lbl_status.after(1000, lbl_status.destroy)
        self.pause_word_count = False
             

    def color_change(self):
        """change root and frm_btn background color"""
        color = askcolor(color='#BDD4E2',
                         title='Choose A Color:',
                         )[1]
        if not color:
            return
        else:
            self.root.config(background=color,)
            self._frame_style.configure('TFrame', background=color)
            self._lbl_style.configure('TLabel', background=color)
            return
        

    def close_window(self):
        current_text = self.edit_text.get('1.0', END).rstrip(string.whitespace)
        # current file is new (not saved) 
        if self.root.title() == 'Teacher\'s Pet':
            # and current_text is not blank
            if current_text != '':
                # ask to confirm: quit before saving it
                if askokcancel('Quit', 'The file is not saved.\nDo you want to quit?'):
                    self.root.destroy()
            else:
                self.root.destroy()
        # current opened file (not new), and no changes made since opened
        elif current_text == self.text.rstrip(string.whitespace):
            self.root.destroy()
        else:
        # if there is difference btw the current_text and current self.text(traced back to last update)
            if askokcancel('Quit', 'The file is not saved.\nDo you want to quit?'):
                self.root.destroy()
                

    def count_words(self):
        if self.pause_word_count == True:
            return
        self.word_count = sum([len(w.rstrip(string.punctuation)) > 0 for w in self.edit_text.get('1.0', END).split()])
        self.word_count_label['text'] = f"word count  {self.word_count} "
        self.edit_text.frame.after(1000, self.count_words)


    def timer(self):
        if self.remaining_hr == 0 and self.remaining_min == 0 and self.remaining_sec == 0:
            self.timer_label['text'] = f"Time's up!"
            self.edit_text.configure(state='disabled')
            self.btn_stop['state'] = 'disabled'
        elif self.timer_stop == True:
            self.timer_label['text'] = "STOP\nremaining time  {:02}:{:02}:{:02}".format(self.remaining_hr,self.remaining_min, self.remaining_sec)
            self.edit_text.configure(state='disabled')
        else:
            self.timer_label['text'] = "remaining time  {:02}:{:02}:{:02}".format(self.remaining_hr,self.remaining_min, self.remaining_sec)
            if self.remaining_sec == 0:
                if self.remaining_min == 0:
                   self.remaining_hr -= 1
                   self.remaining_min = 59
                   self.remaining_sec = 59
                else:
                   self.remaining_min -= 1
                   self.remaining_sec = 59
            else:
                self.remaining_sec -= 1
            self.frm_timer.after(1000, self.timer)
        
            
if __name__ == '__main__':
    s = SimpleTextEditor()
    
