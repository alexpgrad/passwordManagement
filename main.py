from tkinter import *
from tkinter import messagebox
from connect import register, connect, get_all_data, store_passwords
from two_factor_authentication import setup_mfa, verify_mfa
from config import load_config 
from PIL import Image, ImageTk
from customtkinter import *
from CTkTable import CTkTable
import hashlib


safekey= CTk()
safekey.geometry('850x500+300+200')
safekey.resizable(False,False)
safekey.configure(bg_color="white") 

safekey.title("SafeKey Login")

###################################SIGN IN COMMAND#############################################

def signin():
    username= user.get()
    password=psw.get()
    connection = connect(load_config())
    cursor = connection.cursor()

    try: 
        cursor.execute("SELECT password, salt, secretkey FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            db_password, salt, secretkey = result
         
           #hashing user input to compare to hashed password in database
            if isinstance(salt, memoryview):
                salt = bytes(salt)
            hashing= hashlib.sha256()
            hashing.update(salt + password.encode())
            user_hash = hashing.hexdigest()

            if user_hash == db_password:
                if verify_mfa(secretkey,username, safekey):
                    print("login successful")

                    launch_main_ui()

                    
                else: print("Invalid code.")
            else: 
                messagebox.showerror('Login failed', 'Invalid username or password') 
        else: 
            messagebox.showerror('Login failed', 'Invalid username or password')
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if connection:
            cursor.close()
            connection.close()



######################################SIGN UP###############################################
def signup_command():
    window=Toplevel(safekey)
    window.title("Sign Up")
    window.geometry('850x500+300+200')
    window.configure(bg="white") 
    window.resizable(False,False)
    window.title("Sign up")

    side_img_data = Image.open("images/login.png")
    side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(450, 500))
    CTkLabel(master=window, text="", image= side_img).pack(expand=True, side="left")

    frame = CTkFrame(master=window, width=500, height=500, fg_color="#fff")
    frame.pack_propagate(0)
    frame.pack(expand=True, side="right")

    CTkLabel(master=frame, text="Safely Store your Passwords!", text_color="#147efb", anchor="w", justify="left", font=("Arial Bold", 20)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    CTkLabel(master=frame, text="Create an Account Here", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="  Username:", text_color="#147efb", anchor="w", justify="left", font=("Arial Bold", 14),  compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
    user_signup = CTkEntry(master=frame, width=300, fg_color="#fff", border_color="#147efb", border_width=1, text_color="#000")
    user_signup.pack(anchor="w", padx=(25, 0))
    user_signup.insert(0, 'Username')
    user_signup.bind("<FocusIn>", lambda e: user_signup.delete(0, 'end'))
    user_signup.bind("<FocusOut>", lambda e: user_signup.insert(0, 'Username') if user.get() == '' else None)

    CTkLabel(master=frame, text="  Password:", text_color="#147efb", anchor="w", justify="left", font=("Arial Bold", 14), compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
    psw_signup = CTkEntry(master=frame, width=300, fg_color="#fff", border_color="#147efb", border_width=1, text_color="#000", show="*")
    psw_signup.pack(anchor="w", padx=(25, 0))
    psw_signup.insert(0, 'Password')
    psw_signup.bind("<FocusIn>", lambda e: psw_signup.delete(0, 'end'))
    psw_signup.bind("<FocusOut>", lambda e: psw_signup.insert(0, 'Password') if psw.get() == '' else None)

    CTkLabel(master=frame, text="  Confirm Password:", text_color="#147efb", anchor="w", justify="left", font=("Arial Bold", 14), compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
    confirm_psw = CTkEntry(master=frame, width=300, fg_color="#fff", border_color="#147efb", border_width=1, text_color="#000", show="*")
    confirm_psw.pack(anchor="w", padx=(25, 0))
    confirm_psw.insert(0, 'Password')
    confirm_psw.bind("<FocusIn>", lambda e: confirm_psw.delete(0, 'end'))
    confirm_psw.bind("<FocusOut>", lambda e: psw.insert(0, 'Confirm Password') if psw.get() == '' else None)

    def signup():
        username = user_signup.get()
        password = psw_signup.get()
        confirm_password = psw_signup.get()

        if password != confirm_password:
            messagebox.showerror('Error', "Passwords do not match")
            return
        
        result = register(username, password, load_config())
        
        if result == "Password stored successfully!":

            connection = connect(load_config())
            cursor = connection.cursor()
            cursor.execute("SELECT secretkey FROM users WHERE username = %s", (username,))
            secretkey = cursor.fetchone()[0]
            setup_mfa(secretkey,username, window)
        else:
            messagebox.showerror('Error', "User already exists")

    CTkButton(master=frame, text="Sign up", fg_color="#147efb", hover_color="#FB9114", font=("Arial Bold", 12), text_color="#ffffff", width=300, command=signup).pack(anchor="w", pady=(40, 0), padx=(25, 0))


    window.mainloop()




######################################SIGN IN###############################################
side_img_data = Image.open("images/login.png")
side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(450, 500))


CTkLabel(master=safekey, text="", image= side_img).pack(expand=True, side="left")

frame = CTkFrame(master=safekey, width=500, height=500, fg_color="#fff")
frame.pack_propagate(0)
frame.pack(expand=True, side="right")


######################################HEADER FOR SIGN IN###################################
CTkLabel(master=frame, text="Welcome Back!", text_color="#147efb", anchor="w", justify="left", font=("Arial Bold", 40)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
CTkLabel(master=frame, text="Sign in to your account", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 16)).pack(anchor="w", padx=(25, 0))


CTkLabel(master=frame, text="  Username:", text_color="#147efb", anchor="w", justify="left", font=("Arial Bold", 14),  compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
user = CTkEntry(master=frame, width=300, fg_color="#fff", border_color="#147efb", border_width=1, text_color="#000")
user.pack(anchor="w", padx=(25, 0))
user.insert(0, 'Username')
user.bind("<FocusIn>", lambda e: user.delete(0, 'end'))
user.bind("<FocusOut>", lambda e: user.insert(0, 'Username') if user.get() == '' else None)

CTkLabel(master=frame, text="  Password:", text_color="#147efb", anchor="w", justify="left", font=("Arial Bold", 14), compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
psw = CTkEntry(master=frame, width=300, fg_color="#fff", border_color="#147efb", border_width=1, text_color="#000", show="*")
psw.pack(anchor="w", padx=(25, 0))
psw.insert(0, 'Password')
psw.bind("<FocusIn>", lambda e: psw.delete(0, 'end'))
psw.bind("<FocusOut>", lambda e: psw.insert(0, 'Password') if psw.get() == '' else None)


CTkButton(master=frame, text="Login", fg_color="#147efb", hover_color="#FB9114", font=("Arial Bold", 12), text_color="#ffffff", width=300, command=signin).pack(anchor="w", pady=(40, 0), padx=(25, 0))
CTkButton(master=frame, text="Don't have an account? Sign up!", fg_color="#EEEEEE", hover_color="#FB9114", font=("Arial Bold", 9), text_color="#147efb", width=300, command= signup_command).pack(anchor="w", pady=(20, 0), padx=(25, 0))


############################################################################################



def launch_main_ui(): 
##########WINOW CONFIG############

    safekey.destroy()

    launch_safekey = CTk()
    launch_safekey.geometry("1350x645")
    launch_safekey.resizable(True, True)
    launch_safekey.title("SafeKey")


    ##########SIDEBAR################

    side_frame = CTkFrame(master=launch_safekey, fg_color="#147efb",  width=176, height=650, corner_radius=0)
    side_frame.pack_propagate(0)
    side_frame.pack(fill="y", anchor="w", side="left")

    ##########LOGO##################

    logo_img_data = Image.open("images/logo.png")
    logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(190, 190))
    CTkLabel(master=side_frame, text="", image=logo_img).pack(pady=(10, 0), anchor="center")

    ############# MAIN SCREEN SIDEBAR ###############

    #HOME
    home_img_data = Image.open("images/home.png")
    home_img = CTkImage(dark_image=home_img_data, light_image=home_img_data, size=(35,35))
    CTkButton(master=side_frame, image=home_img, text= "Home", fg_color="transparent", font=("Arial Bold", 14), hover_color="#FB9114", anchor="w").pack(anchor="center", ipady=5, pady=(20,0))

    #CHANGE PASSWORDS
    lock_img_data = Image.open("images/lock.png")
    lock_img = CTkImage(dark_image=lock_img_data, light_image=lock_img_data, size=(35,35))
    CTkButton(master=side_frame, image=lock_img, text= "Passwords", fg_color="transparent", font=("Arial Bold", 14), hover_color="#FB9114", anchor="w").pack(anchor="center", ipady=5, pady=(16,0))


    #SEARCH
    search_img_data = Image.open("images/search.png")
    brute_img = CTkImage(dark_image=search_img_data, light_image=search_img_data, size=(35,35))
    CTkButton(master=side_frame, image=brute_img, text= "Search", fg_color="transparent", font=("Arial Bold", 14), hover_color="#FB9114", anchor="w").pack(anchor="center", ipady=5, pady=(16,0))

    #SETTINGS
    settings_img_data = Image.open("images/settings.png")
    settings_img = CTkImage(dark_image=settings_img_data, light_image=settings_img_data, size=(35,35))
    CTkButton(master=side_frame, image=settings_img, text= "Settings", fg_color="transparent", font=("Arial Bold", 14), hover_color="#FB9114", anchor="w").pack(anchor="center", ipady=5, pady=(16,0))

    #ACCOUNT
    account_img_data = Image.open("images/account.png")
    account_img = CTkImage(dark_image=account_img_data, light_image=account_img_data, size=(35,35))
    CTkButton(master=side_frame, image=account_img, text= "Account", fg_color="transparent", font=("Arial Bold", 14), hover_color="#FB9114", anchor="w").pack(anchor="center", ipady=5, pady=(100,0))

    #RIGHT HAND SIDE 
    main_ui = CTkFrame(master= launch_safekey, fg_color="#fff", width=680, height=650, corner_radius=0)
    main_ui.pack_propagate(0)
    main_ui.pack(side="left", expand = True, fill="both")

    #TITLE 
    title= CTkFrame(master= main_ui, fg_color="transparent")
    title.pack(anchor="n", fill="x", padx=27, pady=(10,0))
    CTkLabel(master=title, text="My Passwords", font=("Arial Black", 25), text_color= "#147efb").pack(anchor="nw", side="left")

    #REGISTER PASSWORD
    CTkButton(master=title, text= "+ New Password", font=("Arial Black", 12), text_color="#fff", fg_color= "#147efb", hover_color="#FB9114", command = add_new_pw).pack(anchor="ne", side="right")

    #SEARCH FOR PASSWORD
    search_bar = CTkFrame(master=main_ui, height=50, fg_color="#fff")
    search_bar.pack(fill="both", pady=(15, 0), padx=17)  
    CTkEntry(master=search_bar, width=600, placeholder_text="Search for Website", border_color="#147efb", border_width=2).pack(side="left", fill="both", expand = True, padx=(13, 0), pady=15)
    

    #GETTING DB DATA TO INSERT INTO TABLE
    password_db_data = get_all_data(load_config())
    db = [("ID", "Username", "Password", "Email", "URL", "Site Name", "Created on")]
    db.extend(password_db_data)

    min_rows =20 
    while len(db) < min_rows +1: 
        db.append(('','','','','','','')) 

    password_frame = CTkScrollableFrame(master=main_ui, fg_color="transparent")
    password_frame.pack(expand=True, fill="both", padx=17, pady=15)

    table = CTkTable(master=password_frame, values=db, colors=["#E6E6E6", "#EEEEEE"], header_color="#147efb")
    table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
    table.pack(expand=True, fill='both')

def add_new_pw():

    def add_to_db():
        try: 
            url = user_url.get()
            username = user_username.get()
            email = user_email.get()
            password = user_psw.get()
            site_name = user_sitename.get()
            config = load_config()
                
            result = store_passwords(username, password, email, url, site_name, config)
            messagebox.showinfo('Success', 'Password stored successfully!')
        except Exception as error:
            messagebox.showerror('Error', str(error))
    add_new = CTk()
    add_new.geometry('855x500+300+200')
    add_new.resizable(True, True)
    add_new.title("Save a New Password")

    ##########SIDEBAR################

    side_frame = CTkFrame(master=add_new, fg_color="#147efb",  width=176, height=650, corner_radius=0)
    side_frame.pack_propagate(0)
    side_frame.pack(fill="y", anchor="w", side="left")

    ############# MAIN SCREEN SIDEBAR ###############

    #HOME
    CTkButton(master=side_frame, text= "Home", fg_color="transparent", font=("Arial Bold", 14), hover_color="#FB9114", anchor="w").pack(anchor="center", ipady=5, pady=(20,0))

    #CHANGE PASSWORDS
    CTkButton(master=side_frame,  text= "Passwords", fg_color="transparent", font=("Arial Bold", 14), hover_color="#FB9114", anchor="w").pack(anchor="center", ipady=5, pady=(16,0))

    #BRUTE FORCE
    CTkButton(master=side_frame, text= "Brute Force", fg_color="transparent", font=("Arial Bold", 14), hover_color="#FB9114", anchor="w").pack(anchor="center", ipady=5, pady=(16,0))

    #SETTINGS
    CTkButton(master=side_frame,  text= "Settings", fg_color="transparent", font=("Arial Bold", 14), hover_color="#FB9114", anchor="w").pack(anchor="center", ipady=5, pady=(16,0))

    #ACCOUNT
    CTkButton(master=side_frame, text= "Account", fg_color="transparent", font=("Arial Bold", 14), hover_color="#FB9114", anchor="w").pack(anchor="center", ipady=5, pady=(16,10))

    #RIGHT HAND SIDE 
    psw_ui = CTkFrame(master= add_new, fg_color="#fff", width=680, height=650, corner_radius=0)
    psw_ui.pack_propagate(0)
    psw_ui.pack(side="left", expand = True, fill="both")

    #TITLE 
    title= CTkFrame(master= psw_ui, fg_color="transparent")
    title.pack(anchor="n", fill="x", padx=27, pady=(10,0))
    CTkLabel(master=title, text="Save a New Password", font=("Arial Black", 25), text_color= "#147efb").pack(anchor="nw", side="left")

    #URL
    CTkLabel(master=psw_ui, text="URL", font=("Arial Bold", 16), text_color= "#147efb").pack(anchor="nw", pady=(25,0), padx=27)
    user_url = CTkEntry(master=psw_ui, fg_color="#F0F0F0", border_width=0)
    user_url.pack(fill="x", pady=(12,0), padx=27, ipady=10)

    more_input = CTkFrame(master=psw_ui, fg_color="transparent")
    more_input.pack(fill="both", padx=27, pady=(31,0))
    
    CTkLabel(master=more_input, text="Username", font=("Arial Bold", 17), text_color="#147efb", justify="left").grid(row=0, column=0, sticky="w")
    user_username= CTkEntry(master=more_input, fg_color="#F0F0F0", border_width=0, width=300)
    user_username.grid(row=1, column=0, ipady=10)

    CTkLabel(master=more_input, text="Email", font=("Arial Bold", 17), text_color="#147efb", justify="left").grid(row=0, column=1, sticky="w", padx=(25,0))
    user_email= CTkEntry(master=more_input, fg_color="#F0F0F0", border_width=0, width=300)
    user_email.grid(row=1, column=1, ipady=10, padx=(25,0))

    CTkLabel(master=more_input, text="Password", font=("Arial Bold", 17), text_color="#147efb", justify="left").grid(row=2, column=0, sticky="w", pady=(38,0))
    user_psw= CTkEntry(master=more_input, fg_color="#F0F0F0", border_width=0, width=300)
    user_psw.grid(row=3, column=0, sticky="w", ipady=10)

    CTkLabel(master=more_input, text="Site Name", font=("Arial Bold", 17), text_color="#147efb", justify="left").grid(row=2, column=1, sticky="w", pady=(42,0), padx=(25,0))
    user_sitename= CTkEntry(master=more_input, fg_color="#F0F0F0", border_width=0, width=300)
    user_sitename.grid(row=3, column=1, ipady=10, padx=(25,0))

    new_btn = CTkFrame(master = psw_ui, fg_color="transparent")
    new_btn.pack(fill="both")

    CTkButton(master = new_btn, text= "Return", width=300, fg_color="transparent", font=("Arial Bold", 17),border_color= "#147efb", hover_color="#eee", border_width=2, text_color="#147efb").pack(side="left", anchor="sw", pady=(30,0), padx=(27,24))

    CTkButton(master=new_btn, text="Save", width=300, font=("Arial Bold", 17), hover_color="#FB9114", fg_color="#147efb", text_color="#fff", command= add_to_db).pack(side = "left", anchor="se", pady=(30,0), padx=(0,27))

safekey.mainloop()