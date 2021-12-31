from tkinter import *
from tkinter import ttk
from pytube import YouTube
from time import sleep
import winsound

#NOTE this program was only created for recreational use, not for commercial purposes.
#NOTE sound effect: Music by Muzaproduction from Pixabay

"""
This program is created by Isaiah Sinclair with the use of tkinter and pytube.
"""

#This is the function for when the button is clicked (command callback)
def downloadVideo():
    try:
        downloadButton.state(['disabled']) #While the video is downloading, you cannot press the button again
        progressText.configure(text= "Video downloading. Sit tight!")
        frame.update()

        link = (linkEntry.get()).rstrip() #takes any trailing spaces away
            
        filePath = (filePathEntry.get()).rstrip()

        yt = YouTube(link)

        ytStream = yt.streams.get_by_itag(22) #chooses a stream that is MP4 and I believe 720 p -- found this selection online
    except: 
        progressText.configure(text= "Incorrect input! Make sure you are inputting a proper YouTube URL.")
        frame.update()
        winsound.MessageBeep(winsound.MB_ICONASTERISK)
        sleep(2)
        downloadButton.state(['!disabled']) #Button is reinstated
        return

    try:
        ytStream.download(filePath) #still downloads with an empty string -- just in the current working directory
    except: #I don't think this try/except statement is necessary (when an invalid entry is input, it just creates a new directory in the CWD), but I left it just in case.
        progressText.configure(text= "File path is wrong. Put in the format C:/Users/isaiah/Videos/Downloaded MLS Videos with forward slashes.")
        frame.update()
        winsound.MessageBeep(winsound.MB_ICONASTERISK)
        sleep(2)
        downloadButton.state(['!disabled']) #Button is reinstated
        return

    progressText.configure(text= "Your video has finished downloading!")
    frame.update()
    
    winsound.PlaySound("acoustic-guitar-logo-13084", winsound.SND_ALIAS)
    downloadButton.state(['!disabled']) #Button is reinstated
    progressText.configure(text= "Input a YouTube video URL to download above, and a file path below.")
    frame.update()
    


#Main function below
root = Tk() #setting up the window and frame
root.title("YouTube Video Downloader")

frame = ttk.Frame(root)
frame['padding'] = 5
frame['borderwidth'] = 5
frame['relief'] = 'groove' #setting up how boundaries of frame looks
frame.grid(column=0, row=0, sticky=(N, W, E, S))


title = ttk.Label(frame, text = 'Sinclair YouTube Downloader', font= 'Helvetica 14 bold')
title.grid(row = 0)

#creating entry object for the YouTube video link
link = StringVar()
linkEntry = ttk.Entry(frame, textvariable=link, width= 125)
linkEntry.grid(row = 1, sticky=(W, N)) #Want the entry object to stick to the left

#Creating entry object for the file path link, with a progress label
filePath = StringVar()
filePathEntry = ttk.Entry(frame, textvariable=filePath, width= 125)
filePathEntry.grid(row = 3, sticky=(W, N)) 

#creating button
downloadButton = ttk.Button(frame, text='Download', command = downloadVideo)
downloadButton.grid(row = 2, column = 3, ipadx=15, ipady= 10, padx = 10, sticky=S) #ipadx and ipady add pixels inside of the function

#Creating progess label
progressText = ttk.Label(frame, text= "Input a YouTube video URL to download above, and a file path (any invalid path puts the video in the current working directory) below.")
progressText.grid(row = 2)

root.mainloop()