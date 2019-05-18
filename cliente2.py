from socket import socket #, error
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import Pyro4
#from threading import Thread
from hashlib import sha1
#import mysql.connector
#from tkinter import ttk
#from tkinter import filedialog
#import time
#from datetime import datetime
#from tkscrolledframe import ScrolledFrame

class Cliente(Frame):#, #Pyro4):

    def __init__(self, parent, server, sock):

        Frame.__init__(self, parent)
        self.sock = sock
        self.parent = parent
        self.initialize_user_interface()


        ###### ==== OJO TENGO LLAMODO EL METODO inicio_chat PARA EVITAR LOGIN EN PRUEBAS
        #self.inicio_chat()
        ##### ===== BORRAR LINEA ANTERIOR APENAS TERMINE DESARROLLO

        self.server = server
        self.font =  ('Helvetica', 13)

        #####======print(server.hola())     ASI PUEDO ACCEDER A LOS METODOS DEL SERVIDOR

    def initialize_user_interface(self):
        # self.frame = Frame(self.parent)
        self.parent.title("chatroom Python Tkinter")
        self.parent.geometry("300x150")
        # self.parent.grid_rowconfigure(0, weight=1)
        # self.parent.grid_columnconfigure(0, weight=1)
        self.parent.config(background="lavender")

        self.label_user = Label(self.parent, text=" Nombre de Usuario: ", anchor=W, background="dark slate gray",
                                foreground="white", font="Helvetica 8  bold")
        self.label_password = Label(self.parent, text="Clave:", anchor=W, background="dark slate gray",
                                    foreground="white", font="Helvetica 8  bold")

        self.label_user.grid(row=0, column=3, )
        self.label_password.grid(row=2, column=3, )

        self.dbuser = Entry(self.parent)
        self.dbpassword = Entry(self.parent, show="*")

        self.dbuser.grid(row=1, column=3, )
        self.dbpassword.grid(row=3, column=3, )

        self.connectb = Button(self.parent, text="Acceder", font="Helvetica 10 bold", command=self.dbconnexion)
        self.registrarse = Button(self.parent, text="Registrarse", font="Helvetica 10 bold",
                                  command=self.accionbtnregistrarse)

        self.registrarse.grid(row=4, column=2, )
        self.connectb.grid(row=4, column=4, )
        # self.cancelb.grid(row=2,column=2)

    def registroUser(self):
        self.actuser = Tk()
        self.actuser.wm_title("Crear Usuario")
        self.actuser.geometry("220x150")
        self.actuser.minsize(220, 150)
        self.actuser.maxsize(220, 150)
        # self.actuser.grid_rowconfigure(0, weight=3)
        self.actuser.grid_columnconfigure(2, weight=3)

        self.frame = Frame(self.actuser)
        self.frame.grid(row=0, column=0, columnspan=6, pady=20)
        # self.frame.grid_rowconfigure(2, weight=3)
        # self.frame.grid_columnconfigure(3, weight=1)
        self.label_email = Label(self.frame, text="Email: ", anchor=W, background="dark slate gray",
                            foreground="white", font="Helvetica 8  bold")
        self.label_contrasena = Label(self.frame, text="Contraseña:", anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")
        self.label_nombre = Label(self.frame, text="Nombre:", anchor=W,
                             background="dark slate gray",
                             foreground="white", font="Helvetica 8  bold")

        self.label_email.grid(row=0, column=0, pady=5, columnspan=1, sticky=N + S + W + E)
        self.label_contrasena.grid(row=1, column=0, pady=5, columnspan=1, sticky=N + S + W + E)
        self.label_nombre.grid(row=2, column=0, pady=5, columnspan=1, sticky=N + S + W + E)

        self.txtemail = Entry(self.frame)
        self.txtcontra = Entry(self.frame, show="*")
        self.txtnombre = Entry(self.frame)

        self.txtemail.grid(row=0, column=1, pady=5, columnspan=4, sticky=N + S + W + E)
        self.txtcontra.grid(row=1, column=1, pady=5, columnspan=4, sticky=N + S + W + E)
        self.txtnombre.grid(row=2, column=1, pady=5, columnspan=4, sticky=N + S + W + E)

        self.connectb = Button(self.frame, text="Crear", font="Helvetica 10 bold", command=self.dbregistrarse)

        self.connectb.grid(row=6, column=1, sticky=W)


    def accionbtnregistrarse(self):
        self.parent.destroy()
        self.registroUser() #abre ventana para registro de usuario

    def dbregistrarse(self):
        usuario = self.txtemail.get()
        #passw = self.txtcontra.get()
        passw = sha1(self.txtcontra.get().encode('utf-8')).hexdigest() ### ==== encriptación de contraseña
        nombre = self.txtnombre.get()
        #self.usuario = self.dbuser.get()
        #self.passw = self.dbpassword.get()

        if (usuario != "") and (passw != ""):
            self.datosUser = self.server.logup(usuario, passw, nombre)

            if self.datosUser == 0:
                #======== SI NO EXISTE, MENSAJE "USUARIO creado"
                messagebox.showinfo("Información", "Usuario Creado")
                self.actuser.destroy()
                self.inicio_chat()
            elif self.datosUser == 1:
                #============= si la contraseña y usuario existe, mensaje "usuario ya registrado"
                messagebox.showinfo("Información", "El Usuario Ya Existía")
                self.actuser.destroy()
                self.initialize_user_interface()
            elif self.datosUser == 2:
                # ======= si el user existe, mensaje "contraseña incorrecta"
                messagebox.showerror("error", "El usuario ya esta registrado, ingrese una contraseña valida")
                self.actuser.destroy()
                self.initialize_user_interface()
        else:
            messagebox.showerror("error", "Debe ingresar la informacióon requerida")
            self.actuser.destroy()
            self.registroUser()

    def dbconnexion(self):

        self.usuario = self.dbuser.get()
        # clave = self.dbpassword.get()
        self.passw = self.dbpassword.get() #s/////////////////////////// contraseña encriptada ////////////////////////////////////
        #self.passw = sha1(self.dbpassword.get().encode('utf-8')).hexdigest()
        # p = hashlib.new('md5', clave)
        # passw = p.hexdigest()
        #ip = socket.gethostbyname(socket.gethostname())
        if (self.usuario != "") and (self.passw != ""):
            self.datosUser = self.server.login(self.usuario, self.passw)
            #self.datosUser = respuesta_server
            #respuesta_server

            if self.datosUser != 0:
                print("si logeo")
                self.parent.destroy()
                self.inicio_chat()

            else:
                messagebox.showerror("error", "Usuario o Contraseña incorrecta")
                self.initialize_user_interface()
        else:
            messagebox.showerror("error", "Ingrese los datos solicitados")
            self.initialize_user_interface()


    def inicio_chat(self):  ####===================> esta función crea la ventana principal del chat =======

        self.master = Tk()
        self.master.geometry('700x400')
        self.master.minsize(700, 400)
        self.master.maxsize(700, 400)
        self.master.title("Sala Chat")

        ###=================================> MENU HORIZONTAL
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # acciones
        acciones = Menu(menu, tearoff=0)
        menu.add_cascade(label="Acciones", menu=acciones)
        acciones.add_command(label="Borrar Chat", command=self.clear_chat)
        acciones.add_separator()
        acciones.add_command(label="Salir", command=self.client_exit)

        ####========================================== FIN DE MENU HORIZONTAL

        # ========================================= INTERFAZ PRINCIPAL============================

        ###============= MARCO chat CONTIENEN TEXTBOX Y BOTONES
        chat = Frame(self.master, bd=6)
        chat.pack(expand=True, fill=BOTH, side=LEFT)

        # ======= lista donde se guardan los usuarios conectados
        list_logins = Frame(self.master, bd=0)
        label_logins = Label(list_logins, text="Usuarios Conectados: ", anchor=CENTER, background="dark slate gray",
                             foreground="white", font="verdana 10  bold", width=2)
        label_logins.pack(fill=BOTH)
        list_logins.pack(expand=True, fill=BOTH, side=RIGHT)
        logins_list = Listbox(list_logins, selectmode=SINGLE, font="Verdana 10",
                              exportselection=False, width=2)
        logins_list.bind('<<ListboxSelect>>', self.selected_login_event)

        text_frame = Frame(chat, bd=6)
        text_frame.pack(expand=True, fill=BOTH)

        # scrollbar for text box
        text_box_scrollbar = Scrollbar(text_frame, bd=0)
        text_box_scrollbar.pack(fill=Y, side=RIGHT)

        # contains messages
        text_box = Text(text_frame, yscrollcommand=text_box_scrollbar.set, state=DISABLED,
                        bd=1, padx=6, pady=6, spacing3=8, wrap=WORD, bg=None, font="Verdana 12", relief=GROOVE,
                        width=15, height=1)
        text_box.pack(expand=True, fill=BOTH)
        text_box_scrollbar.config(command=text_box.yview)

        # frame containing user entry field
        entry_frame = Frame(chat, bd=1)
        entry_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # entry field
        self.entry_field = Entry(entry_frame, bd=1, justify=LEFT)
        self.entry_field.pack(fill=X, padx=6, pady=6, ipady=3)
        # users_message = self.entry_field.get()

        # frame containing send button and emoji button
        send_button_frame = Frame(chat, bd=0)
        send_button_frame.pack(fill=BOTH)

        # send button
        send_button = Button(send_button_frame, text="Send", width=8, relief=GROOVE, bg='white',
                             bd=1, command=lambda: self.send_message(), activebackground="#FFFFFF",
                             activeforeground="#000000")
        send_button.pack(side=LEFT, ipady=2)
        self.master.bind("<Return>", self.send_message_event)

        # emoticons
        emoji_button = Button(send_button_frame, text="☺", width=5, relief=GROOVE, bg='white',
                              bd=1, command=self.emoji_options, activebackground="#FFFFFF",
                              activeforeground="#000000")
        emoji_button.pack(side=RIGHT, padx=6, pady=6, ipady=2)
        emoji_button.config(bg="#FFFFFF", fg="#000000", activebackground="#FFFFFF", activeforeground="#000000")


    def emoji_options(self):
        # Con Toplevel coloca coloca la venta sobre la anterior y es necesaria cerrarla para volver a la anterior ventana
        self.emoji_selection_window = Toplevel(bg="#FFFFFF", )
        self.emoji_selection_window.bind("<Return>", self.send_message_event)
        selection_frame = Frame(self.emoji_selection_window, bd=4, bg="#FFFFFF")
        selection_frame.grid()
        self.emoji_selection_window.focus_set()
        self.emoji_selection_window.grab_set()

        close_frame = Frame(self.emoji_selection_window)
        close_frame.grid(sticky=S)
        close_button = Button(close_frame, text="Close", font="Verdana 9", relief=GROOVE, bg="#FFFFFF",
                              fg="#000000", activebackground="#FFFFFF",
                              activeforeground="#000000", command=self.close_emoji)
        close_button.grid(sticky=S)

        root_width = self.master.winfo_width()
        root_pos_x = self.master.winfo_x()
        root_pos_y = self.master.winfo_y()

        position = '180x320' + '+' + str(root_pos_x + root_width) + '+' + str(root_pos_y)
        self.emoji_selection_window.geometry(position)
        self.emoji_selection_window.minsize(180, 320)
        self.emoji_selection_window.maxsize(180, 320)

        emoticon_1 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="☺",
                            activebackground="#FFFFFF", activeforeground="#000000",
                            font='Verdana 14', command=lambda: self.send_emoji("☺"), relief=GROOVE, bd=0)
        emoticon_1.grid(column=1, row=0, ipadx=5, ipady=5)
        emoticon_2 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="☻",
                            activebackground="#FFFFFF", activeforeground="#000000",
                            font='Verdana 14', command=lambda: self.send_emoji("☻"), relief=GROOVE, bd=0)
        emoticon_2.grid(column=2, row=0, ipadx=5, ipady=5)
        emoticon_3 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="☹",
                            activebackground="#FFFFFF", activeforeground="#000000",
                            font='Verdana 14', command=lambda: self.send_emoji("☹"), relief=GROOVE, bd=0)
        emoticon_3.grid(column=3, row=0, ipadx=5, ipady=5)
        emoticon_4 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="♡",
                            activebackground="#FFFFFF", activeforeground="#000000",
                            font='Verdana 14', command=lambda: self.send_emoji("♡"), relief=GROOVE, bd=0)
        emoticon_4.grid(column=4, row=0, ipadx=5, ipady=5)

        emoticon_5 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="♥",
                            activebackground="#FFFFFF", activeforeground="#000000",
                            font='Verdana 14', command=lambda: self.send_emoji("♥"), relief=GROOVE, bd=0)
        emoticon_5.grid(column=1, row=1, ipadx=5, ipady=5)
        emoticon_6 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="♪",
                            activebackground="#FFFFFF", activeforeground="#000000",
                            font='Verdana 14', command=lambda: self.send_emoji("♪"), relief=GROOVE, bd=0)
        emoticon_6.grid(column=2, row=1, ipadx=5, ipady=5)
        emoticon_7 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="❀",
                            activebackground="#FFFFFF", activeforeground="#000000",
                            font='Verdana 14', command=lambda: self.send_emoji("❀"), relief=GROOVE, bd=0)
        emoticon_7.grid(column=3, row=1, ipadx=5, ipady=5)
        emoticon_8 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="❁",
                            activebackground="#FFFFFF", activeforeground="#000000",
                            font='Verdana 14', command=lambda: self.send_emoji("❁"), relief=GROOVE, bd=0)
        emoticon_8.grid(column=4, row=1, ipadx=5, ipady=5)

        emoticon_9 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="✼",
                            activebackground="#FFFFFF", activeforeground="#000000",
                            font='Verdana 14', command=lambda: self.send_emoji("✼"), relief=GROOVE, bd=0)
        emoticon_9.grid(column=1, row=2, ipadx=5, ipady=5)
        emoticon_10 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="☀",
                             activebackground="#FFFFFF", activeforeground="#000000",
                             font='Verdana 14', command=lambda: self.send_emoji("☀"), relief=GROOVE, bd=0)
        emoticon_10.grid(column=2, row=2, ipadx=5, ipady=5)
        emoticon_11 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="✌",
                             activebackground="#FFFFFF", activeforeground="#000000",
                             font='Verdana 14', command=lambda: self.send_emoji("✌"), relief=GROOVE, bd=0)
        emoticon_11.grid(column=3, row=2, ipadx=5, ipady=5)
        emoticon_12 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="✊",
                             activebackground="#FFFFFF", activeforeground="#000000",
                             font='Verdana 14', command=lambda: self.send_emoji("✊"), relief=GROOVE, bd=0)
        emoticon_12.grid(column=4, row=2, ipadx=5, ipady=5)

        emoticon_13 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="✋",
                             activebackground="#FFFFFF", activeforeground="#000000",
                             font='Verdana 14', command=lambda: self.send_emoji("✋"), relief=GROOVE, bd=0)
        emoticon_13.grid(column=1, row=3, ipadx=5, ipady=5)
        emoticon_14 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="☃",
                             activebackground="#FFFFFF", activeforeground="#000000",
                             font='Verdana 14', command=lambda: self.send_emoji("☃"), relief=GROOVE, bd=0)
        emoticon_14.grid(column=2, row=3, ipadx=5, ipady=5)
        emoticon_15 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="❄",
                             activebackground="#FFFFFF", activeforeground="#000000",
                             font='Verdana 14', command=lambda: self.send_emoji("❄"), relief=GROOVE, bd=0)
        emoticon_15.grid(column=3, row=3, ipadx=5, ipady=5)
        emoticon_16 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="☕",
                             activebackground="#FFFFFF", activeforeground="#000000",
                             font='Verdana 14', command=lambda: self.send_emoji("☕"), relief=GROOVE, bd=0)
        emoticon_16.grid(column=4, row=3, ipadx=5, ipady=5)

        emoticon_17 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="☂",
                             activebackground="#FFFFFF", activeforeground="#000000",
                             font='Verdana 14', command=lambda: self.send_emoji("☂"), relief=GROOVE, bd=0)
        emoticon_17.grid(column=1, row=4, ipadx=5, ipady=5)
        emoticon_18 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="★",
                             activebackground="#FFFFFF", activeforeground="#000000",
                             font='Verdana 14', command=lambda: self.send_emoji("★"), relief=GROOVE, bd=0)
        emoticon_18.grid(column=2, row=4, ipadx=5, ipady=5)
        emoticon_19 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="❎",
                             activebackground="#FFFFFF", activeforeground="#000000",
                             font='Verdana 14', command=lambda: self.send_emoji("❎"), relief=GROOVE, bd=0)
        emoticon_19.grid(column=3, row=4, ipadx=5, ipady=5)
        emoticon_20 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="❓",
                             activebackground="#FFFFFF", activeforeground="#000000",
                             font='Verdana 14', command=lambda: self.send_emoji("❓"), relief=GROOVE, bd=0)
        emoticon_20.grid(column=4, row=4, ipadx=5, ipady=5)

        emoticon_21 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="❗",
                             activebackground="#FFFFFF", activeforeground="#000000",
                             font='Verdana 14', command=lambda: self.send_emoji("❗"), relief=GROOVE, bd=0)
        emoticon_21.grid(column=1, row=5, ipadx=5, ipady=5)
        emoticon_22 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="✔",
                             activebackground="#FFFFFF", activeforeground="#000000",
                             font='Verdana 14', command=lambda: self.send_emoji("✔"), relief=GROOVE, bd=0)
        emoticon_22.grid(column=2, row=5, ipadx=5, ipady=5)
        emoticon_23 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="✏",
                             activebackground="#FFFFFF", activeforeground="#000000",
                             font='Verdana 14', command=lambda: self.send_emoji("✏"), relief=GROOVE, bd=0)
        emoticon_23.grid(column=3, row=5, ipadx=5, ipady=5)
        emoticon_24 = Button(selection_frame, bg="#FFFFFF", fg="#000000", text="✨",
                             activebackground="#FFFFFF", activeforeground="#000000",
                             font='Verdana 14', command=lambda: self.send_emoji("✨"), relief=GROOVE, bd=0)
        emoticon_24.grid(column=4, row=5, ipadx=5, ipady=5)

    def send_emoji(self, emoticon):
        self.entry_field.insert(END, emoticon)

    def close_emoji(self):
        ## cierra ventana de emoticones
        self.emoji_selection_window.destroy()

    def send_message_event(self):
        """mensaje = self.entry_field.get()
        self.entry_field.set("")
        print(mensaje)
        print(self.self.sock)
        self.sock.send(bytes(mensaje, "utf-8"))"""
        pass

    def send_message(self):
        mensaje = self.entry_field.get()
        self.entry_field.delete(0, END)
        self.sock.send(bytes(mensaje, "utf-8"))

    def clear_chat(self):
        pass

    def client_exit(self):
        #######=============agregar aca un UPDATE EN tabla logs
        exit()

    def change_username(self):
        pass

    def selected_login_event(self):
        pass

    def cierra_ventana_chat(self):
        self.ventana.destroy()

    def enviar(self):
        pass

    def selected_login_event(self):
        pass

    def send_entry_event(self):
        pass

    def exit_event(self):
        pass

    """
    def recibir(self):
        while True:
            try:
                mensaje = cliente_socket.recv(1024).decode("utf-8")
                mensaje_lista.insert(END, mensaje)
                mensaje_lista.see(END)
            except OSError:
                break

    def enviar(self, event=None):
        mensaje = mi_mensaje.get()
        mi_mensaje.set("")
        cliente_socket.send(bytes(mensaje, "utf-8"))
        if mensaje == '{salir}':
            cliente_socket.close()
            ventana.quit()
    """

def main():
    s = socket()
    s.connect(("localhost", 35000))

    while True:
        output_data = input("Desea Ingresar a la Sala de Chat (S/N):  ")

        if output_data == 's' or output_data == 'S':

            try:
                s.send(output_data)
            except TypeError:
                s.send(bytes(output_data, "utf-8"))

            # Recibir respuesta.
            input_data = s.recv(1024)
            if input_data == bytes("1", "utf-8"):
                #servidor de nombres de Pyro4
                server = Pyro4.Proxy("PYRONAME:myServer")

                #instancia de de Tk
                root = Tk()

                #instancia de la clase Cliente con instancia de Tk y Pyro4
                app = Cliente(root, server, s)
                root.mainloop()
        else:
            print("Terminando Conexión")
            exit()


if __name__ == "__main__":
    main()