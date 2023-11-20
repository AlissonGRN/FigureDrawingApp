import os  # Import the os module for operating system functionalities
import tkinter as tk  # Import the tkinter module for GUI development
from tkinter import filedialog  # Import filedialog from tkinter for file selection
from PIL import Image, ImageTk  # Import Image and ImageTk modules from PIL for image handling

class FigureDrawingApp:
    def __init__(self, root):
        self.root = root  # Set the root window for the application
        self.root.title("Figure Drawing App")  # Set the window title
        
        # Initialize variables to store image folder, files, and current index
        self.image_folder = ""
        self.image_files = []
        self.current_image_index = 0
        
        # Create a label to display images
        self.image_label = tk.Label(root)
        self.image_label.pack()
        
        # Create buttons for selecting image folder, starting, and stopping the slideshow
        self.load_button = tk.Button(root, text="Select Image Folder", command=self.select_image_folder)
        self.load_button.pack()
        self.start_button = tk.Button(root, text="Start", command=self.start_slideshow)
        self.start_button.pack()
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_slideshow)
        self.stop_button.pack()

        # Define options for time intervals and set the default value
        self.time_options = [30, 60, 120, 300, 600]
        self.selected_time = tk.StringVar()
        self.selected_time.set(self.time_options[0])

        # Create a dropdown menu for selecting time intervals
        self.time_dropdown = tk.OptionMenu(root, self.selected_time, *self.time_options)
        self.time_dropdown.pack()

        # Create a label to display the remaining time
        self.time_remaining_label = tk.Label(root, text="Time Remaining: ")
        self.time_remaining_label.pack()

        # Create a frame for navigation buttons
        self.navigation_frame = tk.Frame(root)
        self.navigation_frame.pack()
        
        # Create buttons for navigating to the previous and next images
        self.previous_button = tk.Button(self.navigation_frame, text="<< Previous", command=self.show_previous_image)
        self.previous_button.pack(side=tk.LEFT)
        self.next_button = tk.Button(self.navigation_frame, text="Next >>", command=self.show_next_image)
        self.next_button.pack(side=tk.RIGHT)
        
        # Initialize slideshow state
        self.slideshow_running = False

    def update_time_continuously(self, remaining_time):
        """Update the time remaining continuously while the slideshow is running."""
        if remaining_time >= 0 and self.slideshow_running:
            self.update_time_remaining(remaining_time)
            self.root.after(1000, self.update_time_continuously, remaining_time - 1)
    
    def update_time_remaining(self, time_remaining):
        """Update the label with the remaining time."""
        self.time_remaining_label.config(text=f"Time Remaining: {time_remaining} seconds")

    def start_slideshow(self):
        """Start the slideshow by setting the selected time interval and initiating the continuous update of time."""
        if self.image_files:
            self.slideshow_running = True
            selected_time = int(self.selected_time.get())
            self.update_time_remaining(selected_time)
            self.root.after(0, self.show_next_image_continuously, selected_time)
    
    def select_image_folder(self):
        """Select a folder containing images and display the first image in the folder."""
        self.image_folder = tk.filedialog.askdirectory()
        if self.image_folder:
            self.image_files = [os.path.join(self.image_folder, file) for file in os.listdir(self.image_folder)
                                if file.endswith(('jpg', 'jpeg', 'png'))]
            self.current_image_index = 0
            self.show_image()
    
    def show_image(self):
        """Display the image in the image label."""
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
        """Stop the slideshow."""
        self.slideshow_running = False
    
    def show_previous_image(self):
        """Display the previous image in the image label."""
        if self.image_files:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_files)
            self.show_image()
    
    def show_next_image(self):
        """Display the next image in the image label."""
        if self.image_files:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
            self.show_image()
    
    def show_next_image_continuously(self, time_interval):
        """Display the images continuously based on the selected time interval."""
        if self.slideshow_running:
            self.show_next_image()
            self.update_time_remaining(time_interval)
            self.root.after(time_interval * 1000, self.show_next_image_continuously, time_interval)

if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    app = FigureDrawingApp(root)  # Initialize the FigureDrawingApp instance
    root.mainloop()  # Start the main loop to handle events in the GUI
