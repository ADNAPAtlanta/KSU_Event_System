from firebase import firebase
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
import datetime
import time
from email.mime.text import MIMEText
import os


try:
    # for Python2
    from Tkinter import *
    from tkinter import filedialog
except ImportError:
    # for Python3
    from tkinter import *
    from tkinter import filedialog


ksuBuildings = {"Baily Athletic Facility": "220 Kennesaw State Univ Rd NW Kennesaw, GA 30144",
                "Bailey Performance Hall":"488 Prillaman Way NW Kennesaw, GA 30144",
                 "Baseball Field": "208 Kennesaw State Univ Rd NW Kennesaw, GA 30144",
                "Burruss":"560 Parliament Garden Way NW Kennesaw, GA 30144",
                 "Campus Green": "565 Cobb Ave NW Kennesaw, GA 30144",
                "Campus Services":"1075 Canton Pl NW Kennesaw, GA 30144",
                "Chastain Pointe":"1200 Chastain Rd NW Kennesaw, GA 30144",
                "Clendenin":"275 Kennesaw State Univ Rd NW Kennesaw, GA 30144",
                "Convocation Center":"590 Cobb Ave NW Kennesaw, GA 30144",
                "Education Classroom Facility":"580 Parliament Garden Way NW Kennesaw, GA 30144",
                "English Building":"440 Bartow Ave NW Kennesaw, GA 30144",
                "Gazebo":"410 Bartow Ave NW Kennesaw, GA 30144",
                "House 48 - ASap":"3499 Campus Loop Rd NW Kennesaw, GA 30144",
                "House 49 - Cox Family Enterprise":"3495 Campus Loop Rd NW Kennesaw, GA 30144",
                "House 51 - TBD":"3217 Campus Loop Rd NW Kennesaw, GA 30144",
                "House 52 - Clinic":"3215 Campus Loop Rd NW Kennesaw, GA 30144",
                "House 54 - CETL":"3211 Campus Loop Rd NW Kennesaw, GA 30144",
                "House 55 - MEBUS":"3209 Campus Loop Rd NW Kennesaw, GA 30144",
                "House 56 - Alumni":"3207 Campus Loop Rd NW Kennesaw, GA 30144",
                "House 57 - Center for Elections":"3205 Campus Loop Rd NW Kennesaw, GA 30144",
                "House 58 - Distance Learning":"3203 Campus Loop Rd NW Kennesaw, GA 30144",
                "House 59 - ATOMS":"3201 Campus Loop Rd NW Kennesaw, GA 30144",
                "J.M Wilson":"471 Bartow Ave NW Kennesaw, GA 30144",
                "Jolley Lodge":"1055 Canton Pl NW Kennesaw, GA 30144",
                "Kennesaw Hall":"585 Cobb Ave NW Kennesaw, GA 30144",
                "KSU Center":"3333 Busbee Dr NW Kennesaw, GA 30144",
                "Library":"385 Cobb Ave NW Kennesaw, GA 30144",
                "Math and Statistics":"365 Cobb Ave NW Kennesaw, GA 30144",
                "Music":"491 Bartow Ave NW Kennesaw, GA 30144",
                "Office Annex":"371 Paulding Ave NW Kennesaw, GA 30144",
                "Owl's Nest":"3220 Busbee Dr NW Kennesaw, GA 30144",
                "Pilcher":"375 Cobb Ave NW Kennesaw, GA 30144",
                "Prillaman Health Sciences":"520 Parliament Garden Way NW Kennesaw, GA 30144",
                "Public Safety":"351 Paulding Ave NW Kennesaw, GA 30144",
                "Rec Fields" : "270 Kennesaw State Univ Rd NW Kennesaw, GA 30144",
                "Science":"370 Paulding Ave NW Kennesaw, GA 30144",
                "Science Laboratory":"105 Marietta Dr NW Kennesaw, GA 30144",
                "Student Recreation & Activities Center":"290 Kennesaw State Univ Rd NW Kennesaw, GA 30144",
                "Soccer Field": "1000 Chastain Rd NW Kennesaw, GA 30144",
                "Social Sciences":"402 Bartow Ave NW Kennesaw, GA 30144",
                "Softball Field":"250 Kennesaw State Univ Rd NW Kennesaw, GA 30144",
                "Sports and Recreation Park":"390 Big Shanty Rd NW Kennesaw, GA 30144",
                "Student Athlete Success":"1150 Big Shanty Rd NW Kennesaw, GA 30144",
                "Student Center/Bookstore":"395 Cobb Ave NW Kennesaw, GA 30144",
                "Tech Annex":"361 Paulding Ave NW Kennesaw, GA 30144",
                "Technology Services":"1075 Canton Pl NW Kennesaw, GA 30144",
                "The Commons":"540 Parliament Garden Way NW Kennesaw, GA 30144",
                "Town Point":"3391 Town Point Dr NW Kennesaw, GA 30144",
                "University College":"430 Bartow Ave NW Kennesaw, GA 30144",
                "Visual Arts":"411 Bartow Ave NW Kennesaw, GA 30144",
                "Willingham Hall":"420 Bartow Ave NW Kennesaw, GA 30144",
                "Wilson Annex":"462 Prillaman Way NW Kennesaw, GA 30144",
                "Zuckerman Museum":"492 Prillaman Way NW Kennesaw, GA 30144",
                #Housing
                "Austin Residence Complex":"125 Marietta Dr NW Kennesaw, GA 30144",
                "University Village":"1074 Canton Pl NW Kennesaw, GA 30144",
                "KSU Place Apartments":"1175 Idlewood Ave NW Kennesaw, GA 30144",
                "Other":"",
                "Select building.":""}

