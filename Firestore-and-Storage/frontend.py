#!/usr/bin/env python3
from backend import Backend as backend
import streamlit as st
from PIL import Image
import os

## constants

imageFormats = ["png", "jpg", "jpeg"]
videoFormats = ["mp4", "avi"]
oldestDateTime = "1/12/2021 00:00:00"

## widgets

st.title('TokTik')
st.write("Welcome to TokTik, your fake TikTok app!")

POSTHEADER = st.empty()
UPLOADER = st.empty()
POSTMSG = st.empty()
PREVIEW = st.empty()
SENDBUTTON = st.empty()

FEEDHEADER = st.empty()
NEXTBUTTON = st.empty()
FEEDMSG = st.empty()
FEED = st.empty()



# Posting Interface

## states
if 'uploadedFileType' not in st.session_state:
    st.session_state.uploadedFileType = ""

## functions
def showUploader():
    with UPLOADER.form("Uploader", clear_on_submit=True):
        media = st.file_uploader("Upload an image or a video",
            imageFormats + videoFormats)
        wantPreviewPost = st.form_submit_button("Preview")
        if wantPreviewPost:
            saveUploadedFile(media)

def saveUploadedFile(file):
    # if no uploaded file, clear cache
    if file == None:
        removeSavedUpload()
        POSTMSG.warning("You have removed your uploaded file")
        return
    # saving operations
    ext = file.name.split(".")[-1]
    fileName = "post." + ext
    with open(fileName, "wb") as f:
        f.write(file.getbuffer())
    # caching
    st.session_state.uploadedFileType = ext

def removeSavedUpload():
    ext = st.session_state.uploadedFileType
    fileName = "post." + ext
    if ext:
        os.remove(fileName)
    st.session_state.uploadedFileType = ""

def displayUpload():
    ext = st.session_state.uploadedFileType
    fileName = "post." + ext
    if ext in videoFormats:
        PREVIEW.video(open(fileName, 'rb').read())
    else:
        PREVIEW.image(Image.open(fileName))

def makePost():
    PREVIEW.empty(); SENDBUTTON.empty()
    sendFile()
    removeSavedUpload()

def sendFile():
    ext = st.session_state.uploadedFileType
    fileName = "post." + ext
    isVideo = ext in videoFormats
    prefix = "video" if isVideo else "image"
    fileType = prefix + "/" + ext
    backend.createPost(fileName, fileType) # remove account field

## logic
POSTHEADER.header('📸 Make your post!')
showUploader()
ext = st.session_state.uploadedFileType
if ext:
    displayUpload()
    wantSendPost = SENDBUTTON.button("Send")
    if wantSendPost:
        makePost()
        POSTMSG.success("Successfully sent!")



# Watching Interface

## states
if 'mediaFileType' not in st.session_state:
    st.session_state.mediaFileType = ""
if 'mediaList' not in st.session_state:
    st.session_state.mediaList = []
if 'feed' not in st.session_state:
    st.session_state.feed = None

## functions
def getLatestFeeds():
    mediaList = st.session_state.mediaList
    feed = st.session_state.feed
    if not mediaList:
        if not feed:
            latest = oldestDateTime
        else: latest = feed.dateTime
    else: latest = mediaList[-1].dateTime
    incomingFeeds = backend.getNewPosts(latest)
    if incomingFeeds:
        st.session_state.mediaList += incomingFeeds

def nextFeed():
    mediaList = st.session_state.mediaList
    if not mediaList:
        FEEDMSG.warning("No more feeds at the moment")
        return
    feed = mediaList.pop(0)
    st.session_state.feed = feed
    removeSavedMedia()
    saveMedia(feed.mediaURL)

def saveMedia(mediaURL):
    filePrefix = "media."
    fileName = backend.downloadMedia(filePrefix, mediaURL)
    st.session_state.mediaFileType = fileName.split(".")[-1]

def removeSavedMedia():
    ext = st.session_state.mediaFileType
    fileName = "media." + ext
    if ext:
        os.remove(fileName)
    st.session_state.mediaFileType = ""

def displayFeed(pfeed):
    if not feed:
        return
    ext = st.session_state.mediaFileType
    fileName = "media." + ext
    if feed.mediaType.startswith("video"):
        FEED.video(open(fileName, 'rb').read())
    else:
        FEED.image(Image.open(fileName))


## logic

FEEDHEADER.header('🎥 Watch and Enjoy!')
getLatestFeeds()
if not st.session_state.feed: # if feed is not cached
    nextFeed()
wantNext = NEXTBUTTON.button("Next")
if wantNext:
    nextFeed()
feed = st.session_state.feed
displayFeed(feed)