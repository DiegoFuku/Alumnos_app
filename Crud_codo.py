from tkinter import *
from tkinter import messagebox
import sqlite3  as sq3 # importar la libreria que maneja la BD --> SQLite
import matplotlib.pyplot as plt
from time import sleep




'''
**************************
       PARTE FUNCIONAL
**************************
'''

#Conexion con la BBDD
def conectar():
    global con
    global cur
    sleep(1)
    con=sq3.connect("mi_db.db")
    cur=con.cursor()
    
    messagebox.showinfo("STATUS","Estas conectado a la BBDD")
#Salir
def salir():
     resp=messagebox.askquestion("CONFIRME","¿Desea salir de la aplicacion?")
   
     if resp=="yes":
        #con.close()
        raiz.destroy()

def mostrar_licencia():
     # CREATIVE COMMONS GNU GPL https://www.gnu.org/licenses/gpl-3.0.txt
    msg =  '''
    Demo de un sistema CRUD en Python para gestión 
    de alumnos
    Copyright (C) 2023 - Diego Dalinger
    Email: diegodalinger@gmail.com \n=======================================
    This program is free software: you can redistribute it 
    and/or modify it under the terms of the GNU General Public 
    License as published by the Free Software Foundation, 
    either version 3 of the License, or (at your option) any 
    later version.
    This program is distributed in the hope that it will be 
    useful, but WITHOUT ANY WARRANTY; without even the 
    implied warranty of MERCHANTABILITY or FITNESS FOR A 
    PARTICULAR PURPOSE.  See the GNU General Public License 
    for more details.
    You should have received a copy of the GNU General Public 
    License along with this program.  
    If not, see <https://www.gnu.org/licenses/>.'''
    messagebox.showinfo("LICENCIA", msg)

def mostrar_acercade():
    messagebox.showinfo("ACERCA DE...", "Creado por Diego Dalinger\Codo a Codo 4.0 - Big Data\nJunio, 2023\nEmail: diegodalinger@gmai")


#********Funciones varias**************

def buscar_escuelas(actualiza):
    con = sq3.connect('mi_db.db')
    cur = con.cursor()
    if actualiza:
        cur.execute('SELECT _id, localidad, provincia FROM escuelas WHERE nombre =?',(escuela.get(),))
    else: # esta opción sólo llena la lista de escuelas para el menú
        cur.execute('SELECT nombre FROM escuelas')
    
    resultado = cur.fetchall() # RECIBO LISTA DE TUPLAS con un elemento "fantasma"    
    retorno=[]
    for e in resultado:
        if actualiza:            
            provincia.set(e[2])
            localidad.set(e[1])
        esc = e[0]
        retorno.append(esc)
    con.close()
    return retorno

#Limpiar        
def limpiar():
    legajo.set("")
    apellido.set("")
    nombre.set("")
    email.set("")
    promedio.set("")
    grado.set("")
    escuela.set("Seleccione")
    localidad.set("")
    provincia.set("")
    legajo_input.config(state='normal')


#*****************CRUD **********

#Leer
def buscar_legajo():
    query_buscar ='''SELECT alumnos.legajo, alumnos.apellido, alumnos.nombre, alumnos.nota, alumnos.email,
    escuelas.nombre, escuelas.localidad, escuelas.provincia, alumnos.grado FROM alumnos INNER JOIN escuelas
    ON alumnos.id_escuela = escuelas._id WHERE alumnos.legajo= 
    '''
    cur.execute(query_buscar + legajo.get())
    resultado = cur.fetchall()
    if resultado == []:
        messagebox.showerror("ERROR", "Ese N° de legajo no existe")
        legajo.set("")
    else:
        for campo in resultado:
            legajo.set(campo[0])
            apellido.set(campo[1])
            nombre.set(campo[2])
            promedio.set(campo[3])            
            email.set(campo[4])
            escuela.set(campo[5])
            localidad.set(campo[6])
            provincia.set(campo[7])
            grado.set(campo[8])
            legajo_input.config(state='disabled')
#Crear
def crear():
    id_escuela=int(buscar_escuelas(True)[0])
    datos=id_escuela,legajo.get(),apellido.get(),nombre.get(),promedio.get(),email.get(),grado.get()
    cur.execute("INSERT INTO alumnos (id_escuela, legajo,apellido, nombre,nota,email,grado) VALUES(?,?,?,?,?,?,?)",datos)
    con.commit()
    messagebox.showinfo("status","Registro agregado a la BBDD")
    limpiar()

#Actualizar
def actualizar():
    id_escuela=int(buscar_escuelas(True)[0])
    datos=id_escuela, apellido.get(), nombre.get(), email.get(),grado.get(),promedio.get()
    cur.execute("UPDATE alumnos SET id_escuela=?, apellido=?, nombre=?, email=?, grado=?, nota=? where legajo="+legajo.get(),datos)
    con.commit()
    messagebox.showinfo("STATUS", "Registro actualizado en la BBDD")
    limpiar()
    
    
