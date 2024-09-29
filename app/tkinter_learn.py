import customtkinter
from customtkinter import filedialog

from PIL import Image, ExifTags, ImageTk
import tkinter as tk
try:
    path="app/IMG_1536.JPG"
    img = Image.open(path)
    
except (AttributeError, KeyError) as e:
    # Handle cases where EXIF data is unavailable
    print(e)
try:
        exif = dict(img.getexif())
        orientation = exif.get(ExifTags.TAGS.get('Orientation', 0))
        print(orientation)
        
        if orientation == 2:  # Horizontal flip
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 3:  # 180-degree rotation
            img = img.rotate(180)
        elif orientation == 6:  # 90-degree counterclockwise rotation
            img = img.transpose(Image.ROTATE_270)
        elif orientation == 8:  # 90-degree clockwise rotation
            img = img.transpose(Image.ROTATE_90)
except (AttributeError, KeyError, IndexError) as e:
        # Handle cases where EXIF data is unavailable or corrupted
        print(e)
        


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


#using classes
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.app()
        self.title("my app")
        self.geometry("800x500")
        self.grid_columnconfigure((0, 1), weight=1)

    def app(self):
        
        # self.grid_rowconfigure((0, 1, 2), weight=1) # equally distribute space over rows

        #using CheckboxFrame class
        '''self.checkbox_frame=CheckboxFrame(self)
        self.checkbox_frame.grid(row=1, column=0, padx=0, pady=(10,0), sticky="nsw")'''
        
        #using checkboxframe2
        self.checkbox_frame = CheckboxFrame2(self, values=["add this", "delete this", "hide this", "enhance"], title="options")
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")
        # self.checkbox_frame.configure(fg_color="transparent") #for configuration of checkboxFrame
        
        self.radiobuttonFrame=MyRadiobuttonFrame(self, values=["up", "down"], title="controls")
        self.radiobuttonFrame.grid(row=0, column=1, padx=0, pady=(10,0), sticky="nsw")

        self.button = customtkinter.CTkButton(self, text="select folder", command=self.button_callback, fg_color="#16898e")
        self.button.grid(row=1, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
        
        #image
        self.my_image = ImageFrame(self, img=img)
        self.my_image.grid(row=0, column=3, padx=20, pady=20, sticky="ew")

    def button_callback(self):
        print("button pressed")
        print("checkboxFrame: ", self.checkbox_frame.get())
        print("radioboxFrame: ", self.radiobuttonFrame.get())
        

            

    '''when defined here for same functioning'''
    '''def button_callback(self):
        print("checked checkboxes:", self.checkbox_frame.get())'''
    

        
# checkbox is still hardcoded, let's make it more convenient
class CheckboxFrame2(customtkinter.CTkScrollableFrame): #CTkFrame or CTkScrollableFrame as per use case
    def __init__(self, master, values, title):
        super().__init__(master)
        self.values=values
        self.title=title
        self.checkboxes=[]

        self.title=customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=20, pady=(20,0), sticky="ew")

        for idx, value in enumerate(self.values):
            checkbox=customtkinter.CTkCheckBox(self, text=value)
            checkbox.grid(row=idx+1, column=0, padx=20, pady=(20,0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes=[]
        for checkbox in self.checkboxes:
            if checkbox.get()==1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes
    
    def button_callback(self):
        print("checked checkboxes:", self.get())

class MyRadiobuttonFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value="")

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="ew")

        for i, value in enumerate(self.values):
            radiobutton = customtkinter.CTkRadioButton(self, text=value, value=value, variable=self.variable)
            radiobutton.grid(row=i + 1, column=0, padx=20, pady=(20, 0), sticky="w")
            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)

class ImageFrame(customtkinter.CTkFrame):
    def __init__(self, master, img):
        super().__init__(master)
        self.img=img

        self.my_image = customtkinter.CTkImage(light_image=self.img, size=(300, 200))
        self.image_label = customtkinter.CTkLabel(self, text="", image=self.my_image, fg_color="gray30")
        self.image_label.grid(row=0, column=0, sticky="ew")

        self.button2=customtkinter.CTkButton(self, text="open", fg_color="#16898e", command=self.open_image)
        self.button2.grid(row=1, column=0, sticky="w", pady=10)
        self.imagewin=None

    def open_image(self):
        if self.imagewin is None or not self.imagewin.winfo_exists():
            self.imagewin=openImage(self,img=img)
        else:
            self.imagewin.focus()

class openImage(customtkinter.CTkToplevel):
    def __init__(self, master, img):
        super().__init__(master)
        self.geometry("800x500")
        # self.label=customtkinter.CTkLabel(self, text="img")
        # self.label.grid(padx=20, pady=20)
        self.img=img
        desired_width, desired_height = 800, 500
        self.resized_image = self.img.resize((desired_width, desired_height), Image.Resampling.LANCZOS)

        # Create a PhotoImage from the resized image
        # self.my_image = ImageTk.PhotoImage(resized_image)
        self.my_image = customtkinter.CTkImage(light_image=self.resized_image, size=self.resized_image.size)
        self.image_label = customtkinter.CTkLabel(self, text="", image=self.my_image, fg_color="gray30")
        self.image_label.grid(column=0, row=0, sticky="ew", padx=20, pady=(20,0))
        self.image_label.anchor="CENTER"

app=App()
app.mainloop()