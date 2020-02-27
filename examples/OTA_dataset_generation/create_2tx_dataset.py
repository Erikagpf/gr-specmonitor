import os
import time
import signal
import subprocess
import _thread
import multiprocessing
import threading



#This code will generate the 2tx dataset, controlling 3 radios at the same time. It will use 2 of them with the dataset generator and the third one as an interference of the transmitted data.

def main():
    for i in ["run_ch2_wifi_1.sh","run_ch2_wifi_2.sh","run_ch2_wifi_3.sh","run_ch2_wifi_4.sh","run_ch2_wifi_5.sh","run_ch2_wifi_6.sh"]:
        #######First make it run the interference
        #inicio= sys.path[0]
        inter_path = "/home/connect/repo/y1_showcase/realtime_tx/run/"
        #print os.system("ls")
        #run_interference = os.system("./${i}")
        x = threading.Thread(target=os.system, args=("/home/connect/repo/y1_showcase/realtime_tx/run/"+i,)) #("ls", stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
        #x.communicate("ctvrnodepass")
        #print x.communicate()
        x.start()
        #p = os.popen(command, "w")
        #x.write("ctvrnodepass")
        time.time(100)
        ######Create the dataset for each interation
        
        

    
if __name__ == '__main__':
    main()
