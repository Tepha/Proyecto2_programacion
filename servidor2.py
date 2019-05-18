import socket
from socket import socket, error
from threading import Thread
import Pyro4


clientes = ["undo", "tras"]
@Pyro4.expose
class Servidor(Thread):
    def __init__(self, conn, addr, model):
        # Inicializar clase padre.
        Thread.__init__(self)

        self.conn = conn
        self.addr = addr
        self.model = model

        print(clientes)
        #print(model.holamundo())#######===== ASI PUEDO ACCEDER A LOS METODOS DEL MODELO


    def run(self):
        while True:
            try:
                # Recibir datos del cliente.
                input_data = self.conn.recv(1024)
                print(input_data)
                # Reenviar la información recibida.
                if input_data == bytes("s", "utf-8") or input_data == bytes("S", "utf-8"):
                    msg = '1'
                else:
                    msg = '0'

                self.conn.send(bytes(msg, "utf-8"))
            except error:
                print("[%s] Error de lectura." % self.name)
                break

    def login(self, user, passw):
        result = self.model.consultaUser(user,passw,self.addr)
        return result

    def logup(self, user, passw, nombre):
        datosUser = self.model.consultaUser(user,passw,self.addr)
        if datosUser != 0:
            result = 1 #el usuario existia
        else:
            #result  = 0 #el usuario no existe y se registro
            respuesta = self.model.agregarUser(user, passw, nombre)
            if respuesta == "ok":
                result = 0 #usuario no existia y se registro
            else:
                result = 2 #el usuario existe, no se registra
        return result


def main():
    s = socket()

    # Escuchar peticiones en el puerto 35000.
    s.bind(("localhost", 35000))
    s.listen(10)


    while True:
        #instanciando modelo con procedimientos remotos del modelo
        model = Pyro4.Proxy("PYRONAME:myModel")

        conn, addr = s.accept()
        #addr.setblocking(False)
        c = Servidor(conn, addr, model)
        c.start()
        print("%s:% d se ha conectado." % addr)


        daemon = Pyro4.Daemon()
        ns = Pyro4.locateNS()
        uri = daemon.register(c)
        ns.register("myServer", uri)
        print(uri)     ###==== IMPRIME LA URI PARA QUE PUEDAN ACCEDER REMOTAMENTE A SUS METODOS
        daemon.sockets

        #daemon.requestLoop()##==== BUSCAR  EN QUE MOMENTO DETENER EL LOOP CON  "loopCondition="


if __name__ == "__main__":
    main()