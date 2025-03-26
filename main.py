import tkinter as tk
from pytubefix import YouTube

# Create the main window
root = tk.Tk()
root.title("YouTube Downloader")  # Set window title
root.geometry("400x300")  # Set window size

# Function to handle the download
def download_video():
    url = url_entry.get()
    status_label.config(text="Processing...", fg="blue")
    root.update()  # Update the GUI to show the "Processing..." message
    
    try:
        yt = YouTube(url)
        title = yt.title
        views = yt.views
        yd = yt.streams.get_highest_resolution()
        yd.download()
        
        # Update status label with success message
        status_label.config(text=f"Title: {title}\nViews: {views}\nDownload complete!", fg="green")
    except Exception as e:
        # Update status label with error message
        status_label.config(text=f"An error occurred: {str(e)}", fg="red")

# Title label at the top
title_label = tk.Label(root, text="YouTube Downloader", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# URL entry field
url_label = tk.Label(root, text="Enter YouTube URL:")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=40)
url_entry.pack(pady=5)

# Download button
download_button = tk.Button(root, text="Download", command=download_video)
download_button.pack(pady=10)

# Status label
status_label = tk.Label(root, text="", wraplength=350, justify="center")
status_label.pack(pady=10)

# Start the GUI event loop
root.mainloop()