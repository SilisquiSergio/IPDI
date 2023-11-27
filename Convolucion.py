#importacion de las librerias necesarias
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image,ImageTk 

import numpy as np
import imageio.v3
import matplotlib.pyplot as plt

ruta_imagen1 = ''

#definicion de karnels
k1 = np.array([[1/9,1/9,1/9], [1/9,1/9,1/9],[1/9,1/9,1/9]])#karnel plano 3x3
k2 = np.array([[1/16,2/16,1/16], [2/16,4/16,2/16],[1/16,2/16,1/16]])#bartlett 3x3
k3 = np.array([[1/81,2/81,3/81,2/81,1/81], [2/81,4/81,6/81,4/81,2/81],[3/81,6/81,9/81,6/81,3/81],[2/81,4/81,6/81,4/81,2/81],[1/81,2/81,3/81,2/81,1/81]])#bartlett 5x5
k4 = np.array([[1,2,3,4,3,2,1], [2,4,6,8,6,4,2],[3,6,9,12,9,6,3],[4,8,12,16,12,8,4],[3,6,9,12,9,6,3],[2,4,6,8,6,4,2],[1,2,3,4,3,2,1]])
k5 = np.array([[1,4,6,4,1], [4,16,24,16,4],[6,24,36,24,6],[4,16,24,16,4],[1,4,6,4,1]])*1/256
k6 = np.array([[1,4,7,10,7,4,1], [4,16,26,33,26,16,4],[7,26,41,51,41,26,7],[10,33,51,64,51,33,10],[7,26,41,51,41,26,7],[4,16,26,33,26,16,4],[1,4,7,10,7,4,1]])*1/1003
k7 = np.array([[0,1,0], [1,-4,1],[0,1,0]])#laplaciano de 4 vecinos
k8 = np.array([[1,1,1], [1,8,1],[1,1,1]])#lapalciano de 8 vecinos
k9 = np.array([[-1,0,1], [-2,0,2],[-1,0,1]])#sobel



# definicion funciones

def YIQ_a_RGB(yiq):
    rgb = np.zeros(yiq.shape)
    rgb[:,:,0] = yiq[:,:,0] + 0.9663*yiq[:,:,1]+0.6210*yiq[:,:,2]
    rgb[:,:,1] = yiq[:,:,0] - 0.2721*yiq[:,:,1]-0.6474*yiq[:,:,2]
    rgb[:,:,2] = yiq[:,:,0] - 1.1070*yiq[:,:,1]+1.7046*yiq[:,:,2]
    rgb=np.clip(rgb*255,0,255)
    return rgb

def RGB_a_YIQ(rgb):
    yiq = np.zeros(rgb.shape)
    yiq[:,:,0] = 0.299*rgb[:,:,0] + 0.587*rgb[:,:,1]+0.114*rgb[:,:,2]
    yiq[:,:,1] = 0.595716*rgb[:,:,0] - 0.274453*rgb[:,:,1]-0.321263*rgb[:,:,2]
    rgb[:,:,2] = 0.211456*rgb[:,:,0] - 0.522591*rgb[:,:,1]+0.311135*rgb[:,:,2]
    return yiq

def MostrarImagen(imagen):
    plt.imshow(imagen)

def CargarImagen(dir):
    imag = imageio.v3.imread(dir)
    return imag

# funcion que realiza la convolucion de imagenes

def convolucion (imagen,karnel):
  fil, col = imagen.shape
  conv_y =  np.zeros(imagen.shape)

  for x in range(1, fil - 1):
    for y in range(1, col - 1):
      suma = 0
      for i in range(3):
        for j in range(3):
          suma = suma + imagen[x - 1 + i , y - 1 + j] * karnel[i,j]

      conv_y[x,y] = suma

  return conv_y


def CargarIm():
    global ruta_imagen1
    ruta_imagen1=filedialog.askopenfilename()
    i=Image.open(ruta_imagen1)
    if ruta_imagen1:
        imagen = Image.open(ruta_imagen1)
        imagen = imagen.resize((400,400))  # Ajusta el tamaño de la imagen según sea necesario
        foto = ImageTk.PhotoImage(imagen)
        
        imagen1.config(image=foto)
        imagen1.image = foto
