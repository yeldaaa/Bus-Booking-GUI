'''Main menu and app menu functions'''

import csv
import random
from time import sleep
from datetime import datetime
from string import punctuation,ascii_letters,digits
from booking import *
import booking # to retrieve global scope variables in booking
from admin import *

file_name = "accounts"
bookingfilename = booking.bookingfilename
MIN_PW_LENGTH = 8
BREAK_TO_MENU = "<"
CAESAR_SHIFT = 100 # Shift value for Caesar's cipher
now = datetime.now()
account_header = ["username","password","recoverykey","loggedin"]
header_row = booking.header_row
credit = """This program was developed by:
    
    Chin Min Rayy
    Goh Jun-Hui Adley
    Jackson Tang Qun Yao
    Lee Ting Wen
    Looi Keyang, Ethan\n"""

'''
To encode sensitive information.
Inputs:
    unencrypted_str: String to encrypt
    shift: Value to shift by for encoding process
Output:
    The encoded string
'''
def encode(unencrypted_str,shift):
    # To understand this, first understand how a normal
    # Caesar's cipher (purely letters) work
    # From ASCII table, possible range of ord is 33 to 126. 
    # This will never change unless ASCII table changes.
    # Hence, there are 94 different possibilities
    # Need to "loop back to start" every 94 characters (%94)
    # Using chr(33) as the "anchor point", 
    # determine how far each character is from that (ord(char)-33)
    ## Realise that for every char, the remainder will be different
    ## This uniqueness allows it to be "mapped" and "unmapped" back to same char
    ## Just like how a --> mapped to 97 --> unmapped to a
    # Shift it by a certain value to encode
    # Add back 33 to get the "actual" corresponding char/"absolute value" (+33)
    # Get the corresponding char (chr())
    # Repeat for each character in the string
    encoded = ""
    for i in range(len(unencrypted_str)):
        char = unencrypted_str[i]
        encoded += chr((ord(char)-33 + shift) % 94 + 33)
        encoded += chr(random.randint(33,126)) # for more obfuscation and security
    return encoded

'''
To decode an encoded string.
Inputs:
    encoded: The encoded string
    shift: Shift value. Note that this should be the same as the one in encoded
Output:
    The decoded string
'''
def decode(encoded,shift):
    # To decode, reverse the shift
    decoded = ""
    for i in range(len(encoded)):
        if i%2 == 0:
            char = encoded[i]
            decoded += chr((ord(char)-33 - shift) % 94 + 33)
    return decoded

'''
Check validity of username.
Inputs:
    username: User's chosen username (matriculation number in this case)
Output:
    True if username is valid; False otherwise.
'''
def check_username(username):
    usernames_list = []
    contents = loadcsv(file_name,account_header)
    for i in range(1,len(contents)): # skip header row (row[0])
        usernames_list.append(contents[i][0])
    
    if username == "":
        print("Username cannot be blank.")
        return False
    elif username == BREAK_TO_MENU:
        return BREAK_TO_MENU
    elif username in usernames_list:
        print("The matriculation number already exists. Did you mean to log in?")
        return False
    elif username[0] != "U" and username[0] != "N": # U for local students, N for foreign students
        print("Invalid matriculation number.")
        return False
    elif len(username) != 9:
        print("Invalid matriculation number.")
        return False
    elif username[-1].isalpha() == False: # check last index is a letter (A-Z)
        print("Invalid matriculation number.")
        return False
    elif username[1:-1].isdigit() == False: # check if in between are digits
        print("Invalid matriculation number.")    
        return False
    elif username[1] != "1" and username[1] != "2": 
        print("Invalid matriculation number")
        return False
        # 1st 2 digits correspond to year of matriculation
        # But there can be a case of people who took gap years/dropped out since 2010 etc.
        # And each course has a different candidature
        # Hence, just check the first digit
    else:
        return True

'''
Check validity of password.
Inputs:
    password: User's chosen password
Output:
    True if this password meets requirements; False otherwise
'''
def check_password(password):
    hasdigit = False
    hasupper = False
    haslower = False
    hasspecial = False
    hasspace = False
    
    if len(password) < MIN_PW_LENGTH:
        return False
    else:
        for char in password:
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
        # All True except space
        return True
    else:
        return False

'''
Generate random sequence of characters for recovery key
Output: the recovery key
'''
def keygen():
    values = ascii_letters + digits 
    key = []
    for i in range(random.randint(5,10)):
        key.append(random.choice(values)) 
        recoverykey = "".join(key) # convert to string
    
    return recoverykey

'''
To retrieve the index corresponding to the username.
Inputs:
    username: User's matriculation number
Output:
    index (will be None if cannot be found)
'''
def get_user_index(username):
    contents = loadcsv(file_name,account_header)
    for i in range(1,len(contents)):
        if username == contents[i][0]:
            return i

