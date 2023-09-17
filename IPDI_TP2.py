import customtkinter as ctk
from tkinter import filedialog
from customtkinter import CTkFrame,CTkButton,CTkLabel,CTkComboBox
from PIL import Image,ImageTk 
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import imageio.v3
import tkinter as tk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

root=ctk.CTk()
root.geometry("1200x600")
root.grid_rowconfigure(0,minsize=500)
root.grid_columnconfigure(0,minsize=400)

root.grid_rowconfigure(0,minsize=500)
root.grid_columnconfigure(1,minsize=400)

root.grid_rowconfigure(0,minsize=500)
root.grid_columnconfigure(2,minsize=400)

root.grid_columnconfigure(2,minsize=500)


colorV=root.cget("bg")
valor_seleccionado=tk.StringVar()
ruta_imagen1="dsflasdf"
ruta_imagen2='wewewqwqe'
ruta_guardar='C:/Users/Mi Pc/Downloads/IntroduccionProcesamietoImagenesTPN1/imagenprocesada.png'

def OpenFile1(etiqueta):
    global ruta_imagen1
    ruta_imagen1=filedialog.askopenfilename()
    i=Image.open(ruta_imagen1)
    i=i.resize((500,400),)
    img=ImageTk.PhotoImage(i)
    print(valor_seleccionado)
    etiqueta.configure(image=img,text="")

def OpenFile2(etiqueta):
    global ruta_imagen2
    ruta_imagen2=filedialog.askopenfilename()
    i=Image.open(ruta_imagen2)
    i=i.resize((500,400),)
    img=ImageTk.PhotoImage(i)
    etiqueta.configure(image=img,text="")

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

def sum_rgb_clamp(imagen1_rgb,imagen2_rgb):
    sumaRgb=np.zeros(imagen1_rgb.shape)
    sumaRgb=imagen1_rgb + imagen2_rgb
    sumaRgb=np.clip(sumaRgb,0,255).astype(np.uint8)
    
    return sumaRgb

def sum_rgb_prom(imagen1_rgb,imagen2_rgb):
    sumaRgb=np.zeros(imagen1_rgb.shape)
    sumaRgb=(imagen1_rgb + imagen2_rgb)/2
    sumaRgb=np.clip(sumaRgb,0,255).astype(np.uint8)
    return sumaRgb

def sum_YIQ_clamp(imagen1_rgb,imagen2_rgb):
    imagen1_rgb = np.clip(imagen1_rgb/255,0,1)
    imagen2_rgb = np.clip(imagen2_rgb/255,0,1)
    yiq1 = RGB_a_YIQ(imagen1_rgb)
    yiq2 = RGB_a_YIQ(imagen2_rgb)
    yiq3=np.zeros(yiq1.shape)
  
    yiq3[:,:,0]=yiq1[:,:,0] + yiq2[:,:,0]
    yiq3[:,:,0]=np.clip(yiq3[:,:,0],0,1)
    
    # yiq3[:,:,1]=yiq1[:,:,1] + yiq2[:,:,1]
    # yiq3[:,:,2]=yiq1[:,:,2] + yiq2[:,:,2]
    
    yiq3[:,:,1] = (yiq1[:,:,0] * yiq2[:,:,0]) / (yiq1[:,:,0] + yiq2[:,:,0])
    yiq3[:,:,2] = (yiq1[:,:,0] * yiq1[:,:,2] + yiq2[:,:,0] * yiq2[:,:,2]) / (yiq1[:,:,0] + yiq2[:,:,0])
    
    return yiq3

def sum_YIQ_prom(imagen1_rgb,imagen2_rgb):
    imagen1_rgb = np.clip(imagen1_rgb/255,0,1)
    imagen2_rgb = np.clip(imagen2_rgb/255,0,1)
    yiq1 = RGB_a_YIQ(imagen1_rgb)
    yiq2 = RGB_a_YIQ(imagen2_rgb)
    yiq3=np.zeros(yiq1.shape)
    yiq3[:,:,0] = yiq1[:,:,0]+yiq2[:,:,0]/2
    yiq3[:,:,0] =np.clip(yiq3[:,:,0],0,1)
    
    yiq3[:,:,1] = (yiq1[:,:,0] * yiq2[:,:,0]) / (yiq1[:,:,0] + yiq2[:,:,0])
    yiq3[:,:,2] = (yiq1[:,:,0] * yiq1[:,:,2] + yiq2[:,:,0] * yiq2[:,:,2]) / (yiq1[:,:,0] + yiq2[:,:,0])
    
    return yiq3

