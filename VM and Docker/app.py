import streamlit as st
from PIL import Image

st.title("Title")
st.header("Header")
st.subheader("Subheader")
st.text("Text")

# button
clicked = st.button("Click")
if clicked:
    st.write("Button clicked")
    
# text input
text = st.text_input("Write")
if text:
    st.write("You typed {}".format(text))
    
# image file uploader
photo = st.file_uploader("Upload image", ["png", "jpg", "jpeg"])
if photo != None:
    image = Image.open(photo)
    st.image(image)
    
# video file uploader
video = st.file_uploader("Upload video", ["mp4"])
if video != None:
    st.video(video)
    
# https://docs.streamlit.io/library/api-reference
