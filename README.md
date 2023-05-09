# ytdl - YouTube Downloader
A YouTube Downloader program based on the pytube library. Has a well-developed CLI interface and a python module interface.

## Description
Be a developer or an average household, you might come across situations where you need to download YouTube videos. Perhaps you need to extract audio from a video for a project, or you want to keep a backup of your favorite videos to enjoy them offline. However, this seemingly easy task of downloading youtube videos isn't all that simple. On the contrary , an average user has to rely on sketchy websites which take forever to work, or download unwanted software for this.

That's where YTDL comes in. It is a lightweight Python module that provides a simple and reliable way to download YouTube videos. With YTDL, you can easily specify the quality of the video you want to download and even automate the process if needed. Best of all, YTDL is completely free and open-source (FOSS), making it an ideal choice for hackers and normal users alike who want a lightweight and reliable solution for downloading YouTube videos.

## Features
- Ability to download DASH and Progressive streams
- Ability to extract all required information from the link
- Well developed CLI interface for both user utility and back-end use
- Well developed module interface for use internally by python programs.

## Installation
### Requirements
- ffmpeg [see this](#notes)
- git (for installation of dependencies)

#### Windows
- Install git from https://git-scm.com/download/win
- Install ffmpeg from https://ffmpeg.org/download.html#build-windows
- Clone this repository
```bash
git clone https://github.com/Tanay-Kar/ytdl.git
```
- Navigate to the directory
```bash
cd ytdl/
```
- Install the requirements
```bash
pip install -r requirements.txt
```

#### Linux
- Use the appropriate package manager to install 
```bash
sudo apt install git ffmpeg
```
- Clone this repository
```bash
git clone https://github.com/Tanay-Kar/ytdl.git
```
- Navigate to the directory
```bash
cd ytdl/
```
- Install the requirements
```bash
pip install -r requirements.txt
```

## Quick start with CLI
Staying in the directory , run
```python ytdl.py <URL>```
for example
```bash
python ytdl.py https://www.youtube.com/watch?v=lJvRohYSrZM
```
If all the dependencies were installed correctly , this should show the details of the link [*](#notes) and show further instructions to download
<p align="center">
<img src=https://user-images.githubusercontent.com/93914273/233820691-c6d9902d-e82f-4a90-987e-659b471c5ed1.png>
</p>

Choose the appropriate resolution and download location to proceed with the download. By default the video will be downloaded to the user's Downloads folder.
<p align="center">
<img src=https://user-images.githubusercontent.com/93914273/233820815-8806bc55-478a-4735-849a-afdf159c233f.png>
</p>

## Quick start with use as a module
This module can also be used as an importable python package. 
Firstly, you have to copy the ```ytdownloader``` folder to your project directory. Then, you can import the package as follows
```python
from ytdownloader import YoutubeDownloader
```
Then, you can download a video as follows.


```python
url = "https://www.youtube.com/watch?v=lJvRohYSrZM"

# Initialize the class with the URL
ytdl = YoutubeDownloader(url)

# Get the resolutions
res_list = ytdl.get_resolutions()

# Download the video in highest resolution in user's downloads folder
try:
    ytdl.download(res_list[0])
except Exception as e:
    print(e)
```
## Notes
- The code is designed such that the user has the option to add a portable ffmpeg binary for his/her operating system in a specified directory(Check the release page for instructions). The appropriate binary can be downloaded from the release page of this repository, and are obtained from the official website. However, it is always recomended to have a system-wide installation of ffmpeg

- Youtube is notoriously famous for changing its internal api. As a result, sometimes pytube might fail to show the details and consequently fail. If the program fails despite your  youtube link being correct , feel free to notify me in the [issues](https://github.com/Tanay-Kar/ytdl/issues) page of this repository.

- I have tested this program on windows platforms (Win11) and on linux platforms(Ubuntu and Manjaro). For helping me with testing on Mac os, contact me on contact.tanaykar@gmail.com.