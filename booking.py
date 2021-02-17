''' Booking functions '''

from datetime import  date, timedelta, datetime
import admin # to retrieve the variables stored in that module

eachbuscap = admin.eachbuscap

bookingfilename = "bookings"
busfilename = f"demand_{date.today()}"
# A new file will be created every day
header_row = ["Date", "Location", "Matric Number", "Time","Confirmed"]
locations = ["Tampines","Sengkang","Punggol","Ang Mo Kio","Bukit Gombak","Pasir Ris"]
cutoff = datetime.now().replace(hour=21,minute=0,second=0,microsecond=0)

'''
To make a booking.
Inputs:
    matric_no: user's matriculation number (str)
'''
def make_booking(matric_no):
    userlocation = ""
    timeslot = -1
    confirmation = ""
    to_day = date.today()
    one_day = timedelta(days=1)
    booking_day = ((to_day +one_day).strftime("%d/%m/%Y"))   #Only allows one day advanced booking
    now = datetime.now()
    
    bookings = admin.loadcsv(bookingfilename,header_row)
    data = admin.loadbusdata(busfilename)
    bus_times = data["data"]
    
    menu = """Locations:
    - Tampines
    - Sengkang
    - Punggol
    - Ang Mo Kio
    - Bukit Gombak
    - Pasir Ris
    
    Enter "q" to quit.
    """
    
    for i in range(1,len(bookings)): #checks if the csv file contains an existing booking
            if bookings[i][2] == matric_no and bookings[i][0] == booking_day:
                print("Please withdraw your previous booking before making a new one.")
                return
    
    if now >= cutoff:
        print("Sorry, it is too late to book. Please come again tomorrow.")
        return
    
    admin.header("BOOKING")
    while userlocation not in locations: #Asking user to choose location
        print(menu)
        userlocation = input("Please enter a pickup location from this menu: ").title()
        if userlocation == "q":
            admin.returntomenu()
            
    
    if userlocation != "q":
        print(f"Time slots for {userlocation}:")
        for key in bus_times[userlocation].keys():
            print("-",key)
        
        while timeslot not in bus_times[userlocation]:
            print("Please enter the EXACT timeslot shown.")
            timeslot = input("Choose a timeslot: ")
                
        receipt = f"""
        1. Date: {booking_day}
        2. Location = {userlocation}
        3. Matric Number = {matric_no}
        4. Time: {timeslot}
        """
        
        print(receipt)

    while confirmation.lower() != "y" and confirmation.lower() != "n":
        confirmation = input("Please confirm your booking details. Is the above infomation correct? (Y/N): ")
                            
        if confirmation.lower() == "y":
            new_entry = [booking_day,userlocation,matric_no,timeslot,"N"]
            demand = bus_times[userlocation][timeslot][0]
            capacity = bus_times[userlocation][timeslot][1]
            demand += 1
            
            
            # Update the json file and save it for bus co. to access later
            bus_times[userlocation][timeslot][0] = demand
            admin.savebusdata(busfilename,data)
            
            success = countdemand(userlocation,demand,capacity,timeslot)


            if success == 1: # succeessfully booked
                new_entry[4] = "Y"
                admin.savecsv([new_entry],bookingfilename,"a")
                print("""Booking confirmed! Here is your receipt.
                Please show this to the bus driver tomorrow :)""")
                print(receipt)
            elif success == 0: # unsuccessful booking
                bus_times[userlocation][timeslot][0] -= 1
                admin.savebusdata(busfilename,data) # Reverse the demand and update JSOn
                print("""Your booking has been unsuccessful. 
                Reason: Not enough buses to support.""")     
            else: # on waitlist
                admin.savecsv([new_entry],bookingfilename,"a")
                print("You have been put on the waitlist. Please check back again later.")
            
        
        elif confirmation.lower() == "n":
            return make_booking(matric_no)
        else:
            print("Invalid. Please type only Y or N.")
        
        
        admin.returntomenu()
        
'''
To count the number of users who made booking, then determine
how many users will be on the waitlist.
This function calculates the number of buses needed for the bus company to send
It also does calculations to determine if booking is successful.
Inputs:
    location - location (str)
    demand - number of users who made booking (int)
    capacity - total capacity of all buses sent for the location (int)
    timeslot - timeslot booked (str for convenience)
Output:
    1 - demand <= capacity. i.e. user successfully booked
    0 - demand > capacity and no additional buses will be sent. Unsuccesful booking
    -1 - user still on waitlist
'''           
def countdemand(location, demand, capacity, timeslot):
    data = admin.loadbusdata(busfilename)
    bus_times = data["data"]
    waitlist = bus_times[location][timeslot][2]
    
    
    if demand <= capacity:
        return 1
    else:
        # update json file for bus co. to access
        waitlist = demand - capacity
        bus_times[location][timeslot][2] = waitlist
        additionalbusneeded = round(waitlist/eachbuscap) 
        # waitlist demand needs to be more than 50% of bus capacity 
        if additionalbusneeded > 0:
            #request for additional buses from bus company. 
            bus_times[location][timeslot][3] = additionalbusneeded
            admin.savebusdata(busfilename,data)
    
    # reload data
    newdata = admin.loadbusdata(busfilename)
    
    if newdata["data"][location][timeslot][4] == -1:
        return 0
    else:
        return -1 # still on waitlist e.g. because company has not approved additional buses yet
     # read from json file the add. buses. If -1, success = 0         

