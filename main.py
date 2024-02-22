from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from pytube import YouTube
from pytube.exceptions import PytubeError
from threading import Thread

class DownloadApp(App):
    def build(self):
        self.dark_mode = False
        self.progress = ProgressBar(max=100, size_hint_y=None, height=20)
        self.status_label = Label(text="", size_hint_y=None, height=40)
        self.url_input = TextInput(hint_text="Enter Video link:", foreground_color=[0, 0, 0, 1], size_hint_y=None, height=40)
        self.filename_input = TextInput(hint_text="Enter Filename:", foreground_color=[0, 0, 0, 1], size_hint_y=None, height=40)
        self.download_button = Button(text="Download", on_release=self.start_download, size_hint_y=None, height=40)
        self.stop_button = Button(text="Stop", on_release=self.stop_download, size_hint_y=None, height=40)
        self.mode_button = Button(text="Dark Mode", on_release=self.switch_mode, size_hint_y=None, height=40)
        self.title_label = Label(text="Youtube Video Downloader", size_hint_y=None, height=40, font_size=24, bold=True)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        with layout.canvas.before:
            self.color = Color(1, 1, 1, 1)  # white
            self.rect = Rectangle(size=Window.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        layout.add_widget(self.title_label)
        layout.add_widget(self.url_input)
        layout.add_widget(self.filename_input)
        layout.add_widget(self.download_button)
        layout.add_widget(self.stop_button)
        layout.add_widget(self.mode_button)
        layout.add_widget(self.status_label)
        layout.add_widget(self.progress)

        self.switch_mode(None)  # initialize to light mode

        return layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def switch_mode(self, instance):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.color.rgb = [0.2, 0.2, 0.2, 1]  # dark mode color
            self.mode_button.text = "Light Mode"
            self.status_label.color = [1, 1, 1, 1]  # white text
            self.url_input.foreground_color = [0, 0, 0, 1]  # black text
            self.filename_input.foreground_color = [0, 0, 0, 1]  # black text
            self.download_button.color = [0.57, 0.73, 0.84, 1]  # dark blue
            self.stop_button.color = [0.57, 0.73, 0.84, 1]  # dark blue
            self.title_label.color = [1, 1, 1, 1]  # white title
        else:
            self.color.rgb = [1, 1, 1, 1]  # white
            self.mode_button.text = "Dark Mode"
            self.status_label.color = [0, 0, 0, 1]  # black text
            self.url_input.foreground_color = [0, 0, 0, 1]  # black text
            self.filename_input.foreground_color = [0, 0, 0, 1]  # black text
            self.download_button.color = [0.57, 0.73, 0.84, 1]  # dark blue
            self.stop_button.color = [0.57, 0.73, 0.84, 1]  # dark blue
            self.title_label.color = [0, 0, 0, 1]  # black title

    def start_download(self, instance):
        Thread(target=self.download_video).start()

    def stop_download(self, instance):
        self.status_label.text = "Stopping download is not supported."

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        self.progress.value = percentage_of_completion

    def download_video(self):
        link = self.url_input.text
        filename = self.filename_input.text + '.mp4'
        try:
            self.status_label.text = "Download started..."
            youtube = YouTube(link, on_progress_callback=self.on_progress)
            stream = youtube.streams.get_highest_resolution()
            stream.download(output_path='./', filename=filename)
            self.status_label.text = "Download successful"
        except PytubeError as e:
            self.status_label.text = f"Error: {str(e)}"

if __name__ == "__main__":
    DownloadApp().run()
