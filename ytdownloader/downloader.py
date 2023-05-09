from colorama import Fore, Back, Style, init
import pytube
import subprocess
from time import sleep
import sys
from ffmpeg_progress_yield import FfmpegProgress
import shutil
import datetime
import json
import os
from colorama import Fore, Back, Style, init
from tempfile import TemporaryDirectory
import requests


class YoutubeDownloaderException(Exception):
    """Custom exception class."""

    def __init__(self, message="An error occurred."):
        self.message = 'ERROR : ' + message
        super().__init__(self.message)


class YoutubeDownloader:
    '''Youtube Downloader Class'''

    def __init__(self, url, apptype="API", verbose=False):
        '''
        Initialize the class
        arguments ::
        url : Youtube URL
        app_type : CLI or API or RESPONSE
        verbose : True or False
        '''

        self.url = url
        self.Error = YoutubeDownloaderException
        self.verbose = verbose
        self.vprint = print if self.verbose else lambda *a, **k: None

        self.setup()
        self.current = ""  # VO = Video Only, A = Audio, V = Video, F = ffmpeg
        # CLI = Command Line Interface (for pretty interface), API = Application Programming Interface (for module use), RESPONSE = Response Output (for program interface)
        self.apptype = apptype

    def assign_ffmpeg(self):
        '''Assign ffmpeg binary'''
        try:
            subprocess.call(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        except Exception as e:
            self.vprint("FFMPEG not found. Using backup binaries...")
            if sys.platform == "win32":
                binary = ("win","ffmpeg.exe")
            elif sys.platform == "linux":
                binary = ("linux","ffmpeg")
            
            elif sys.platform == "darwin":
                binary = ("mac","ffmpeg")
            
            self.vprint('Using binary at '+os.path.join(os.path.dirname(
                os.path.realpath(__file__)), 'ffmpeg_binaries', binary[0], binary[1]))
            self.ffmpeg_bin = os.path.join(os.path.dirname(
                os.path.realpath(__file__)), 'ffmpeg_binaries', binary[0], binary[1])
            try:
                subprocess.call([self.ffmpeg_bin, "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            except FileNotFoundError:
                raise self.Error("FFMPEG binary not found. Please download the appropriate binary from the github page.\nhttps://github.com/Tanay-Kar/ytdl")        
        else:
            self.ffmpeg_bin = "ffmpeg"

    def create_temp(self):
        '''Create a temp folder'''
        cwd = os.getcwd()
        try:
            os.mkdir(os.path.join(cwd, "temp"))
        except FileExistsError:
            self.temp_dir = os.path.join(cwd, "temp")
            self.clear_temp()
            os.mkdir(os.path.join(cwd, "temp"))

        dir = os.path.join(cwd, "temp")
        return dir

    def check_args(self):
        '''Checking validity of arguments'''
        if self.apptype not in ["CLI", "API", "RESPONSE"]:
            raise self.Error("Invalid app_type")

        if self.apptype == "API" and self.verbose:
            self.verbose = False
            # verbose is not supported in API mode
        if self.apptype == "RESPONSE" and self.verbose:
            self.vprint("Warning : verbose mode is enabled.")

    def setup(self):
        '''Setup the class'''
        self.vprint("Temp Folder : CLEARED")
        # One-Liner to Check Internet Connection:
        isinternet = True if requests.get(
            "https://www.youtube.com").status_code else False
        if not isinternet:
            raise self.Error("No Internet Connection")

        self.vprint("Internet Connection : OK")

        try:
            self.yt = pytube.YouTube(self.url)

            self.vprint("Youtube Connection : OK")

        except pytube.exceptions.PytubeError as e:
            raise self.Error(f'Internal Error .\n{e}')

        self.yt.register_on_progress_callback(self.on_ytprogress)

        self.temp_dir = self.create_temp()
        self.vprint("Temp Folder : CREATED")
        self.get_details()

    def clear_temp(self):
        '''Clear the temp folder'''

        try:
            shutil.rmtree(self.temp_dir)
        except AttributeError:
            raise self.Error('Error clearing temp')

    def timeformat(self, s):
        '''Format the time'''
        time = datetime.timedelta(seconds=s)
        days, seconds = time.days, time.seconds
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        time_parts = []
        if days:
            time_parts.append(f"{days} days")
        if hours:
            time_parts.append(f"{hours} hrs")
        if minutes:
            time_parts.append(f"{minutes} min")
        if seconds:
            time_parts.append(f"{seconds} sec")

        return ", ".join(time_parts)

    def move_file(self, dest, ext="mp4"):
        '''Move the file to the destination'''
        name = "".join(x for x in self.title if x.isalnum())

        try:
            shutil.move(f"{self.temp_dir}/output.mp4", dest+f'/{name}.{ext}')
            self.vprint("File Moved : OK")
        except Exception as e:
            raise self.Error(f'Internal Error .\n{e}')

    def show_progress(self, _percent):
        '''Show the progress'''
        if self.current == "VO":
            percent = float(f'{round(_percent*70,1)}')
        elif self.current == "A":
            percent = float(f'{round(_percent*15,1)}')
        elif self.current == "V":
            percent = float(f'{round((_percent*55)+15,1)}')
        elif self.current == "F":
            percent = float(f'{round(((_percent)*30)+70,1)}')

        # print(f'{percent}%')
        if self.apptype == "CLI" and not self.verbose:
            cols = shutil.get_terminal_size().columns

            progress_width = cols - 17  # Adjust as needed

            # Calculate the number of filled blocks in the progress bar
            filled_blocks = int(percent / 100 * progress_width)

            # Calculate the number of empty blocks in the progress bar
            empty_blocks = progress_width - filled_blocks
            label = "Downloading Audio ..." if self.current == "A" else (
                "Downloading Video ..." if self.current == "V" or self.current == "VO" else "Converting ...       ")
            # Print the progress bar
            print(Style.BRIGHT + f"\n{label}\n\n" + Style.RESET_ALL, end='\r')
            print(
                Fore.WHITE + Back.BLUE + Style.BRIGHT + f'\nProgress: {(3 - len(str(int(percent)))) * " "}{int(percent)}%' + Style.RESET_ALL + Back.RESET + f'|{"▇" * filled_blocks}{" " * empty_blocks}|\n\033[F\033[F\033[F\033[F\033[F', end='\r')

        elif self.apptype == "RESPONSE":
            return (f'{percent}%')
        elif self.apptype == "API" or self.verbose:
            pass

    def on_ytprogress(self, stream, _chunk, bytes_remaining):
        '''Callback function for youtube progress'''
        current = ((stream.filesize - bytes_remaining)/stream.filesize)
        self.show_progress(current)

    def get_details(self):
        '''
        Get the details of the video
        returns tuple : (url,title,channel,duration,thumbnail,res_list)
        '''
        i = 0
        while True:
            if i <= 15:
                try:
                    self.title = self.yt.title
                    self.vprint("Title : OK")
                    break
                except:
                    # Failed to get name. Retrying...
                    self.vprint("Title : Failed ... Retrying ...")
                    i += 1
                    sleep(0.5)
                    self.yt = pytube.YouTube(self.url)
                    self.yt.register_on_progress_callback(self.on_ytprogress)
                    continue
            else:
                raise self.Error("Failed to get title\nTry again later ...")

        self.channel = self.yt.author
        self.duration = self.timeformat(self.yt.length)
        self.thumbnail = self.yt.thumbnail_url
        i = 0
        while True:
            if i <= 15:
                try:
                    self.res_list = self.get_resolutions()
                    self.vprint("Resolutions : Querying ...")
                except Exception:
                    # Failed to get resolution. Retrying...
                    self.vprint("Resolutions : Failed ... Retrying ...")
                    i += 1
                    sleep(1)
                    continue
                else:
                    self.vprint("Resolutions : OK")
                    break
            else:
                raise self.Error(
                    "Failed to get resolutions\nTry again later ...")
        self.vprint("Details : OK")
        return (self.url, self.title, self.channel, self.duration, self.thumbnail, self.res_list)

    def get_resolutions(self) -> list:
        '''
        Get the resolutions of the video
        returns list : [resolutions]
        '''
        st_list = self.yt.streams.filter().order_by('resolution').desc()

        org_list, new_list = [i.resolution for i in st_list], []
        for i in org_list:
            if i not in new_list:
                new_list.append(i)
        self.res_list = new_list
        return self.res_list

    def download(self, resolution, location=None):
        '''
        Download the video
        arguments ::
        resolution : resolution of the video
        location : location to save the video (default : temp)
        '''
        self.assign_ffmpeg()

        if resolution in self.res_list:

            # print("With Audio" if self.yt.streams.filter(resolution=resolution).first().is_progressive else "Without Audio")

            if self.yt.streams.filter(resolution=resolution).first().is_adaptive:
                # ADAPTIVE STREAM - audio and video in seperate file
                self.vprint("Adaptive Stream")
                self.vprint("Resolution chosen : " + resolution)
                # AUDIO STREAM
                aud_stream = self.yt.streams.filter(
                    only_audio=True
                ).first()
                self.vprint("Audio Stream : OK")
                # VIDEO STREAM
                vid_stream = self.yt.streams.filter(
                    resolution=resolution,
                    adaptive=True
                ).first()
                self.vprint("Video Stream : OK")
                ext = vid_stream.mime_type.split("/")[1]

                # AUDIO DOWNLOAD
                self.current = "A"
                aud_stream.download(
                    filename=f"{self.temp_dir}/audio.{aud_stream.mime_type.split('/')[1]}")

                self.vprint("Audio Download : OK")

                # VIDEO DOWNLOAD
                self.current = "V"
                vid_stream.download(
                    filename=f"{self.temp_dir}/video.{ext}")

                self.vprint("Video Download : OK")
                # PROCESSING
                # check if ffmpeg is installed
                # ffmpeg is installed
                self.vprint("ffmpeg : INSTALLED")
                self.current = "F"
                cmd = [self.ffmpeg_bin, "-i", f"{self.temp_dir}/video.{ext}", "-i",
                       f"{self.temp_dir}/audio.{aud_stream.mime_type.split('/')[1]}", "-c", "copy", "-y", f"{self.temp_dir}/output.mp4"]
                ff = FfmpegProgress(cmd)
                self.vprint("ffmpeg : STARTED")
                try:
                    for progress in ff.run_command_with_progress():
                        self.show_progress(progress/100)
                    self.vprint("ffmpeg : DONE")
                    if location != None:
                        self.move_file(location)
                        self.vprint("File Moved : OK")
                    else:
                        self.move_file(os.path.join(
                            (os.path.expanduser("~")), "Downloads"))
                        self.vprint("File Moved : OK")
                except KeyboardInterrupt:
                    raise self.Error("Process interrupted by user.")
                except RuntimeError:
                    raise self.Error(
                        "An error occurred while processing the video.")

            else:
                # PROGRESSIVE STREAM - audio and video in same file

                # VIDEO STREAM
                vid_stream = self.yt.streams.filter(
                    resolution=resolution, progressive=True
                ).first()
                self.vprint("Video Stream : OK")

                ext = vid_stream.mime_type.split("/")[1]

                self.current = "VO"

                # VIDEO DOWNLOAD
                vid_stream.download(filename=f"{self.temp_dir}/video.{ext}")
                self.vprint("Video Download : OK")

                # check if ffmpeg is installed
                self.vprint("ffmpeg : INSTALLED")
                self.current = "F"
                cmd = [
                    self.ffmpeg_bin, "-i", f"{self.temp_dir}/video.{ext}", "-c", "copy", "-y", f"{self.temp_dir}/output.mp4"]
                ff = FfmpegProgress(cmd)
                self.vprint("ffmpeg : STARTED")
                try:
                    for progress in ff.run_command_with_progress():
                        self.show_progress(progress/100)
                    self.vprint("ffmpeg : DONE")
                    if location != None:
                        self.move_file(location)
                        self.vprint("File Moved : OK")

                    else:
                        self.move_file(os.path.join(
                            (os.path.expanduser("~")), "Downloads"))
                        self.vprint("File Moved : OK")

                except KeyboardInterrupt:
                    raise self.Error("Process interrupted by user.")
                except RuntimeError:
                    raise self.Error(
                        "An error occurred while processing the video.")

            self.clear_temp()
        else:
            raise self.Error("Invalid resolution selected.")