#Borrar
def borrar():
    
    resp=messagebox.askquestion("BORRAR","¿Desea eliminar el registro?")
    if resp=='yes':
        cur.execute("DELETE FROM alumnos WHERE legajo="+legajo.get())
        con.commit
        messagebox.showinfo("STATUS","Registro eliminado")
        limpiar()
# GRÁFICAS
# Por escuelas
def alumnos_en_escuelas():
    query_buscar='''SELECT COUNT(alumnos.legajo) as "total", escuelas.nombre from alumnos INNER JOIN escuelas ON alumnos.id_escuela=escuelas._id GROUP BY escuelas.nombre ORDER BY total DESC '''
    cur.execute (query_buscar)
    resultado=cur.fetchall()
   # print(resultado)

    cuenta=[]
    escuela=[]
    for i in resultado:
        cuenta.append(i[0])
        escuela.append(i[1])
    #print(cuenta)
    #print(escuela)
    
    plt.scatter(escuela, cuenta)
    plt.xticks(rotation=90)
    plt.title("Alumnos por escuelas")
    plt.show()

# Alumnos por grado

def alumnos_por_grado():
    query='''SELECT COUNT (alumnos.legajo) as "alumnos_totales", grado from alumnos group by grado;'''
    cur.execute (query)
    resultado=cur.fetchall()
    
    cantidad_alumnos=[]
    grado=[]

    for i in resultado:
        cantidad_alumnos.append(int(i[0]))
        grado.append(str(i[1]))
        
        
    plt.bar(grado, cantidad_alumnos)
    plt.xticks(rotation=90)
    plt.title("Alumnos por Grados")
    plt.show()
    




#Notas 
def Notas_escuelas():
    
    query='''SELECT avg(alumnos.nota) as promedio, escuelas.nombre from alumnos INNER JOIN escuelas on alumnos.id_escuela= escuelas._id GROUP By escuelas.nombre ORDER BY promedio DESC; '''
    cur.execute(query)
    resultado=cur.fetchall()

    promedios=[]
    escuelas=[]

    for i in resultado:
        promedios.append(round(i[0],2))
        escuelas.append(i[1])

    plt.bar(escuelas, promedios )
    plt.title("Promedio notas por escuelas")
    plt.xticks(rotation=90)
    plt.show()
   



#Ventana  y funcion login

def ventana_log():
    global ventana_loguin
    
      
    pestas_color="DarkGray"
    ventana_loguin=Tk()
    ventana_loguin.geometry("400x350")
    ventana_loguin.title("Login")
    Label(ventana_loguin,text="Escoja su opcion",bg="lightgreen",width="300",height="2",font=("Calibri",13)).pack()
    Label(ventana_loguin,text="").pack()
    Button(ventana_loguin,text="Acceder",height="2",width="30",bg=pestas_color,command=login).pack()
    Label(ventana_loguin,text="").pack()
    Button(ventana_loguin, text="Regsitrarse",height="2",width="30",bg=pestas_color,command=registro).pack()
    Label(ventana_loguin,text="").pack()
    
    ventana_loguin.mainloop()


def registro():
    global ventana_registro
    ventana_registro= Toplevel(ventana_loguin)
    ventana_registro.title=("Registro")
    ventana_registro.geometry("300x250")
    
    global nombre_usuario
    global clave
    global entrada_nombre
    global entrada_clave
    nombre_usuario=StringVar()
    clave=StringVar()
    
    Label(ventana_registro, text="Introduzca datos",bg="lightgreen").pack()
    Label(ventana_registro,text="").pack()
    etiqueta_nombre=Label(ventana_registro,text="Nombre de Usuario * " )
    etiqueta_nombre.pack()
    entrada_nombre=Entry(ventana_registro, textvariable=nombre_usuario)
    entrada_nombre.pack()
    entiqueta_clave=Label(ventana_registro,text="Contraseña * " )
    entiqueta_clave.pack()
    entrada_clave=Entry(ventana_registro,textvariable=clave, show="*")
    entrada_clave.pack()
    Label(ventana_registro,text="").pack()
    Button(ventana_registro,text="Registrarse",width=10,height=1,bg="lightgreen",command=registro_usuario).pack()
    
def registro_usuario():
    usuario_info= entrada_nombre.get()
    clave_info=entrada_clave.get()
    
    with open("CRUD.txt","w") as file:
        file.write(usuario_info + "\n") 
        file.write(clave_info)
        file.close()
        
        
    
    entrada_nombre.delete(0,END)
    entrada_clave.delete(0,END)
    
    Label(ventana_registro,text="Registro completado con Exito",fg="Green",font=("calibri",11)).pack()


