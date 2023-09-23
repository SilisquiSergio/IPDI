import customtkinter as ctk
from tkinter import filedialog
from customtkinter import CTkFrame,CTkButton,CTkLabel,CTkComboBox,CTkEntry
from PIL import Image,ImageTk 
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import imageio.v3
import tkinter as tk

#apariencia de la ventana principal

ctk.set_appearance_mode("light") #cambia la aparencia de la ventana
ctk.set_default_color_theme("green") # tema del color de los botones
root=ctk.CTk()
root.geometry("1200x600")

#variables globales
colorV=root.cget("bg") #obtiene el color de la ventana


#definir dimensiones de la primera fila del grid
#------------------------------------------------
root.grid_rowconfigure(0,minsize=500)
root.grid_columnconfigure(0,minsize=400)
root.grid_rowconfigure(0,minsize=500)
root.grid_columnconfigure(1,minsize=400)
root.grid_rowconfigure(0,minsize=500)
root.grid_columnconfigure(2,minsize=400)
root.grid_columnconfigure(2,minsize=500)
#-----------------------------------------------

#Ruta de las imagenes gurdadas
#----------------------------------------------
ruta_img1=''
ruta_img2=''
ruta_guardar='C:/Users/Mi Pc/Downloads/IntroduccionProcesamietoImagenesTPN1/imagenprocesada.png'
#----------------------------------------------


#definicion de funciones
#--------------------------------------------------------------
#--------------------------------------------------------------
#funcion que abre un archivo

def OpenFile1(etiqueta):
    global ruta_imagen1
    ruta_imagen1=filedialog.askopenfilename()
    i=Image.open(ruta_imagen1)
    
    plt.figure()
    plt.title("Imagen original")
    plt.imshow(i)
    plt.savefig("imagen.png")
    
    i=Image.open('imagen.png')
    i=i.resize((500,400))
    img=ImageTk.PhotoImage(i)
    etiqueta.configure(image=img,text="") 
    

#funciones que convierte una imagen a  RGB E YIQ respectivamente

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

# funciones para realizar las operaciones funciones lineal
# funcion raiz, funcion a trozos

def Histograma(img,titulo,eti):
    rango=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    arreglo=np.ravel(img[:,:,0]) #convierte una matriz a un arreglo
    plt.figure()
    plt.hist(arreglo,bins=rango,range=(0,1),edgecolor="black",stacked=True)
    plt.title(titulo)
    plt.xlabel("datos")
    plt.ylabel("Probabilidad")
    plt.savefig('histograma.png')
    
    i=Image.open('histograma.png')
    i=i.resize((500,400))
    img=ImageTk.PhotoImage(i)
    eti.configure(image=img,text="")
    #plt.show()


# funcion para interactuar con el boton procesar

def operar():
    im1=imageio.v3.imread(ruta_imagen1)
    #im2=imageio.v3.imread(ruta_imagen2)
    
    if cbx1.get()=="raiz":
       im1=np.clip(im1/255,0,1)
       yiq=RGB_a_YIQ(im1)
       titulo1="histogra de imagen original"
       Histograma(yiq,titulo1,imagen3)
       
       yiq[:,:,0]=np.sqrt(yiq[:,:,0])# funcion raiz
       titulo2="histograma de imagen filtrada"
       Histograma(yiq,titulo2,hist2)
       
       rgb=YIQ_a_RGB(yiq).astype(np.uint8)
       plt.figure()
       plt.title("Imagen Filtrada")
       plt.imshow(rgb)
       plt.savefig("resultado.png")
        
       i=Image.open('resultado.png')
       i=i.resize((500,400))
       img=ImageTk.PhotoImage(i)
       imagen2.configure(image=img,text="") 
    
    if cbx1.get()=="cuadrada":
        #global ruta_guardar
        im1=np.clip(im1/255,0,1)
        yiq=RGB_a_YIQ(im1)
        titulo4="histogra de imagen original"
        Histograma(yiq,titulo4,imagen3)
       
        yiq[:,:,0]=(yiq[:,:,0])**2 # funcion cuadrada
       
        titulo3="histogra de imagen filtrada"
        Histograma(yiq,titulo3,hist2)
        rgb=YIQ_a_RGB(yiq).astype(np.uint8)
        plt.figure()
        plt.title("Imagen Filtrada")
        plt.imshow(rgb)
        plt.savefig("resultado.png")
        
        i=Image.open('resultado.png')
        i=i.resize((500,400))
        img=ImageTk.PhotoImage(i)
        imagen2.configure(image=img,text="") 
        
        
def guardarimagen():
    global ruta_guardar
    imagen_guardar=Image.open(ruta_guardar)
        
    ruta=filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("Archivos de Imagenes",".bmp *,.png *")])
    imagen_guardar.save(ruta)
        
def salir():
    root.quit()       

# Frames para insertar dentro de los grids

marco1=CTkFrame(root,fg_color=colorV)
marco2=CTkFrame(root,fg_color=colorV)
marco3=CTkFrame(root,fg_color=colorV)

#botones, label y combobox ubicados en cada marco

imagen1=CTkLabel(root,text="imagen 1")
imagen2=CTkLabel(root,text="imagen filtrada")
imagen3=CTkLabel(root,text="histograma 1")

btn10=CTkButton(marco1,text="Procesar",command=operar)
btn20=CTkButton(marco1,text="Guardar",command=guardarimagen)
btn30=CTkButton(marco1,text="Salir",command=salir)

cbx1=CTkComboBox(marco2,values=["raiz","cuadrada","lineal a trozos"])
lbl1=CTkLabel(marco2,text="Filtrado: ")

et1=CTkLabel(marco3,text="ymin:")
caja1=CTkEntry(marco3)
et2=CTkLabel(marco3,text="ymax:")
caja2=CTkEntry(marco3)


# Posicion de cada de los elementos en cada marco

et1.grid(row=0,column=0,padx=10,pady=10)
caja1.grid(row=0,column=1,padx=10,pady=10)
et2.grid(row=0,column=2,padx=10,pady=10)
caja2.grid(row=0,column=3,padx=10,pady=10)

btn10.grid(row=0,column=0,padx=10,pady=10)
btn20.grid(row=0,column=1,padx=10,pady=10)
btn30.grid(row=0,column=2,padx=10,pady=10)

lbl1.grid(row=0,column=0,padx=2)
cbx1.grid(row=0,column=1,padx=2)


# Poscion en grid de la ventana principal

imagen1.grid(row=0,column=0,padx=5,pady=5)
imagen2.grid(row=0,column=1,padx=5,pady=5)
imagen3.grid(row=0,column=2,padx=5,pady=5)
btn1=CTkButton(root,text="Cargar Imagen 1",command = lambda:OpenFile1(imagen1))
hist2=CTkLabel(root,text="histograma 2")

btn1.grid(row=1, column=0)
hist2.grid(row=1,column=2, rowspan=3)
marco1.grid(row=1,column=1)
marco2.grid(row=2,column=0,padx=20,pady=35)
marco3.grid(row=2,column=1,padx=10,pady=35)

root.mainloop()