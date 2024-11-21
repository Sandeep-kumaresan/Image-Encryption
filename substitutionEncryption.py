import logisticKey as key  # Importing the key generating function
from tkinter import *
import tkinter as tk
from tkinter import filedialog
import numpy as np
import os
import cv2 
import matplotlib.pyplot as plt
import matplotlib.image as img
import subprocess
from PIL import ImageTk, Image, ImageFile


global image,image_arr,fln,pic,encryptedImage,height,width,generatedKey,enc
height = 0
width = 0



def chooseFile():
    global image,pic,fln,height,width,generatedKey,image_arr
    fln = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select Image',
                                        filetypes=(("JPG File", "*.jpg"), ("PNG file", "*.png"), ("All Files", "*.*")))
    image = Image.open(fln).convert("RGB")
    image_arr = np.array(image)
    pic = image.load()
    height, width, _ = image_arr.shape
    print(height, width)
    generatedKey = key.logistic_key(0.01, 3.95, height*width) 
    print(generatedKey)
    tk.messagebox.showinfo("Success", "The Image is Loaded and Key is generated")

    
def hist():
    global generatedKey,height,width,encryptedImage
    histogram_blue = cv2.calcHist([image_arr],[0],None,[256],[0,256])
    plt.plot(histogram_blue, color='blue') 
    histogram_green = cv2.calcHist([image_arr],[1],None,[256],[0,256]) 
    plt.plot(histogram_green, color='green') 
    histogram_red = cv2.calcHist([image_arr],[2],None,[256],[0,256]) 
    plt.plot(histogram_red, color='red') 
    plt.title('Intensity Histogram - Logistic Map Original Image', fontsize=15)
    plt.xlabel('pixel values', fontsize=10)
    plt.ylabel('pixel count', fontsize=10) 
    plt.show()
# Generating dimensions of the image

# Generating keys
# Calling logistic_key and providing r value such that the keys are pseudo-random
# and generating a key for every pixel of the image
   
def encrypt_image(): 
    global image_arr,generatedKey,height,width,encryptedImage,enc
# Encryption using XOR
    z = 0

# Initializing the encrypted image
    encryptedImage = np.zeros(shape=[height, width, 3], dtype=np.uint8)
   
    enc = open('D:\\Image Encryption\\Image Encryptor\\enc.txt', 'w+')
    for a in generatedKey:
        enc.write(str(a) + '\n')
   
# Substituting all the pixels in original image with nested for
    for i in range(height):
        for j in range(width):
        # USing the XOR operation between image pixels and keys
            encryptedImage[i, j] = image_arr[i, j].astype(int) ^ generatedKey[z]
            z += 1
 
    
# Saving the encrypted image
    im = Image.fromarray(encryptedImage)
    im.save('D:\\Image Encryption\\Image Encryptor\\Logistic_Encrypted images\\encrypted_image.png')
    print("Success")
    tk.messagebox.showinfo("Success", "The Image is Encrypted")
    
    # Displaying the encrypted image
    im.show()
def hist_enc():
    histogram_blue = cv2.calcHist([encryptedImage],[0],None,[256],[0,256])
    plt.plot(histogram_blue, color='blue') 
    histogram_green = cv2.calcHist([encryptedImage],[1],None,[256],[0,256]) 
    plt.plot(histogram_green, color='green') 
    histogram_red = cv2.calcHist([encryptedImage],[2],None,[256],[0,256]) 
    plt.plot(histogram_red, color='red') 
    plt.title('Intensity Histogram - Logistic Map Encrypted', fontsize=20)
    plt.xlabel('pixel values', fontsize=16)
    plt.ylabel('pixel count', fontsize=16) 
    plt.show()
    
    

def decrypt_image():
    global encryptedImage, generatedKey, height, width,decryptedImage
# Decryption using XOR
    z = 0
    """with open('C:\\Users\\Sandeep\\Desktop\\Image encryptor\\encim.txt', "r") as f:
        kl=f.read()
        encryptedImage = (kl)"""
    """with open ('C:\\Users\\Sandeep\\Desktop\\Image encryptor\\enc.txt', "r") as f:
        br=f.read()
        generatedKey = (br)"""

# Initializing the decrypted image
    decryptedImage = np.zeros(shape=[height, width, 3], dtype=np.uint8)

# Substituting all the pixels in encrypted image with nested for
    for i in range(height):
        for j in range(width):
            # USing the XOR operation between encrypted image pixels and keys
            decryptedImage[i, j] = encryptedImage[i, j].astype(int) ^ generatedKey[z]
            z += 1

# Displaying the decrypted image
    if decryptedImage.any():
        
        imf = Image.fromarray(decryptedImage)
        imf.save('D:\\Image Encryption\\Image Encryptor\\Logistic_decrypted images\\decrypted_image.png')
        print("Success")
        tk.messagebox.showinfo("Success", "The Image is Decrypted")
        imf.show()
def hist_dec():
    
    histogram_blue = cv2.calcHist([decryptedImage],[0],None,[256],[0,256])
    plt.plot(histogram_blue, color='blue') 
    histogram_green = cv2.calcHist([decryptedImage],[1],None,[256],[0,256]) 
    plt.plot(histogram_green, color='green') 
    histogram_red = cv2.calcHist([decryptedImage],[2],None,[256],[0,256]) 
    plt.plot(histogram_red, color='red') 
    plt.title('Intensity Histogram - Logistic Map Decrypted', fontsize=20)
    plt.xlabel('pixel values', fontsize=16)
    plt.ylabel('pixel count', fontsize=16) 
    plt.show()

def open_file5():
    subprocess.Popen(["python", "D:\\Image Encryption\\Image Encryptor\\emailworking.py"])
    
window=Tk()
window.resizable(False, False)
window.title('Image Encryptor')
window.geometry("400x400")
canvas = Canvas(window, width=400, height=400)
canvas.grid(row=0, column=0)

# or add the canvas widget to the window using place()
canvas.place(x=0, y=0)

if canvas is None:
    print("Failed to create canvas widget")
    exit()
else:
    print("Canvas widget created successfully")
bg_image = PhotoImage(file="C:\\Users\\HP\\Desktop\\76YS.gif")
if bg_image is None:
    print("Failed to load background image")
    exit()
canvas.create_image(0, 0, anchor=NW, image=bg_image )
tk.Button(text="Choose Image", command=chooseFile).grid(row=5, column=11, columnspan=4, padx=5,pady=50)
tk.Button(text="Histogram ", command=hist).grid(row=5, column=16, columnspan=7, padx=150,pady=50)
tk.Button(text="Encrypt", command=encrypt_image).grid(row=7, column=11, columnspan=4, padx=10,pady=20)
tk.Button(text="Histogram", command=hist_enc).grid(row=7, column=16, columnspan=7, padx=10,pady=10)
tk.Button(text="Decrypt", command=decrypt_image).grid(row=8, column=11, columnspan=4, padx=10,pady=10)
tk.Button(text="Histogram", command=hist_dec).grid(row=8, column=16, columnspan=7, padx=10,pady=10)
tk.Button(text="Send Email", command=open_file5).grid(row=9, column=15, columnspan=4, padx=20,pady=50)
window.mainloop()
