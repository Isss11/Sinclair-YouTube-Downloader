from tkinter import *
from tkinter import ttk
from pytube import YouTube

"""
This program is created by Isaiah Sinclair with the use of tkinter and pytube.
"""

#This is the function for when the button is clicked (command callback)
def downloadVideo():
    link = (linkEntry.get()).rstrip() #takes any trailing spaces away

    yt = YouTube(link)

    ytStream = yt.streams.get_by_itag(22) #chooses a stream that is MP4 and I believe 720 p -- found this selection online

    ytStream.download() #specific directory where I want my videos downloaded to

#Main function below
root = Tk() #setting up the window and frame
root.title("YouTube Video Downloader")

frame = ttk.Frame(root)
frame['padding'] = 5
frame['borderwidth'] = 5
frame['relief'] = 'groove' #setting up how boundaries of frame looks
frame.grid(column=0, row=0, sticky=(N, W, E, S))


title = ttk.Label(frame, text = 'YouTube Video Downloader')
title.grid(row = 0)

#creating entry object
link = StringVar()
linkEntry = ttk.Entry(frame, textvariable=link, width= 50)
linkEntry.grid(row = 20)

#creating button
downloadButton = ttk.Button(frame, text='Download', command = downloadVideo)
downloadButton.grid(row = 20, column = 40)

root.mainloop()