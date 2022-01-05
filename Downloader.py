
from tkinter import *
from tkinter import ttk
from pytube import YouTube
from time import sleep
import winsound

class Downloader:
    def __init__(self, root):
        self.root = root

        self.root.title("YouTube Video Downloader")

        self.frame = ttk.Frame(root)
        self.frame['padding'] = 5
        self.frame['borderwidth'] = 5
        self.frame['relief'] = 'groove' #setting up how boundaries of frame looks
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))


        self.title = ttk.Label(self.frame, text = 'Sinclair YouTube Downloader', font= 'Helvetica 14 bold')
        self.title.grid(row = 0)

        #creating entry object for the YouTube video link
        self.link = StringVar()
        self.linkEntry = ttk.Entry(self.frame, textvariable=self.link, width= 125)
        self.linkEntry.grid(row = 1, sticky=(W, N)) #Want the entry object to stick to the left

        #Creating entry object for the file path link, with a progress label
        self.filePath = StringVar()
        self.filePathEntry = ttk.Entry(self.frame, textvariable=self.filePath, width= 125)
        self.filePathEntry.grid(row = 3, sticky=(W, N)) 

        #creating button
        self.downloadButton = ttk.Button(self.frame, text='Download', command = self.downloadVideo)
        self.downloadButton.grid(row = 2, column = 3, ipadx=15, ipady= 10, padx = 10, sticky=S) #ipadx and ipady add pixels inside of the function

        #Creating progess label
        self.progressText = ttk.Label(self.frame, text= "Input a YouTube video URL to download above, and a file path (any invalid path puts the video in the current working directory) below.")
        self.progressText.grid(row = 2)

    #This is the function for when the button is clicked (command callback)
    def downloadVideo(self):
        try:
            self.downloadButton.state(['disabled']) #While the video is downloading, you cannot press the button again
            self.progressText.configure(text= "Video downloading. Sit tight!")
            self.frame.update()

            self.link = (self.linkEntry.get()).rstrip() #takes any trailing spaces away
                
            self.filePath = (self.filePathEntry.get()).rstrip()

            self.yt = YouTube(self.link)

            self.ytStream = self.yt.streams.get_by_itag(22) #chooses a stream that is MP4 and I believe 720 p -- found this selection online
        except: 
            self.progressText.configure(text= "Incorrect input! Make sure you are inputting a proper YouTube URL.")
            self.frame.update()
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
            sleep(2)
            self.downloadButton.state(['!disabled']) #Button is reinstated
            return

        try:
            self.ytStream.download(self.filePath) #still downloads with an empty string -- just in the current working directory
        except: #I don't think this try/except statement is necessary (when an invalid entry is input, it just creates a new directory in the CWD), but I left it just in case.
            self.progressText.configure(text= "File path is wrong. Put in the format C:/Users/isaiah/Videos/Downloaded MLS Videos with forward slashes.")
            self.frame.update()
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
            sleep(2)
            self.downloadButton.state(['!disabled']) #Button is reinstated
            return

        self.progressText.configure(text= "Your video has finished downloading!")
        self.frame.update()
        
        winsound.MessageBeep() #Plays beep sound when video is downloaded
        self.downloadButton.state(['!disabled']) #Button is reinstated
        self.progressText.configure(text= "Input a YouTube video URL to download above, and a file path below.")
        self.frame.update()