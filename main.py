import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class FigureDrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Figure Drawing App")
        
        self.image_folder = ""
        self.image_files = []
        self.current_image_index = 0
        
        self.image_label = tk.Label(root)
        self.image_label.pack()
        
        self.load_button = tk.Button(root, text="Select Image Folder", command=self.select_image_folder)
        self.load_button.pack()
        
        self.start_button = tk.Button(root, text="Start", command=self.start_slideshow)
        self.start_button.pack()
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_slideshow)
        self.stop_button.pack()

        self.navigation_frame = tk.Frame(root)
        self.navigation_frame.pack()
        
        self.previous_button = tk.Button(self.navigation_frame, text="<< Previous", command=self.show_previous_image)
        self.previous_button.pack(side=tk.LEFT)
        
        self.next_button = tk.Button(self.navigation_frame, text="Next >>", command=self.show_next_image)
        self.next_button.pack(side=tk.RIGHT)
        
        self.slideshow_running = False
    
    def select_image_folder(self):
        self.image_folder = tk.filedialog.askdirectory()
        if self.image_folder:
            self.image_files = [os.path.join(self.image_folder, file) for file in os.listdir(self.image_folder)
                                if file.endswith(('jpg', 'jpeg', 'png'))]
            self.current_image_index = 0
            self.show_image()
    
    def show_image(self):
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
    
    def start_slideshow(self):
        if self.image_files:
            self.slideshow_running = True
            self.show_next_image_continuously()
    
    def stop_slideshow(self):
        self.slideshow_running = False
    
    def show_previous_image(self):
        if self.image_files:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_files)
            self.show_image()
    
    def show_next_image(self):
        if self.image_files:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
            self.show_image()
    
    def show_next_image_continuously(self):
        if self.slideshow_running:
            self.show_next_image()
            self.root.after(60000, self.show_next_image_continuously)

if __name__ == "__main__":
    root = tk.Tk()
    app = FigureDrawingApp(root)
    root.mainloop()
