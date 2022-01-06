
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

        self.drawProgram()
    #This is the function for when the button is clicked (command callback)
    def downloadVideo(self):
        try:
            self.downloadButton.state(['disabled']) #While the video is downloading, you cannot press the button again
            self.progressText.configure(text= "Video downloading. Sit tight!")
            self.frame.update()

            self.link = (self.linkEntry.get()).rstrip() #takes any trailing spaces away
                
            self.filePath = (self.filePathEntry.get()).rstrip()

            self.yt = YouTube(self.link)

            self.getStream() #Chooses the stream based on resolution, audio only variable, etc.
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
            self.progressText.configure(text= "Either the file path, or the resolution choice is invalid (might not be available).")
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

    def drawProgram(self): #Just created this program so __init__ wasn't too cluttered
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

        #Creating label indicating youtube video selections
        self.selectionsLabel = ttk.Label(self.frame, text="Select Download Options:", font= 'Helvetica 11 bold')
        self.selectionsLabel.grid(row = 4, column= 0, sticky="W", pady= 5)

        #Creating checkButton to determien audio only as opposed to video
        self.audioOnly = StringVar(value="video")
        self.checkAudioOnly = ttk.Checkbutton(self.frame, text='Audio Only', variable= self.audioOnly, onvalue= 'audioOnly', offvalue= 'video', command=self.updateVideoOptions)

        self.checkAudioOnly.grid(row=5, column=0, sticky="W")

        self.updateVideoOptions() #Adds video options

    def getStream(self):
        if (self.audioOnly == "video"):
            self.ytStream = self.yt.streams.filter(progressive=True, res=self.resolutionType.get()).first() #chooses streams with given resolution and has to be progressive
        else:
            self.ytStream = self.yt.streams.filter(only_audio=True, file_extension="mp4").first() #if audio only this happens

    def updateVideoOptions(self):
        if (self.audioOnly.get() == "video"):
            self.resolutionType = StringVar(value="720p")

            self.resolutionType144 = ttk.Radiobutton(self.frame, text="144p", variable=self.resolutionType, value= "144p")
            self.resolutionType240 = ttk.Radiobutton(self.frame, text="240p", variable=self.resolutionType, value= "240p")
            self.resolutionType360 = ttk.Radiobutton(self.frame, text="360p", variable=self.resolutionType, value= "360p")
            self.resolutionType480 = ttk.Radiobutton(self.frame, text="480p", variable=self.resolutionType, value= "480p")
            self.resolutionType720 = ttk.Radiobutton(self.frame, text="720p", variable=self.resolutionType, value= "720p")

            self.resolutionRadioButtons = [self.resolutionType144, self.resolutionType240, self.resolutionType360, self.resolutionType480, self.resolutionType720]

            self.radioButtonUpdate = 6
            for i in (self.resolutionRadioButtons):
                i.grid(row= self.radioButtonUpdate, column = 0, sticky="W")
                self.radioButtonUpdate = self.radioButtonUpdate + 1

            self.radioButtonUpdate = 6
        else:
            for i in (self.resolutionRadioButtons):
                i.destroy()

            self.radioButtonUpdate = 6