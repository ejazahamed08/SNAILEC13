import cv2
from PIL import Image

cap = cv2.VideoCapture('video.mp4')
frames = []

# UPDATED: More aggressive variables
frame_count = 0 
scale_percent = 30 # UPDATED: Reduced to 30% of original size

while True:
    ret, frame = cap.read()
    if not ret:
        break # BREAKS AT LAST FRAME OF VIDEO
        
    # UPDATED: Keep 1 frame, skip 2. Cuts the total frames by 66%.
    if frame_count % 3 != 0:
        frame_count += 1 
        continue 
        
    # NEW: Calculate the new dimensions and resize the current frame
    width = int(frame.shape[1] * scale_percent / 100) # Calculates the scaled-down width
    height = int(frame.shape[0] * scale_percent / 100) # Calculates the scaled-down height
    frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA) # Overwrites the original frame with the smaller version

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # converting BGR to RGB as pillow only reads RGB

    pil_img = Image.fromarray(frame_rgb) # converting to a pillow pillow image
    
    # NEW: Compress colors! Convert to a 128-color palette (default is 256). 
    # This drastically reduces file size with a slight drop in color quality.
    pil_img = pil_img.convert("P", palette=Image.ADAPTIVE, colors=128) 
    
    frames.append(pil_img) # appending all pillow images into frames
    
    # NEW: Increment the counter for the frames we actually keep
    frame_count += 1

cap.release() #closes the video file and frees up the memory and system resources that OpenCV was using to read the mp4

if frames:
    # duration is in milliseconds per frame (40ms = 25 frames per second)
    # loop=0 means the GIF will loop infinitely
    frames[0].save( # pillow stitches the frames into a gif and saves it
        'output.gif', # output file
        save_all=True, # saves all sequences of images
        append_images=frames[1:], # stiches images from 1 onwards on the base 0th frame
        optimize=True, # optimizes the file size at the end by removing redundant date
        duration=120, # UPDATED: Increased to 120ms because we are only keeping 1 out of every 3 frames (40ms * 3)
        loop=0 # looping infintely feature any natural number it loops on that number of times
    )
    print("GIF created successfully!")