ksuBuildingsOrdered = ["Baily Athletic Facility",
                "Bailey Performance Hall",
                "Baseball Field",
                "Burruss",
                 "Campus Green",
                "Campus Services",
                "Chastain Pointe",
                "Clendenin",
                "Convocation Center",
                "Education Classroom Facility",
                "English Building",
                 "Gazebo",
                "House 48 - ASap",
                "House 49 - Cox Family Enterprise",
                "House 51 - TBD",
                "House 52 - Clinic",
                "House 54 - CETL",
                "House 55 - MEBUS",
                "House 56 - Alumni",
                "House 57 - Center for Elections",
                "House 58 - Distance Learning",
                "House 59 - ATOMS",
                "J.M Wilson",
                "Jolley Lodge",
                "Kennesaw Hall",
                "KSU Center",
                "Library",
                "Math and Statistics",
                "Music",
                "Office Annex",
                "Owl's Nest",
                "Pilcher",
                "Prillaman Health Sciences",
                "Public Safety",
                "Rec Fields",
                "Science",
                "Science Laboratory",
                "Student Recreation & Activities Center",
                "Social Sciences",
                "Softball Field",
                "Sports and Recreation Park",
                "Student Athlete Success",
                "Student Center/Bookstore",
                "Tech Annex",
                "Technology Services",
                "The Commons",
                "Town Point",
                "University College",
                "Visual Arts",
                "Willingham Hall",
                "Wilson Annex",
                "Zuckerman Museum",
                #Housing
                "Austin Residence Complex",
                "University Village",
                "KSU Place Apartments",
                "Other"]
days = ["01", "02", "03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24",
        "25","26","27","28","29","30","31"]

months = {"Jan": "01", "Feb":"02", "Mar":"03", "Apr":"04",
	   			    "May":"05", "Jun":"06", "July":"07", "Aug":"08",
				    "Sep":"09", "Oct":"10", "Nov":"11", "Dec":"12"}

years = ["2016","2017","2018"]

hours = ["00","01","02","3","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24"]

minutes = ["00","01", "02", "03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24",
        "25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57",
           "58","59","60"]
pmAM = ["PM", "AM"]

categories = ["fun","academic","greek","networking","ncaa","cultural","athletics","service","social"]

