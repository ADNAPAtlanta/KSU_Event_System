from firebase import firebase
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3

try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *


ksuBuildings = {"Baily Athletic Facility": "220 Kennesaw State Univ Rd NW Kennesaw, GA 30144",
                "Bailey Performance Hall":"488 Prillaman Way NW Kennesaw, GA 30144",
                "Burruss":"560 Parliament Garden Way NW Kennesaw, GA 30144",
                "Campus Services":"1075 Canton Pl NW Kennesaw, GA 30144",
                "Chastain Pointe":"1200 Chastain Rd NW Kennesaw, GA 30144",
                "Clendenin":"275 Kennesaw State Univ Rd NW Kennesaw, GA 30144",
                "Convocation Center":"590 Cobb Ave NW Kennesaw, GA 30144",
                "Education Classroom Facility":"580 Parliament Garden Way NW Kennesaw, GA 30144",
                "English Building":"440 Bartow Ave NW Kennesaw, GA 30144",
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
                "Science":"370 Paulding Ave NW Kennesaw, GA 30144",
                "Science Laboratory":"105 Marietta Dr NW Kennesaw, GA 30144",
                "Student Recreation & Activities Center":"290 Kennesaw State Univ Rd NW Kennesaw, GA 30144",
                "Social Sciences":"402 Bartow Ave NW Kennesaw, GA 30144",
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
                "Burruss",
                "Campus Services",
                "Chastain Pointe",
                "Clendenin",
                "Convocation Center",
                "Education Classroom Facility",
                "English Building",
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
                "Science",
                "Science Laboratory",
                "Student Recreation & Activities Center",
                "Social Sciences",
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

months = ["Jan", "Feb", "Mar", "Apr",
	   			    "May", "Jun", "July", "Aug",
				    "Sep", "Oct", "Nov", "Dec"]

years = ["2016","2017","2018"]
            



class eventForm:
    def __init__(self,master):
        self.master = master
        master.title("KSU Event System (organization ver.)")
        master.minsize(width=300,height=300)
        self.type = StringVar()
        self.type.set("Vacation")

        #entry variables
        self.name = StringVar()
        self.address = StringVar()
        self.building = StringVar()
        self.organization = StringVar()
        self.description = StringVar()
        self.lat = DoubleVar()
        self.longitude = DoubleVar()
        self.date = StringVar()
        self.category = StringVar()
        self.food = StringVar()
        self.food.set("No")
        self.alcohol = StringVar()
        self.alcohol.set("No")
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

        #Entry labels
        self.nameLabel = Label(master, text="Name of Event",underline=0)
        self.nameLabel.grid(row=1,column=1)
        self.nameEntry = Entry(master,bd=3,textvariable=self.name)
        self.nameEntry.grid(row=2,column=1,padx=5)
        
        self.organizationLabel = Label(master, text="Organization/Club",underline=0)
        self.organizationLabel.grid(row=1,column=2)
        self.organizationEntry = Entry(master,bd=3,textvariable=self.organization)
        self.organizationEntry.grid(row=2,column=2,padx=5)
        
        self.dateLabel = Label(master, text="Date",underline=0)
        self.dateLabel.grid(row=1,column=4)
        self.dayOption = OptionMenu(master,self.day,*days)
        self.dayOption.grid(row=2,column=3)
        self.monthOption = OptionMenu(master,self.month,*months)
        self.monthOption.grid(row=2,column=4)
        self.yearOption = OptionMenu(master,self.year,*years)
        self.yearOption.grid(row=2,column=5)
        
        self.descriptionLabel = Label(master, text="Description",underline=0)
        self.descriptionLabel.grid(row=3,column=1)
        self.descriptionEntry = Text(master,bd=3,height=5)
        self.descriptionEntry.grid(row=4,column=1,columnspan=2)

        self.buildingLabel = Label(master, text="Building",underline=0)
        self.buildingLabel.grid(row=5,column=1)
        self.building.set("Other")
        self.buildingSelection = OptionMenu(master,self.building,*ksuBuildingsOrdered)
        self.buildingSelection.grid(column=1)



        self.addressLabel = Label(master, text="Address (Enter if off campus)",underline=0)
        self.addressLabel.grid(row=5,column=2,sticky=W)
        self.addressEntry = Entry(master,textvariable=self.address,bd=3)
        self.addressEntry.grid(row=6,column=2,sticky=W)


        self.foodChoiceLabel = Label(master, text="Is food available?",underline=0)
        self.foodChoiceLabel.grid(column=1)
        self.foodChoiceYes = Radiobutton(master,text="Yes",variable=self.food,value="Yes")
        self.foodChoiceYes.grid(column=1)
        self.foodChoiceNo = Radiobutton(master,text="No",variable=self.food,value="No")
        self.foodChoiceNo.grid(column=1)

        self.alcoholChoiceLabel = Label(master,text= "Will there be alcohol?")
        self.alcoholChoiceLabel.grid(column=1)
        self.alcoholChoiceYes = Radiobutton(master,text="Yes",variable=self.alcohol,value="Yes")
        self.alcoholChoiceYes.grid(column=1)
        self.alcoholChoiceNo = Radiobutton(master,text="No",variable=self.alcohol,value="No")
        self.alcoholChoiceNo.grid(column=1)

        self.merchandiseChoiceLabel = Label(master,text= "Will there be merchandise?")
        self.merchandiseChoiceLabel.grid(column=1)
        self.merchandiseChoiceYes = Radiobutton(master,text="Yes",variable=self.merchandise,value="Yes")
        self.merchandiseChoiceYes.grid(column=1)
        self.merchandiseChoiceNo = Radiobutton(master,text="No",variable=self.merchandise,value="No")
        self.merchandiseChoiceNo.grid(column=1)

        self.submitButton = Button(master,text="Submit",command=self.submit)
        self.submitButton.grid(column=2)

    def submit(self):
        geolocator = GoogleV3(api_key="AIzaSyB9NYRXQZN3gIcJue5SJa2jem7UdOzmOvI")
        name = self.name.get()
        organization = self.organization.get()
        date = self.day.get() + "/" + self.month.get() + "/" + self.year.get()
        description = self.description.get()
        food = self.food.get()
        alcohol = self.alcohol.get()
        merchandise = self.merchandise.get()
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

        print(name,organization,date,description,address,food,alcohol,merchandise,lat,longitude)












        


if __name__ == "__main__":
    root = Tk()
    GUI = eventForm(root)
    root.mainloop()