'''
Create account
'''
def create_account():
    valid_username = False
    valid_password = False
    
    header("CREATE ACCOUNT")
    while not valid_username:
        print(f"To return to main menu, enter {BREAK_TO_MENU}")
        username = input("Please enter your matriculation number: ").upper()
        # use matric no. to verify they are NTU students
        
        user_verification = check_username(username) # create a variable to store result
        # to avoid calling the function twice in the below lines.
        if user_verification == True:
            valid_username = True
        elif user_verification == BREAK_TO_MENU:
            returntomenu()
            return main_menu()
        else:
            continue

    print(f"Password should fulfil the following: \n\
          1. At least {MIN_PW_LENGTH} characters long \n\
          2. Contain at least 1 upper and lowercase letter \n\
          3. Contain at least 1 digit \n\
          4. Contain at least 1 special character\n\
          5. No spaces allowed.")
    while not valid_password:
        password = input("Choose a password: ")
        if check_password(password) == True:
            recoverykey = keygen()
            encodedkey = encode(recoverykey,CAESAR_SHIFT)
            encodedpw = encode(password,CAESAR_SHIFT)
            
            newuser = [username,encodedpw,encodedkey,0]
            # last element is 0 to indicate user not logged in
            # NOTE: Upon saving, 0 will become a string "0"
            savecsv([newuser],file_name,"a")
        
            print(f"Account created! \n\
            Here is your recovery key: {recoverykey} \n\
            Don't lose it!")
            input("Press ENTER to return to menu.") # Any key can be pressed, but won't continue until ENTER pressed
            valid_password = True
        else:
            print("Password requirements not met.")
        
    returntomenu()
    return main_menu()

'''
Log in
'''
def login():
    username = ""
    verified = False
    
    contents = loadcsv(file_name,account_header)
    
    header("LOG IN")
    while not verified:
        print(f"To return to main menu, enter {BREAK_TO_MENU} when entering username AND password.")
        username = input("Username: ").upper()
        password = input("Password: ")
        
        index = get_user_index(username)
        
        if username == BREAK_TO_MENU and password == BREAK_TO_MENU:
            returntomenu()
            return main_menu()
        elif index == None:
            print("Invalid credentials")
        elif decode(contents[index][1],CAESAR_SHIFT) == password:
            if contents[index][3] == "0":
                verified = True
                contents[index][3] = "1"
            else:
                print("You are already logged in.")
                verified = True
                
            #app(username) # or something like that
        else:
            print("Invalid credentials.")
        
    
    savecsv(contents,file_name,"w")
    return app_menu(verified, username)
    
'''
Log out
'''       
def logout(username):
    contents = loadcsv(file_name,account_header)
    index = get_user_index(username)
    
    if index == None:
        print("It seems like we have an error. Please try again later.")
    elif contents[index][3] == "1":
        contents[index][3] = "0"
        savecsv(contents,file_name,"w")
        print(credit)
        print("Thank you for using the program!")
        sleep(0.5)
    else:
        print("You are not currently logged in.")
    
'''
Reset password.
'''
def reset_password():
    username = ""
    successful = False
    pw_changed = False
    
    contents = loadcsv(file_name,account_header)
    header("RESET PASSWORD")
    
    while not successful:
        print(f"To return to main menu, enter {BREAK_TO_MENU} for username AND recovery key")
        username = input("Username: ").upper()
        recoverykey = input("Recovery key: ")
        index = get_user_index(username)
        
        if username == BREAK_TO_MENU and recoverykey == BREAK_TO_MENU:
            returntomenu()
            return main_menu()
        elif index == None:
            print("User not found.")
        elif decode(contents[index][2],CAESAR_SHIFT) != recoverykey:
            print("Invalid recovery key.")
        else:
            successful = True

    # will only happen if above loop broken i.e. successful
    while not pw_changed:
        newpw = input("Please enter a new password: ")
        if newpw == decode(contents[index][1],CAESAR_SHIFT):
            print("New password cannot be the same as old password.")
        elif check_password(newpw) == False:
            print(f"""Password must meet requirements. Remember that password must meet the following:
            1. At least {MIN_PW_LENGTH} characters long
            2. At least 1 uppercase letter and lowecase letter 
            3. At least 1 digit
            4. At least 1 special character
            5. No spaces allowed""")
        else:
            contents[index][1] = encode(newpw,CAESAR_SHIFT)
            pw_changed = True
            savecsv(contents,file_name,"w")
            print("Your password has been changed successfully!")
            returntomenu()
            return main_menu()

'''
Main menu. This is the "main loop". 
'''
def main_menu():
    valid_options = ["1","2","3","4"] # for easier future expanion if want to add more options
    selection = ""

    header("MAIN MENU")
    print("""Welcome to the bus program!
In this current pandemic climate, NTU has implemented a no-standing rule on buses.
With this program, you can indicate your interest to take the heartland shuttle buses and secure yourself a seat.
This way, you won't hae to worry about queuing only to realise there are no more seats left.

Please choose one of the following options to proceed:
    1. Log in
    2. Create account
    3. Reset password
    4. Quit""")

    while selection not in valid_options:
        selection = input("Option: ")

        if selection == "1":
            login()
        elif selection == "2":
            create_account()
        elif selection == "3":
            reset_password()
        elif selection == "4":
            print(credit)
            print("We hope you enjoyed using the program!") # Another print statement to improve readability
            sleep(2)
            return
        else:
            print("Invalid option.")

'''
App menu. This is the menu users see after logging in.
The app menu connects to functions in booking.py
Inputs:
    login: Whether user is logged in (1) or not (0)
    username: User's matriculation number
'''
def app_menu(login, username):
    selection = ""
    
    header("WELCOME!")
    while True:
        menu = """What would you like to do?
        1. Make booking
        2. Check booking
        3. Withdraw booking
        4. Log out"""
        print(menu)
        selection = input("Enter your selection: ")
    
        if selection == "1":
            loadcsv(bookingfilename,header_row)
            make_booking(username)
            return app_menu(login,username) # when function above completes, will return here
        elif selection == "2":
            check_booking(username)
            return app_menu(login,username)
        elif selection == "3":
            withdraw_booking(username)
            return app_menu(login,username)
        elif selection == "4":
            logout(username)
            return
        else:
            print("Invalid selection.")

''' If you wish to run the command line version, uncomment the below line'''
#main_menu()