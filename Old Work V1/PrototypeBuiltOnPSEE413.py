import cv2
import time
import queue
import serial
import pathlib
import psee413
import datetime
import threading
import subprocess
import numpy as np
import neuromorphic_drivers as nd
import matplotlib.pyplot as plt

ser = serial.Serial('COM6', 115200)
time.sleep(2)
ser.write(("$H" + "\n").encode())  
ser.write(("G92 X0Y0" + "\n").encode())  
ser.write(("G90" + "\n").encode())  
ser.write(("G00 X200Y650" + "\n").encode())
time.sleep(5)

configuration = nd.prophesee_evk4.Configuration(
    biases=nd.prophesee_evk4.Biases(
        diff_off=0,
        diff_on=150,
    )
)

def read_psee(q, camera):
    global stopped, thread_active
    while not(stopped):
        evt = camera.all_packets()
        q.put(evt)
    thread_active = False

dirname = pathlib.Path(__file__).resolve().parent
camera = psee413.Camera(
    recordings_path = dirname / "recordings",
    log_path = dirname / "recordings" / "log.jsonl",
)
th_on = 115
diff = 80
th_off = 1
camera.set_parameters(
    psee413.Parameters(
        biases = psee413.Biases(
            diff_on = th_on,  # default 115
            diff = 80,
            diff_off = th_off,  # default 52
        )
    )
)

cv2.namedWindow("Events | q: quit")
cv2.moveWindow("Events | q: quit", 0, 0)

q = queue.Queue(maxsize=1)
stopped = False
paused = False
recording = False

cam_t = threading.Thread(target=read_psee, args=(q, camera))
cam_t.name = "psee_t"
cam_t.start()
thread_active = True

height = 720
width = 1280
img = np.ones((height, width), np.uint8)

check = 'Idle|WPos:0.000,0.000,0.000'
checkI= 'Idle'
iflag = 0
count = 0