def filtrar():
    
    global ruta_imagen1
    
    if cbx.get() == "Plano":
        
        img = CargarImagen(ruta_imagen1)
        im = np.clip(img/255.,0.,1.)
        im = convolucion(im, k1,)
        im = np.clip(im*255.,0.,255.).astype(np.uint8)

        imageio.v3.imwrite('imagen2.bmp',im)
        i=Image.open('imagen2.bmp')
        i=i.resize((400,400))
        img=ImageTk.PhotoImage(i)
        imagen2.config(image=img)
        imagen2.i = img
        
        
    if cbx.get() == "Bartlett 3x3":
        img = CargarImagen(ruta_imagen1)
        im = np.clip(img/255.,0.,1.)
        im = convolucion(im, k2)
        im = np.clip(im*255.,0.,255.).astype(np.uint8)

        imageio.v3.imwrite('imagen2.bmp',im)
        i=Image.open('imagen2.bmp')
        i=i.resize((400,400))
        img=ImageTk.PhotoImage(i)
        imagen2.config(image=img)
        imagen2.i = img
        
    if cbx.get() == "Bartlett 5x5":
        img = CargarImagen(ruta_imagen1)
        im = np.clip(img/255.,0.,1.)
        im = convolucion(im, k3)
        im = np.clip(im*255.,0.,255.).astype(np.uint8)

        imageio.v3.imwrite('imagen2.bmp',im)
        i=Image.open('imagen2.bmp')
        i=i.resize((400,400))
        img=ImageTk.PhotoImage(i)
        imagen2.config(image=img)
        imagen2.i = img
        
    if cbx.get() == "Bartlett 7x7":
        img = CargarImagen(ruta_imagen1)
        im = np.clip(img/255.,0.,1.)
        im = convolucion(im, k4)
        im = np.clip(im*255.,0.,255.).astype(np.uint8)

        imageio.v3.imwrite('imagen2.bmp',im)
        i=Image.open('imagen2.bmp')
        i=i.resize((400,400))
        img=ImageTk.PhotoImage(i)
        imagen2.config(image=img)
        imagen2.i = img
     
    if cbx.get() == "Gaussiano 5x5":
        img = CargarImagen(ruta_imagen1)
        im = np.clip(img/255.,0.,1.)
        im = convolucion(im, k5)
        im = np.clip(im*255.,0.,255.).astype(np.uint8)

        imageio.v3.imwrite('imagen2.bmp',im)
        i=Image.open('imagen2.bmp')
        i=i.resize((400,400))
        img=ImageTk.PhotoImage(i)
        imagen2.config(image=img)
        imagen2.i = img    
    
    if cbx.get() == "Gaussiano 7x7":
        img = CargarImagen(ruta_imagen1)
        im = np.clip(img/255.,0.,1.)
        im = convolucion(im, k6)
        im = np.clip(im*255.,0.,255.).astype(np.uint8)

        imageio.v3.imwrite('imagen2.bmp',im)
        i=Image.open('imagen2.bmp')
        i=i.resize((400,400))
        img=ImageTk.PhotoImage(i)
        imagen2.config(image=img)
        imagen2.i = img
        
    if cbx.get() == "Laplaciano v4":
        img = CargarImagen(ruta_imagen1)
        im = np.clip(img/255.,0.,1.)
        im = convolucion(im, k7)
        im = np.clip(im*255.,0.,255.).astype(np.uint8)

        imageio.v3.imwrite('imagen2.bmp',im)
        i=Image.open('imagen2.bmp')
        i=i.resize((400,400))
        img=ImageTk.PhotoImage(i)
        imagen2.config(image=img)
        imagen2.i = img
        
    if cbx.get() == "Laplaciano v8":
        img = CargarImagen(ruta_imagen1)
        im = np.clip(img/255.,0.,1.)
        im = convolucion(im, k8)
        im = np.clip(im*255.,0.,255.).astype(np.uint8)

        imageio.v3.imwrite('imagen2.bmp',im)
        i=Image.open('imagen2.bmp')
        i=i.resize((400,400))
        img=ImageTk.PhotoImage(i)
        imagen2.config(image=img)
        imagen2.i = img
        
    if cbx.get() == "Sobel":
        img = CargarImagen(ruta_imagen1)
        im = np.clip(img/255.,0.,1.)
        im = convolucion(im, k9)
        im = np.clip(im*255.,0.,255.).astype(np.uint8)

        imageio.v3.imwrite('imagen2.bmp',im)
        i=Image.open('imagen2.bmp')
        i=i.resize((400,400))
        img=ImageTk.PhotoImage(i)
        imagen2.config(image=img)
        imagen2.i = img


#------------------------------interfaces grafica-------------------------------------

ventana = tk.Tk()

ventana.grid_columnconfigure(0,minsize=400)
ventana.grid_columnconfigure(1,minsize=100)
ventana.grid_columnconfigure(2,minsize=400)

ventana.grid_rowconfigure(0,minsize=400)
ventana.grid_rowconfigure(1,minsize=50)
ventana.grid_rowconfigure(2,minsize=50)

imagen1 = tk.Label(ventana,text='imagen 1') 
imagen1.grid(row=0,column=0)


marco = tk.Frame(ventana)
marco.grid(row=0,column=1)


boton1 = tk.Button(marco,text='Filtrar-->',command=filtrar)
boton1.pack()

imagen2 = tk.Label(ventana,text='imagen 2')
imagen2.grid(row=0,column=2)

et1 = tk.Label(ventana,text='imagen original')
et1.grid(row=1,column=0)

et2 = tk.Label(ventana,text = 'ventana 3x3')
et2.grid(row=1,column=1)

et3 = tk.Label(ventana,text='imagen filtrada')
et3.grid(row=1,column=2)

btn1 = tk.Button(ventana,text='cargar',command=CargarIm)
btn1.grid(row=2,column=0)

cbx = ttk.Combobox(ventana,values=["Plano","Bartlett 3x3","Bartlett 5x5","Bartlett 7x7","Gaussiano 5x5","Gaussiano 7x7","Laplaciano v4","Laplaciano v8","Sobel"])
cbx.grid(row=2,column=1)

btn2= tk.Button(ventana,text='Guardar')
btn2.grid(row=2,column=2)

ventana.mainloop()
