from tkinter import *
from tkinter import ttk
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
        for F in (LogInPage, JurorDash, JuryChairDash, CommitteeChairDash, GuestView, ReviewView):
            page_name = F.__name__
            frame = F(parent = container, controller = self)
            self.frames[page_name] = frame

            frame.grid(row=0, column = 0, sticky = "nsew")

        self.show_frame("LogInPage")

    def show_frame(self, page_name):
        #Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()
    
    def get_frame(self, classname):
        '''Returns an instance of a frame given it's class name as a string'''
        for F in self.frames.values():
            if str(F.__class__.__name__) == classname:
                return F
        return None

class LogInPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        

        #Creation of the available fields
        userLabel = Label(self, text = "Username: ")
        self.usernameTF = Entry(self, bd = 5)
        passwordLabel = Label(self, text = "Password: ")
        self.passwordTF = Entry(self, show = '*', bd = 5)

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

        #print("Username: " + userName + "\nPassword: " + passWord)

        #Below: the functionality of the button should be entered here
        #Such as the query
        
        #Determines which view to use based on the type of account used to log in
        view = connect(userName, passWord)
        if view == "juror":
            self.controller.show_frame("JurorDash")
            juror = self.controller.get_frame("JurorDash")
            juror.populateTree()
            juror.tree.bind("<Double-1>", juror.getOverview)
        elif view == "juryChair":
            self.controller.show_frame("JuryChairDash")
        elif view == "committeeChair":
            self.controller.show_frame("CommitteeChairDash")
        

        self.usernameTF.delete(0, END)
        self.passwordTF.delete(0, END)

    def Guest(self):

        #change frame for the guest film submission page
        self.controller.show_frame("GuestView")


#This is the new generic frame for jurors
class JurorDash(Frame):

    

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        

        # create the treeview on the ui
        self.tree = ttk.Treeview(self, columns = (1,2,3,4), height = 5, show = "headings")
        review = Button(self, text = "Review", command = self.reviewBtn)
        logOut = Button(self, text = "Log Out", command = self.logOutBtn)

        #create the headings for the columns
        self.tree.heading(1, text="Film")
        self.tree.heading(2, text="Director")
        self.tree.heading(3, text="Runtime")
        self.tree.heading(4, text="Reviewed")

        #formatting the columns
        self.tree.column(1, width = 100)
        self.tree.column(2, width = 100)
        self.tree.column(3, width = 100)
        self.tree.column(4, width = 100)

        #including a scrollbar
        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.grid(column=0, row = 1)
        scroll.grid(column =1, row = 1)
        
        #To connect to the review screen
        self.mChoice = StringVar(self)
        titleList = []
        movieData = getDataTree("dummy")
        for movie in movieData:
            titleList.append(movie[0])
        self.mChoice.set('Choose a movie to review')
        self.choiceMenu = OptionMenu(self, self.mChoice, *titleList)
        self.choiceMenu.grid(column =2, row =1)
        review.grid(column =3, row =1)
        logOut.grid(column = 5, row = 5)

    #Tree View -- Fill with data on the Films
    def populateTree(self):
        #Query to put film data into the tree view
        #Enter Below

        login = self.controller.get_frame("LogInPage")
        user = login.usernameTF.get()
        data = getDataTree(user)
        
        #inserts the data into the treeview
        for val in data:
            self.tree.insert('', 'end', values = (val[0], val[1], val[2], val[3]) )

    #Tree View -- Get the more specific film information
    def getOverview(self, event):
        #Gets the selected row
        Item = self.tree.focus()

        #gets the name of the film that has been selected
        curItem = self.tree.item(Item)['values'][0]
        movie = curItem
        data = getFilmOverview(curItem)
        self.overviewPopUp(data)

    def overviewPopUp(self, data):
        #popup window
        win = Toplevel()
        win_title = data[0][1] + " Information"
        win.wm_title(win_title)
        director = Label(win, text = "Director of Film")
        title = Label(win, text = "Title of Film")
        synopsis = Label(win, text = "Synopsis")
        runtime = Label(win, text = "Total Runtime")
        language = Label(win, text = "Language")
        subtitles = Label(win, text = "Subtitles")
        location = Label(win, text = "How to access film")
        genre = Label(win, text = "Genre")

        dir_entry = Label(win, text = data[0][1])
        title_entry = Label(win, text = data[0][2])
        synopsis_entry = Label(win, text = data[0][3])
        runtime_entry = Label(win, text = data[0][4])
        language_entry = Label(win, text = data[0][5])
        subtitles_entry = Label(win, text = data[0][6])
        location_entry = Label(win, text = data[0][7])
        genre_entry = Label(win, text = data[0][8])

        director.grid(row = 1, column = 0)
        dir_entry.grid(row = 1, column = 1)
        title.grid(row = 2, column = 0)
        title_entry.grid(row = 2, column = 1)
        synopsis.grid(row = 3, column = 0)
        synopsis_entry.grid(row = 3, column = 1)
        runtime.grid(row = 4, column = 0)
        runtime_entry.grid(row = 4, column = 1)
        language.grid(row = 5, column = 0)
        language_entry.grid(row = 5, column = 1)
        subtitles.grid(row = 6, column = 0)
        subtitles_entry.grid(row = 6, column = 1)
        location.grid(row = 7, column = 0)
        location_entry.grid(row = 7, column = 1)
        genre.grid(row = 8, column = 0)
        genre_entry.grid(row = 8, column = 1)

    
    def logOutBtn(self):
        self.controller.show_frame("LogInPage")

    def reviewBtn(self):
        reviewF = self.controller.get_frame("ReviewView")
        reviewF.movie.set(self.mChoice.get())
        self.controller.show_frame("ReviewView")
        
        

