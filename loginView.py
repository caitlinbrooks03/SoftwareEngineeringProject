from tkinter import *

#Button Function
#-------------------------------------------
def LogInFunc():

    #get the string from the entry field
    userName = usernameTF.get()
    passWord = passwordTF.get()

    print("Username: " + userName + "\nPassword: " + passWord)

    #clear the entry fields 
    usernameTF.delete(0, END)
    passwordTF.delete(0, END)

    #Below: the functionality of the button should be entered here
    #Such as the query
    print("This will login eventually")


#Setting up window
#-------------------------------------------
window = Tk()
window.title("Login")
window.geometry("400x400")

#Code for widgits
#-------------------------------------------

#Creation of the available fields
userLabel = Label(window, text = "Username: ")
usernameTF = Entry(window, bd = 5)
passwordLabel = Label(window, text = "Password: ")
passwordTF = Entry(window, bd = 5)
LogIn = Button(window, text = "Log In", command = LogInFunc)


#Placing the fields in the window
#------------------------------------------
userLabel.grid(row=0, column=0)
usernameTF.grid(row=0, column=1)
passwordLabel.grid(row = 1, column = 0)
passwordTF.grid(row = 1, column = 1)
LogIn.grid(row = 2, column = 1)



if __name__ == "__main__":
    window.mainloop()