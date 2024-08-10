import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.cluster import KMeans
from PIL import Image, ImageDraw


# Use HTML and CSS to center-align the title
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        font-size: 3.5em;
        font-weight: bold;
        margin-bottom: 1px;
    }
    </style>
    <h1 class="centered-title">Shade Analyzer</h1>
    <h3 style="text-align: center; margin-bottom: 20px">Discover the most prominent colors in your images</h3>
    """,
    unsafe_allow_html=True
)


# Insert photos
img = st.file_uploader("Choose an image...")

# How many colors you want
k = st.text_input("Please specify the number of colors you would like to display:")

# button to run the application
btn = st.button("Run")

if img is not None:

    image = matplotlib.image.imread(img)
    
    # reshaping the image
    X = image.reshape(-1,3)

    # if button click
    if btn:

        if k.isdigit() and int(k) >0:
            k = int(k)

            kmeans = KMeans(n_clusters=k, init='k-means++', algorithm='lloyd')
            kmeans.fit(X)

            def create_color_palette(dominant_colors, palette_size=(500, 100)):
                # Create an image to display the colors
                palette = Image.new("RGB", palette_size)
                draw = ImageDraw.Draw(palette)

                # Calculate the width of each color swatch
                swatch_width = palette_size[0] // len(dominant_colors)

                # Draw each color as a rectangle on the palette
                for i, color in enumerate(dominant_colors):
                    draw.rectangle([i * swatch_width, 0, (i + 1) * swatch_width, palette_size[1]], fill=tuple(color))
                    

                # Display your image 
                st.subheader("Your Image")
                st.image(image)

                # Display Top Colors from your image
                st.subheader(f"Top {k} Colors")
                st.image(palette)

                for i, color in enumerate(dominant_colors):
                    st.write(f"RGB Color Codes {i}: {tuple(map(int, color))}")
            
            create_color_palette(kmeans.cluster_centers_.astype(int))
            
                
            
else:        
    if btn:
        st.error("Upload the image first...")



        



