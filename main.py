import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class FigureDrawingApp:
    def __init__(self, root):
        # Initialize the application
        self.root = root
        self.root.title("Figure Drawing App")
        
        # Variables to store image folder, files, current index, and pause state
        self.image_folder = ""
        self.image_files = []
        self.current_image_index = 0
        self.paused = False
        
        # Label to display images
        self.image_label = tk.Label(root)
        self.image_label.pack()
        
        # Buttons for selecting image folder, starting, pausing, and stopping the slideshow
        self.load_button = tk.Button(root, text="Select Image Folder", command=self.select_image_folder)
        self.load_button.pack()

        # Frame for start, pause, and stop buttons
        self.start_pause_frame = tk.Frame(root)
        self.start_pause_frame.pack()

        self.start_button = tk.Button(self.start_pause_frame, text="Start", command=self.start_slideshow)
        self.start_button.pack(side=tk.RIGHT)

        self.pause_button = tk.Button(self.start_pause_frame, text="Pause", command=self.pause_slideshow)
        self.pause_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_slideshow)
        self.stop_button.pack()

        # Time interval options and dropdown menu
        self.time_options = [30, 60, 120, 300, 600]
        self.selected_time = tk.StringVar()
        self.selected_time.set(self.time_options[0])

        # Frame for navigation buttons
        self.navigation_frame = tk.Frame(root)
        self.navigation_frame.pack()
        
        # Buttons to navigate to previous and next images
        self.previous_button = tk.Button(self.navigation_frame, text="←", command=self.show_previous_image)
        self.previous_button.pack(side=tk.LEFT)
        self.next_button = tk.Button(self.navigation_frame, text="→", command=self.show_next_image)
        self.next_button.pack(side=tk.RIGHT)
        
        # Slideshow state initialization
        self.slideshow_running = False

    def start_slideshow(self):
        # Starts or continues the slideshow based on the pause state
        if self.image_files:
            self.slideshow_running = True
            selected_time = int(self.selected_time.get())
            if self.paused:
                self.show_next_image_continuously(selected_time)
            else:
                self.root.after(0, self.show_next_image_continuously, selected_time)

    def pause_slideshow(self):
        # Toggles the pause state of the slideshow
        self.paused = not self.paused
    
    def select_image_folder(self):
        # Selects a folder containing images and displays the first image in the folder
        self.image_folder = tk.filedialog.askdirectory()
        if self.image_folder:
            self.image_files = [os.path.join(self.image_folder, file) for file in os.listdir(self.image_folder)
                                if file.endswith(('jpg', 'jpeg', 'png'))]
            self.current_image_index = 0
            self.show_image()
    
    def show_image(self):
        # Displays the image in the image label
        if self.image_files:
            image_path = self.image_files[self.current_image_index]
            original_image = Image.open(image_path)
        
            width, height = original_image.size
            max_size = 400
            if width > height:
                new_width = max_size
                new_height = int(height * max_size / width)
            else:
                new_height = max_size
                new_width = int(width * max_size / height)
            
            resized_image = original_image.resize((new_width, new_height))
        
            photo = ImageTk.PhotoImage(resized_image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
    
    def stop_slideshow(self):
        # Stops the slideshow and removes the displayed image
        self.slideshow_running = False
        self.image_label.config(image="")
        self.image_label.image = None

    def show_previous_image(self):
        # Displays the previous image in the image label
        if self.image_files:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_files)
            self.show_image()
    
    def show_next_image(self):
        # Displays the next image in the image label
        if self.image_files:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
            self.show_image()
    
    def show_next_image_continuously(self, time_interval):
        # Displays images continuously based on the selected time interval
        if self.slideshow_running and not self.paused:
            self.show_next_image()
            self.root.after(time_interval * 1000, self.show_next_image_continuously, time_interval)

if __name__ == "__main__":
    root = tk.Tk()
    app = FigureDrawingApp(root)
    root.mainloop()
