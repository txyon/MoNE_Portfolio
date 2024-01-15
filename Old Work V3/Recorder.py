# Import required dependencies into script
import csv                          
import time                         
import serial                       
import numpy as np                  
import neuromorphic_drivers as nd

# Function used to process recordings 
def save_to_csv(fname, packetdata, chunk_size=1000):
    with open(fname, 'w', newline='') as data:
        csv_writer = csv.writer(data)
        csv_writer.writerow(['t', 'x', 'y', 'on'])
        for i in range(0, len(packetdata), chunk_size):
            chunk = packetdata[i:i + chunk_size]
            csv_writer.writerows(chunk)
            data.flush()  

def grblpos():
    ser.flushInput() 
    ser.write(("?" + "\n").encode()) 
    pos=ser.readline()
    pos=pos.decode("utf-8")
    #print(pos)
    return pos

packetdata = []
done = 0
save = 0
error = 0
reclist={}
homing = 0
moving = 0
set200 = 0
set800 = 0
move200 = 0
move800 = 0
recording = 0
checkI= 'Idle|WPos:200.000,700.000,0.000'
checkII = 'Idle|WPos:800.000,700.000,0.000'

ser = serial.Serial('COM6', 115200)
time.sleep(2)

with open('C:\\Users\\Josh.F\\Desktop\\19317377\
          \\PG\\WorkingFolderV2\\gcode\\homing.gcode', 'r') as f:
    for line in f:
        print('Sending: ' + line)
        ser.write((line + "\n").encode())  
        time.sleep(0.1)

while True:
    pos = grblpos()
    if checkII in pos:
        homing = 1
        break

nd.print_device_list()

devices: list[nd.GenericDevice] = []
for listed_device in nd.list_devices():
    device = nd.open(serial=listed_device.serial)
    devices.append(device)

configuration = nd.prophesee_evk4.Configuration(
    biases=nd.prophesee_evk4.Biases(
        diff_off=255,
        diff_on=255,
    )
)

##############################################################################################################################

backlogs = np.array([0 for _ in devices])

while configuration.biases.diff_on > 1 and error == 0 and done == 0:
    try:
        index = np.argmax(backlogs)
        status, packet = devices[index].__next__()
        backlog = status.ring.backlog()
        print(f"{index}: {round(status.delay() * 1e6)} µs, backlog: {backlog} recording {recording} on_{configuration.biases.diff_on}")
        backlogs[:] += 1
        backlogs[index] = backlog

        pos = grblpos()

        if recording == 1:
            if 'dvs_events' in packet:
                packetdata.extend(packet['dvs_events'])
            
        if save == 1:
            fname = f"off_{configuration.biases.diff_off}_on_{configuration.biases.diff_on}"
            reclist[fname] = packetdata

            configuration.biases.diff_on -= 1 
            device.update_configuration(configuration)
            print(configuration.biases.diff_on)
            save = 0

        if checkI in pos and moving == 1:
            with open('C:\\Users\\Josh.F\\Desktop\\19317377\
                      \\PG\\WorkingFolderV2\\gcode\\c800.gcode', 'r') as f:
                for line in f:
                    print('Sending: ' + line)
                    ser.write((line + "\n").encode())  
                    time.sleep(0.5)
            
            recording = 0
            move800 = 1
            move200 = 0
            moving = 0
            save = 1

        if checkII in pos and moving == 1:
            ser.write(("G01 F3000 X200" + "\n").encode())  
            time.sleep(0.5)

            packetdata = []
            recording = 1
            move800 = 0
            move200 = 1
            moving = 0

        if checkI not in pos and move800 == 1:
            moving = 1

        if checkII not in pos and move200 == 1:
            moving = 1

        if homing == 1 and checkII in pos:
            moving = 1

        if configuration.biases.diff_on == 0:
            print('converting to csv, finished')
            done = 1
            for vname, vdata in reclist.items():
                print(vname)
                filename = f"{vname}.csv"
                save_to_csv(filename, vdata)
            break
            
    except RuntimeError:
        print('converting to csv, error')
        error = 1
        for vname, vdata in reclist.items():
            print(vname)
            filename = f"{vname}.csv"
            save_to_csv(filename, vdata)
        break

print('done')

            
                       


