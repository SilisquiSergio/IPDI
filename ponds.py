# Instalacion librerias
import cv2 as cv
import numpy as np 
import matplotlib.pyplot as plt
import imageio
from skimage.util import random_noise
from PIL import Image, ImageTk
from sklearn.cluster import MeanShift, estimate_bandwidth

# Mis funciones
import funciones_pdi as nf

def calculate_histogram(values, ax):
#     fig, ax = plt.subplots(figsize=(4, 3))
    ax.set(title='Histograma')
    n, bins, patches = ax.hist(values, bins=20, range=(0,1), density=True)    
    altura_total = np.sum(n)
    factor_de_escala = 100 / altura_total
    n *= factor_de_escala
    # Graficar el histograma escalado
    ax.bar(bins[:-1], n, width=np.diff(bins), align="edge", edgecolor='black')
    # Establecer límite en el eje y hasta 100%
    ax.set_ylim(0, 100)
    
def show_images(values, title):
    fig, ax = plt.subplots()
    ax.imshow(values, 'gray')
    ax.set_title(title)
    fig.set_size_inches(18, 10, forward=True)

    fig, ax2 = plt.subplots()
    calculate_histogram(values.flatten(), ax2)
    

im = imageio.imread('ponds.bmp')

im = np.clip(im/255.,0.,1.) #normalizando [0,1]

yiq = np.clip(nf.RGB_to_YIQ(im),0.,1.)
print(yiq.min(), yiq.max())
luminancia = yiq[:,:,0]
show_images(luminancia,'Imagen Original')

yiq_lineal = nf.histogram_lineal(yiq, 0.2, 0.8)
print(yiq_lineal.min(), yiq_lineal.max())
luminancia_lineal = yiq_lineal[:,:,0]
show_images(luminancia_lineal,'Imagen Modificada Lineal')

img_rgb = nf.YIQ_to_RGB(yiq_lineal)
img_rgb = np.clip((img_rgb*255),0,255).astype(np.uint8)

def MeanShiftFunc(img, quantile):
    # filter to reduce noise
    img = cv.medianBlur(img, 3)

    # flatten the image
    flat_image = img.reshape((-1,3))
    flat_image = np.float32(flat_image)

    bandwidth = estimate_bandwidth(flat_image, quantile=quantile, n_samples=3000)
    ms = MeanShift(bandwidth=bandwidth, max_iter=800, bin_seeding=True)
    ms.fit(flat_image)
    labeled=ms.labels_


    # get number of segments
    segments = np.unique(labeled)
    #print('Number of segments: ', segments.shape[0])

    # get the average color of each segment
    total = np.zeros((segments.shape[0], 3), dtype=float)
    count = np.zeros(total.shape, dtype=float)
    for i, label in enumerate(labeled):
        total[label] = total[label] + flat_image[i]
        count[label] += 1
    avg = total/count
    avg = np.uint8(avg)

    # cast the labeled image into the corresponding average color
    res = avg[labeled]
    result = res.reshape((img.shape))

    #show the result

    return (result, segments.shape[0])


quantile_size = [0.0125, 0.0256 , 0.04, 0.06, 0.12, 0.2]
ms_results = {}
x = 1
for qua_value in quantile_size:
    mean_image, segment = MeanShiftFunc(img_rgb, qua_value)
    img_ms = np.clip(mean_image/255.,0.,1.) #normalizando [0,1]
    yiq_ms = np.clip(nf.RGB_to_YIQ(img_ms),0.,1.)
    luminancia_ms = yiq_ms[:,:,0]
    ms_results[x] = (luminancia_ms, segment)
    fig, ax = plt.subplots()
    ax.imshow(luminancia_ms, 'gray')
    ax.set_title("Image {} Number of segments: {}".format(x,segment))
    fig.set_size_inches(18, 10, forward=True)
    x = x + 1
    
def binarizacion(bandaY, umbral):
    result = np.zeros(bandaY.shape)
    for x in range(bandaY.shape[0]):
        for y in range(bandaY.shape[1]):
            result[x,y] = 0 if bandaY[x,y] > umbral else 1
    return result

segments = np.unique(ms_results[3][0])
print(segments)

fig.set_size_inches(18, 10, forward=True)
