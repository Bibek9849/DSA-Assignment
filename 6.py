import os
import requests
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import threading
import time

class ImageDownloaderGUI:
    def __init__(self, root):
        self.futures = None
        self.root = root
        self.root.title("Image Downloader")

        self.urls_entry = ttk.Entry(root, width=50)
        self.urls_entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

        # Define styles for buttons
        self.style = ttk.Style()
        self.style.configure('Normal.TButton', background='white')  # Normal state
        self.style.configure('Active.TButton', background='blue')  # Active (clicked) state
        self.style.configure('Paused.TButton', background='orange')  # Paused state
        self.style.configure('Cancelled.TButton', background='red')  # Cancelled state

        # Start Download button
        self.start_button = ttk.Button(root, text="Start Download", command=self.start_download, style='Normal.TButton')
        self.start_button.grid(row=1, column=0, padx=10, pady=10)

        # Pause Download button
        self.pause_button = ttk.Button(root, text="Pause Download", command=self.pause_download, style='Normal.TButton')
        self.pause_button.grid(row=1, column=1, padx=10, pady=10)

        # Resume Download button
        self.resume_button = ttk.Button(root, text="Resume Download", command=self.resume_download, style='Normal.TButton')
        self.resume_button.grid(row=1, column=2, padx=10, pady=10)

        # Cancel Download button
        self.cancel_button = ttk.Button(root, text="Cancel Download", command=self.cancel_download, style='Normal.TButton')
        self.cancel_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Status Label
        self.status_label = ttk.Label(root, text="")
        self.status_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.download_path = os.getcwd()+'/images'
        self.download_queue = queue.Queue()
        self.thread_pool = None  # ThreadPoolExecutor instance
        self.is_paused = False
        self.is_cancelled = False
        self.progress_labels = dict()
        self.lock = threading.Lock()

        # Dictionary to store progress bars for each URL
        self.progress_bars = dict()

    def download_image(self, url,image_id):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = os.path.join(self.download_path, f"{timestamp}_{image_id}.jpg")
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=4000):
                    with self.lock:
                        if self.is_cancelled:
                            break

                        while self.is_paused:
                            if self.is_cancelled:
                                break
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        # Update progress bar
                        progress = int((downloaded_size / total_size) * 100)
                        self.progress_bars[url].set(progress)
                        status_text = f"{timestamp}_{image_id}.jpg: {progress}%"
                        self.progress_labels[url].config(text=status_text)

                        time.sleep(1)

            with self.lock:
                self.download_queue.put(f"Downloaded: {url}")

        except Exception as e:
            with self.lock:
                self.download_queue.put(f"Error downloading {url}: {e}")

    def start_download(self):
        urls = self.urls_entry.get().split(',')
        self.urls_entry.config(state=tk.DISABLED)
        self.status_label.config(text="Downloading...")

        os.makedirs(self.download_path, exist_ok=True)

        # Create a ThreadPoolExecutor with a maximum of 5 worker threads
        self.thread_pool = ThreadPoolExecutor(max_workers=5)

        for i, url in enumerate(urls):
            # Create a progress bar for each URL
            progress_var = tk.DoubleVar()
            progress_bar = ttk.Progressbar(self.root, variable=progress_var, length=200, mode='determinate')
            progress_bar.grid(row=len(self.progress_bars) + 4, column=0, columnspan=3, padx=10, pady=5, sticky='ew')

            # Create a label for showing progress status text
            progress_label = ttk.Label(self.root, text="")
            progress_label.grid(row=len(self.progress_bars) + 3, column=0, columnspan=3)

            # Store the progress bar and label references
            self.progress_bars[url] = progress_var
            self.progress_labels[url] = progress_label

            # Submit the download task to the ThreadPoolExecutor
            self.thread_pool.submit(self.download_image, url.strip(), i)

        # Schedule checking the download queue
        self.root.after(100, self.check_download_queue)

    def check_download_queue(self):
        try:
            while True:
                message = self.download_queue.get_nowait()
                self.status_label.config(text=message)

        except queue.Empty:
            # Check if there are any running tasks in the ThreadPoolExecutor
            self.status_label.config(text="Download complete")
            self.urls_entry.config(state=tk.NORMAL)

    def pause_download(self):
        self.is_paused = True
        self.status_label.config(text="Download paused")
        self.style.configure('Paused.TButton', background='orange')  # Change color for paused state
        self.pause_button.configure(style='Paused.TButton')  # Apply new style
        self.style.configure('Resume.TButton', background='white')  # Reset color for resume button
        self.resume_button.configure(style='Resume.TButton')  # Apply new style

    def resume_download(self):
        self.is_paused = False
        self.status_label.config(text="Download resumed")
        self.style.configure('Resume.TButton', background='green')  # Change color for resume state
        self.resume_button.configure(style='Resume.TButton')  # Apply new style
        self.style.configure('Paused.TButton', background='white')  # Reset color for pause button
        self.pause_button.configure(style='Paused.TButton')  # Apply new style

    def cancel_download(self):
        self.is_cancelled = True
        self.status_label.config(text="Download cancelled")
        self.style.configure('Cancelled.TButton', background='red')  # Change color for cancelled state
        self.cancel_button.configure(style='Cancelled.TButton')  # Apply new style
        self.root.destroy()


if __name__ == "__main__":
    import queue

    root = tk.Tk()
    app = ImageDownloaderGUI(root)
    root.mainloop()

# https://images.pexels.com/photos/372490/pexels-photo-372490.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1```