def sum_Ligther_YIQ(imagen1_rgb,imagen2_rgb):
    imagen1_rgb = np.clip(imagen1_rgb/255,0,1)
    imagen2_rgb = np.clip(imagen2_rgb/255,0,1)
    yiq1 = RGB_a_YIQ(imagen1_rgb)
    yiq2 = RGB_a_YIQ(imagen2_rgb)
    yiq3=np.zeros(yiq1.shape)
    
    if (yiq1[:,:,0].all() > yiq2[:,:,0].all()):
        
        yiq3[:,:,0] = yiq1[:,:,0]
        yiq3[:,:,1] = yiq1[:,:,1]
        yiq3[:,:,2] = yiq1[:,:,2]
    else:
        yiq3[:,:,0] = yiq2[:,:,0]
        yiq3[:,:,1] = yiq2[:,:,1]
        yiq3[:,:,2] = yiq2[:,:,2]
        
    return yiq3

def resta_rgb_clamp(imagen1_rgb,imagen2_rgb):
    sumaRgb=np.zeros(imagen1_rgb.shape)
    sumaRgb=imagen1_rgb - imagen2_rgb
    sumaRgb=np.clip(sumaRgb,0,255).astype(np.uint8)
    return sumaRgb

def resta_rgb_prom(imagen1_rgb,imagen2_rgb):
    sumaRgb=np.zeros(imagen1_rgb.shape)
    sumaRgb=(imagen1_rgb - imagen2_rgb)/2
    sumaRgb=np.clip(sumaRgb,0,255).astype(np.uint8)
    return sumaRgb

def sum_dark_YIQ(imagen1_rgb,imagen2_rgb):
    imagen1_rgb = np.clip(imagen1_rgb/255,0,1)
    imagen2_rgb = np.clip(imagen2_rgb/255,0,1)
    yiq1 = RGB_a_YIQ(imagen1_rgb)
    yiq2 = RGB_a_YIQ(imagen2_rgb)
    yiq3=np.zeros(yiq1.shape)
    
    if (yiq1[:,:,0].all() > yiq2[:,:,0].all()):
        
        yiq3[:,:,0] = yiq2[:,:,0]
        yiq3[:,:,1] = yiq2[:,:,1]
        yiq3[:,:,2] = yiq2[:,:,2]
    else:
        yiq3[:,:,0] = yiq1[:,:,0]
        yiq3[:,:,1] = yiq1[:,:,1]
        yiq3[:,:,2] = yiq1[:,:,2]
        
    return yiq3

def resta_YIQ_clamp(imagen1_rgb,imagen2_rgb):
    imagen1_rgb = np.clip(imagen1_rgb/255,0,1)
    imagen2_rgb = np.clip(imagen2_rgb/255,0,1)
    yiq1 = RGB_a_YIQ(imagen1_rgb)
    yiq2 = RGB_a_YIQ(imagen2_rgb)
    yiq3=np.zeros(yiq1.shape)
  
    yiq3[:,:,0]=yiq1[:,:,0] - yiq2[:,:,0]
    yiq3[:,:,0]=np.clip(yiq3[:,:,0],0,1)
    
    # yiq3[:,:,1]=yiq1[:,:,1] + yiq2[:,:,1]
    # yiq3[:,:,2]=yiq1[:,:,2] + yiq2[:,:,2]
    
    yiq3[:,:,1] = (yiq1[:,:,0] * yiq2[:,:,0]) / (yiq1[:,:,0] + yiq2[:,:,0])
    yiq3[:,:,2] = (yiq1[:,:,0] * yiq1[:,:,2] + yiq2[:,:,0] * yiq2[:,:,2]) / (yiq1[:,:,0] + yiq2[:,:,0])
    
    return yiq3