'''
Allow user to check booking status by printing status out.
Inputs:
    username - user's matriculation number (str)
'''
def check_booking(username):
    verified = False
    bookings = admin.loadcsv(bookingfilename,header_row)
    
    to_day = date.today()
    booking_day = ((to_day + timedelta(days=1)).strftime("%d/%m/%Y"))
    
    admin.header("CHECK BOOKING STATUS")
    while verified == False:
        location = input("Enter the location you wish to check booking: ").title()
        timeslot = input("Enter the timeslot booked (H:MM): ")
        for i in range(1,len(bookings)):
            if bookings[i][2] == username.upper() and bookings[i][0] == booking_day\
                and bookings[i][1] == location and bookings[i][3] == timeslot:
                    verified = True
                    break # to break out of for loop and stop searching
        else: # cannot find in the entire file
            print("Next-day booking cannot be found. Please verify the information entered is correct.")
            to_quit = input("Type Y to return to menu: ")
            if to_quit.upper() == "Y":
                admin.returntomenu()
                return
    
    # When verified == True
    busdata = admin.loadbusdata(busfilename)
    confirmeddata = []
    
    # if bus co agreed to send bus, confirm booking
    if busdata["data"][location][timeslot][4] not in  (-1,0):
        bookings[i][4] = "Y"
    
    if bookings[i][4] == "Y":
        print(f"""Here is your booking:
              Matriculation Number: {username}
              Date: {booking_day}
              Time: {timeslot}
              Location: {location}""")
        admin.savecsv(bookings,bookingfilename,"w")
        input("Press ENTER to return to menu.")
    elif bookings[i][4] == "N":
        if busdata["data"][location][timeslot][4] == -1:
            print("Your booking has been unsuccessful.")
            busdata["data"][location][timeslot][0] -= 1 # Reduce demand
            # if demand > 1.5*capacity, user is on waitlist. Remove from waitlist.
            if busdata["data"][location][timeslot][0] > 1.5 * busdata["data"][location][timeslot][1]:
                busdata["data"][location][timeslot][2] -= 1 #Reduce waitlist
            admin.savebusdata(busfilename,busdata)
            # Remove record from booking file
            for j in range(len(bookings)):
                if j == i:
                    continue
                else:
                    confirmeddata.append(bookings[j])
            admin.savecsv(confirmeddata,bookingfilename,"w")
        else:
            print("Your booking is still being processed. Please check back later.")
    
    admin.returntomenu()
    
'''
Allow user to withdraw booking.
Inputs:
    username - user's matriculation number (str)
'''
def withdraw_booking(username):
    verified = False
    bookings = admin.loadcsv(bookingfilename,header_row)
    data = admin.loadbusdata(busfilename)
    to_day = date.today()
    booking_day = ((to_day + timedelta(days=1)).strftime("%d/%m/%Y"))
    now = datetime.now()
    newdata = []
    
    if now >= cutoff:
        print(f"Withdrawal of booking not allowed after {cutoff.strftime('%I:%M %p')}")
        return
    
    admin.header("WITHDRAW BOOKING")
    while verified == False:
        location = input("Enter the location you wish to withdraw booking: ").title()
        timeslot = input("Enter the timeslot booked (H:MM): ")
        for i in range(1,len(bookings)):
            if bookings[i][2] == username.upper() and bookings[i][0] == booking_day\
                and bookings[i][1] == location and bookings[i][3] == timeslot:
                    data["data"][location][timeslot][0] -= 1
                    # if demand > 1.5*capacity, user is on waitlist. Remove from waitlist.
                    if data["data"][location][timeslot][0] > 1.5 * data["data"][location][timeslot][1]:
                        data["data"][location][timeslot][2] -= 1
                        
                    verified = True
                    admin.savebusdata(busfilename,data)
                    print("Booking withdrawn.")
                    break
        else:
            print("Next-day booking cannot be found. Please verify the information entered is correct.")
            i += 1 # To avoid deleting actual rows in the later for loop
            to_quit = input("Enter Y to return to menu: ")
            if to_quit.upper() == "Y":
                admin.returntomenu()
                return

    #Remove row by rewriting file
    for j in range(len(bookings)):
        if j == i:
            continue
        else:
            newdata.append(bookings[j])
            
    admin.savecsv(newdata,bookingfilename,"w")
    admin.returntomenu()
    