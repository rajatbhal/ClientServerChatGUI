########### NAME : RAJAT CHAUDHARY
########### STUDENT ID : 1001724370
import random
## random is imported to select clients randomly
import socket
import threading
import tkinter
import time

HEADERSIZE = 64
BUFRSIZE = 1024
connected_clients = []
clients = []
username_list = []
SERVER = socket.gethostbyname(socket.gethostname())
#### SOCK_STREAM is used as data flow in strams
### socket object s is created
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
## bind has been used to bind the ip address with the port number
s.bind((socket.gethostname(), 1235))
##
###main server idea i picked from https://github.com/effiongcharles/multi_user_chat_application_in_python/blob/master/server_gui.py
# i wrote this function to deal with username conflict but it is not used here i thouht not to remove
def check_conflict(username, clientsocket):
    for name in username_list:
        if name == username:
            clientsocket.send(bytes("Use another username", "utf-8"))
            clientsocket.close()
        else:
            username_list.append(username)

## below funcion is to issue pause command at every 10 seconds
def pause_randomly(socket_list):
    time.sleep(10)
    #####this thread make sure pause command is issued every 10 seconds from https://stackoverflow.com/a/34589447
    threading.Timer(10, pause_randomly, args=(socket_list,)).start()
    conn = random.choice(socket_list)
    data = "Pause"
    conn.send(bytes(data, "utf-8"))


def receive(incoming_socket, addr):
    while True:
        try:
            ### encoding and decoding is used for sending and receiving messages format is utf-8
            name = incoming_socket.recv(BUFRSIZE).decode("utf-8")
            if name in username_list:
                incoming_socket.send(bytes("Type another username", "utf-8"))
                text.insert("insert", "{}".format(username_list))
            else:
                ######## username_list contains all the username
                username_list.append(name)
                text.insert("insert", "CONNECTED CLIENTS : {}".format(username_list))

            data = incoming_socket.recv(BUFRSIZE).decode("utf-8")
            ### if a user send exit then its username will be removed from the list and connection is closed
            if data == "exit":
                text.insert("insert", f"\n{addr} is closed\n")
                incoming_socket.close()
                del clients[incoming_socket]
                del username_list[name]
                text.insert("insert", "{}".format(username_list))
                text.insert("insert", "{}".format(clients))
        except OSError:  # Possibly client has left the chat.
            break


def incoming_connections():
    while True:
        clientsocket, address = s.accept()
        ## clients is the list of al the incoming sockets
        clients.append(clientsocket)

        msg = "Welcome to server!"
        #### connected_clients contains adress of the client ip and port number
        connected_clients.append(address)
        clients.append(clientsocket)
        clientsocket.send(bytes(msg, " utf-8"))
        #text.insert("insert", f"\nLIST OF CONNECTED CLIENTS : {connected_clients}")
        threading.Thread(target=pause_randomly, args=(clients,)).start()
        threading.Thread(target=receive, args=(clientsocket, address)).start()


def start(event=None):
    ## server will start to listen to the incoming connection
    s.listen(5)
    ## text.insert is used to insert any text to the ui
    text.insert("insert", "Server has started on {}".format(SERVER))
    ### differenet function are connected throuh threads below thread call function incoming connections
    t1 = threading.Thread(target=incoming_connections).start()
    start_button.configure(state=tkinter.DISABLED)


top = tkinter.Tk()
### server ui is creted titled Server
top.title("Server")
messages_frame = tkinter.Frame(top)
#geometry is used to define the size
top.geometry("400x500")
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()
text = tkinter.Text(master=msg_list)
text.pack()
### a start button is added to start the server on clickin it start function is called
start_button = tkinter.Button(top, text="Start Server", command=start)
start_button.pack()
### on clicking stop server button the window will close destroy is the function used to close tkinter gui
close_window = tkinter.Button(top, text="Stop Server", command=top.destroy)
close_window.pack()
top.protocol("WM_DELETE_WINDOW")

tkinter.mainloop()