def resta_YIQ_prom(imagen1_rgb,imagen2_rgb):
    
    imagen1_rgb = np.clip(imagen1_rgb/255,0,1)
    imagen2_rgb = np.clip(imagen2_rgb/255,0,1)
    yiq1 = RGB_a_YIQ(imagen1_rgb)
    yiq2 = RGB_a_YIQ(imagen2_rgb)
    yiq3=np.zeros(yiq1.shape)
    yiq3[:,:,0] = yiq1[:,:,0]-yiq2[:,:,0]/2
    yiq3[:,:,0] =np.clip(yiq3[:,:,0],0,1)
    
    yiq3[:,:,1] = (yiq1[:,:,0] * yiq2[:,:,0]) / (yiq1[:,:,0] + yiq2[:,:,0])
    yiq3[:,:,2] = (yiq1[:,:,0] * yiq1[:,:,2] + yiq2[:,:,0] * yiq2[:,:,2]) / (yiq1[:,:,0] + yiq2[:,:,0])
    
    return yiq3

def operar():
    im1=imageio.v3.imread(ruta_imagen1)
    im2=imageio.v3.imread(ruta_imagen2)
    
    if cbx1.get()=="suma" and cbx2.get()=="RGB Cleampeado":
       # global ruta_guardar
        
        suma=sum_rgb_clamp(im1,im2)
        imageio.v3.imwrite(ruta_guardar,suma)
        
        i=Image.open(ruta_guardar)
        i=i.resize((500,400),)
        img=ImageTk.PhotoImage(i)
        imagen3.configure(image=img,text="")
        
    
    if cbx1.get()=="suma" and cbx2.get()=="RGB Promediado":
        #global ruta_guardar
        suma=sum_rgb_prom(im1,im2)
        imageio.v3.imwrite(ruta_guardar,suma)
        i=Image.open(ruta_guardar)
        i=i.resize((500,400),)
        img=ImageTk.PhotoImage(i)
        imagen3.configure(image=img,text="")
        
    if cbx1.get()=="suma" and cbx2.get()=="YIQ Cleampeado":
       # global ruta_guardar
        suma=sum_YIQ_clamp(im1,im2)
        suma=YIQ_a_RGB(suma).astype(np.uint8)
        
        imageio.v3.imwrite(ruta_guardar,suma)
        i=Image.open(ruta_guardar)
        i=i.resize((500,400),)
        img=ImageTk.PhotoImage(i)
        imagen3.configure(image=img,text="")
        
    if cbx1.get()=="suma" and cbx2.get()=="YIQ Promediado":
        #global ruta_guardar
        suma=sum_YIQ_prom(im1,im2)
        suma=YIQ_a_RGB(suma).astype(np.uint8)
        imageio.v3.imwrite(ruta_guardar,suma)
        i=Image.open(ruta_guardar)
        i=i.resize((500,400),)
        img=ImageTk.PhotoImage(i)
        imagen3.configure(image=img,text="")
    
    if cbx1.get()=="suma" and cbx2.get()=="YIQ Light":
        #global ruta_guardar
        suma=sum_Ligther_YIQ(im1,im2)
        suma=YIQ_a_RGB(suma).astype(np.uint8)
        
        imageio.v3.imwrite(ruta_guardar,suma)
        i=Image.open(ruta_guardar)
        i=i.resize((500,400),)
        img=ImageTk.PhotoImage(i)
        imagen3.configure(image=img,text="")
        
    if cbx1.get()=="suma" and cbx2.get()=="YIQ dark":
        #global ruta_guardar
        suma=sum_dark_YIQ(im1,im2)
        suma=YIQ_a_RGB(suma).astype(np.uint8)
        
        imageio.v3.imwrite(ruta_guardar,suma)
        i=Image.open(ruta_guardar)
        i=i.resize((500,400),)
        img=ImageTk.PhotoImage(i)
        imagen3.configure(image=img,text="")
    
    if cbx1.get()=="resta" and cbx2.get()=="RGB Promediado":
    
        suma=resta_rgb_prom(im1,im2)
        imageio.v3.imwrite(ruta_guardar,suma)
        i=Image.open(ruta_guardar)
        i=i.resize((500,400),)
        img=ImageTk.PhotoImage(i)
        imagen3.configure(image=img,text="")
        
    if cbx1.get()=="resta" and cbx2.get()=="RGB Cleampeado":
        
        suma=resta_rgb_clamp(im1,im2)
        imageio.v3.imwrite(ruta_guardar,suma)  
        i=Image.open(ruta_guardar)
        i=i.resize((500,400),)
        img=ImageTk.PhotoImage(i)
        imagen3.configure(image=img,text="")
    
    if cbx1.get()=="resta" and cbx2.get()=="YIQ Cleampeado":
           # global ruta_guardar
        suma=resta_YIQ_clamp(im1,im2)
        suma=YIQ_a_RGB(suma).astype(np.uint8)
        
        imageio.v3.imwrite(ruta_guardar,suma)
        i=Image.open(ruta_guardar)
        i=i.resize((500,400),)
        img=ImageTk.PhotoImage(i)
        imagen3.configure(image=img,text="")
        
    if cbx1.get()=="resta" and cbx2.get()=="YIQ Promediado":
        #global ruta_guardar
        suma=resta_YIQ_prom(im1,im2)
        suma=YIQ_a_RGB(suma).astype(np.uint8)
        imageio.v3.imwrite(ruta_guardar,suma)
        i=Image.open(ruta_guardar)
        i=i.resize((500,400),)
        img=ImageTk.PhotoImage(i)
        imagen3.configure(image=img,text="")
    
    
