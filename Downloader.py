
from tkinter import *
from tkinter import ttk
from pytube import YouTube
from time import sleep
import winsound
import os

class Downloader:
    def __init__(self, root):
        self.root = root

        self.root.title("YouTube Video Downloader")

        root.tk.call("source", "sun-valley.tcl")
        root.tk.call('set_theme', "dark")
        
        self.frame = ttk.Frame(root)
        self.frame['padding'] = 5
        self.frame['borderwidth'] = 5
        self.frame['relief'] = 'groove' #setting up how boundaries of frame looks

        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))

        self.drawProgram()
    #This is the function for when the button is clicked (command callback)
    def downloadVideo(self):
        self.downloadButton.state(['disabled']) #While the video is downloading, you cannot press the button again
        self.progressText.configure(text= "Video downloading. Sit tight!")
        self.frame.update()
                
        self.filePath = (self.filePathEntry.get()).rstrip()

        self.getStream() #Chooses the stream based on resolution, audio only variable, etc.
        
        self.outFile = self.ytStream.download(self.filePath) #still downloads with an empty string -- just in the current working directory

        if (self.audioOnly.get() == "audioOnly"):
            self.changeAudioFileExtension() #this will change the kind of file that is produced for the user

        self.progressText.configure(text= "Your video has finished downloading!")
        self.frame.update()
        
        winsound.MessageBeep() #Plays beep sound when video is downloaded
        self.downloadButton.state(['!disabled']) #Button is reinstated
        self.progressText.configure(text= "Input a YouTube video URL to download above, and a file path below.")
        self.frame.update()

        self.downloadButton.state(['disabled']) #disabling this button again in case the user changes the link of video input

    def drawProgram(self): #Just created this program so __init__ wasn't too cluttered
        self.title = ttk.Label(self.frame, text = 'Sinclair YouTube Downloader', font= 'Helvetica 14 bold')
        self.title.grid(row = 0, columnspan = 4)

        #creating entry object for the YouTube video link
        self.link = StringVar()
        self.linkEntry = ttk.Entry(self.frame, textvariable=self.link, width= 125)
        self.linkEntry.grid(row = 1, sticky=(W, N), columnspan=4) #Want the entry object to stick to the left

        #Creating entry object for the file path link, with a progress label
        self.filePath = StringVar()
        self.filePathEntry = ttk.Entry(self.frame, textvariable=self.filePath, width= 125)
        self.filePathEntry.grid(row = 3, column=0, sticky=(W, N), columnspan=4) 

        #creating stream finder button
        self.streamsButton = ttk.Button(self.frame, text="Find Streams", command= self.validateStreams)
        self.streamsButton.grid(row = 11, column = 3, ipadx=10, ipady= 10)

        #creating button
        self.downloadButton = ttk.Button(self.frame, text='Download', command = self.downloadVideo)
        self.downloadButton.state(['disabled'])
        self.downloadButton.grid(row = 12, column = 3, ipadx=10, ipady= 10) #ipadx and ipady add pixels inside of the function

        #Creating progess label
        self.progressText = ttk.Label(self.frame, text= "Input a YouTube video URL to download above, and a file path (any invalid path puts the video in the current working directory) below.")
        self.progressText.grid(row = 2, column=0, columnspan = 4)

        #Creating label indicating youtube video selections
        self.selectionsLabel = ttk.Label(self.frame, text="Select Download Options:", font= 'Helvetica 11 bold')
        self.selectionsLabel.grid(row = 4, columnspan=4, sticky=W)

        #Creating a label for the checkbutton created for audio only
        self.audioOnlyLabel = ttk.Label(self.frame, text="Audio/Video", font="helvetica 9 bold")
        self.audioOnlyLabel.grid(row = 5, column=0, sticky = W)

        #Creating checkButton to determien audio only as opposed to video
        self.audioOnly = StringVar(value="video")
        self.checkAudioOnly = ttk.Checkbutton(self.frame, text='Audio Only', variable= self.audioOnly, onvalue= 'audioOnly', offvalue= 'video', command = self.disableButtons)

        self.checkAudioOnly.grid(row=6, column=0, sticky=W)

        #Creating Label for resolution choices
        self.resolutionChoiceLabel = ttk.Label(self.frame, text="Resolution", font="helvetica 8 bold")
        self.resolutionChoiceLabel.grid(row=5, column = 1, sticky = W)

        #Creating Label for audio extension choices
        self.resolutionChoiceLabel = ttk.Label(self.frame, text="Audio Extension", font="helvetica 8 bold")
        self.resolutionChoiceLabel.grid(row=5, column = 2, sticky = W)

        #Creating radio button selections for each category for video download customization and disables proper buttons
        self.createResolutionChoices()
        self.createAudioDownloadOptions()
        self.disableButtons()

    def getStream(self):
        if (self.audioOnly.get() == "video"):
            self.ytStream = self.yt.streams.filter(progressive=True, res=self.resolutionType.get()).first() #chooses streams with given resolution and has to be progressive
        else:
            self.ytStream = self.yt.streams.filter(only_audio=True).first() #if audio only this happens

    def createResolutionChoices(self): #this was created to simplify the other widget drawing functions
        self.resolutionType = StringVar(value="720p")

        #Created the variable and assigned it by default to 720p - now creating the buttons

        self.resolutionType720 = ttk.Radiobutton(self.frame, text="720p", variable = self.resolutionType, value = "720p")
        self.resolutionType480 = ttk.Radiobutton(self.frame, text="480p", variable = self.resolutionType, value = "480p")
        self.resolutionType360 = ttk.Radiobutton(self.frame, text="360p", variable = self.resolutionType, value = "360p")
        self.resolutionType240 = ttk.Radiobutton(self.frame, text="240p", variable = self.resolutionType, value = "240p")
        self.resolutionType144 = ttk.Radiobutton(self.frame, text="144p", variable = self.resolutionType, value = "144p")

        self.resolutionRadioButtons = [self.resolutionType720, self.resolutionType480, self.resolutionType360, self.resolutionType240, self.resolutionType144]

        #stored the radiobuttons in a list to more modularly control them with drawing and such

        tempRowCounter = 6
        for i in (self.resolutionRadioButtons):
            i.grid(column = 1, row = tempRowCounter, sticky=W)
            tempRowCounter +=1

    def createAudioDownloadOptions(self):
        self.audioDownloadTypeExtension = StringVar(value=".mp3") #initial audio type is mp3

        self.audioTypeMP3 = ttk.Radiobutton(self.frame, text = "MP3", variable= self.audioDownloadTypeExtension, value = ".mp3")
        self.audioTypeMP4 = ttk.Radiobutton(self.frame, text = "MP4", variable= self.audioDownloadTypeExtension, value = ".mp4")
        self.audioTypeWAV = ttk.Radiobutton(self.frame, text = "WAV", variable= self.audioDownloadTypeExtension, value = ".wav")
        self.audioTypeAAC = ttk.Radiobutton(self.frame, text = "AAC", variable= self.audioDownloadTypeExtension, value = ".m4a") #Note how this is not saved as .aac

        self.audioDownloadRadioButtons = [self.audioTypeMP3, self.audioTypeMP4, self.audioTypeWAV, self.audioTypeAAC]

        tempRowCounter = 6
        for i in (self.audioDownloadRadioButtons):
            i.grid(column = 2, row = tempRowCounter, sticky=W)
            tempRowCounter +=1

    def disableButtons(self): #at the moment, this function disables/enables the resolution buttons and the audio download type buttons
        if (self.audioOnly.get() == "audioOnly"):
            for i in (self.resolutionRadioButtons):
                i.state(['disabled'])
            
            for i in (self.audioDownloadRadioButtons):
                i.state(['!disabled'])
        else:
            for i in (self.resolutionRadioButtons):
                i.state(['!disabled'])

            for i in (self.audioDownloadRadioButtons):
                i.state(['disabled'])

    def changeAudioFileExtension(self):
        # https://www.geeksforgeeks.org/download-video-in-mp3-format-using-pytube/
        base, ext = os.path.splitext(self.outFile) #renames the output file to an mp3
        new_file = base + self.audioDownloadTypeExtension.get()
        os.rename(self.outFile, new_file)

    def validateStreams(self): #this essentially determines if certain streams exist (and disables them if they don't)
        self.resetResolutionButtons() #renables all buttons so that only the invalid resolution options for the present video are disabled

        self.link = (self.linkEntry.get()).rstrip() #takes any trailing spaces away
        self.yt = YouTube(self.link)

        self.resolutionTypes = ["720p", "480p", "360p", "240p", "144p"]

        for i in range(len(self.resolutionTypes)): #the length of resolutionTypes should always be the same as the radioButtons one, so that shouldn't be an issue
            if (self.yt.streams.filter(progressive=True, res=self.resolutionTypes[i]).first() == None): #checks if there is a stream available for each resolution, and disables the radio button if so
                self.resolutionRadioButtons[i].state(["disabled"])
            else:
                self.resolutionType.set(self.resolutionTypes[i])

        self.downloadButton.state(["!disabled"])

    def resetResolutionButtons(self): #resets resolution buttons if any of them have been disabled
        for i in (self.resolutionRadioButtons):
            i.state(['!disabled'])
        