###### NAME : RAJAT CHAUDHARY
###### STUDENT ID : 1001724370
###all the clients prorams are same i have mentioned comments only in this
###  https://github.com/effiongcharles/multi_user_chat_application_in_python/blob/master/client_gui.py
###tkinter gui is same
import tkinter
import socket
import time
import random
import threading

# network client

HOST_PORT = 1235
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(),HOST_PORT))

####view_message function is invoked when view messagge button is clicked
def view_message():
    msg = my_msg.get()
    my_msg.set("")
    #####text file is opened and read
    file1 = open("repository.txt","r+")
    with open("repository.txt") as f:
        if "{} = ".format(msg) in f.read():
            pass
        else:
            text.insert("insert","\nNo message to display")

    for line in file1:
        if line.startswith("{} = ".format(msg)):
            text.insert("insert","\n{}".format(line))
            ########the text file is opened in read mode and then in write mode
            with open("repository.txt", "r") as f:
                lines = f.readlines()
            with open("repository.txt", "w") as f:
                for line in lines:
                    if line.startswith("{} = ".format(msg)):
                        pass
                    else:
                        f.write(line)

        else:
            pass

def receive_msg_from_server(client):
    while True:
        try:
            #######receive message from server and display it on the client gui
            msg = client.recv(4096).decode("utf-8")
            text.insert("insert","{}".format(msg))
        except OSError:
            break

###this function is called when send message button is clicked
def send_msg(event=None):
    msg = my_msg.get()
    my_msg.set("")
    client.send(bytes(msg,"utf-8"))
    ####if client user type exit and enter then client ui will et closed
    if msg == "exit":
        top.destroy()

top = tkinter.Tk()
top.title("CLIENT")
messages_frame = tkinter.Frame(top)
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
entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send_msg)
entry_field.pack()
####send message button to send message
send_button = tkinter.Button(top, text="Send message", command =send_msg)
send_button.pack()
####view message button is used to view messages
view_button = tkinter.Button(top,text="View message", command = view_message)
view_button.pack()
text.insert("insert","CONNECTED..exit and press enter to exit")
text.insert("insert","\nTo Send message type LengthQueue ex. 3.29B\n")
text.insert("insert","To View message type Queue ex. A")


top.mainloop()

