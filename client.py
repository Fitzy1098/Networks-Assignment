import socket
import logging
import datetime
import time


    
def client():
    confirm=""
    total=0
    connect=""


    logging.basicConfig(filename='client.log', filemode="w", level=logging.INFO) #Initalises the log file with a level, name and write file mode

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(("127.0.0.1", 65432))
        except ConnectionRefusedError:
            return("Server Not Available")
        while True:
            
            while connect=="":
                print("Waiting for server to be free...")
                connect=s.recv(1024)
                connect=connect.decode()
            while True: 
                artist=input("Which artist are you interested in? ")
                s.send(artist.encode())
                start=time.time()
                confirm=s.recv(1024)
                confirm=confirm.decode()
                if confirm!="Artist Not in File":
                    break
                else:
                    print("Artist Not in File")
                    continue
            while True:
                data = s.recv(1024)
                data=data.decode()
                if data=="break":
                    end=time.time()
                    duration=end-start
                    logging.info("Date and Time: "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S" ))
                    logging.info("Server Response Length: "+str(total)+" bytes")
                    logging.info("Server Response Time: "+str(duration)+"s")
                    break
                else:
                    total+=len(data.encode('utf-8'))
                    print(data)
            dis=""
            while dis not in ["yes","no"]:
                dis=input("Would you like to disconnect? Yes/No ").lower()
            if dis=="no":
                s.send(dis.encode())
                continue
            if dis=="yes":
                s.send(dis.encode())
                print("Disconnected")
                break
            
        
client()
