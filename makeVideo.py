from moviepy.editor import ImageSequenceClip
import os

#######################
folder = 'Plots'

fileName = "mandelbrotSeq1.mp4"
#######################



os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

# Path to the folder containing the images
image_folder = os.getcwd()+'/'+folder


# List all the image file names in the folder
images = [f"{image_folder}/{img}" for img in sorted(os.listdir(image_folder)) if img.endswith(".png")]
# Function to extract timestamp from filename or metadata
def get_creation_time(file_path):
    return os.stat(file_path).st_mtime

# Sort images based on timestamps
sorted_images = sorted(images, key=get_creation_time)

# Create a video clip from the images
clip = ImageSequenceClip(sorted_images, fps=24)

# Save the video


clip.write_videofile(fileName)