while thread_active:
    events = q.get()
    
    if recording == True:
        count = count + 1
        if count > 1500:
            with open('C:\\Users\\Josh.F\\Desktop\\19317377\\PG\\Frame design\\Python\\position.gcode', 'r') as f:
                for line in f:
                    ser.write((line + "/r").encode())  # Send g-code block to grbl
                    pos=ser.readline()
                    pos=pos.decode("utf-8")
                    print(pos)

            if checkI not in pos:
                iflag = 1

            if checkI in pos and iflag == 1:
                camera.stop_recording()
                recording = False
                iflag = 0
                print("Recording off")
                render = ("python C:\\Users\\Josh.F\\Desktop\\19317377\\PG\\command_line_tools\\render.py C:\\Users\\Josh.F\\Desktop\\19317377\\PG\\psee413-main_orig\\psee413-main\\python\\recordings\\" + name)            
                #subprocess.call(render)            
       
    #####################################################################
    ### Camera stream
    #####################################################################
    if len(events) > 0 and not(paused):
        img.fill(128)
        img[events["y"], events["x"]] = events["on"].astype(np.uint64) * 255
        img = cv2.flip(img, -1)

        base = 20        
        onevt = np.sum(events["on"])/np.shape(events["on"])[0]
        ep2 = (base + 25, int(510-(400*(onevt))))
        img = cv2.rectangle(img, (base + 15,510), ep2, (255,0,0), -1)
        ep3 = (base + 40, int(510-(400*(1-onevt))))
        img = cv2.rectangle(img, (base + 30,510), ep3, (0,0,255), -1)
        ep4 = (base + 10, int(510-(400*(np.shape(events["on"])[0]/(1280*720)))))
        img = cv2.rectangle(img, (base,510), ep4, (0,0,0), -1)
        img = cv2.rectangle(img, (base,510), (base + 10,110), (0,0,0), 1)

        cv2.putText(img,('Reset Bias (2)' ),(base,25),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,255),2)
        cv2.putText(img,('On (7 and 4)' ) + str(th_on),(base,50),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,255),2)
        cv2.putText(img,('Diff (8 and 5)' ) + str(diff),(base,75),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,255),2)
        cv2.putText(img,( 'Off (9 and 6)') + str(th_off),(base,100),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,255),2)
        cv2.imshow("Events | q: quit", img)
    
    #####################################################################
    ### Set keyboard inputs
    #####################################################################
    c = cv2.waitKey(1) % 0x100            

    #####################################################################
    ### Quit/Pause output stream
    #####################################################################
    if c == ord("q"):
        stopped = True
    if c == ord(" "):
        paused = not(paused)

    #####################################################################
    ### Start gcode 
    #####################################################################
    if c == ord("g"):
        #ser.write(("G00 X10Y10" + "\n").encode()) 
        th_off += 1
        name = f'{datetime.datetime.now(tz=datetime.timezone.utc).isoformat().replace("+00:00", "Z"+ str(th_off) + "OFF" + str(th_on)+"ON").replace(":", "-")}.es'
        camera.start_recording_to(name)
        recording = True
        print("Recording to " + name)
        time.sleep(0.5)
        with open('C:\\Users\\Josh.F\\Desktop\\19317377\\PG\\Frame design\\Python\\startest.gcode', 'r') as f:
            for line in f:
                print('Sending: ' + line)
                ser.write((line + "\n").encode())  # Send g-code block to grbl
                time.sleep(0.1)

        count = 0
        
    #####################################################################
    ### Manual stop/start recoding
    #####################################################################
    if c == ord("r"):
        if recording:
            camera.stop_recording()
            recording = False
            print("Recording off")
        else:
            name = f'{datetime.datetime.now(tz=datetime.timezone.utc).isoformat().replace("+00:00", "Z").replace(":", "-")}.es'
            camera.start_recording_to(name)
            recording = True
            print("Recording to " + name)
            
    #####################################################################
    ### BIAS ADJUSTMENTS
    #####################################################################
    if c == ord("7") and th_on < 160:
        th_on += 1
        camera.set_parameters(
            psee413.Parameters(
                biases = psee413.Biases(
                    diff_on = th_on,
                    diff = diff,
                    diff_off = th_off,
                )
            )
        )
    if c == ord("4") and th_on > 85:
        th_on -= 1
        camera.set_parameters(
            psee413.Parameters(
                biases = psee413.Biases(
                    diff_on = th_on,
                    diff = diff,
                    diff_off = th_off,
                )
            )
        )
    if c == ord("8") and diff < 90:
        diff += 1
        camera.set_parameters(
            psee413.Parameters(
                biases = psee413.Biases(
                    diff_on = th_on,
                    diff = diff,
                    diff_off = th_off,
                )
            )
        )
    if c == ord("5") and diff > 70:
        diff -= 1
        camera.set_parameters(
            psee413.Parameters(
                biases = psee413.Biases(
                    diff_on = th_on,
                    diff = diff,
                    diff_off = th_off,
                )
            )
        )
    if c == ord("9") and th_off < 80:
        th_off += 1
        camera.set_parameters(
            psee413.Parameters(
                biases = psee413.Biases(
                    diff_on = th_on,
                    diff = diff,
                    diff_off = th_off,
                )
            )
        )
    if c == ord("6") and th_off > 1:
        th_off -= 1
        camera.set_parameters(
            psee413.Parameters(
                biases = psee413.Biases(
                    diff_on = th_on,
                    diff = diff,
                    diff_off = th_off,
                )
            )
        )
    if c == ord("2"):
        th_on = 115
        diff = 80
        th_off = 52
        camera.set_parameters(
            psee413.Parameters(
                biases = psee413.Biases(
                    diff_on = th_on,
                    diff = diff,
                    diff_off = th_off,
                )
            )
        )


        
        
cv2.destroyAllWindows()
cv2.waitKey(1)
ser.close() 

