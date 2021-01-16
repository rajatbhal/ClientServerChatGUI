######## NAME : RAJAT CHAUDHARY
######## STUDENT ID : 1001724370
import random
import socket
import threading
import tkinter
import re
import time

HEADERSIZE = 64
BUFRSIZE = 1024
connected_clients = []
clients = []
username_list = []

SERVER = socket.gethostbyname(socket.gethostname())
#### SOCK_STREAM is used as data flow in streams
### socket object s is created
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
## bind has been used to bind the ip address with the port number
s.bind((socket.gethostname(), 1235))
###main server idea i picked from https://github.com/effiongcharles/multi_user_chat_application_in_python/blob/master/server_gui.py

####calculation function perform the length conversion
def calculation(l,q):
    if q=="A":
        ###a contains formulas to convert the received input to desired format
        a = [ l / 1609.344, l * 1000, l * 100, l / 1000, l / 1.4960E+11]
        file1 = open("repository.txt", "a")
        file1.write("A = {}\n".format(a))
        file1.close()
    if q=="B":
        b = [l * 1.0936133, l / 3.0857E+16, l / 9.4607E+15, l * 39.3700787, l * 3.2808399]
        file1 = open("repository.txt", "a")
        file1.write("B = {}\n".format(b))
        file1.close()
    if q=="C":
        c = [l, l / 1852, l * 0.01094, l * 9.8425, l / 2.4]
        file1 = open("repository.txt", "a")
        file1.write("C = {}\n".format(c))
        file1.close()


def receive(incoming_socket, addr, clientslist):
    list1 = ['A', 'B', 'C']
    #client_msg = incoming_socket.recv(4096).decode("utf-8")
    while True:
        try:
            ##########will receive the incomin messages
            incoming_msg = incoming_socket.recv(4096).decode("utf-8")
            if incoming_msg != "exit" :
                text.insert("insert","\n{} : {}".format(addr,incoming_msg))
                len = re.findall("\d+\.\d+",incoming_msg)
                length = len[0]
                queue = incoming_msg[-1]
                text.insert("insert","\nLength in metres: {} Queue: {}".format(length,queue))
                ### thread is started to do manupulations
                threading.Thread(target=calculation, args=(float(length),queue)).start()
            else:
                incoming_socket.close()
                text.insert("insert","\n{} exited..\n".format(addr))
                for cl in clientslist:
                    if cl == addr:
                        #### if client exit the connection it'll get deleted from the list
                        clientslist.remove(cl)
                text.insert("insert","Connected Clients {}".format(clientslist))
        except OSError:
            break

def incoming_connections():
    while True:
        clientsocket, address = s.accept()
        clients.append(clientsocket)
        ####clients is the list that contains all the incomin sockets
        connected_clients.append(address)
        ####connected_clients contains the address of the clients
        text.insert("insert","Connected clients {}".format(connected_clients))

        welcome_msg = "Hi {} You are now connected to server..".format(address)
        clientsocket.send(bytes(welcome_msg,"utf-8"))

        threading.Thread(target=receive, args=(clientsocket, address, connected_clients)).start()


###start function is defined..the server will start listening
def start(event=None):
    s.listen(5)
    text.insert("insert", "Server has started on {}\n".format(SERVER))
    #### thread is started to listen to the incomin connections
    threading.Thread(target=incoming_connections).start()
    ### start server button gets disabled after the server is started
    start_button.configure(state=tkinter.DISABLED)


top = tkinter.Tk()
top.title("SERVER")
#####server gui is created wit the title SERVER
messages_frame = tkinter.Frame(top)
top.geometry("400x500")
#####geometry helps to define the size of the gui
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