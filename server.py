import socket
import logging
import datetime
import time


def getSongs(artist,dictionary):
    songs=dictionary[artist.lower()]  #Retrieves the list of songs associated with an artist
    return(songs)

def readFile():    
    file=open("100worst.txt","r")   #Opens the text file of songs and artists
    lineNum=0                      #Keeps track of the current line in the file
    data=[]                         #List of all artists and songs retrieved from file
    dictionary={}                   #Dictionary with artists as keys and a list of associated songs as values
    i=0
    for line in file.readlines():   #Iterates through the lines of the file
        if lineNum<112 and lineNum>5:   #Ignores the lines that don't list songs
            if line.endswith(("0\n","1\n","2\n","3\n","4\n","5\n","6\n","7\n","8\n","9\n")):    #Checks if rows end with a number and linebreak
                if lineNum==28:
                    line="21- Me and You and a Dog Named Boo  Lobo                          1971" ####Make it better if possible####
                line=line[4:len(line)-5].split("  ")            #Splits the song and artist
                for x in line:                                  #Iterates through the split line
                    if x!="" and  x!=" ":                       #Checks if x is not the artist or song
                        if x[0]==" ":                           #Checks if space at the start of string 
                            x=x[1:]                             #Removes the extra space, so all formatted similarly
                        data.append(x)                          #Adds song and artist to list of data
                
            else:                                               #For rows that end with a linebreak only
                line=line[4:len(line)-1].split("  ")            #Splits the song and artist
                for x in line:                                  #Iterates through the split line
                    if x!=""  and  x!=" ":                      #Checks if x is not the artist or song
                        if x[0]==" ":                           #Checks if space at the start of string
                            x=x[1:]                             #Removes the extra space, so all formatted similarly
                        data.append(x)                          #Adds song and artist to list of data
        lineNum+=1                                              #Increments line number
        
    while i<len(data)-1:                                        #Iterates through the list of data                                      
        artist=data[i+1].lower()                                #Retrieves the artist name and changes to lowercase, so key is more easy to find
        if artist in dictionary:                                #Checks if key already exists
            dictionary[artist].append(data[i])                  #If exists then append song to list of songs
        else:                                                   #If key doesn't already exist
            dictionary[artist]=[data[i]]                        #Create list for songs with the song in it
        i+=2                                                    #Inrements through the pairs of artist and songs
    file.close()                                                #Closes the file when done
    return dictionary

    
def host():
    data=""
    HOST='127.0.0.1'            #Host address
    PORT=65432                  #Port number
    
    logging.basicConfig(filename='server.log', filemode="w", level=logging.INFO)#Initalises the log file with a level, name and write file mode
 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST,PORT))                                     #Binds the host address to the port number
        except OSError:
            return("Port In Use")                                     #Binds the host address to the port number
        logging.info("Server Start Time: "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S" ))
        t=s.listen(5)
        
        while True:
            s.settimeout(30)
            try:
                conn, addr = s.accept()
            except socket.timeout:
                print("No Client Connections: Server Shutdown")
                logging.info("No More Client Connections Established")
                s.close()
                break
            s.settimeout(0)
            conn.send("Connected".encode())
            start = time.time()
            diction=readFile()
            logging.info("Client Request Time: "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S" ))
            with conn:
                print('Connected by', addr)
                logging.info("Connection Success")
                while True:
                    while True:
                        data = conn.recv(1024)
                        data=data.decode()
                        data=data.lower()
                        if data not in diction:
                            conn.send("Artist Not in File".encode())
                            continue
                        else:
                            conn.send("Artist in File".encode())
                            break
                    logging.info("Artist Name: " +data)
                    song=getSongs(data,diction)
                    songs=""
                    if not data:
                        break
                    else:
                        songs+="Request Received \n"
                        songs+="The associated songs are: \n"
                        for i in range (len(song)):
                            songs+="\n"
                            songs+=song[i]
                            songs+="\n"
                    conn.send(songs.encode())
                    conn.send("break".encode())
                    end = time.time()
                    duration=end-start
                    logging.info("Duration of Connection: "+str(duration)+"s")
                    dis = conn.recv(1024)
                    dis = dis.decode()
                    if dis.lower()=="yes":
                        break
                    else:
                        continue
                
host()                

                
                


    

