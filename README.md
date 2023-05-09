# ytdl - YouTube Downloader
A YouTube Downloader program based on the pytube library. Has a well-developed CLI interface and a python module interface.

## Description
As a developer a normal user, you might come across situations where you need to download YouTube videos. Perhaps you need to extract audio from a video for a project, or you want to keep a backup of your favorite videos before they get taken down. Whatever the reason, downloading YouTube videos can be a tedious task, especially if you have to rely on web-based downloaders that may not always work.

That's where YTDL comes in. It is a lightweight Python module that provides a simple and reliable way to download YouTube videos. With YTDL, you can easily specify the quality of the video you want to download and even automate the process if needed. Best of all, YTDL is completely free and open-source, making it an ideal choice for hackers and normal users alike who want a lightweight and reliable solution for downloading YouTube videos.

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
If all the dependencies were installed correctly , this should show the details of the link and show further instructions to download
<p align="center">
<img src=https://user-images.githubusercontent.com/93914273/233820691-c6d9902d-e82f-4a90-987e-659b471c5ed1.png>
</p>

Choose the appropriate resolution and download location to proceed with the download. By default the video will be downloaded to the user's Downloads folder.
<p align="center">
<img src=https://user-images.githubusercontent.com/93914273/233820815-8806bc55-478a-4735-849a-afdf159c233f.png>
</p>

## Notes
- A FFmpeg binary (for windows and linux) is included in the package as a backup solution for situations where an existing FFmpeg installation is not available, but a system-wide installation is still recommended for optimal performance.