def login():
    global login_ventana
    login_ventana= Toplevel(ventana_loguin)
    login_ventana.title("Acceso a la Cuenta")
    login_ventana.geometry("300x250")
    Label(login_ventana,text="Introduzca su nombre de usuario y contraseña").pack()
    Label(login_ventana,text="").pack()
    
    global verifica_usuario
    global verifica_clave
    
    verifica_usuario =StringVar()
    verifica_clave =StringVar()
    
    global entrada_login_usuario
    global entrada_login_clave
    
    Label(login_ventana,text="Nombre Usuario * ").pack()
    entrada_login_usuario= Entry(login_ventana, textvariable=verifica_usuario)
    entrada_login_usuario.pack()
    Label(login_ventana,text="").pack()
    Label(login_ventana,text="Contraseña * ").pack()
    entrada_login_clave=Entry(login_ventana,textvariable=verifica_clave,show="*")
    entrada_login_clave.pack()
    Label(login_ventana,text="").pack()
    Button(login_ventana,text="Acceder",width=10,height=1,command=verifica_login).pack()
    
    
def verifica_login():
    usuario1=entrada_login_usuario.get()
    clave1=entrada_login_clave.get()
    
    
 
    
    
    with open("CRUD.txt","r")as f:
        lineas=(f.readlines())
        if usuario1==(lineas[0].strip()):
            
            if clave1==(lineas[1].strip()):
                exito_login()
                conectar()
                
                
                
            else:
                no_clave()
        else:
            no_usuario()
                  
        
    entrada_login_usuario.delete(0,END)
    entrada_login_clave.delete(0,END)

def no_usuario():
    global ventana_no_usuario
    ventana_no_usuario = Toplevel(login_ventana)
    ventana_no_usuario.title("Error")
    ventana_no_usuario.geometry("150x100")
    Label(ventana_no_usuario,text="Usuario inexistente").pack()
    Button(ventana_no_usuario,text="ok",command=borrar_no_usuario).pack()
    
def exito_login():
    global ventana_exito
    ventana_exito= Toplevel(login_ventana)
    ventana_exito.title("Exito")
    ventana_exito.geometry("250x100")
    Label(ventana_exito,text="Login finalizado con exito").pack()
    Button(ventana_exito,text="OK",command=borrar_exito_login).pack()
    
    
def no_clave():
    global ventana_no_clave
    ventana_no_clave=Toplevel(login_ventana)
    ventana_no_clave.title("Error")
    ventana_no_clave.geometry("150x100")
    Label(ventana_no_clave,text="contraseña incorrecta ").pack()
    Button(ventana_no_clave,text="OK",command=borrar_no_clave).pack()

def borrar_exito_login():
    ventana_loguin.destroy()
    
def borrar_no_clave():
    ventana_loguin.destroy()
    
def borrar_no_usuario():
    ventana_loguin.destroy() 
    
#Fin Ventana Login------------------------------    


'''
**************************
INTERFAZ GRÁFICA
**************************
'''
#color Framecampos
color_fondo='cyan'
color_letra='black'
#color framebotones
fondo_framebotones='plum'
color_fondo_boton='black'
color_texto_boton=fondo_framebotones

raiz=Tk()
raiz.title('Python CRUD-Comision 23203')
#BARRA MENU
barramenu=Menu(raiz)
raiz.config(menu=barramenu)
#MENU BBDD
bbddmenu=Menu(barramenu, tearoff=0)
bbddmenu.add_command(label='Login',command=ventana_log)
bbddmenu.add_command(label='Salir', command=salir)

#Estadísticas
estadmenu=Menu(barramenu,tearoff=0)
estadmenu.add_command(label='Alumnos por Escuela',command=alumnos_en_escuelas)
estadmenu.add_command(label='Calificaciones',command=Notas_escuelas)
estadmenu.add_command(label='Alumnos por Grado', command=alumnos_por_grado)
#Menu Limpiar
limpiarmenu=Menu(barramenu,tearoff=0)
limpiarmenu.add_command(label='Limpiar campos', command=limpiar)
#Menu Acerca de
ayudamenu=Menu(barramenu,tearoff=0)
ayudamenu.add_command(label='Licencia', command=mostrar_licencia)
ayudamenu.add_command(label='Acerca de..', command=mostrar_acercade)

barramenu.add_cascade(label='BBDD',menu=bbddmenu)
barramenu.add_cascade(label='Gráficas',menu=estadmenu)
barramenu.add_cascade(label='Limpiar',menu=limpiarmenu)
barramenu.add_cascade(label='Acerca de',menu=ayudamenu)