class eventForm:
    def __init__(self,master):
        self.master = master
        master.title("KSU Event System (organization ver.)")
        master.minsize(width=300, height=300)
        self.type = StringVar()
        self.type.set("Vacation")

        #entry variables
        self.name = StringVar()
        self.email = StringVar()
        self.address = StringVar()
        self.building = StringVar()
        self.organization = StringVar()
        self.category = StringVar()
        self.category.set("fun")
        self.description = StringVar()
        self.shareMessage = StringVar()
        self.picture = StringVar()
        self.lat = DoubleVar()
        self.longitude = DoubleVar()
        self.date = StringVar()
        self.category = StringVar()
        self.food = StringVar()
        self.food.set("No")
        self.music = StringVar()
        self.music.set("No")
        self.merchandise = StringVar()
        self.merchandise.set("No")

        self.vacation = StringVar()
        self.date = StringVar()
        self.day = StringVar()
        self.day.set("01")
        self.month = StringVar()
        self.month.set("Jan")
        self.year = StringVar()
        self.year.set("2016")

        self.pmAM = StringVar()
        self.pmAM.set("PM")

        self.hour = StringVar()
        self.hour.set("00")
        self.minute = StringVar()
        self.minute.set("00")
        self.endHour = StringVar()
        self.endHour.set("00")
        self.endMinute = StringVar()
        self.endMinute.set("00")


        #Entry labels
        self.nameLabel = Label(master, text="Name of Event",underline=0)
        self.nameLabel.grid(column=1,row=0)
        self.nameEntry = Entry(master,bd=3,textvariable=self.name)
        self.nameEntry.grid(column=1,padx=5,row=1)

        self.emailLabel = Label(master, text="Enter email",underline=0)
        self.emailLabel.grid(column=1)
        self.emailEntry = Entry(master, bd=3,textvariable=self.email)
        self.emailEntry.grid(column=1)

        
        self.organizationLabel = Label(master, text="Organization/Club",underline=0)
        self.organizationLabel.grid(column=2,row=0)
        self.organizationEntry = Entry(master,bd=3,textvariable=self.organization)
        self.organizationEntry.grid(column=2,padx=5,row=1)
        
        self.dateLabel = Label(master, text="Date",underline=0)
        self.dateLabel.grid(column=4,row=0)
        self.dayOption = OptionMenu(master, self.day,*days)
        self.dayOption.grid(column=3,row=1)
        self.monthOption = OptionMenu(master,self.month,*months)
        self.monthOption.grid(column=4,row=1)
        self.yearOption = OptionMenu(master,self.year,*years)
        self.yearOption.grid(column=5,row=1)

        self.pmAMOption = OptionMenu(master, self.pmAM, *pmAM)
        self.pmAMOption.grid(column=3, row=3)

        self.hourLabel = Label(master, text="Hour", underline=0)
        self.hourLabel.grid(column=4,row=2)
        self.minuteLabel = Label(master, text="Minute", underline=0)
        self.minuteLabel.grid(column=5, row=2)
        self.hourOption = OptionMenu(master,self.hour,*hours)
        self.hourOption.grid(column=4, row=3)
        self.minuteOption = OptionMenu(master,self.minute,*minutes)
        self.minuteOption.grid(column=5, row=3)
        
        self.endHourLabel = Label(master, text="Enter ending hour", underline=0)
        self.endHourLabel.grid(column=6, row=2)
        self.endMinuteLabel = Label(master, text="Enter ending minute", underline=0)
        self.endMinuteLabel.grid(column=7, row=2)
        self.endHourOption = OptionMenu(master, self.endHour,*hours)
        self.endHourOption.grid(column=6, row=3)
        self.endMinuteOption = OptionMenu(master, self.endMinute, *minutes)
        self.endMinuteOption.grid(column=7, row=3)
        
        self.descriptionLabel = Label(master, text="Description",underline=0)
        self.descriptionLabel.grid(column=1)
        self.descriptionEntry = Text(master,bd=3,height=5 )
        self.descriptionEntry.grid(column=1,columnspan=2)

        self.shareMessageLabel = Label(master, text="Enter message to be shared",underline=0)
        self.shareMessageLabel.grid(column=1)
        self.shareMessageEntry = Text(master, bd=3,height=2)
        self.shareMessageEntry.grid(column=1,columnspan=2)

        self.addressLabel = Label(master, text="Address (Enter if off campus)", underline=0)
        self.addressLabel.grid(column=2, sticky=W)
        self.addressEntry = Entry(master, textvariable=self.address,bd=3)
        self.addressEntry.grid(column=2, sticky=W)

        self.pictureLabel = Label(master, text="Insert picture")
        self.pictureLabel.grid(column=2, sticky=W)
        self.pictureEntry = Entry(master)
        self.pictureEntry.grid(column=2, sticky=W)
        self.pictureButton = Button(master, text="Search", command=self.getPicture)
        self.pictureButton.grid(column=2,sticky=W)

        self.categoryLabel = Label(master, text="Category", underline=0)
        self.categoryLabel.grid(column=2,row=2 )
        self.categoryOption = OptionMenu(master, self.category, *categories)
        self.categoryOption.grid(column=2, row=3)


        self.buildingLabel = Label(master, text="Building", underline=0)
        self.buildingLabel.grid(column=1, row=8)
        self.building.set("Other")
        self.buildingSelection = OptionMenu(master, self.building, *ksuBuildingsOrdered)
        self.buildingSelection.grid(column=1, row=9)


        self.foodChoiceLabel = Label(master, text="Is food available?", underline=0)
        self.foodChoiceLabel.grid(column=1, row=10)
        self.foodChoiceYes = Radiobutton(master, text="Yes", variable=self.food, value="Yes")
        self.foodChoiceYes.grid(column=1, row=11)
        self.foodChoiceNo = Radiobutton(master,text="No",variable=self.food,value="No")
        self.foodChoiceNo.grid(column=1, row=12)

        self.musicChoiceLabel = Label(master,text= "Will there be music?")
        self.musicChoiceLabel.grid(column=1)
        self.musicChoiceYes = Radiobutton(master,text="Yes",variable=self.music,value="Yes")
        self.musicChoiceYes.grid(column=1)
        self.musicChoiceNo = Radiobutton(master,text="No",variable=self.music,value="No")
        self.musicChoiceNo.grid(column=1)

        self.merchandiseChoiceLabel = Label(master,text= "Will there be merchandise?")
        self.merchandiseChoiceLabel.grid(column=1)
        self.merchandiseChoiceYes = Radiobutton(master,text="Yes",variable=self.merchandise,value="Yes")
        self.merchandiseChoiceYes.grid(column=1)
        self.merchandiseChoiceNo = Radiobutton(master,text="No",variable=self.merchandise,value="No")
        self.merchandiseChoiceNo.grid(column=1)

        self.submitButton = Button(master, text="Submit", command=self.submit)
        self.submitButton.grid(column=2)

    def submit(self):
        geolocator = GoogleV3(api_key="AIzaSyB9NYRXQZN3gIcJue5SJa2jem7UdOzmOvI")
        name = "name :" + self.name.get()
        organization = "organization :" + self.organization.get()
        locationName = "location name :" + self.building.get()
        picture = self.picture.get()
        pmAM = self.pmAM.get()
        hour = self.hour.get()
        minute = self.minute.get()
        endHour = self.endHour.get()
        endMinute = self.endMinute.get()
        month =  months[self.month.get()]
        date =  self.day.get() + "/" + month + "/" + self.year.get() + " " + hour + ":" + minute
        dateNum =  time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y %H:%M").timetuple())
        description = "description :" + self.descriptionEntry.get("1.0",END)
        shareMessage = "shareMessage :" + self.shareMessageEntry.get("1.0",END)
        food = "food :" + self.food.get()
        music = "music : " +self.music.get()
        merchandise = "merchandise :" + self.merchandise.get()
        strFrom = self.email.get()
        strTo = ["techSupport@adnap.co"]
        msgRoot = MIMEMultipart(organization)
        message = MIMEMultipart()




        message["Subject"] = self.organization.get()


        fp = open(picture, "rb")
        img = MIMEImage(fp.read())
        fp.close()
        #msg.attach(img)

        if self.building.get() == "Other":
            address = self.address.get()
            location = geolocator.geocode(address, timeout=10)
            lat = location.latitude
            longitude = location.longitude
        else:
            address = ksuBuildings[self.building.get()]
            print(ksuBuildings[self.building.get()])
            location = geolocator.geocode(address, timeout=10)
            lat = location.latitude
            longitude = location.longitude
        messageText =  name,organization, locationName,date, dateNum, description, shareMessage,address,food, music,merchandise,"lat :" +str(lat),"longitude :" +str(longitude), pmAM,hour, minute, "ending time: "+ endHour,endMinute
        msg = MIMEText(str(messageText))
        message.attach(msg)
        fp = open(picture, "rb").read()
        img = MIMEImage(fp,name=os.path.basename(picture))
        #fp.close()
        img.add_header('Content-ID', '<image1>')
        message.attach(img)
        
        s = smtplib.SMTP("mail.adnap.co",26)
        #s.set_debuglevel(1)
        s.ehlo()
        s.starttls()
        s.login("eventRequest@adnap.co","Heero4501")
        s.sendmail("eventRequest@adnap.co", strTo,  message.as_string())
        s.quit()
        print(name,organization,date,dateNum,description,address,food,music,merchandise,lat,longitude)
        self.nameEntry.delete(0, END)
        self.organizationEntry.delete(0, END)
        self.pictureEntry.delete(0, END)
        self.descriptionEntry.delete("1.0", END)
        self.addressEntry.delete(0, END)
        self.emailEntry.delete(0, END)
        self.shareMessageEntry.delete("1.0",END)
    def getPicture(self):
         root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
         self.picture.set((root.filename))
         self.pictureEntry.insert(0,root.filename)


if __name__ == "__main__":
    root = Tk()
    GUI = eventForm(root)
    root.mainloop()


