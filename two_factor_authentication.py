from tkinter import *
from tkinter import messagebox, simpledialog
from config import load_config 
from PIL import Image, ImageTk
from customtkinter import *
import pyotp
import qrcode
import io 


def setup_mfa(secretkey, username, parent_window):
   uri = pyotp.totp.TOTP(secretkey).provisioning_uri(name=username, issuer_name="SafeKey")
   img = qrcode.make(uri)

   ##need to convert img to a file that tkinter can open 
   img_buffer = io.BytesIO()
   img.save(img_buffer, format="PNG")
   img_buffer.seek(0)
   pil_img = Image.open(img_buffer)

   tk_image = ImageTk.PhotoImage(pil_img)

  # Open a new Tkinter Toplevel window to display the QR code
   qr_window = Toplevel(parent_window)
   qr_window.title("Scan QR Code")
   qr_window.geometry('500x500')  
   qr_window.configure(bg='white')

    # displays qr code in a new window
   qr_label = Label(qr_window, image=tk_image)
   qr_label.image = tk_image  # keep a reference!
   qr_label.pack(expand=True)

    # Add a label with instructions
   Label(qr_window, text="Please scan this QR code with Google Authenticator.", bg='white').pack()

   qr_window.mainloop()

def verify_mfa(secretkey, username, parent_window):
    # Ask user for 6 digit code
    user_input_code = simpledialog.askstring("MFA Verification", "Enter the six digit code from Google Authenticator:", parent=parent_window)
    if user_input_code:
        totp = pyotp.TOTP(secretkey)
        if totp.verify(user_input_code):
            messagebox.showinfo('Login', 'Login successful')
            return True
        else:
            messagebox.showerror('Login', 'Invalid code. Please try again.')
    return False
