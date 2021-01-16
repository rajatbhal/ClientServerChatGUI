########### NAME : RAJAT CHAUDHARY
########### STUDENT ID : 1001724370
##### all he comments are same for this as of client 2s
import tkinter
import socket
import time
import random
import threading
HEADERSIZE = 64
BUFRSIZE = 1024

def close_connection(sock, uname):
    sock.send(bytes("{} closed connection".format(uname), "utf-8"))
    sock.close()
    top.destroy()



def receive(sock, name):
    while True:
        try:
            msg = sock.recv(BUFRSIZE).decode("utf-8")
            text.insert("insert","\n{}".format(msg))
            if msg == "Pause":
                t = random.randint(3, 9)
                message = "{} waited for {} seconds".format(name, t)
                while t >= 0:
                    text.insert("insert","...{}".format(t))
                    time.sleep(1)
                    t -= 1

                text.insert("insert", "...Connection is resumed")
                sock.send(bytes(message, "utf-8"))
        except OSError:  # Possibly client has left the chat.
            break


def connect(event=None):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 1235))
    #text.insert("insert", "\nYou are now connected to server. Type exit and press enter to close connection\n")
    username = my_msg.get()
    my_msg.set("")  # Clears input field.
    if username:
        if username != "exit":
            #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #s.connect((socket.gethostname(), 1235))
            s.send(bytes(username, "utf-8"))
            text.insert("insert", "Hi {} !! Type exit and press enter to close\n".format(username))
            #text.insert("insert","{}".format(s))
            t1 = threading.Thread(target=receive, args=(s,username)).start()
            send_button.configure(state = tkinter.DISABLED)
        else:
            threading.Thread(target=close_connection, args = (s,username,)).start()


    else:
        text.insert("insert","Enter a username!!!")


    #send_button.configure(state = tkinter.DISABLED)


top = tkinter.Tk()
top.title("Client2")
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
button_label = tkinter.Label(top, text="Username")
button_label.pack()
entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", connect)
entry_field.pack()
send_button = tkinter.Button(top, text="Connect", command = connect)
send_button.pack()
quit_button = tkinter.Button(top, text="Resume")
quit_button.pack()
top.protocol("WM_DELETE_WINDOW")

tkinter.mainloop()