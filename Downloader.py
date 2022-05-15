from tkinter import *
from tkinter import ttk
from pytube import YouTube
from time import sleep
import winsound
import os
from tkinter import filedialog
from threading import *

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

    #This is the function that does the threading part for the download video function, so we don't get issues with the tkinter screen updates
    #Source: https://www.geeksforgeeks.org/how-to-use-thread-in-tkinter-python/
    def downloadVideoThreading(self):
        #call download video function
        t1 = Thread(target=self.downloadVideo)
        t1.start()

    #This is the function for when the button is clicked (command callback)
    def downloadVideo(self):
        self.downloadButton.state(['disabled']) #While the video is downloading, you cannot press the button again
        self.progressText.configure(text= "Video downloading. Sit tight!")
        self.frame.update()

        self.getStream() #Chooses the stream based on resolution, audio only variable, etc.
        
        self.outFile = self.ytStream.download(self.filePath) #still downloads with an empty string -- just in the current working directory

        if (self.audioOnly.get() == "audioOnly"):
            self.changeAudioFileExtension() #this will change the kind of file that is produced for the user

        self.progressText.configure(text= "Your video has finished downloading!")
        self.frame.update()
        
        winsound.MessageBeep() #Plays beep sound when video is downloaded
        self.downloadButton.state(['!disabled']) #Button is reinstated
        self.progressText.configure(text= "Input a YouTube video URL to download above.")
        self.frame.update()

        self.disableInputs() #disabling these buttons again in case the user changes the link of video input

    def drawProgram(self): #Just created this program so __init__ wasn't too cluttered
        self.title = ttk.Label(self.frame, text = 'Sinclair YouTube Downloader', font= 'Helvetica 14 bold')
        self.title.grid(row = 0, columnspan = 4, pady=(0, 10))

        #creating entry object for the YouTube video link
        self.link = StringVar()
        self.linkEntry = ttk.Entry(self.frame, textvariable=self.link, width= 125)
        self.linkEntry.grid(row = 1, sticky=(W, N), columnspan=4) #Want the entry object to stick to the left

        #creating stream finder button
        self.streamsButton = ttk.Button(self.frame, text="Find Streams", command= self.validateStreams)
        self.streamsButton.grid(row = 10, column = 1, sticky=W)

        #creating button
        self.downloadButton = ttk.Button(self.frame, text='Download', command = self.downloadVideoThreading, style="Accent.TButton")
        self.downloadButton.grid(row = 10, column = 2, sticky=W) #ipadx and ipady add pixels inside of the function

        #Creating progess label
        self.progressText = ttk.Label(self.frame, text= "Input a YouTube video URL to download above, and a folder to download your files to.")
        self.progressText.grid(row = 2, column=0, columnspan = 4, pady=10)


        #Creating a label for the checkbutton created for audio only
        self.audioOnlyLabel = ttk.Label(self.frame, text="Audio/Video", font="helvetica 9 bold")
        self.audioOnlyLabel.grid(row = 3, column=0, sticky = W)

        #Creating checkButton to determien audio only as opposed to video
        self.audioOnly = StringVar(value="video")
        self.checkAudioOnly = ttk.Checkbutton(self.frame, text='Audio Only', variable= self.audioOnly, onvalue= 'audioOnly', offvalue= 'video', command = self.adjustButtons)

        self.checkAudioOnly.grid(row=4, column=0, sticky=W)

        #Creating Label for resolution choices
        self.resolutionChoiceLabel = ttk.Label(self.frame, text="Resolution", font="helvetica 8 bold")
        self.resolutionChoiceLabel.grid(row=3, column = 1, sticky = W)

        #Creating Label for audio extension choices
        self.resolutionChoiceLabel = ttk.Label(self.frame, text="Audio Extension", font="helvetica 8 bold")
        self.resolutionChoiceLabel.grid(row=3, column = 2, sticky = W)

        #Creating radio button selections for each category for video download customization and disables proper buttons
        self.createResolutionChoices()
        self.createAudioDownloadOptions()
        self.disableInputs()

        #Create file path putton
        self.filePath = StringVar()
        self.filePath = os.getcwd() #default file path is present working directory
        self.filePathButton = ttk.Button(self.frame, text = "Choose Download Folder", command=self.determineFilePath)
        self.filePathButton.grid(row = 10, column = 0, sticky=W)

    def getStream(self):
        if (self.audioOnly.get() == "video"):
            self.ytStream = self.yt.streams.filter(progressive=True, res=self.resolutionType.get(), file_extension="mp4").first() #chooses streams with given resolution and has to be progressive
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
        self.resolutionTypes = ["720p", "480p", "360p", "240p", "144p"]

        #stored the radiobuttons in a list to more modularly control them with drawing and such

        tempRowCounter = 4
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

        tempRowCounter = 4
        for i in (self.audioDownloadRadioButtons):
            i.grid(column = 2, row = tempRowCounter, sticky=W)
            tempRowCounter +=1

    def adjustButtons(self): #at the moment, this function disables/enables the resolution buttons and the audio download type buttons
        if (self.audioOnly.get() == "audioOnly"):
            for i in (self.resolutionRadioButtons):
                i.state(['disabled'])
            
            for i in (self.audioDownloadRadioButtons):
                i.state(['!disabled'])
        else:
            self.enableStreamButtons() #had to create a custom option for this so that invalid stream buttons don't show up

            for i in (self.audioDownloadRadioButtons):
                i.state(['disabled'])

    def changeAudioFileExtension(self):
        # https://www.geeksforgeeks.org/download-video-in-mp3-format-using-pytube/
        base, ext = os.path.splitext(self.outFile) #renames the output file to an mp3
        new_file = base + self.audioDownloadTypeExtension.get()
        os.rename(self.outFile, new_file)

    def validateStreams(self): #this essentially determines if certain streams exist and stores them in a list, to then enable their buttons
        self.link = (self.linkEntry.get()).rstrip() #takes any trailing spaces away
        self.yt = YouTube(self.link)

        self.validStreamButtons = []

        for i in range(len(self.resolutionTypes)):
            if (self.yt.streams.filter(progressive=True, res=self.resolutionTypes[i], file_extension="mp4").first() != None):
                self.validStreamButtons.append(self.resolutionRadioButtons[i])
                self.resolutionType.set(self.resolutionTypes[i])

        self.enableStreamButtons()
        self.checkAudioOnly.state(["!disabled"])
        self.downloadButton.state(["!disabled"])

    def disableInputs(self): #this disable all the input buttons
        for i in (self.resolutionRadioButtons):
            i.state(["disabled"])

        for i in (self.audioDownloadRadioButtons):
            i.state(["disabled"])

        self.downloadButton.state(["disabled"])
        self.checkAudioOnly.state(["disabled"])

    def enableStreamButtons(self):
        for i in (self.validStreamButtons):
            i.state(["!disabled"])

    # https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/
    def determineFilePath(self):
        self.filePath = str(filedialog.askdirectory())