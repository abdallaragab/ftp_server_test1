from ftplib import FTP
import ftplib 
import re
import os
from datetime import datetime
import time
import threading
now = datetime.now()

server_file_found=False
local_file_found=False
server_connected=False


while(1):
        last_time_checked=now.time()
        try:
         print("trying to connect to update server...")
         myftp=FTP('192.168.1.10')
         myftp.login('admin','02967291a');
         server_connected=True
        except ftplib.all_errors:
            print("error connecting server")
        
        
        # myftp.retrlines('LIST');
        #search for the update file in the server
        if(server_connected):
            file_names= myftp.nlst()
            for i in range(0,len(file_names)):
                 #print("server"+file_names[i])  #list the server existing files
                 if(bool(re.match("update\d+\.\d+.txt",file_names[i]))):
                    server_file_name=file_names[i]
                    server_version_str=server_file_name[6:-4]
                    server_file_found=True
                    print("server file version is "+server_version_str)
                    break
        
        #asssume the update file name Consists of "update"+version number so the program
        #will compare the local file with the server file to check if there is an update
        
        
        
        #find the local version number
        local_files = os.listdir(os.getcwd())
        for i in range(0,len(local_files)):
            if(bool(re.match("update\d+\.\d+.txt",local_files[i]))):
                local_version_str=local_files[i][6:-4]
                print("local file version is "+local_version_str)
                local_file_found=True
                break
            
        
        

        
        
        
        
        #compare between the server file and the local file
        if(server_file_found):
            if((not local_file_found ) or((float(server_version_str)>float(local_version_str)))):
             with open(server_file_name, "wb") as file:
                 # use FTP's RETR command to download the file
                myftp.retrbinary(f"RETR {server_file_name}", file.write)
                print("Local file updated sucssfuly to "+server_version_str);
        
        
        
        server_file_found=False
        local_file_found=False
        if(server_connected):
             myftp.close();
             server_connected=False
   
        time.sleep(900.0);
        