marco1=CTkFrame(root,fg_color=colorV)

marco2=CTkFrame(root,fg_color=colorV)
marco3=CTkFrame(root,fg_color=colorV)

cbx1=CTkComboBox(marco2,values=["suma","resta"])

lbl1=CTkLabel(marco2,text="Operacion: ")


cbx2=CTkComboBox(marco3,values=["RGB Cleampeado","RGB Promediado","YIQ Cleampeado","YIQ Promediado","YIQ Light","YIQ dark",])
lbl2=CTkLabel(marco3,text="Formato:  ")

lbl1.grid(row=0,column=0,padx=2)
cbx1.grid(row=0,column=1,padx=2)

lbl2.grid(row=0,column=0,padx=2)
cbx2.grid(row=0,column=1,padx=2)

def guardarimagen():
    global ruta_guardar
    imagen_guardar=Image.open(ruta_guardar)
        
    ruta=filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("Archivos de Imagenes",".bmp *,.png *")])
    imagen_guardar.save(ruta)
        
def salir():
    root.quit()

btn10=CTkButton(marco1,text="Procesar",command=operar)
btn20=CTkButton(marco1,text="Guardar",command=guardarimagen)
btn30=CTkButton(marco1,text="Salir",command=salir)
btn10.grid(row=0,column=0,padx=10,pady=10)
btn20.grid(row=0,column=1,padx=10,pady=10)
btn30.grid(row=0,column=2,padx=10,pady=10)

imagen1=CTkLabel(root,text="imagen 1")
imagen2=CTkLabel(root,text="Imagen 2")
imagen3=CTkLabel(root,text="imagen 3")

imagen1.grid(row=0,column=0,padx=5,pady=5)
imagen2.grid(row=0,column=1,padx=5,pady=5)
imagen3.grid(row=0,column=2,padx=5,pady=5)
btn1=CTkButton(root,text="Cargar Imagen 1",command = lambda:OpenFile1(imagen1))
btn2=CTkButton(root,text="Cargar Imagen 2",command = lambda:OpenFile2(imagen2))
#ubicacion de los elemento en la pantalla usando grid
#------------------------------------------
btn1.grid(row=1, column=0)
btn2.grid(row=1, column=1)
marco1.grid(row=1,column=2)
marco2.grid(row=2,column=0,padx=20,pady=35)
marco3.grid(row=2,column=1,padx=10,pady=35)
#-----------------------------------------
root.mainloop()