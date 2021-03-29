from tkinter import *
import mysql.connector
from mysql.connector import Error


class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        container = Frame(self)
        
        container.pack(side="top", fill= "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight =1)

        #the frames are stored here
        self.frames = {}
        for F in (LogInPage, JurorDash, JuryChairDash, CommitteeChairDash, GuestView):
            page_name = F.__name__
            frame = F(parent = container, controller = self)
            self.frames[page_name] = frame

            frame.grid(row=0, column = 0, sticky = "nsew")

        self.show_frame("LogInPage")

    def show_frame(self, page_name):
        #Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()


class LogInPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        

        #Creation of the available fields
        userLabel = Label(self, text = "Username: ")
        self.usernameTF = Entry(self, bd = 5)
        passwordLabel = Label(self, text = "Password: ")
        self.passwordTF = Entry(self, bd = 5)

        LogIn = Button(self, text = "Log In", command = self.LogInFunc)
        Guest = Button(self, text = "Guest", command = self.Guest)
        
        #Layout of the available fields
        userLabel.grid(row=0, column=0)
        self.usernameTF.grid(row=0, column=1)
        passwordLabel.grid(row = 1, column = 0)
        self.passwordTF.grid(row = 1, column = 1)
        LogIn.grid(row = 2, column = 1)
        Guest.grid(row = 2, column = 0)

    
        #Button Function
    #-------------------------------------------
    def LogInFunc(self):

        #get the string from the entry field
        userName = self.usernameTF.get()
        passWord = self.passwordTF.get()

        print("Username: " + userName + "\nPassword: " + passWord)

        #Below: the functionality of the button should be entered here
        #Such as the query
        
        if connect(userName, passWord):
            self.controller.show_frame("JurorDash")

    def Guest(self):

        #change frame for the guest film submission page
        self.controller.show_frame("GuestView")


#This is the new generic frame for jurors
class JurorDash(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text = "This will be the view on login")
        label.pack(side = "top", fill = "x", pady=10)

#This is the new generic frame for jury chair
class JuryChairDash(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text = "This will be the view on login")
        label.pack(side = "top", fill = "x", pady=10)

#This is the new generic frame for committee chair
class CommitteeChairDash(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text = "This will be the view on login")
        label.pack(side = "top", fill = "x", pady=10)


class GuestView(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text = "This will be the guest submission form")
        label.pack(side = "top", fill = "x", pady = 10)


def connect(userName, passWord):
    """ Connect to mySQL database """
    try:
        '''
            username is always root
            password is Y7uzourl
            host name is either the server name or the ip address where mysql is running
            database name is film_review_db'
        '''
        conn = mysql.connector.connect(host='puff.mnstate.edu',
                                       database='aries-qualey_film_review',
                                       user='aries-qualey',
                                       password='Y7uzourl')

        if conn.is_connected():
            logincursor = conn.cursor()
            logincursor.execute("SELECT EXISTS (SELECT * FROM login_table WHERE username_c = %s AND password_c = %s)", (userName, passWord,))
            result = logincursor.fetchone()

            if result[0] == 1:
                print ("Login successful!")
                return True
            else:
                print ("Username or password incorrect. Please try again.")
                return False

    except Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    app = App()
    app.geometry('600x400')
    app.mainloop()