#This is the new generic frame for jury chair
class JuryChairDash(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text = "This will be the view on Jury Chair login")
        label.grid(column = 1, row = 1)
        logOut = Button(self, text = "Log Out", command = self.logOutBtn)
        logOut.grid(column = 5, row = 5)

    def logOutBtn(self):
        self.controller.show_frame("LogInPage")


#This is the new generic frame for committee chair
class CommitteeChairDash(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text = "Film Application Info")
        
        self.tree = ttk.Treeview(self, columns = (1,2,3,4), height = 5, show = "headings")
          
        #create the headings for the columns
        self.tree.heading(1, text="Film")
        self.tree.heading(2, text="Director")
        self.tree.heading(3, text="Runtime")
        self.tree.heading(4, text = "Status")
        
        #Setting up the treeview columns
        self.tree.column(1, width = 100)
        self.tree.column(2, width = 100)
        self.tree.column(3, width = 100)
        self.tree.column(4, width = 100)

        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        #Setting up the buttons on the frame
        logOut = Button(self, text = "Log Out", command = self.logOutBtn)
      

        #Grid layout
        label.grid(column = 0, row = 0)
        self.tree.grid(column=0, row = 1)
        scroll.grid(column =1, row = 1)
        
        logOut.grid(column = 5, row = 5)


        self.populateTree()
        self.tree.bind("<Double-1>", self.getOverview)

    def logOutBtn(self):
        self.controller.show_frame("LogInPage")

    def populateTree(self):
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
            data = []
            if conn.is_connected():
                logincursor = conn.cursor()
                #Need to know what the status situation is regarding approved, rejected, and pending film applications
                logincursor.execute("SELECT movieName, director, runtime, approved, movieID FROM application_table")
            
        
            for row in logincursor.fetchall():
                if row[3] == 0:
                    data.append([row[0],row[1],row[2], "Pending", row[4]])
                if row[3] == 1:
                    data.append([row[0], row[1], row[2], "Approved", row[4]])
                if row[3] == 2:
                    data.append([row[0], row[1], row[2], "Rejected", row[4]])
             

        except Error as e:
            print(e)

        finally:
            if conn is not None and conn.is_connected():
                conn.close()

        
        for val in data:
            self.tree.insert('', 'end', values = (val[0], val[1], val[2], val[3]) )

    def getOverview(self, event):
        #Gets the selected row
        Item = self.tree.focus()

        #gets the name of the film that has been selected
        curItem = self.tree.item(Item)['values'][0]
        movie = curItem
        data = getFilmOverview(curItem)
        self.overviewPopUp(data)

    def overviewPopUp(self, data):

        self.movieID = data[0][0]
        #popup window
        
        win = Toplevel()
        win_title = data[0][1] + " Information"
        win.wm_title(win_title)
        director = Label(win, text = "Director of Film")
        title = Label(win, text = "Title of Film")
        synopsis = Label(win, text = "Synopsis")
        runtime = Label(win, text = "Total Runtime")
        language = Label(win, text = "Language")
        subtitles = Label(win, text = "Subtitles")
        location = Label(win, text = "How to access film")
        genre = Label(win, text = "Genre")

        approve = Button(win, text = "Approve", command =self.approveFilmBtn)
        reject = Button(win, text = "Reject", command = self.rejectFilmBtn)

        

        dir_entry = Label(win, text = data[0][1])
        title_entry = Label(win, text = data[0][2])
        synopsis_entry = Label(win, text = data[0][3])
        runtime_entry = Label(win, text = data[0][4])
        language_entry = Label(win, text = data[0][5])
        subtitles_entry = Label(win, text = data[0][6])
        location_entry = Label(win, text = data[0][7])
        genre_entry = Label(win, text = data[0][8])

        director.grid(row = 1, column = 0)
        dir_entry.grid(row = 1, column = 1)
        title.grid(row = 2, column = 0)
        title_entry.grid(row = 2, column = 1)
        synopsis.grid(row = 3, column = 0)
        synopsis_entry.grid(row = 3, column = 1)
        runtime.grid(row = 4, column = 0)
        runtime_entry.grid(row = 4, column = 1)
        language.grid(row = 5, column = 0)
        language_entry.grid(row = 5, column = 1)
        subtitles.grid(row = 6, column = 0)
        subtitles_entry.grid(row = 6, column = 1)
        location.grid(row = 7, column = 0)
        location_entry.grid(row = 7, column = 1)
        genre.grid(row = 8, column = 0)
        genre_entry.grid(row = 8, column = 1)
        approve.grid(row =9, column = 1)
        reject.grid(row=9, column = 0)
  
    def approveFilmBtn(self):
        #Approve the films
        try:
            '''username is always root
           password is Y7uzourl
           host name is either the server name or the ip address where mysql is running
           database name is film_review_db'
            '''
            conn = mysql.connector.connect(host='puff.mnstate.edu',
                                       database='aries-qualey_film_review',
                                       user='aries-qualey',
                                       password='Y7uzourl')

            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("UPDATE application_table SET approved = 1 WHERE movieID = %s", (self.movieID,))
                conn.commit()

        except Error as e:
            print(e)

        finally:
            if conn is not None and conn.is_connected():
                conn.close()

        self.refresh()
        
        
    def rejectFilmBtn(self):
        #reject the films
        try:
            '''username is always root
           password is Y7uzourl
           host name is either the server name or the ip address where mysql is running
           database name is film_review_db'
            '''
            conn = mysql.connector.connect(host='puff.mnstate.edu',
                                       database='aries-qualey_film_review',
                                       user='aries-qualey',
                                       password='Y7uzourl')

            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("UPDATE application_table SET approved = 2 WHERE movieID = %s", (self.movieID,))
                conn.commit()

        except Error as e:
            print(e)

        finally:
            if conn is not None and conn.is_connected():
                conn.close()

        self.refresh()

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)  
        self.populateTree()


        
    

