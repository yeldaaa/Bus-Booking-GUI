'''Functions that the bus company will use'''

from admin import loadbusdata, savebusdata, header
import booking

busfilename = booking.busfilename
eachbuscap = booking.eachbuscap

'''
Bus company's response to the demand. 
Bus co. can either send bus or not send additional buses.
Response will be saved in a json file, which the app will use to communicate
to determine if additional buses are sent.
'''
# Company will need to manually call the function before day is over.
def busresponse():
    data = loadbusdata(busfilename)

    for location in data["data"].keys():
        header(location.upper())
        for timeslot in data["data"][location].keys():
            sendbus = ""
            needed = data["data"][location][timeslot][3]
            
            # reset ADDITIONAL buses sent to 0
            # This allows bus co. to change their mind later if e.g. waitlist increased
            data["data"][location][timeslot][4] = 0

            print(timeslot)
            if needed == 0: # No action required by bus company
                print("There are currently enough buses.")   
                continue 
            else:
                print(f"\tWaiting list: {data['data'][location][timeslot][2]}")
                print(f"\tAdditional buses needed: {needed}")
                
                
                while sendbus != "Y" and sendbus != "N":
                    sendbus = input("Send buses? [Y/N]: ").upper()
                    
                if sendbus == "Y":
                    newcap = needed * eachbuscap
                    data["data"][location][timeslot][4] += needed #add. buses sent
                    data["data"][location][timeslot][3] -= needed #hence, less buses needed
                    data["data"][location][timeslot][1] += newcap #total capacity increased
                    data["data"][location][timeslot][2] -= newcap #waitlist decreased
                    if data["data"][location][timeslot][2] < 0:
                        data["data"][location][timeslot][2] = 0
    
                    
    
                elif sendbus == "N":
                    data["data"][location][timeslot][4] = -1 # indicate no bus sent
                    savebusdata(busfilename,data)
                else:
                    print("Only enter Y for yes, N for no.")
    
        savebusdata(busfilename,data)
      
''' For bus company to run this program.'''
busresponse()
