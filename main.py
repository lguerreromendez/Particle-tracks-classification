# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 18:57:38 2023

@author: luisg
"""


from time import sleep
import os
import time
import matplotlib
matplotlib.use('Agg')
import cv2
import imutils
import numpy as np
from PIL import Image
import pytesseract as tess
import re
import copy


# cv2.destroyAllWindows()
video_path = 'video1min.mp4'
# video_path = 'video1.mkv'
#create a object videocapture to open the video
cap = cv2.VideoCapture(video_path)

# check if the video is opened correctly
# extract characteristics from the video file, such as its duration and frames per second (fps)
if not cap.isOpened():
    print("Error openeing the video.")
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

# Once you have the characteristics of the video you must insert some inputs in rder to make easier the analysis
# Here you can specify ho much frames do you want to analyze in each segment fragmented of the video.
# For example, if my video is 1 min and 19 s long, and i have 79 frames collected
# i would like to have 4 arrays in a list of 20 frames stored in each one.
duracion_segmento = int(input("Input the amount of frame sin each segment: "))
total_segmentos=round(total_frames_seconds/duracion_segmento)
print('There are', total_segmentos, 'total segments with this duration',duracion_segmento)
# segmento_a_analizar=int(input("Ingrese el que quiere analizar: "))
# frames_inicio=duracion_segmento*segmento_a_analizar
# frames_final=frames_inicio+duracion_segmento
# print('los frames que se van a almacer son:[',frames_inicio,'-',frames_final,']' )



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
    
#%%
import matplotlib
matplotlib.use('Agg')
# import cv2
# import imutils
# import numpy as np
# from PIL import Image
# import pytesseract as tess
# import re
# import copy
# import keras_ocr

inicio_tiempo2 = time.time()
x1, y1, x2, y2 = 1270, 410, 1760,810 
# img1=im_list[5][y1:y2, x1:x2] #analyze one frame at these pixels
# img1_alphas=img1[45:75,170:220]
# img1_e=img1[85:115,170:220]
# img1_muons=img1[120:150,170:220]
# img1_dots=img1[160:190,170:220]

# img2=im_list[40][y1:y2, x1:x2]

# cv2.imshow('imagen1', img1) #plot this image
# cv2.imshow('imagen2', img2)

tess.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# text=tess.image_to_string(img1)

def textpattern(pattern,text, particle):
# We use a regular expression to search for the number following 'Electrons:'
    # we search the pattern in the text
    match = re.search(pattern, text)
    # verify if the module has found the number and we obtain it
    if match:
        numero = int(match.group(1))
        # print("Número de ",particle,":", numero)
        return numero
    else:
        print("Número de ",particle," no encontrado.")

# pattern_e = r"Electrons:\s*(\d+)"
# pattern_muons = r"Muons:\s*(\d+)"
# pattern_alphas = r"Alphas:\s*(\d+)"
# pattern_total= r"Total:\s*(\d+)"
# n_total=textpattern(pattern_total, 'total')
# n_alphas=textpattern(pattern_alphas, 'alphas')
# n_e=textpattern(pattern_e, 'electrones')
# n_muons=textpattern(pattern_muons, 'muons')


def n_particles(image):
    x1, y1, x2, y2 = 1270, 410, 1760,810 
    img1=image[y1:y2, x1:x2]
    text=tess.image_to_string(img1)
    pattern_e = r"Electrons:\s*(\d+)"
    pattern_muons = r"Muons:\s*(\d+)"
    pattern_alphas = r"Alphas:\s*(\d+)"
    pattern_total= r"Total:\s*(\d+)"
    n_total=textpattern(pattern_total,text,  'total')
    n_alphas=textpattern(pattern_alphas,text, 'alphas')
    n_e=textpattern(pattern_e,text, 'electrones')
    n_muons=textpattern(pattern_muons,text, 'muons')
    return n_total, n_alphas, n_e, n_muons

def diferencia(image1, image2):
    x1, y1, x2, y2 = 475, 105, 1115, 740 #size of the image track
    frame1 = image1[y1:y2, x1:x2]
    frame2 = image2[y1:y2, x1:x2]
    frame2_new = copy.copy(frame2)

    # calculate the diff between both frames
    diferencia = cv2.absdiff(frame1, frame2_new)
    
    # convert the diff into a gray scale
    diferencia_gris = cv2.cvtColor(diferencia, cv2.COLOR_BGR2GRAY)
    
    # apply a thresold to see the resultss
    _, umbralizada = cv2.threshold(diferencia_gris, 25, 255, cv2.THRESH_BINARY)
    
    # Find the contours of the thresholded differences
    contornos, _ = cv2.findContours(umbralizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    diferencias = False
    # verify if contours have been found
    if len(contornos) > 0:
        # Draw the contours on the original frame (frame2) with a thickness of 1 pixel
        for contorno in contornos:
            x, y, w, h = cv2.boundingRect(contorno)
            cv2.rectangle(frame2_new, (x, y), (x + w, y + h), (0, 255, 0), 1)
        diferencias = True
        return diferencias, frame1, frame2, frame2_new, umbralizada, contornos
    else:
        return diferencias, frame1, frame2, frame2_new, umbralizada


def name_of_frame(n_muons_dif, n_e_dif, n_alphas_dif):
    if n_muons_dif!=0 and n_e_dif ==0 and n_alphas_dif==0:
        name='muon'   
        return name
    if n_muons_dif==0 and n_e_dif !=0 and n_alphas_dif==0:
        name='electron'
        return name
    if n_muons_dif==0 and n_e_dif ==0 and n_alphas_dif!=0:
        name='alpha' 
        return name
    if n_muons_dif!=0 and n_e_dif !=0 and n_alphas_dif==0:
        name='muon or electron'
        return name
    else:
        name='nada'
        return name

def particle_dif(n_particle_1, n_particle_2):
    n_particle_dif=0
    if n_particle_1 is not None and n_particle_2 is not None:
        n_particle_dif=n_particle_2-n_particle_1
    return n_particle_dif
# n_total, n_alphas, n_e, n_muons=n_particles(im_list[5])

#start wih the first frame
frame_list=0
for im_list in im_list_2:
    frame_list+=1
    
    n_total_list=[];n_alphas_list=[];n_e_list=[];n_muons_list=[]
    n_frame_list=[]
    
    for i, image in enumerate(im_list):
        n_total, n_alphas, n_e, n_muons=n_particles(image)
        n_total_list.append(n_total)
        n_alphas_list.append(n_alphas)
        n_e_list.append(n_e)
        n_muons_list.append(n_muons)
        n_frame_list.append(i)
    

    # We call the 'diferencia()' function with the corresponding frames.
    for i,j in enumerate(im_list[:-1]):
        diferencias=diferencia(im_list[i], im_list[i+1])[0]
        if diferencias==True and i>-1: # if there is any differences between tracks
            diferencias, frame1, frame2, frame2_new,umbralizada, contornos = diferencia(im_list[i], im_list[i+1])
            print('=====================')
            print('frame',frame_list,i)
            new_frame=i
            x11, y11, x22, y22 = 1270, 410, 1760,810 
            img1=im_list[i][y11:y22, x11:x22]
            img2=im_list[i+1][y11:y22, x11:x22]
            # cv2.imshow('Frame 1', frame1)
            # cv2.imshow('Texto del frame 1', img1)
            # cv2.imshow('Frame 2 con contornos', frame2_new)
            # cv2.imshow('Texto del frame 2', img2)
            # cv2.imshow('Diferencias', umbralizada)
            n_total_1, n_alphas_1, n_e_1, n_muons_1=n_particles(im_list[i]) #particles finfd in the text of frame 1
            n_total_2, n_alphas_2, n_e_2, n_muons_2=n_particles(im_list[i+1]) # particles find in the text of frame 2
            # now we have to see the diff between numbers of particles found for each frame 
            n_alphas_dif=particle_dif(n_alphas_1,n_alphas_2 )
            n_e_dif=particle_dif(n_e_1,n_e_2)
            n_muons_dif=particle_dif(n_muons_1,n_muons_2);
            # n_total_dif=n_total_2-n_total_1
            #print the diff between particles, if there is a new particle detected
            if n_muons_dif !=0:
                print('diferencias entre muones',n_muons_dif)
            if n_e_dif !=0:
                print('diferencias entre electrones',n_e_dif)
            if n_alphas_dif !=0:
                print('diferencias entre alphas',n_alphas_dif)
            
            
            # algorithms developed when two or more particles has been detected between two frames, in order to classified it correctly
            # when we here are two diff we hav two images and maybe two diff particles detected
            # one track detcted could be a muon and the oter one a electron.
            
            filas_blancas, columnas_blancas = np.where(umbralizada == 255)
            condicion_filas_list=[]
            condicion_columnas_list=[]
            for i in range(len(filas_blancas[:-1])):
                condicion=filas_blancas[i+1]-filas_blancas[i]
                if condicion>10 or condicion<-10:
                    condicion_filas_list.append(filas_blancas[i])
                    condicion_filas_list.append(filas_blancas[i+1])
            for i in range(len(columnas_blancas[:-1])):
                condicion_c=columnas_blancas[i+1]-columnas_blancas[i]
                if condicion_c>20 or condicion_c<-20:
                    condicion_columnas_list.append(columnas_blancas[i])
                    condicion_columnas_list.append(columnas_blancas[i+1])
                
                
            condicion_filas_list.insert(0,filas_blancas[0])
            condicion_filas_list.append(filas_blancas[-1])
            condicion_columnas_list.insert(0,columnas_blancas[0])
            condicion_columnas_list.append(columnas_blancas[-1])
            
             #classify the tracks in diff folders with the corresponding particle
             # also a folder named muon or electron in the case we found this diff  in the same frame, as explained above
            carpeta_muon='muon';carpeta_muon_or_electron='muon or electron';carpeta_electron='electron'
            carpeta_alphas='alphas'
            def create_folder(nombre_carpeta):
                if not os.path.exists('frames/'+nombre_carpeta):
                    # Crea la carpeta si no existe
                    os.mkdir('frames/'+ nombre_carpeta)
        
            create_folder(carpeta_muon); create_folder(carpeta_muon_or_electron); create_folder(carpeta_electron)
            create_folder(carpeta_alphas)
            for i in range(0, len(condicion_columnas_list),2):
                condicion_columnas_list_new=[0]*2
                condicion_columnas_list_new[0]=condicion_columnas_list[i]
                condicion_columnas_list_new[1]=condicion_columnas_list[i+1]
                if len(columnas_blancas)==1:
                    condicion_columnas_list_new[1]=condicion_columnas_list[i+1]+1    
            for i in range(0, len(condicion_filas_list),2):
                condicion_filas_list_new=[0]*2
                
                # print(i)
                condicion_filas_list_new[0]=condicion_filas_list[i]
                condicion_filas_list_new[1]=condicion_filas_list[i+1]
                if len(filas_blancas)==1:
                    condicion_filas_list_new[1]=condicion_filas_list[i+1]+1
                

                
                x1,y1,x2,y2 =min(condicion_columnas_list_new), min(condicion_filas_list_new),max(condicion_columnas_list_new), max(condicion_filas_list_new)
                if x1==x2:
                    x2=x2+1
                if y1==y2:
                    y2=y2+1
                zoom = umbralizada[y1:y2, x1:x2]
                # cv2.imshow('zoom'+str(i), zoom)
                names=name_of_frame(n_muons_dif, n_e_dif, n_alphas_dif)
                if names=='muon or electron':
                    cv2.imwrite('frames/muon or electron/frame'+str(frame_list)+'_'+str(new_frame)+'_'+str(i)+'.png', zoom)
                else:
                    cv2.imwrite('frames/'+names+'/frame'+str(frame_list)+'_'+str(new_frame)+'.png', zoom)
                
                sleep(1)

# Registra el tiempo de finalización
fin_tiempo2 = time.time()

# Calcula el tiempo transcurrido en segundos
tiempo_transcurrido2 = fin_tiempo2 - inicio_tiempo2

print(f"El código tomó {tiempo_transcurrido2} segundos en ejecutarse.")