class GuestView(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # Creation of the available fields
        # Film information
        title = Label(self, text = "Title of Film")
        self.titleTF = Entry(self, bd = 5)
        director = Label(self, text = "Director of Film")
        self.directorTF = Entry(self, bd = 5)
        submitterName = Label(self, text = "Name of Submitter")
        self.submitterNameTF = Entry(self, bd = 5)
        submitterPhone = Label(self, text = "Phone Number")
        self.submitterPhoneTF = Entry(self, bd = 5)
        synopsis = Label(self, text = "Synopsis")
        self.synopsisTF = Entry(self, bd = 5)
        runtime = Label(self, text = "Total Runtime")
        self.runtimeTF = Entry(self, bd = 5)
        self.runtimeTF.insert(0, "In Minutes")
        language = Label(self, text = "Language")
        self.languageTF = Entry(self, bd = 5)
        subtitles = Label(self, text = "Subtitles")
        self.subtitleTF = Entry(self, bd = 5)
        location = Label(self, text = "How to access film")
        self.locationTF = Entry(self, bd = 5)
        genre = Label(self, text = "Genre")
        self.genreTF = Entry(self, bd = 5)

        #Creation of Buttons
        submit = Button(self, text = "Submit", command = self.submitApp)
        cancel = Button(self, text = "Cancel", command = self.cancelApp)
        back = Button(self, text = "Return to Login", command = self.logOutBtn)


        #Layout of available fields
        title.grid(row = 1, column = 0)
        self.titleTF.grid(row = 1, column = 1)
        director.grid(row = 2, column = 0)
        self.directorTF.grid(row = 2, column = 1)
        submitterName.grid(row = 3, column = 0)
        self.submitterNameTF.grid(row = 3, column = 1)
        submitterPhone.grid(row = 4, column = 0)
        self.submitterPhoneTF.grid(row = 4, column = 1)
        synopsis.grid(row = 5, column = 0)
        self.synopsisTF.grid(row = 5, column = 1)
        runtime.grid(row = 6, column = 0)
        self.runtimeTF.grid(row = 6, column = 1)
        language.grid(row = 7, column = 0)
        self.languageTF.grid(row = 7, column = 1)
        subtitles.grid(row = 8, column = 0)
        self.subtitleTF.grid(row = 8, column = 1)
        location.grid(row = 9, column = 0)
        self.locationTF.grid(row = 9, column = 1)
        genre.grid(row = 10, column = 0)
        self.genreTF.grid(row = 10, column = 1)
        submit.grid(row = 11, column = 1)
        cancel.grid(row = 11, column = 0)
        back.grid(row = 11 , column = 2)

    def cancelApp(self):
        #clears out text fields 
        self.titleTF.delete(0, END)
        self.directorTF.delete(0, END)
        self.submitterNameTF.delete(0, END)
        self.submitterPhoneTF.delete(0, END)
        self.synopsisTF.delete(0, END)
        self.runtimeTF.delete(0, END)
        self.languageTF.delete(0, END)
        self.subtitleTF.delete(0, END)
        self.locationTF.delete(0, END)
        self.genreTF.delete(0, END)

    def submitApp(self):
        #Submit the application to the database for approval
        str_title = self.titleTF.get()
        str_director = self.directorTF.get()
        str_submitterName = self.submitterNameTF.get()
        str_submitterPhone = self.submitterPhoneTF.get()
        str_synopsis = self.synopsisTF.get()
        str_language = self.languageTF.get()
        str_runtime = self.runtimeTF.get()      
        str_subtitle = self.subtitleTF.get()
        str_location = self.locationTF.get()
        str_genre = self.genreTF.get()

        #insert the query to execute below here
        #---------------------------------------------------


        paramList = [str_director, str_submitterName, str_title, str_synopsis, str_runtime,
                    str_language, str_subtitle, str_location, str_genre, str_submitterPhone]

        try:
            '''username is always root
           password is Y7uzourl
           host name is either the server name or the ip address where mysql is running
           database name is film_review_db'
            '''
            conn = mysql.connector.connect(host='puff.mnstate.edu',
                                       database='aries-qualey_film_review',
                                       user='aries-qualey',
                                       password='Y7uzourl')

            if conn.is_connected():
                cursor = conn.cursor()
                cursor.callproc('submitMovie3', paramList)
                conn.commit()

        except Error as e:
            print(e)

        finally:
            if conn is not None and conn.is_connected():
                conn.close()

        self.cancelApp()

    def logOutBtn(self):
        self.controller.show_frame("LogInPage")

class ReviewView(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.aveStr = StringVar()
        self.aveStr.set("1.00")

        #Set up the frame to hold the ratings
        scrollCanvas = Canvas(self)
        ratings = Frame(scrollCanvas)
        scroll = Scrollbar(self,orient="vertical",command=scrollCanvas.yview)
        ratings.bind(
            "<Configure>",
            lambda e: scrollCanvas.configure(
                scrollregion=scrollCanvas.bbox("all")
            )
        )
        scrollCanvas.create_window((0, 0), window=ratings, anchor=NW)
        scrollCanvas.configure(yscrollcommand=scroll.set)

        #Creating misc. stuff

        self.movie = StringVar()
        self.movie.set('Default')
        movieName = Label(self, textvariable=self.movie)
        Cancel = Button(self, text = "Cancel", command = self.CancelFunc)
        Submit = Button(self, text = "Submit")

        #Creating the rating categories
        directingLabel = Label(ratings, text = "Directing: ")
        self.Directing = Scale(ratings, from_=1, to=9, tickinterval=1, orient="horizontal", command=self.updateValue)
        actingLabel = Label(ratings, text = "Acting: ")
        self.Acting = Scale(ratings, from_=1, to=9, tickinterval=1, orient="horizontal", command=self.updateValue)
        editingLabel = Label(ratings, text = "Editing: ")
        self.Editing = Scale(ratings, from_=1, to=9, tickinterval=1, orient="horizontal", command=self.updateValue)
        soundLabel = Label(ratings, text = "Sound Quality: ")
        self.Sound = Scale(ratings, from_=1, to=9, tickinterval=1, orient="horizontal", command=self.updateValue)
        scoreLabel = Label(ratings, text = "Soundtrack (Score): ")
        self.Score = Scale(ratings, from_=1, to=9, tickinterval=1, orient="horizontal", command=self.updateValue)
        cinemaLabel = Label(ratings, text = "Cinematography: ")
        self.Cinema = Scale(ratings, from_=1, to=9, tickinterval=1, orient="horizontal", command=self.updateValue)
        screenplayLabel = Label(ratings, text = "Screenplay: ")
        self.Screenplay = Scale(ratings, from_=1, to=9, tickinterval=1, orient="horizontal", command=self.updateValue)
        audienceLabel = Label(ratings, text = "Audience Appeal: ")
        self.Audience = Scale(ratings, from_=1, to=9, tickinterval=1, orient="horizontal", command=self.updateValue)
        intentLabel = Label(ratings, text = "Filmaker's Intent Realized: ")
        self.Intent = Scale(ratings, from_=1, to=9, tickinterval=1, orient="horizontal", command=self.updateValue)
        averageLabel = Label(ratings, text = "Average Score: ")
        AverageScore = Label(ratings, textvariable = self.aveStr)
        overallLabel = Label(ratings, text = "Overall Score: ")
        self.Overall = Scale(ratings, from_=1, to=9, tickinterval=1, orient="horizontal", command=self.updateValue)

        #Textfield for review
        reviewLabel = Label(self, text="Enter Comments Here:")
        self.reviewText = Text(self, width=5, height=5)

        #Awards nomination
        awardLabel = Label(self, text="Award nomination?")
        self.AwardVar = StringVar(self)
        awardList = ['None','Best Film','Directing','Cinematography','Editing','Sound','Actor','Actress','Other']
        self.AwardVar.set('None')
        self.awardMenu = OptionMenu(self, self.AwardVar, *awardList)

        #Layout for main elements
        movieName.pack(side=TOP)
        Cancel.pack(side=LEFT, anchor=NW)
        Submit.pack(side=RIGHT, anchor=NE)
        scroll.pack(side=RIGHT, fill=Y, anchor=NE)
        scrollCanvas.pack(side=TOP, fill=BOTH)
        reviewLabel.pack(side=TOP, pady=5)
        self.reviewText.pack(side=TOP, fill=X)
        awardLabel.pack(side=TOP, pady=5)
        self.awardMenu.pack(side=TOP)

        #Gridding the ratings
        directingLabel.grid(row=1, column=1)
        self.Directing.grid(row=1, column=2)
        
        actingLabel.grid(row=2, column=1)
        self.Acting.grid(row=2, column=2)
        
        editingLabel.grid(row=3, column=1)
        self.Editing.grid(row=3, column=2)
        
        soundLabel.grid(row=4, column=1)
        self.Sound.grid(row=4, column=2)

        scoreLabel.grid(row=5, column=1)
        self.Score.grid(row=5, column=2)
        
        cinemaLabel.grid(row=6, column=1)
        self.Cinema.grid(row=6, column=2)
        
        screenplayLabel.grid(row=7, column=1)
        self.Screenplay.grid(row=7, column=2)
        
        audienceLabel.grid(row=8, column=1)
        self.Audience.grid(row=8, column=2)

        intentLabel.grid(row=9, column=1)
        self.Intent.grid(row=9, column=2)

        averageLabel.grid(row=10, column=1)
        AverageScore.grid(row=10, column=2)

        overallLabel.grid(row=11, column=1)
        self.Overall.grid(row=11, column=2)

    def updateValue(self,dummy):
        ave = 0
        ave += self.Directing.get()
        ave += self.Acting.get()
        ave += self.Editing.get()
        ave += self.Sound.get()
        ave += self.Score.get()
        ave += self.Cinema.get()
        ave += self.Screenplay.get()
        ave += self.Audience.get()
        ave += self.Intent.get()
        ave = round(ave / 9, 2)
        self.aveStr.set(str(ave))

    def CancelFunc(self):
        self.Directing.set(1)
        self.Acting.set(1)
        self.Editing.set(1)
        self.Sound.set(1)
        self.Score.set(1)
        self.Cinema.set(1)
        self.Screenplay.set(1)
        self.Audience.set(1)
        self.Intent.set(1)
        self.Overall.set(1)
        self.reviewText.delete(1.0,END)
        self.AwardVar.set('None')
        self.controller.show_frame("JurorDash")

    def SubmitFunc(self):
        int_directing = self.Directing.get()
        int_acting = self.Acting.get()
        int_editing = self.Editing.get()
        int_sound = self.Sound.get()
        int_score = self.Score.get()
        int_cinema = self.Cinema.get()
        int_screen = self.Screenplay.get()
        int_audience = self.Audience.get()
        int_intent = self.Intent.get()
        str_average = self.aveStr.get()
        int_overall = self.Overall.get()
        str_review = self.reviewText.get("1.0","end")
        login = self.controller.get_frame("LogInPage")
        user = login.usernameTF.get()
        str_awardNom = self.AwardVar.get()
        try:
            conn = mysql.connector.connect(host='puff.mnstate.edu',
                                           database='aries-qualey_film_review',
                                           user='aries-qualey',
                                           password='Y7uzourl')
            if conn.is_connected():
                submitCursor = conn.cursor()
                submitCursor.execute("SELECT movieID FROM application_table WHERE movieName = %s", (self.movie.get(),))
                result = submitCursor.fetchone()
                movieID = int(result[0])
                paramList = [movieID,user,int_directing,int_acting,int_editing,int_sound,int_score,int_cinema,int_screen,int_audience,int_intent,str_review,int_overall,str_average]
                submitCursor.callproc("submitReview2",paramList)
                submitCursor.execute("INSERT INTO nominations_table (movieID, award) VALUES (%s, %s)", (movieID, str_awardNom,))
                conn.commit()
        
        except Error as e:
            print(e)

        finally:
            if conn is not None and conn.is_connected():
                conn.close()
                self.Directing.set(1)
                self.Acting.set(1)
                self.Editing.set(1)
                self.Sound.set(1)
                self.Score.set(1)
                self.Cinema.set(1)
                self.Screenplay.set(1)
                self.Audience.set(1)
                self.Intent.set(1)
                self.Overall.set(1)
                self.reviewText.delete(1.0,END)
                self.AwardVar.set('None')
                self.controller.show_frame("JurorDash")


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
            logincursor.execute("SELECT userTypeCode_c FROM login_table WHERE username_c = %s AND password_c = %s", (userName, passWord,))
            result = logincursor.fetchone()

            try:
                if result[0] == 2:
                    return "juror"
                elif result[0] == 3:
                    return "juryChair"
                elif result[0] == 4: 
                    return "committeeChair"
            except:
                print("Invalid Login! Incorrect Username or Password")
            
                

    except Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


def getDataTree(user):
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
        data = []
        movielist = []
        if conn.is_connected():
            logincursor = conn.cursor()
            logincursor.execute("SELECT movieID FROM review_table WHERE username_c = %s", (user,))
            for row in logincursor.fetchall():
                movielist.append(row[0])
            logincursor.execute("SELECT movieName, director, runtime, approved, movieID FROM application_table")
            
        
        for row in logincursor.fetchall():
            if row[4] in movielist:
                data.append([row[0],row[1],row[2],True])
            else:
                data.append([row[0],row[1],row[2],False])
        return data        

    except Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()



def getFilmOverview(curItem):
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
            logincursor.execute("SELECT * FROM application_table WHERE movieName = %s", (curItem,))
            result = logincursor.fetchone()

        data = []
        data.append([result[0], result[1], result[3], result[4], 
                    result[5], result[6], result[7], result[8], result[9]])
        return data

    except Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    app = App()
    app.geometry('600x400')
    app.title("Movie Review Application")
    app.mainloop()
