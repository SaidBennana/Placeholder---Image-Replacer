import tkinter as tk
import os
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from PIL import Image, ImageDraw, ImageFont

# Function to generate a placeholder image with the given width and height
def generate_placeholder_image(width, height):
    # Create a blank image with a solid color (light gray)
    placeholder_img = Image.new("RGB", (width, height), color=(211, 211, 211))  # Light gray background

    # Add text to the image (centered)
    draw = ImageDraw.Draw(placeholder_img)
    
    try:
        # You can use a default font or specify a font file
        font = ImageFont.load_default()
    except IOError:
        # Fallback if the default font is unavailable
        font = ImageFont.load_default()

    text = f"{width}x{height}"
    
    # Get the bounding box of the text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Calculate the position to center the text
    position = ((width - text_width) // 2, (height - text_height) // 2)
    
    # Draw the text on the placeholder image
    draw.text(position, text, fill="black", font=font)

    return placeholder_img

# Function to replace images with placeholder images in a folder (including subfolders)
def replace_images_with_placeholders(folder_path, progress_bar, progress_label):
    if not os.path.isdir(folder_path):
        messagebox.showerror("Error", "Invalid folder path.")
        return

    # Get the list of all image files in the folder and subfolders using os.walk
    image_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
                image_files.append(os.path.join(root, file))

    total_images = len(image_files)
    if total_images == 0:
        messagebox.showwarning("No Images", "No images found in the selected folder.")
        return

    # Update the progress bar and label
    progress_bar["maximum"] = total_images
    progress_bar["value"] = 0
    progress_label.config(text=f"Progress: 0/{total_images}")

    # Iterate over all files in the folder
    for index, file_path in enumerate(image_files, start=1):
        try:
            # Attempt to open the image
            with Image.open(file_path) as img:
                width, height = img.size

                # Generate the placeholder image
                placeholder_img = generate_placeholder_image(width, height)

                # Save the placeholder image with the same filename
                placeholder_img.save(file_path)
                print(f"Replaced {file_path} with placeholder.")
            
            # Update progress bar
            progress_bar["value"] = index
            progress_label.config(text=f"Progress: {index}/{total_images}")
            root.update_idletasks()  # Update the UI in real-time

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    messagebox.showinfo("Success", "All images in the folder have been replaced with placeholders.")

# Function to replace one image with a placeholder
def replace_one_image(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size

            # Generate the placeholder image
            placeholder_img = generate_placeholder_image(width, height)

            # Save the placeholder image with the same filename
            placeholder_img.save(image_path)
            print(f"Replaced {image_path} with placeholder.")
        
        messagebox.showinfo("Success", "The selected image has been replaced with a placeholder.")
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        messagebox.showerror("Error", f"Failed to replace image: {e}")

# Function to open a file dialog and get the selected folder
def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_label.config(text=f"Folder selected: {folder_selected}")
        folder_start_button.config(state=tk.NORMAL)  # Enable the Start button for folder once selected

# Function to open a file dialog and get the selected image
def select_image():
    image_selected = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
    if image_selected:
        image_label.config(text=f"Image selected: {image_selected}")
        replace_image_button.config(state=tk.NORMAL)  # Enable the Replace button for image once selected

# Function to open a file dialog and get the selected folder for the images
def select_images_folder():
    images_folder_selected = filedialog.askdirectory()
    if images_folder_selected:
        images_folder_label.config(text=f"Images Folder selected: {images_folder_selected}")
        
        # Find all image files in the folder using os.walk
        image_files = []
        for root, dirs, files in os.walk(images_folder_selected):
            for file in files:
                if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
                    image_files.append(os.path.join(root, file))

        # Show how many images were found
        if image_files:
            images_found_label.config(text=f"Found {len(image_files)} images in the selected folder.")
            replace_images_button.config(state=tk.NORMAL)  # Enable the Replace Images button once images are found
        else:
            images_found_label.config(text="No images found in the selected folder.")
            replace_images_button.config(state=tk.DISABLED)

# Creating the tkinter UI
def create_ui():
    global folder_label, image_label, folder_start_button, replace_image_button, images_folder_label, replace_images_button, progress_bar, progress_label, images_found_label

    root = tk.Tk()
    root.title("Image Placeholder Replacer")

    # Set the window size
    root.geometry("600x600")
    root.configure(bg="#f4f4f9")  # Light background color

    # Add "SAID BENNANA" logo at the top
    logo_label = tk.Label(root, text="SAID BENNANA", font=("Helvetica", 24, "bold"), bg="#333", fg="#ffffff")
    logo_label.pack(pady=20, fill="x", padx=10)  # Fill horizontally

    # Create a frame for the buttons and labels
    frame = tk.Frame(root, bg="#f4f4f9")
    frame.pack(pady=10, padx=20, fill="x")

    # Create a label for instructions
    label = tk.Label(frame, text="Select an image or folder to replace with placeholders.", font=("Arial", 12), bg="#f4f4f9", fg="#666")
    label.pack(pady=5)

    # Create a label to display selected folder path
    folder_label = tk.Label(frame, text="No folder selected", anchor="w", width=40, bg="#f4f4f9", fg="#333")
    folder_label.pack(pady=5)

    # Create a button to select folder
    select_folder_button = tk.Button(frame, text="Select Folder", command=select_folder, bg="#4CAF50", fg="white", font=("Arial", 12), relief="flat", width=20)
    select_folder_button.pack(pady=10)

    # Create a button to start replacing images inside the selected folder
    folder_start_button = tk.Button(frame, text="Start Folder Replacement", state=tk.DISABLED, command=lambda: replace_images_with_placeholders(folder_label.cget("text").replace("Folder selected: ", ""), progress_bar, progress_label), bg="#FF9800", fg="white", font=("Arial", 12), relief="flat", width=20)
    folder_start_button.pack(pady=10)

    # Create a label to display selected image path
    image_label = tk.Label(frame, text="No image selected", anchor="w", width=40, bg="#f4f4f9", fg="#333")
    image_label.pack(pady=5)

    # Create a button to select a single image
    select_image_button = tk.Button(frame, text="Select Image", command=select_image, bg="#2196F3", fg="white", font=("Arial", 12), relief="flat", width=20)
    select_image_button.pack(pady=10)

    # Create a button to replace the selected image
    replace_image_button = tk.Button(frame, text="Replace Image", state=tk.DISABLED, command=lambda: replace_one_image(image_label.cget("text").replace("Image selected: ", "")), bg="#FF5722", fg="white", font=("Arial", 12), relief="flat", width=20)
    replace_image_button.pack(pady=10)

    # Create a label to display selected images folder path
    images_folder_label = tk.Label(frame, text="No images folder selected", anchor="w", width=40, bg="#f4f4f9", fg="#333")
    images_folder_label.pack(pady=5)

    # Create a button to select a folder of images
    select_images_folder_button = tk.Button(frame, text="Select Images Folder", command=select_images_folder, bg="#4CAF50", fg="white", font=("Arial", 12), relief="flat", width=20)
    select_images_folder_button.pack(pady=10)

    # Create a label to show how many images are in the selected folder
    images_found_label = tk.Label(frame, text="No images found.", anchor="w", width=40, bg="#f4f4f9", fg="#333")
    images_found_label.pack(pady=5)

    # Create a button to replace images in the selected folder
    replace_images_button = tk.Button(frame, text="Replace All Images", state=tk.DISABLED, command=lambda: replace_images_with_placeholders(images_folder_label.cget("text").replace("Images Folder selected: ", ""), progress_bar, progress_label), bg="#FF9800", fg="white", font=("Arial", 12), relief="flat", width=20)
    replace_images_button.pack(pady=10)

    # Create a progress bar
    progress_bar = Progressbar(frame, length=300, mode="determinate")
    progress_bar.pack(pady=10)

    # Create a progress label
    progress_label = tk.Label(frame, text="Progress: 0/0", font=("Arial", 12), bg="#f4f4f9", fg="#333")
    progress_label.pack(pady=10)

    # Run the application
    root.mainloop()

# Create and run the UI
create_ui()