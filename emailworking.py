import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
import tkinter as tk
from tkinter import filedialog

class EmailSenderUI:
    def __init__(self, master):
        self.master = master
        master.title("Email Sender")

        # email settings
        self.sender_email = tk.StringVar()
        self.sender_password = tk.StringVar()
        self.receiver_email = tk.StringVar()
        self.subject = tk.StringVar()
        self.message = tk.StringVar()
        self.image_path = tk.StringVar()
        self.key_path = tk.StringVar()
        
        # create widgets
        tk.Label(master, text="Sender Email:").grid(row=0, column=0)
        tk.Entry(master, textvariable=self.sender_email).grid(row=0, column=1)

        tk.Label(master, text="Sender Password:").grid(row=1, column=0)
        tk.Entry(master, textvariable=self.sender_password, show="*").grid(row=1, column=1)

        tk.Label(master, text="Receiver Email:").grid(row=2, column=0)
        tk.Entry(master, textvariable=self.receiver_email).grid(row=2, column=1)

        tk.Label(master, text="Subject:").grid(row=3, column=0)
        tk.Entry(master, textvariable=self.subject).grid(row=3, column=1)

        tk.Label(master, text="Message:").grid(row=4, column=0)
        tk.Entry(master, textvariable=self.message).grid(row=4, column=1)

        tk.Button(master, text="Choose Image", command=self.choose_image).grid(row=5, column=0)
        tk.Label(master, textvariable=self.image_path).grid(row=5, column=1)
        
        tk.Button(master, text="Choose key", command=self.choose_key).grid(row=6, column=0)
        tk.Label(master, textvariable=self.key_path).grid(row=6, column=1)

        tk.Button(master, text="Send Email", command=self.send_email).grid(row=7, column=0, columnspan=2)
        

    def choose_image(self):
        # open file dialog to choose image
        self.image_path.set(filedialog.askopenfilename(title="Choose Image", filetypes=[("Image files", "*.jpg *.jpeg *.png")]))
        
    def choose_key(self):
        # open file dialog to choose key
        self.key_path.set(filedialog.askopenfilename(title="Choose Key", filetypes=[("Key files", "*.txt")]))
    
    def send_email(self):
        if not self.image_path.get():
            print("Please select an image to attach.")
            tk.messagebox.showerror("Error", "Please select an image to attach.")
            return
        if not self.key_path.get():
            print("Please select a key to attach.")
            tk.messagebox.showerror("Error", "Please select a key to attach.")
            return
        # create message container
        msg = MIMEMultipart()
        msg['From'] = self.sender_email.get()
        msg['To'] = self.receiver_email.get()
        msg['Subject'] = self.subject.get()
        #msg.attach(MIMEImage(open(self.image_path.get(), 'rb').read()))
        #msg.attach(MIMEApplication(open(self.key_path.get(), 'rb').read()))
        with open(self.image_path.get(), 'rb') as f:
            img = f.read()
        attachh = MIMEImage(img)
        attachh.add_header('Content-Disposition', 'attachment', filename='Image.png')
        msg.attach(attachh)
        with open(self.key_path.get(), 'r') as f:
            text = f.read()
        attachment = MIMEApplication(text)
        attachment.add_header('Content-Disposition', 'attachment', filename='key.txt')
        msg.attach(attachment)

        # create SMTP session
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(self.sender_email.get(), self.sender_password.get())
            smtp.sendmail(self.sender_email.get(), self.receiver_email.get(), msg.as_string())

        # clear form
        self.sender_email.set('')
        self.sender_password.set('')
        self.receiver_email.set('')
        self.subject.set('')
        self.message.set('')
        self.image_path.set('')
        self.key_path.set('')
        tk.messagebox.showinfo("Email Sent", "Email sent successfully!")

root = tk.Tk()
EmailSenderUI(root)
root.mainloop()
