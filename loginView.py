from tkinter import *


class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        container = Frame(self)
        
        container.pack(side="top", fill= "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight =1)

        #the frames are stored here
        self.frames = {}
        for F in (LogInPage, Dashboard):
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
        
        #Layout of the available fields
        userLabel.grid(row=0, column=0)
        self.usernameTF.grid(row=0, column=1)
        passwordLabel.grid(row = 1, column = 0)
        self.passwordTF.grid(row = 1, column = 1)
        LogIn.grid(row = 2, column = 1)

    
        #Button Function
    #-------------------------------------------
    def LogInFunc(self):

        #get the string from the entry field
        userName = self.usernameTF.get()
        passWord = self.passwordTF.get()

        print("Username: " + userName + "\nPassword: " + passWord)

        #Below: the functionality of the button should be entered here
        #Such as the query
        
        print("This will login eventually")

        #How to switch frames
        self.controller.show_frame("Dashboard")
        

#This is the new generic frame
class Dashboard(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text = "This will be the view on login")
        label.pack(side = "top", fill = "x", pady=10)



if __name__ == "__main__":
    app = App()
    app.mainloop()