#---------FRAME CAMPOS-----------
framecampos=Frame(raiz)
framecampos.config(bg=color_fondo)
framecampos.pack(fill='both')
'''
"STICKY"
     n
  nw   ne
w         e
  sw   se
     s
'''
#LABELS
def config_label(mi_label,fila):
    espaciado_labels={'column':0,'sticky':'e', 'padx':10, 'pady':10}
    mi_label.config(bg=color_fondo, fg=color_letra)
    #mi_label.grid(row=fila, column=0, sticky='e', padx=10, pady=10)
    mi_label.grid(row=fila, **espaciado_labels)


legajo_label=Label(framecampos,text='N° de Legajo')
#legajo_label.grid(row=0, column=0, sticky='e', padx=10, pady=10)
config_label(legajo_label,0)

apellido_label=Label(framecampos,text='Apellido')
#apellido_label.grid(row=1, column=0, sticky='e', padx=10, pady=10)
config_label(apellido_label,1)

nombre_label=Label(framecampos,text='Nombre')
config_label(nombre_label,2)

email_label=Label(framecampos,text='Email')
config_label(email_label,3)

promedio_label=Label(framecampos,text='Promedio')
config_label(promedio_label,4)

grado_label=Label(framecampos,text='Grado')
config_label(grado_label,5)

escuela_label=Label(framecampos,text='Escuelal')
config_label(escuela_label,6)

localidad_label=Label(framecampos,text='Localidad')
config_label(localidad_label,7)

Provincia_label=Label(framecampos,text='Provincia')
config_label(Provincia_label,8)


'''
entero = IntVar()  # Declara variable de tipo entera
flotante = DoubleVar()  # Declara variable de tipo flotante
cadena = StringVar()  # Declara variable de tipo cadena
booleano = BooleanVar()  # Declara variable de tipo booleana
'''
#INPUTS
legajo=StringVar()
apellido=StringVar()
nombre=StringVar()
email=StringVar()
promedio=DoubleVar()
grado=StringVar()
escuela=StringVar()
localidad=StringVar()
provincia=StringVar()

def config_input(mi_input, fila):
    espaciado_input={'column':1, 'padx':10, 'pady':10}
    mi_input.grid(row=fila, **espaciado_input)


legajo_input=Entry(framecampos,textvariable=legajo)
#legajo_input.grid(row=0, column=1,padx=10, pady=10)
config_input(legajo_input,0)

apellido_input=Entry(framecampos,textvariable=apellido )
#apellido_input.grid(row=1, column=1,padx=10, pady=10)
config_input(apellido_input,1)

nombre_input=Entry(framecampos,textvariable=nombre )
config_input(nombre_input,2)

email_input=Entry(framecampos,textvariable=email )
config_input(email_input,3)

promedio_input=Entry(framecampos,textvariable=promedio )
config_input(promedio_input,4)

grado_input=Entry(framecampos,textvariable=grado )
config_input(grado_input,5)
#Input de escuelas con opciones para elegir

escuelas=buscar_escuelas(False)
escuela.set('Seleccione escuela')
escuela_option=OptionMenu(framecampos,escuela,*escuelas)
escuela_option.grid(row=6, column=1, padx=10, pady=10, sticky='w', ipadx=40)

localidad_input=Entry(framecampos,textvariable=localidad )
config_input(localidad_input,7)
localidad_input.config(state='readonly')

provincia_input=Entry(framecampos,textvariable=provincia )
config_input(provincia_input,8)
provincia_input.config(state='readonly')

#Frame Botones >FUNCIONES CRUD (create, read, update, delete)
framebotones=Frame(raiz)
framebotones.config(bg=fondo_framebotones)
framebotones.pack(fill='both')
def config_button(mi_button, column):
      mi_button.config(bg=color_fondo_boton,fg=color_texto_boton)
      mi_button.grid(row=0, column=column, padx=5, pady=10, ipadx=7)

boton_crear=Button(framebotones,text='Crear',command=crear)
#boton_crear.grid(row=0, column=0, padx=5, pady=10, ipadx=7)
config_button(boton_crear,0)

boton_buscar=Button(framebotones,text='Buscar',command=buscar_legajo)
config_button(boton_buscar,1)

boton_actualizar=Button(framebotones,text='Actualizar',command=actualizar)
config_button(boton_actualizar,2)

boton_borrar=Button(framebotones,text='Borrar',command=borrar)
config_button(boton_borrar,3)

# FRAME DEL PIE
framecopy = Frame(raiz)
framecopy.config(bg='black')
framecopy.pack(fill='both')

copylabel = Label(framecopy, text="(2023) por Diego Dalinger para CaC 4.0 - Big Data")
copylabel.config(bg='black',fg='white')
copylabel.grid(row=0, column=0, padx=10, pady=10)





raiz.mainloop()

