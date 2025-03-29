import tkinter as tk
from tkinter import filedialog
from pytubefix import YouTube

# create the main window
root = tk.Tk()
root.title("YouTube Downloader")  # set window title
# set window size (increased height for the browse button)
root.geometry("400x350")

# global variable to store the download path
download_path = ""

# function to open the file dialog and choose a download location


def browse_folder():
    global download_path
    download_path = filedialog.askdirectory()
    if download_path:
        location_label.config(text=f"Download Location: {download_path}")
    else:
        location_label.config(text="Download Location not selected")

# function to handle the download


def download_video():
    global download_path
    url = url_entry.get()
    status_label.config(text="Processing...", fg="blue")
    root.update()  # update the GUI to show the "Processing..." message

    try:
        yt = YouTube(url)
        title = yt.title
        views = yt.views
        yd = yt.streams.get_highest_resolution()

        # use the selected download path if it exists, otherwise download to default
        if download_path:
            yd.download(output_path=download_path)
        else:
            yd.download()

        # update status label with success message
        status_label.config(
            text=f"Title: {title}\nViews: {views}\nDownload complete!", fg="green")
    except Exception as e:
        # update status label with error message
        status_label.config(text=f"An error occurred: {str(e)}", fg="red")


# title label at the top
title_label = tk.Label(root, text="YouTube Downloader",
                       font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# url entry field
url_label = tk.Label(root, text="Enter YouTube URL:")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=40)
url_entry.pack(pady=5)

# browse button for selecting download location
browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.pack(pady=5)

# label to display the selected download location
location_label = tk.Label(
    root, text="Download Location not selected", wraplength=350, justify="center")
location_label.pack(pady=5)

# download button
download_button = tk.Button(root, text="Download", command=download_video)
download_button.pack(pady=10)

# status label
status_label = tk.Label(root, text="", wraplength=350, justify="center")
status_label.pack(pady=10)

# start the GUI event loop
root.mainloop()
