from tkinter import *
from tkinter import ttk
from pytube import YouTube
from time import sleep

#NOTE this program was only created for recreational use, not for commercial purposes.

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

        yt = YouTube(link)

        ytStream = yt.streams.get_by_itag(22) #chooses a stream that is MP4 and I believe 720 p -- found this selection online

        ytStream.download()

        progressText.configure(text= "Your video has finished downloading!")
        frame.update()
    except: 
        progressText.configure(text= "Incorrect input! Make sure you are inputting a proper YouTube URL.")
        frame.update()

    sleep(2) #Added a little wait so this statement will be seen.
    downloadButton.state(['!disabled']) #Button is reinstated
    progressText.configure(text= "Input another YouTube video URL to download.")
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

#creating entry object
link = StringVar()
linkEntry = ttk.Entry(frame, textvariable=link, width= 50)
linkEntry.grid(row = 1)

#creating button
downloadButton = ttk.Button(frame, text='Download', command = downloadVideo)
downloadButton.grid(row = 1, column = 2)

#Creating progess label
progressText = ttk.Label(frame, text= "Input a YouTube video URL to download.")
progressText.grid(row = 3)

root.mainloop()