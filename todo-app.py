from customtkinter import *
import time
import sqlite3 as sql

db = sql.connect('data.db')
ref = db.cursor()
class Mission():
    def __init__(self ,frame ,title ,description ,date, check_state):
        self.frame = frame
        self.date= date
        self.title = title
        self.mainfrm = CTkFrame(frame, width=900, height=150, border_color='black', border_width=1)
        self.mainfrm.pack(fill=BOTH, expand=True, pady=20, padx=10)
        self.titlelabel = CTkLabel(self.mainfrm, text=title, font=('Inter Regular', 32 * -1))
        self.titlelabel.place(x=19, y=13)
        self.desclabel = CTkLabel(self.mainfrm, justify='left', text=description, font=('Inter Regular', 15 * -1), wraplength=690)
        self.desclabel.place(x=28, y=64)
        self.check_var = StringVar()
        self.checkbox = CTkCheckBox(self.mainfrm, text="", command=self.checkbox_event,
                                            variable=self.check_var, onvalue="yes", offvalue="no", checkbox_height=31, checkbox_width=31)
        self.donelabel = CTkLabel(self.mainfrm, text='Done !', font=('Arial', 20), text_color='green')
        self.checkbox.place(x=930, y=10)
        if check_state == 'yes':
            self.check_var.set('yes')
            self.donelabel.place(x=830, y=10)
            self.checkbox.destroy()
        
        self.showTime()
    def checkbox_event(self):
        
        if self.check_var.get() == 'yes':
            self.donelabel.place(x=830, y=10)
            self.checkbox.destroy()
            ref.execute(f"""
                        UPDATE missions
                        SET checked = 'yes'
                        WHERE title = '{self.title}';
                        """)
            db.commit()
    def showTime(self):
        self.datelbl = CTkLabel(self.mainfrm, text=self.date, font=("Arial", 20))
        self.datelbl.place(x=799, y=115)
class TodoApp:
    def __init__(self):
        self.title = 'TODO'
        self.theme = 'light'
        self.day_state = 'AM'
        self.welcoming = 'Good Morning !'
        # Initialize the ori application
        set_appearance_mode(self.theme)
        self.app = CTk()
        self.app.title(self.title)
        self.app.geometry('1080x620')
        self.main = CTkFrame(self.app)
        self.main.pack(fill=BOTH, expand=True)
        # Nessasery threads
        self.set_welcoming()
        

        # Widgets
        self.hilabel = CTkLabel(self.main, text=f'{self.welcoming} What are you going to do today ?', font=('Arial', 20))
        self.list = CTkScrollableFrame(self.main, width=1020, height=475)
        self.addbtn = CTkButton(self.main, text='+  Add', font=('Arial', 14), command= lambda: self.open_add_page())       
        self.delallbtn = CTkButton(self.main, text='-  Delete all done missions', font=('Arial', 15), command = lambda : self.del_all())  
        self.addframe = CTkFrame(self.main, width=356, height=620, border_width=1, border_color='grey')
        self.backbtn = CTkButton(self.main, text='<', font=('Arial', 25), command= lambda : self.back_from_sidebar(), width=22, height=22)
        self.addlbl = CTkLabel(self.addframe, text='Add', font=('Arial', 50))
        self.titleentry = CTkEntry(self.addframe, placeholder_text='Mission Title', font=('Arial', 22), width=297)
        self.desclbl = CTkLabel(self.addframe, text='description', font=('Arial', 14))
        self.descbox = CTkTextbox(self.addframe, width=297, height=300, font=('Arial', 20))
        self.fnshaddbtn = CTkButton(self.addframe, width=131, height=40, text='Add', font=('Arial', 25), command = lambda: self.add())
        self.show_widgets()
        self.fetch_database()

        self.app.resizable(0,0)
        self.app.mainloop()
    def show_widgets(self):
        self.hilabel.place(x=21, y=17)
        self.list.place(x=21, y=107)
        self.addbtn.place(x=45, y=69)
        self.delallbtn.place(x=190, y=69)
    def change_theme(self):
        if self.theme == 'light':
            self.theme = 'dark'
        elif self.theme == 'dark':
            self.theme = 'light'
        set_appearance_mode(self.theme)
    def set_welcoming(self):
        if (time.localtime()).tm_hour < 12:
            self.day_state = 'AM'
        else :
            self.day_state = 'PM'
        if self.day_state == 'AM':
            self.welcoming = 'Good Morning !'
        elif self.day_state == 'PM':
            self.welcoming = 'Good Evening !'
    def open_add_page(self):
        self.addframe.place(x=0,y=0)
        self.backbtn.place(x=320, y=12)
        self.addlbl.place(x=128, y=35)
        self.titleentry.place(x=26, y=158)
        self.descbox.place(x=26, y=240)
        self.desclbl.place(x=37, y=212)
        self.fnshaddbtn.place(x=105, y=565)
    def fetch_database(self):
        missions = ref.execute("SELECT * FROM missions")
        for mission in missions:
            Mission(self.list, mission[0], mission[1], mission[3], mission[2])
    def del_all(self):
        ref.execute("""
                        DELETE FROM missions
                        WHERE checked = 'yes';
                    """)
        db.commit()
        for wm in self.list.winfo_children():
            wm.destroy()
        self.fetch_database()
    def back_from_sidebar(self):
        self.addframe.destroy()
        self.backbtn.destroy()
        self.addframe = CTkFrame(self.main, width=356, height=620, border_width=1, border_color='grey')
        self.backbtn = CTkButton(self.main, text='<', font=('Arial', 25), command= lambda : self.back_from_sidebar(), width=22, height=22)
        self.addlbl = CTkLabel(self.addframe, text='Add', font=('Arial', 50))
        self.titleentry = CTkEntry(self.addframe, placeholder_text='Mission Title', font=('Arial', 22), width=297)
        self.desclbl = CTkLabel(self.addframe, text='description', font=('Arial', 14))
        self.descbox = CTkTextbox(self.addframe, width=297, height=300, font=('Arial', 20))
        self.fnshaddbtn = CTkButton(self.addframe, width=131, height=40, text='Add', font=('Arial', 25), command = lambda : self.add())
    def add(self):
        self.t = self.titleentry.get()
        self.d = self.descbox.get('1.0', END)
        ref.execute(f"""INSERT INTO missIons (title, description, checked, date) VALUES ('{self.t}', '{self.d}', 'no', '')""")
        db.commit()
        self.back_from_sidebar()
        for wm in self.list.winfo_children():
            wm.destroy()
        self.fetch_database()
TodoApp()
