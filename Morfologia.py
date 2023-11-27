import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image,ImageTk 

import numpy as np
import imageio.v3
import matplotlib.pyplot as plt

ruta_imagen1 = ''

k = np.array([[-1,-1,-1], [-1,10,-1],[-1,-1,-1]])
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

def CargarImagen(dir):
    imag = imageio.v3.imread(dir)
    return imag
# funcion que realiza la convolucion de imagenes

def Erosion (imagen,karnel,n):

# para la funcion de erosion tomamos el valor minimo de luminancia
# en la vencidad

  fil, col = imagen.shape
  mor_y =  np.zeros(imagen.shape)

  for x in range(1, fil - 1):
    for y in range(1, col - 1):
      lista = [] #lo colocamos en una lista para poder comparar valores
      for i in range(n):
        for j in range(n):
           num = imagen[x - 1 + i , y - 1 + j]
           lista.append(num)
      mor_y[x,y] = min(lista)
  return mor_y

def Dilatacion (imagen,karnel,n):

# para la funcion de dilatacion tomamos el valor maximo de luminancia
# en la vencidad

  fil,col = imagen.shape
  mor_y =  np.zeros(imagen.shape)

  for x in range(1, fil - 1):
    for y in range(1, col - 1):
      lista = [] #lo colocamos en una lista para poder comparar valores
      for i in range(n):
        for j in range(n):
           num = imagen[x - 1 + i , y - 1 + j]
           lista.append(num)
      mor_y[x,y] = max(lista)
  return mor_y

def Apertura (im,k,n):

# para la funcion de apertura realizamos la operacion erosion seguida
#de la dilatacion

  im = Erosion(im,k,n)
  im = Dilatacion(im,k,n)

  return im

def Cierre (im,k,n):

# para la funcion de cierre realizamos la operacion dilatacion seguida
#de la erosion

  im = Dilatacion(im,k,n)
  im= Erosion(im,k,n)

  return im

def BordeMorfologico (im,k,n):

# para la funcion de borde morfologico realizamos la dilatacion menos imagen
# original.

  img = Dilatacion(im,k,n)

  img = img - im

  return img

def Mediana (imagen,karnel,n):

# para la funcion de dilatacion tomamos el valor maximo de luminancia
# en la vencidad

  fil,col = imagen.shape
  mor_y =  np.zeros(imagen.shape)

  for x in range(1, fil - 1):
    for y in range(1, col - 1):
      lista = [] #lo colocamos en una lista para poder comparar valores
      for i in range(n):
        for j in range(n):
           num = imagen[x - 1 + i , y - 1 + j]
           lista.append(num)
      mor_y[x,y] = sum(lista) / len(lista)

  return mor_y





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
    if cbx.get() == "Erosion":
        
        img = CargarImagen(ruta_imagen1)
        im = np.clip(img/255.,0.,1.)
        im = Erosion(im, k,3)
        im = np.clip(im*255.,0.,255.).astype(np.uint8)

        imageio.v3.imwrite('imagen2.bmp',im)
        i=Image.open('imagen2.bmp')
        i=i.resize((400,400))
        img=ImageTk.PhotoImage(i)
        imagen2.config(image=img)
        imagen2.i = img
        
        
    if cbx.get() == "Dilatacion":
        img = CargarImagen(ruta_imagen1)
        im = np.clip(img/255.,0.,1.)
        im = Dilatacion(im, k,3)
        im = np.clip(im*255.,0.,255.).astype(np.uint8)

        imageio.v3.imwrite('imagen2.bmp',im)
        i=Image.open('imagen2.bmp')
        i=i.resize((400,400))
        img=ImageTk.PhotoImage(i)
        imagen2.config(image=img)
        imagen2.i = img
        
    if cbx.get() == "Apertura":
        img = CargarImagen(ruta_imagen1)
        im = np.clip(img/255.,0.,1.)
        im = Apertura(im, k,3)
        im = np.clip(im*255.,0.,255.).astype(np.uint8)

        imageio.v3.imwrite('imagen2.bmp',im)
        i=Image.open('imagen2.bmp')
        i=i.resize((400,400))
        img=ImageTk.PhotoImage(i)
        imagen2.config(image=img)
        imagen2.i = img
        
    if cbx.get() == "Cierre":
        img = CargarImagen(ruta_imagen1)
        im = np.clip(img/255.,0.,1.)
        im = Cierre(im, k,3)
        im = np.clip(im*255.,0.,255.).astype(np.uint8)

        imageio.v3.imwrite('imagen2.bmp',im)
        i=Image.open('imagen2.bmp')
        i=i.resize((400,400))
        img=ImageTk.PhotoImage(i)
        imagen2.config(image=img)
        imagen2.i = img
        
    if cbx.get() == "Borde Morfologico":
        img = CargarImagen(ruta_imagen1)
        im = np.clip(img/255.,0.,1.)
        im = BordeMorfologico(im, k,3)
        im = np.clip(im*255.,0.,255.).astype(np.uint8)

        imageio.v3.imwrite('imagen2.bmp',im)
        i=Image.open('imagen2.bmp')
        i=i.resize((400,400))
        img=ImageTk.PhotoImage(i)
        imagen2.config(image=img)
        imagen2.i = img
        
    if cbx.get() == "Mediana":
        img = CargarImagen(ruta_imagen1)
        im = np.clip(img/255.,0.,1.)
        im = Mediana(im, k,3)
        im = np.clip(im*255.,0.,255.).astype(np.uint8)

        imageio.v3.imwrite('imagen2.bmp',im)
        i=Image.open('imagen2.bmp')
        i=i.resize((400,400))
        img=ImageTk.PhotoImage(i)
        imagen2.config(image=img)
        imagen2.i = img


def copiar():
    global ruta_imagen1
    ruta_imagen1 ='imagen2.bmp'
    i=Image.open(ruta_imagen1)
    if ruta_imagen1:
        imagen = Image.open('imagen2.bmp')
        imagen = imagen.resize((400,400))  # Ajusta el tamaño de la imagen según sea necesario
        foto = ImageTk.PhotoImage(imagen)
        
        imagen1.config(image=foto)
        imagen1.image = foto
    
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

boton2 = tk.Button(marco,text='<--Copiar',command=copiar)
boton2.pack()

imagen2 = tk.Label(ventana,text='imagen 2')
imagen2.grid(row=0,column=2)

et1 = tk.Label(ventana,text='imagen original')
et1.grid(row=1,column=0)

et2 = tk.Label(ventana,text = 'ventana 3x3')
et2.grid(row=1,column=1)

et3 = tk.Label(ventana,text='imagen filtrada')
et3.grid(row=1,column=2)

btn1 = tk.Button(ventana,text='cargar',command= CargarIm)
btn1.grid(row=2,column=0)

cbx = ttk.Combobox(ventana,values=["Erosion","Dilatacion","Apertura","Cierre","Borde Morfologico","Mediana"])
cbx.grid(row=2,column=1)

btn2= tk.Button(ventana,text='Guardar')
btn2.grid(row=2,column=2)

ventana.mainloop()
