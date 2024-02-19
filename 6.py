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

        self.start_button = ttk.Button(root, text="Start Download", command=self.start_download)
        self.start_button.grid(row=1, column=0, padx=10, pady=10)

        self.pause_button = ttk.Button(root, text="Pause Download", command=self.pause_download)
        self.pause_button.grid(row=1, column=1, padx=10, pady=10)

        self.resume_button = ttk.Button(root, text="Resume Download", command=self.resume_download)
        self.resume_button.grid(row=1, column=2, padx=10, pady=10)

        self.cancel_button = ttk.Button(root, text="Cancel Download", command=self.cancel_download)
        self.cancel_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.status_label = ttk.Label(root, text="")
        self.status_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.download_path = os.getcwd()+'/images'
        self.download_queue = queue.Queue()
        self.thread_pool = None  # ThreadPoolExecutor instance
        self.is_paused = False
        self.is_cancelled = False
        self.lock = threading.Lock()


        # Dictionary to store progress bars for each URL
        self.progress_bars = {}

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
                        time.sleep(10)

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

        for i,url in enumerate(urls):
            # Create a progress bar for each URL
            progress_var = tk.DoubleVar()
            progress_bar = ttk.Progressbar(self.root, variable=progress_var, length=200, mode='determinate')
            progress_bar.grid(row=len(self.progress_bars) + 4, column=0, columnspan=3, padx=10, pady=5, sticky='ew')

            self.progress_bars[url] = progress_var

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

    def resume_download(self):
        self.is_paused = False
        self.status_label.config(text="Download resumed")

    def cancel_download(self):
        self.is_cancelled = True
        self.status_label.config(text="Download cancelled")
        self.urls_entry.config(state=tk.NORMAL)

        # Remove downloaded images
        # for filename in os.listdir(self.download_path):
        #     file_path = os.path.join(self.download_path, filename)
        #     try:
        #         if os.path.isfile(file_path) and (filename.endswith('.jpg') or filename.endswith('.png')):
        #             os.unlink(file_path)
        #     except Exception as e:
        #         print(f"Error deleting {file_path}: {e}")
        # Close the application window
        self.root.destroy()


if __name__ == "__main__":
    import queue

    root = tk.Tk()
    app = ImageDownloaderGUI(root)
    root.mainloop()
# https://images.pexels.com/photos/372490/pexels-photo-372490.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1```