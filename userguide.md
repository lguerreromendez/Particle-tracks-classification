# USERGUIDE

### This file provides a guide on how the program works and the parameters that the user can access

```python
import matplotlib
matplotlib.use('Agg')
import cv2
import imutils
import numpy as np
from PIL import Image
import pytesseract as tess
import re
import copy
```

```python
video_path = 'video1.mkv' #videoroute

#create a object videocapture to open the video
cap = cv2.VideoCapture(video_path)

#check if the video is opened correctly
if not cap.isOpened():
    print("error opening the video.")
else:
    #obtain the amount of fps (frames per second) and the duration in seconds
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_seconds = total_frames / fps

    #  convert the duration into minutes and seconds
    duration_minutes = int(duration_seconds // 60)
    duration_seconds %= 60
    total_frames_seconds=round(total_frames/fps)
    print(f'Duración of the video: {duration_minutes} minutos {duration_seconds} segundos')
    print(f'Total frames = Total segundos = {total_frames_seconds}')
```

Once you have the characteristics of the video you must insert some inputs in order to make easier the analysis.
Here you can specify how much frames do you want to analyze in each segment fragmented of the video.
For example, if my video is 1 min and 19 s long, and i have 79 frames collected
I would like to have 4 arrays in a list of 20 frames stored in each one.

```python
duracion_segmento = int(input("Input the amount of frame sin each segment: "))
total_segmentos=round(total_frames_seconds/duracion_segmento)
print('There are', total_segmentos, 'total segments with this duration',duracion_segmento)
```

Now, we store the frames according to the parameters we have instructed the program to follow

```python
# register of the initial time
inicio_tiempo = time.time()

# open the video
cap = cv2.VideoCapture(video_path)

# check if the video is opened correctly
if not cap.isOpened():
    print("Error al abrir el video.")
else:
    frames = []
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # add the frame to the array
        frames.append(frame)

        # go to the next second
        for _ in range(frame_rate - 1):
            cap.read()

    # close the video
    cap.release()
    # Ahora 'frames' contiene un muestreo de fotogramas del video
    print(f' {len(frames)} frames have been stored in the array.')

# close windows opened by opencv
cv2.destroyAllWindows()
fin_tiempo = time.time()

# calculate the time in seconds
tiempo_transcurrido = fin_tiempo - inicio_tiempo

print(f"The code took {tiempo_transcurrido} second to execute.")

# close windows opened by OpenCV
cv2.destroyAllWindows()
im_list=frames #here we have the arrays of frames
intervalo=duracion_segmento
im_list_2=[] # and here we have the list of arrays of frames we want to analyze later
for i in range(0,len(im_list), intervalo):
    sublista=im_list[i:i+intervalo]
    im_list_2.append(sublista)
```

This way, we have all the video frames (79) stored in a list of arrays. Within each array, 20 video frames are stored. 
This allows us to store them efficiently, in an organized manner, and use loops for subsequent analysis



In this section, the video is opened, and the frames are processed one by one, which can take some time. 
For instance, if the video has a duration of 30 minutes, it took 15 minutes to execute

### Now, what we need to do is analyze these stored frames following the main idea explained in the readme

First, I explain how we can analyze in each frame which particles have been detected by the algorithm in the software. 
Within the frame, we focus on the corresponding part of this text
```python
x1, y1, x2, y2 = 1270, 410, 1760,810 
img1=im_list[0][y1:y2, x1:x2] #analyze one frame at these pixels
img1_dots=img1[160:190,170:220] #plot this image
```

![picture](images/image2.PNG)

Once we have a zoom of this part of the image, we can analyze this text using computer vision modules and text analysis


