from tkinter import *

#Button Function
#-------------------------------------------
def LogInFunc():
    print("This will login eventually")


#Setting up window
#-------------------------------------------
window = Tk()
window.title("Login")
window.geometry("400x400")

#Code for widgits
#-------------------------------------------

#Creation of the available fields
L1 = Label(window, text = "Username: ")
E1 = Entry(window, bd = 5)
L2 = Label(window, text = "Password: ")
E2 = Entry(window, bd = 5)
LogIn = Button(window, text = "Log In", command = LogInFunc)


#Placing the fields in the window
L1.grid(row=0, column=0)
E1.grid(row=0, column=1)
L2.grid(row = 1, column = 0)
E2.grid(row = 1, column = 1)
LogIn.grid(row = 2, column = 1)







if __name__ == "__main__":
    window.mainloop()