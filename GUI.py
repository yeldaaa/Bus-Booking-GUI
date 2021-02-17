from tkinter import *
from tkinter import messagebox # sometimes messagebox won't be called which is why this code is used
import tkinter as tk
import csv
import json
import random
from time import *
from datetime import *
from string import *
from booking import *
from admin import *
from menu import *
from PIL import ImageTk,Image 

'''Main Menu classes'''
class LoginWindow:
    username = ""
    password = ""
    def __init__(self, master):
        self.master = master
        master.title("NTU Bus Booking System")
        master.geometry("580x510")
        master.configure(bg = "white")
        
        # self.label1 = Label(master, text = """Welcome to the Shuttle Bus 
        #   Booking System""", font = ("Open sans", 24, "bold"), bg = "white", fg = "blue" )
        # self.label1.place(x=50, y=53)
        
        self.label2 = Label(master, text = "Username", font = ("Open sans", 18), bg = "white", fg = "blue")
        self.label2.place(x = 30, y = 220)
        self.inputno1 = Entry(master)
        self.inputno1.place(x= 180, y = 222)
        
        self.label3 = Label(master, text = "Password", font = ("Open sans", 18), bg = "white", fg = "blue")
        self.label3.place(x = 30, y = 320)
        self.inputno2 = Entry(master, show = "*")
        self.inputno2.place(x= 180, y = 322)

        self.b1 = Button(master, text="Login", width=8, bg="white", fg="red", command = lambda: [master.withdraw(), self.login()])
        self.b1.place(x=70, y=420)

        self.b2 = Button(master, text="Create account", width=13, bg="white", fg="red", command = lambda: [self.account_create(), master.withdraw()])
        self.b2.place(x=180, y=420)
        
        self.b3 = Button(master, text="Reset password", width=13, bg="white", fg="red", command = lambda: [self.password_reset(), master.withdraw()])
        self.b3.place(x=320, y=420) 
        
        self.b4 = Button(master, text="Quit", width=8, bg="white", fg="red", command = master.destroy)
        self.b4.place(x=450, y=420) 

    def login(self):
       
        LoginWindow.username = self.inputno1.get().upper()
        LoginWindow.password = self.inputno2.get()
        
        contents = loadcsv(file_name,account_header)
        index = get_user_index(LoginWindow.username)
        
        if index == None:
            messagebox.showerror("Error","Invalid matriculation no.")
            root.deiconify()  
        elif decode(contents[index][1],CAESAR_SHIFT) == LoginWindow.password:
            if contents[index][3] == "0":
                contents[index][3] = "1"
                self.app_menu()
            else:
                messagebox.showwarning("Warning","It seems you did not log out properly in the previous session. Please log in again.")
                contents[index][3] = "0"
                savecsv(contents,file_name,"w")
                root.deiconify()
        else:
            messagebox.showerror("Error","Invalid password.")
            root.deiconify()
        
        savecsv(contents,file_name,"w")
        self.inputno1.delete(0, 'end')
        self.inputno2.delete(0, 'end')

    def app_menu(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = menuappWindow(self.newWindow)
        
    def account_create(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = create_accountWindow(self.newWindow)

    def password_reset(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = reset_passwordWindow(self.newWindow)


class create_accountWindow:
    def __init__(self, master):
        self.master = master
        master.title("NTU Bus Booking System")
        master.geometry("600x700")
        master.configure(bg = "white")
        
        self.label1 = Label(master, text = f"""Password should fulfil the following: 
          1. At least {MIN_PW_LENGTH} characters long 
          2. Contain at least 1 upper and lowercase letter
          3. Contain at least 1 digit 
          4. Contain at least 1 special character
          5. No spaces allowed
          
          Username is your matriculation no.""", font = ("Open sans", 18), bg = "white", fg = "blue" )
        self.label1.place(x=0, y=53)
        
        self.label2 = Label(master, text = "Username", font = ("Open sans", 18), bg = "white", fg = "blue")
        self.label2.place(x = 30, y = 340)
        self.inputno1 = Entry(master)
        self.inputno1.place(x= 180, y = 342)
        
        self.label3 = Label(master, text = "Password", font = ("Open sans", 18), bg = "white", fg = "blue")
        self.label3.place(x = 30, y = 440)
        self.inputno2 = Entry(master, show = "*")
        self.inputno2.place(x= 180, y = 442)

        self.b1 = Button(master, text="Create account", width=13, bg="white", fg="red", command = self.create_account)
        self.b1.place(x=150, y=580)
        
        self.b4 = Button(master, text="Back", width=8, bg="white", fg="red", command = lambda: [master.destroy(), root.deiconify()])
        self.b4.place(x=260, y=580) 
    
    recoverykey = ""
    def create_account(self):          
        self.username = self.inputno1.get().upper()
        self.password = self.inputno2.get()   
        check_user = self.check_username()
        check_pass = self.check_password()
        
        if check_user == True:
            if check_pass == True:
                create_accountWindow.recoverykey = keygen()
                encodedkey = encode(create_accountWindow.recoverykey,CAESAR_SHIFT)
                encodedpw = encode(self.password,CAESAR_SHIFT)     
                newuser = [self.username,encodedpw,encodedkey,0]
                savecsv([newuser],file_name,"a")
                messagebox.showinfo("Account created!", f"Here is your recovery key: {create_accountWindow.recoverykey}\nDon't lose it!")
                self.master.withdraw()
                root.deiconify()
                
            elif check_pass == False: 
                messagebox.showerror("Error","Invalid password.")
        elif check_user == False: 
            messagebox.showerror("Error","Invalid username. Enter your matriculation no. e.g U1912345L")
            
    def check_username(self):
        usernames_list = []
        contents = loadcsv(file_name,account_header)
        for i in range(1,len(contents)): # skip header row (row[0])
            usernames_list.append(contents[i][0])
        
        if self.username == "":
            return False
        elif self.username[0] != "U" and self.username[0] != "N": # U for local students, N for foreign students
            return False
        elif len(self.username) != 9:
            return False
        elif self.username[-1].isalpha() == False: # check last index is a letter (A-Z)
            return False
        elif self.username[1:-1].isdigit() == False: # check if in between are digits
            return False
        elif self.username[1] != "1" and self.username[1] != "2": 
            return False
            # 1st 2 digits correspond to year of matriculation
            # But there can be a case of people who took gap years/dropped out since 2010 etc.
            # And each course has a different candidature
            # Hence, just check the first digit
        elif self.username in usernames_list:
            messagebox.showerror("Error","Username already exists. Did you mean to log in instead?")
            return
        else:
            return True
        
    def check_password(self):
        hasdigit = False
        hasupper = False
        haslower = False
        hasspecial = False
        hasspace = False
        
        if len(self.password) < MIN_PW_LENGTH:
            return False
        else:
            for char in self.password:
                if char.isdigit() == True:
                    hasdigit = True
                elif char.islower() == True:
                    haslower = True
                elif char.isupper() == True:
                    hasupper = True
                elif char in punctuation:
                    hasspecial = True
                elif char == " ":
                    hasspace = True
                
        if hasdigit and hasupper and haslower and hasspecial and not hasspace: 
            return True
        else:
            return False   
            
class reset_passwordWindow:
    username = ""
    def __init__(self, master):
        self.master = master
        master.title("Reset Password")
        master.geometry("500x500")
        master.configure(bg = "white")
        
        self.label1 = Label(master, text = "Please enter your Username and recovery key.", 
                            font = ("Open sans", 18), bg = "white", fg = "blue", wraplengt = 400)
        self.label1.place(x=0, y=103)
        self.label1.pack(fill=BOTH)
        
        self.label2 = Label(master, text = "Username", font = ("Open sans", 18), bg = "white", fg = "blue")
        self.label2.place(x = 30, y = 140)
        self.inputno1 = Entry(master)
        self.inputno1.place(x= 180, y = 142)
        
        self.label3 = Label(master, text = "Recovery key", font = ("Open sans", 18), bg = "white", fg = "blue")
        self.label3.place(x = 30, y = 240)
        self.inputno2 = Entry(master)
        self.inputno2.place(x= 180, y = 242)

        self.b1 = Button(master, text="Reset", width=8, bg="white", fg="red", command = self.reset_password)
        self.b1.place(x=120, y=380)
        
        self.b4 = Button(master, text="Back", width=8, bg="white", fg="red", command = lambda: [master.destroy(), root.deiconify()])
        self.b4.place(x=230, y=380)
        
    def reset_password(self):
  
        reset_passwordWindow.username = self.inputno1.get().upper()
        self.recoverykey = self.inputno2.get()   
        
        contents = loadcsv(file_name,account_header)
        index = get_user_index(self.username)
        
        if index == None:
            messagebox.showerror("Error","User not found.")
        elif decode(contents[index][2],CAESAR_SHIFT) != self.recoverykey:
            messagebox.showerror("Error","Invalid recovery key.")
        else:
            self.new_password()

    def new_password(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = new_passwordWindow(self.newWindow)
    
class new_passwordWindow(create_accountWindow,reset_passwordWindow):
    def __init__(self, master):
        self.master = master
        master.title("Input new password")
        master.geometry("500x500")
        master.configure(bg = "white")
        
        self.label1 = Label(master, text = f"""Please enter new password. 
        New password must be different from old password
            
        Password must meet requirements. 
        Remember that password must meet the following:
        1. At least {MIN_PW_LENGTH} characters long
        2. At least 1 uppercase letter and lowercase letter 
        3. At least 1 digit
        4. At least 1 special character
        5. No spaces allowed""", font = ("Open sans", 14), bg = "white", fg = "blue" )
        self.label1.place(x=0, y=53)
        
        self.label2 = Label(master, text = "New Password", font = ("Open sans", 18), bg = "white", fg = "blue")
        self.label2.place(x = 30, y = 340)
        self.inputno1 = Entry(master, show = "*")
        self.inputno1.place(x= 220, y = 342)
        
        self.b1 = Button(master, text="Confirm", width=13, bg="white", fg="red", command = self.password_new)
        self.b1.place(x=150, y=400)
        
        self.b4 = Button(master, text="Back", width=8, bg="white", fg="red", command = lambda: [master.destroy(), root.deiconify()])
        self.b4.place(x=260, y=400)
        
    def password_new(self):
        self.password = self.inputno1.get()     
        check_pass = self.check_password()
        contents = loadcsv(file_name,account_header)
        index = get_user_index(reset_passwordWindow.username)
        
        if self.password == decode(contents[index][1],CAESAR_SHIFT):
            messagebox.showwarning("Warning","New password cannot be same as old password.")
        elif check_pass == False:
            messagebox.showerror("Error","Password does not meet requirements.")
        else:
            contents[index][1] = encode(self.password,CAESAR_SHIFT)
            savecsv(contents,file_name,"w")
            messagebox.showinfo("Success","Your password has been changed successfully!")
            self.master.withdraw()


'''App Menu classes'''    
class menuappWindow:
    def __init__(self, master):
        self.master = master
        master.title("NTU Bus Booking System")
        master.geometry("580x350")
        master.configure(bg = "white")
        
        self.label1 = Label(master, text = "What would you like to do?", font = ("Open sans", 24, "bold"), 
                            bg = "white", fg = "blue", wraplength=500)
        self.label1.place(x=50, y=53)
        self.label1.pack(fill=BOTH, pady=30)
        
        self.b1 = Button(master, text="Make booking", width=13, bg="white", fg="red", command = lambda: [self.make_booking(), master.withdraw()])
        self.b2 = Button(master, text="Check booking", width=13, bg="white", fg="red", command = self.check_booking)
        self.b3 = Button(master, text="Withdraw booking", width=15, bg="white", fg="red", command = self.withdraw_booking)
        self.b4 = Button(master, text="Log out", width=10, bg="white", fg="red", command = lambda: [self.logout(), master.destroy(),root.deiconify()])

        self.b1.pack(pady=10)
        self.b2.pack(pady=10)
        self.b3.pack(pady=10)
        self.b4.pack(pady=10)
    
    def logout(self):
        contents = loadcsv(file_name,account_header)
        index = get_user_index(LoginWindow.username)
        
        if index == None:
            messagebox.showwarning("Error","Unable to log you out at the time. Please try again later.")
        elif contents[index][3] == "1":
            contents[index][3] = "0"
            savecsv(contents,file_name,"w")
            messagebox.showinfo("Log out successful!",credit + "\nThank you for using the program!")
        else:
            messagebox.showinfo("","You are not currently logged in.")

    def make_booking(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = make_bookingWindow(self.newWindow)       
   
    def check_booking(self):
        bookings = admin.loadcsv(bookingfilename,header_row)
        to_day = date.today()
        booking_day = ((to_day + timedelta(days=1)).strftime("%d/%m/%Y"))  
        verified = False
        
        for i in range(1,len(bookings)):
            if bookings[i][2] == LoginWindow.username and bookings[i][0] == booking_day:              
                location = bookings[i][1]
                timeslot = bookings[i][3]           
                verified = True
                break # to break out of for loop and stop searching
        else: # cannot find in the entire file
            messagebox.showerror("Error","Next-day booking cannot be found.")
     
        if verified == True:
            busdata = admin.loadbusdata(busfilename)
            confirmeddata = []
            
            # if bus co agreed to send bus, confirm booking
            if busdata["data"][location][timeslot][4] not in  (-1,0):
                bookings[i][4] = "Y"
            
            if bookings[i][4] == "Y":
                messagebox.showinfo("Booking Details",f"""
                      Here is your booking:
                      Matriculation no.: {LoginWindow.username}
                      Date: {booking_day}
                      Time: {timeslot}
                      Location: {location}""")
                admin.savecsv(bookings,bookingfilename,"w")
        
            elif bookings[i][4] == "N":
                if busdata["data"][location][timeslot][4] == -1:
                    messagebox.showwarning("Booking Unsuccessful","Your booking has been unsuccessful.")
                    busdata["data"][location][timeslot][0] -= 1 #Reduce demand
                    # if demand > 1.5*capacity, user is on waitlist. Remove from waitlist.
                    if data["data"][location][timeslot][0] > 1.5 * data["data"][location][timeslot][1]:
                        busdata["data"][location][timeslot][2] -=1 #Reduce waitlist
                    admin.savebusdata(busfilename,busdata)
                    # Remove record from booking file
                    for j in range(len(bookings)):
                        if j == i:
                            continue
                        else:
                            confirmeddata.append(bookings[j])
                    admin.savecsv(confirmeddata,bookingfilename,"w")
                else:
                    messagebox.showinfo("","Your booking is still being processed. Please check back later.")   

    def withdraw_booking(self):
        bookings = admin.loadcsv(bookingfilename,header_row)
        data = admin.loadbusdata(busfilename)
        to_day = date.today()
        booking_day = ((to_day + timedelta(days=1)).strftime("%d/%m/%Y")) 
        now = datetime.now()
        newdata = []
        
        if now >= cutoff:
            messagebox.showwarning("",f"Withdrawal of booking not allowed after {cutoff.strftime('%I:%M %p')}")
            return
        
        for i in range(1,len(bookings)):
            if bookings[i][2] == LoginWindow.username and bookings[i][0] == booking_day:
                location = bookings[i][1]
                timeslot = bookings[i][3]   
                data["data"][location][timeslot][0] -= 1
                # if demand > 1.5*capacity, user is on waitlist. Remove from waitlist.
                if data["data"][location][timeslot][0] > 1.5 * data["data"][location][timeslot][1]:
                    data["data"][location][timeslot][2] -= 1 #Reduce waitlist
                admin.savebusdata(busfilename,data)
                messagebox.showinfo("Success!",f"Booking withdrawn for {booking_day}, at {location}, {timeslot}.")
                break
        else: # else belongs to the for loop. Will run if booking cannot be found at all.
            messagebox.showerror("Error","Next-day booking cannot be found.")
            i += 1 # To avoid deleting actual rows in the later for loop

        #Remove row by rewriting file
        for j in range(len(bookings)):
            if j == i:
                continue
            else:
                newdata.append(bookings[j])
                
        admin.savecsv(newdata,bookingfilename,"w")
  
class make_bookingWindow(menuappWindow):        
    def __init__(self, master):
        self.master = master
        master.title("Make booking")
        master.geometry("500x500")
        master.configure(bg = "white")
        
        self.label3 = Label(master, text = "Choose your Location", font = ("Open sans", 18),bg = "white", fg = "blue")
        self.label3.place(x=30, y=180)
        
        self.locationlist = ["Ang Mo Kio", "Bukit Gombak", "Pasir Ris", "Punggol", "Sengkang", "Tampines"]
        self.var1 = StringVar()
        self.droplocationlist = OptionMenu(master, self.var1, *self.locationlist)
        self.var1.set("Select your Location")
        self.droplocationlist.config(width=20)
        self.droplocationlist.place(x=280, y = 180)
       
        self.b1 = Button(master, text="Next", width=10, bg="white", fg="red", command = self.nextpage)
        self.b1.place(x=150, y=380)

        self.b2 = Button(master, text="Quit", width=10, bg="white", fg="red", command = self.app_menu)
        self.b2.place(x=280, y=380)
      
    def nextpage(self):
        make_bookingWindow.userlocation = self.var1.get()
        if make_bookingWindow.userlocation == "Ang Mo Kio":
            self.window_AMK()
        elif make_bookingWindow.userlocation == "Bukit Gombak":
            self.window_BG()
        elif make_bookingWindow.userlocation == "Pasir Ris":
            self.window_PR()
        elif make_bookingWindow.userlocation == "Punggol":
            self.window_PG()
        elif make_bookingWindow.userlocation == "Sengkang":
            self.window_SK()
        elif make_bookingWindow.userlocation == "Tampines":
            self.window_TP()
        elif make_bookingWindow.userlocation == "Select your Location":
            messagebox.showwarning("Error 404","Please select your location")
            
    def app_menu(self): #goes back to previous page
        self.newWindow = tk.Toplevel(self.master)
        self.app = menuappWindow(self.newWindow)
        self.master.withdraw()
        
    def window_AMK(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = AMKWindow(self.newWindow)

    def window_BG(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = BGWindow(self.newWindow)

    def window_PR(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = PRWindow(self.newWindow)
        
    def window_PG(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = PGWindow(self. newWindow)
        
    def window_SK(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = SKWindow(self.newWindow)
        
    def window_TP(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = TPWindow(self.newWindow)
        
    def booking_make(self):          
        to_day = date.today()
        one_day = timedelta(days=1)
        booking_day = ((to_day +one_day).strftime("%d/%m/%Y"))   #Only allows one day advanced booking
        now = datetime.now()
        data = admin.loadbusdata(busfilename)
        bus_times = data["data"]     
        bookings = admin.loadcsv(bookingfilename,header_row)
        
        for i in range(1,len(bookings)): #checks if the csv file contains an existing booking

            if bookings[i][2] == LoginWindow.username and bookings[i][0] == booking_day:
                self.master.destroy()
                messagebox.showerror("Error","Please withdraw your previous booking before making a new one.")
                return
            
        if now >= cutoff:
            messagebox.showinfo("","Sorry, it is too late to book. Please come again tomorrow.")
            self.master.destroy()  
        elif self.var1.get() == "Select Your Time":
            messagebox.showwarning("Error 404","Please select a timeslot.")
        else:
            receipt = f"""
            Date: {booking_day}
            Location: {make_bookingWindow.userlocation}
            Matriculation no.: {LoginWindow.username}
            Time: {self.var1.get()}"""
            
            confirmation = messagebox.askyesno("Confirm booking", f"""
            Please confirm your booking details:
                                       
            {receipt}""") 
                        
            if confirmation == True:
                # self.var1.get() is the timeslot chosen
                new_entry = [booking_day,make_bookingWindow.userlocation,LoginWindow.username,self.var1.get(),"N"]
                demand = bus_times[make_bookingWindow.userlocation][self.var1.get()][0]
                capacity = bus_times[make_bookingWindow.userlocation][self.var1.get()][1]
                demand += 1                
                
                # Update the json file and save it for bus co. to access later
                bus_times[make_bookingWindow.userlocation][self.var1.get()][0] = demand
                admin.savebusdata(busfilename,data)
                
                success = countdemand(make_bookingWindow.userlocation,demand,capacity,self.var1.get())
       
                if success == 1: # succeessfully booked
                    new_entry[4] = "Y"
                    admin.savecsv([new_entry],bookingfilename,"a")
                    messagebox.showinfo("Booking Confirmed!", f"""Here is your receipt.\nPlease show this to the bus driver tomorrow:
                        
                    {receipt}""")
                    self.master.destroy()
                    
                elif success == 0: # unsuccessful booking
                    bus_times[make_bookingWindow.userlocation][self.var1.get()][0] -= 1
                    admin.savebusdata(busfilename,data) # Reverse the demand and update JSOn
                    messagebox.showinfo("Booking Unsuccessful","Your booking has been unsuccessful.")     
                else: # on waitlist
                    admin.savecsv([new_entry],bookingfilename,"a")
                    messagebox.showinfo("Booking In Process","You have been put on the waitlist. Please check back again later.")
            
            else: # If not confirmed, do nothing (don't save into file etc.)
                pass           

class AMKWindow(make_bookingWindow):
     def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        master.geometry("300x350")
        master.title("Ang Mo Kio")
        master.configure(bg = "white")
        
        self.label1 = Label(master, text = "Ang Mo Kio", font = ("Open sans", 20), bg = "white", fg = "blue" )
        self.label1.place(x=0, y=0)
        
        self.label2 = Label(master, text = "Choose your Time", font = ("Open sans", 14),bg = "white", fg = "blue")
        self.label2.place(x=0, y=45)
        
        self.timelist = ["7:00", "7:10", "7:20"]
        self.var1 = StringVar()
        self.droptimelist = OptionMenu(master, self.var1, *self.timelist)
        self.var1.set("Select Your Time")
        self.droptimelist.config(width=13)
        self.droptimelist.place(x=60, y = 80)
        
        self.timeslot = self.var1.get()
        
        self.b1 = Button(master, text="Confirm", width=10, bg="white", fg="red", command = self.booking_make)
        self.b1.place(x=40, y=200)

        self.b2 = Button(master, text="Back", width=10, bg="white", fg="red", command = master.destroy)
        self.b2.place(x=120, y=200)
        
    
class BGWindow(make_bookingWindow):
     def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        master.geometry("300x350")
        master.title("Bukit Gombak")
        master.configure(bg = "white")
        
        self.label1 = Label(master, text = "Bukit Gombak", font = ("Open sans", 20), bg = "white", fg = "blue" )
        self.label1.place(x=0, y=0)
        
        self.label2 = Label(master, text = "Choose your Time", font = ("Open sans", 14),bg = "white", fg = "blue")
        self.label2.place(x=0, y=45)
        
        self.timelist = ["7:40", "7:50", "8:00"]
        self.var1 = StringVar()
        self.droptimelist = OptionMenu(master, self.var1, *self.timelist)
        self.var1.set("Select Your Time")
        self.droptimelist.config(width=13)
        self.droptimelist.place(x=60, y = 80)
        
        self.b1 = Button(master, text="Confirm", width=10, bg="white", fg="red", command = self.booking_make)
        self.b1.place(x=40, y=200)

        self.b2 = Button(master, text="Back", width=10, bg="white", fg="red", command = master.destroy)
        self.b2.place(x=120, y=200)
        

class PRWindow(make_bookingWindow):
     def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        master.geometry("300x350")
        master.title("Pasir Ris")
        master.configure(bg = "white")
        
        self.label1 = Label(master, text = "Pasir Ris", font = ("Open sans", 20), bg = "white", fg = "blue" )
        self.label1.place(x=0, y=0)
        
        self.label2 = Label(master, text = "Choose your Time", font = ("Open sans", 14),bg = "white", fg = "blue")
        self.label2.place(x=0, y=45)
        
        self.timelist = ["7:00"]
        self.var1 = StringVar()
        self.droptimelist = OptionMenu(master, self.var1, *self.timelist)
        self.var1.set("Select Your Time")
        self.droptimelist.config(width=13)
        self.droptimelist.place(x=60, y = 80)
        
        self.b1 = Button(master, text="Confirm", width=10, bg="white", fg="red", command = self.booking_make)
        self.b1.place(x=40, y=200)

        self.b2 = Button(master, text="Back", width=10, bg="white", fg="red", command = master.destroy)
        self.b2.place(x=120, y=200)
               
class PGWindow(make_bookingWindow):
     def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        master.geometry("300x350")
        master.title("Punggol")
        master.configure(bg = "white")
        
        self.label1 = Label(master, text = "Punggol", font = ("Open sans", 20), bg = "white", fg = "blue" )
        self.label1.place(x=0, y=0)
        
        self.label2 = Label(master, text = "Choose your Time", font = ("Open sans", 14),bg = "white", fg = "blue")
        self.label2.place(x=0, y=45)
        
        self.timelist = ["7:10"]
        self.var1 = StringVar()
        self.droptimelist = OptionMenu(master, self.var1, *self.timelist)
        self.var1.set("Select Your Time")
        self.droptimelist.config(width=13)
        self.droptimelist.place(x=60, y = 80)
        
        self.b1 = Button(master, text="Confirm", width=10, bg="white", fg="red", command = self.booking_make)
        self.b1.place(x=40, y=200)

        self.b2 = Button(master, text="Back", width=10, bg="white", fg="red", command = master.destroy)
        self.b2.place(x=120, y=200)
            
class SKWindow(make_bookingWindow):
     def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        master.geometry("300x350")
        master.title("Sengkang")
        master.configure(bg = "white")
        
        self.label1 = Label(master, text = "Sengkang", font = ("Open sans", 20), bg = "white", fg = "blue" )
        self.label1.place(x=0, y=0)
        
        self.label2 = Label(master, text = "Choose your Time", font = ("Open sans", 14),bg = "white", fg = "blue")
        self.label2.place(x=0, y=45)
        
        self.timelist = ["7:00", "7:10"]
        self.var1 = StringVar()
        self.droptimelist = OptionMenu(master, self.var1, *self.timelist)
        self.var1.set("Select Your Time")
        self.droptimelist.config(width=13)
        self.droptimelist.place(x=60, y = 80)
        
        self.b1 = Button(master, text="Confirm", width=10, bg="white", fg="red", command = self.booking_make)
        self.b1.place(x=40, y=200)

        self.b2 = Button(master, text="Back", width=10, bg="white", fg="red", command = master.destroy)
        self.b2.place(x=120, y=200)

class TPWindow(make_bookingWindow):
     def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        master.geometry("300x350")
        master.title("Tampines")
        master.configure(bg = "white")
        
        self.label1 = Label(master, text = "Tampines", font = ("Open sans", 20), bg = "white", fg = "blue" )
        self.label1.place(x=0, y=0)
        
        self.label2 = Label(master, text = "Choose your Time", font = ("Open sans", 14),bg = "white", fg = "blue")
        self.label2.place(x=0, y=45)
        
        self.timelist = ["7:00", "7:10"]
        self.var1 = StringVar()
        self.droptimelist = OptionMenu(master, self.var1, *self.timelist)
        self.var1.set("Select Your Time")
        self.droptimelist.config(width=13)
        self.droptimelist.place(x=60, y = 80)
        
        self.b1 = Button(master, text="Confirm", width=10, bg="white", fg="red", command = self.booking_make)
        self.b1.place(x=40, y=200)

        self.b2 = Button(master, text="Back", width=10, bg="white", fg="red", command = master.destroy)
        self.b2.place(x=120, y=200)

def disable_event():
    pass

root = Tk()
root.protocol("WM_DELETE_WINDOW", disable_event) #disables red 'x' at the top right of window
canvas = Canvas(root, width = 290, height = 170)  
canvas.pack()  
img = ImageTk.PhotoImage(Image.open("donkeybus.jpg"))  
canvas.create_image(0, 0, anchor=NW, image=img) 
root.iconbitmap("favicon.ico")
my_gui = LoginWindow(root)
root.mainloop()