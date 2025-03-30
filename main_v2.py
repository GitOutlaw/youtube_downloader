import tkinter as tk
from tkinter import filedialog
from tkinter import ttk 
from pytubefix import YouTube
import threading
import time
import traceback

# create the main window
root = tk.Tk()
root.title("YouTube Downloader")  # set window title
# set window size (increased height for the browse button and progress bar)
root.geometry("400x425")

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

# function to update the progress bar and status
def update_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    progress_var.set(percentage)
    progress_bar['value'] = percentage  # Update the progress bar value
    root.update_idletasks()  # Force GUI update

    downloaded_mb = bytes_downloaded / (1024 * 1024)
    total_mb = total_size / (1024 * 1024)
    speed_mbps = 0
    if hasattr(update_progress, 'last_time') and hasattr(update_progress, 'last_bytes'):
        time_diff = time.time() - update_progress.last_time
        bytes_diff = bytes_downloaded - update_progress.last_bytes
        if time_diff > 0:
            speed_mbps = (bytes_diff / (1024 * 1024)) / time_diff
    update_progress.last_time = time.time()
    update_progress.last_bytes = bytes_downloaded

    status_label.config(
        text=f"Downloaded: {downloaded_mb:.2f} MB / {total_mb:.2f} MB ({percentage:.2f}%) | Speed: {speed_mbps:.2f} MB/s",
        fg="blue"
    )

# function to handle the download in a separate thread
def download_video_threaded():
    global download_path
    url = url_entry.get()
    status_label.config(text="Preparing download...", fg="blue")
    progress_var.set(0)
    progress_bar['value'] = 0
    root.update_idletasks()
    download_button.config(state=tk.DISABLED)  # Disable button during download

    try:
        yt = YouTube(url, on_progress_callback=update_progress)
        time.sleep(2)  # Adding a delay as suggested previously
        title = yt.title
        yd = yt.streams.get_highest_resolution()
        total_size_bytes = yd.filesize
        total_size_mb = total_size_bytes / (1024 * 1024)
        status_label.config(text=f"Downloading: {title} ({total_size_mb:.2f} MB)", fg="blue")

        # use the selected download path if it exists, otherwise download to default
        if download_path:
            yd.download(output_path=download_path)
        else:
            yd.download()

        # update status label with success message
        status_label.config(text=f"Download complete: {title}", fg="green")
    except Exception as e:
        status_label.config(text=f"An error occurred: {str(e)}", fg="red")
        print(f"An error occurred during download:")
        traceback.print_exc()  # Print the full traceback to the console
    finally:
        download_button.config(state=tk.NORMAL)  # Enable button after download

# function to start the download thread
def start_download():
    update_progress.last_time = time.time()  # Initialize last_time here
    thread = threading.Thread(target=download_video_threaded)
    thread.start()

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

# progress Bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(fill=tk.X, padx=10, pady=5)

# download button
download_button = tk.Button(root, text="Download", command=start_download)
download_button.pack(pady=10)

# status label
status_label = tk.Label(root, text="", wraplength=350, justify="center")
status_label.pack(pady=10)

# initialize last_time and last_bytes for speed calculation
update_progress.last_time = None
update_progress.last_bytes = 0

# start the GUI event loop
root.mainloop()