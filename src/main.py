import customtkinter as ctk
import pytube
import requests
import os
import threading


class App(ctk.CTk):
    title_font = ("Arial", 55)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("YTPy")
        self.geometry("500x500")

        # Title
        self.title_label = ctk.CTkLabel(self, text="YTPy", font=self.title_font)
        self.title_label.pack(pady=30)
        # Url entry bar
        self.url_string = ctk.StringVar()
        self.url_entry = ctk.CTkEntry(self, placeholder_text="URL", width=400, textvariable=self.url_string)
        self.url_entry.pack(pady=30)
        # Select Option
        self.option_chosen = ctk.StringVar()
        self.options_box = ctk.CTkComboBox(self, state="readonly", values=["Video", "Audio"], variable=self.option_chosen)
        self.options_box.pack()
        # Download button
        self.download_button = ctk.CTkButton(self, text="Download", command=self.start_download)
        self.download_button.pack(pady=30)
        # Status label
        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack()

    def check_video_url(self, url):
        request = requests.get(url)
        return "Video unavailable" not in request.text

    # TODO Refactor this into multiple functions

    def start_download(self):
        threading.Thread(target=self.download).start()

    def download(self):
        download_path = "../downloads"
        url = self.url_string.get()
        if url == '':
            self.status_label.configure(text="You may not leave the URL empty!")
            return
        download_type = self.option_chosen.get()
        is_url_valid = self.check_video_url(url)
        if not is_url_valid:
            self.status_label.configure(text="URl is not valid! Check your link and try again!")
            return

        self.status_label.configure(text="Downloading video..")

        yt = pytube.YouTube(url)

        if download_type == "Video":
            file_type = "mp4"
        elif download_type == "Audio":
            file_type = "mp3"
        else:
            self.status_label.configure(text="You need to select a format!")
            return

        video_name = yt.streams[0].title
        try:
            if file_type == "mp3":
                # TODO Make is so it actually re-encodes the file with ffmpeg
                out_file = yt.streams.first().download(download_path)
                base, ext = os.path.splitext(out_file)
                audio_file = base + ".mp3"
                os.rename(out_file, audio_file)
            else:
                yt.streams.filter(file_extension=file_type).first().download(download_path)
        except:
            print("There was an error")

        self.status_label.configure(text=f"Download complete! {download_path}/{video_name}.{file_type}")


if __name__ == '__main__':
    app = App()
    app.mainloop()
