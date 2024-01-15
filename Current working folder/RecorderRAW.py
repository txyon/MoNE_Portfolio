### Dependencies
import time                        
import serial
import neuromorphic_drivers as nd

### Function that returns the position of the camera within the xy plane  
def grblpos():
    ser.flushInput()                        # Clears any waiting input commands
    ser.write(("?" + "\n").encode())        # Sends ? to through serial requesting status
    pos=ser.readline()                      # Loads status in byte form
    pos=pos.decode("utf-8")                 # Decodes bytes to unicode string
    return pos                              # Returns position in variable "pos"

### Variables and flags
output = None                               # File update, if not none a file is open for packets from camera
done = 0                                    # Program is finished 
save = 0                                    # If = 1 a file has been saved and closed 
error = 0                                   # Timeout or assertion error will force end program
homing = 0                                  # Flag for homing status of GRBL machine      
moving = 0                                  # Flag indicating movement 
move200 = 0                                 # Current moving towards X200
move800 = 0                                 # Current moving towards X800
recording = 0                               # Recording status
checkI = 'Idle|WPos:200.000,700.000,0.000'  # (End) String to check against camera actual position (X200)
checkII = 'Idle|WPos:800.000,700.000,0.000' # (Start) String to check against camera actual position (X800)

### Serial initilisation
ser = serial.Serial('COM4', 115200)         # Connect to GRBL serial device in COM4
time.sleep(2)                               # Wait 2s for connection to establish

### Open and start homing process
with open('WorkingFolderV3\gcode\homing.gcode', 'r') as f:
    for line in f:                          # Read each line consecutively from gcode file
        print('Sending: ' + line)           # Print in terminal line sent
        ser.write((line + "\n").encode())   # Send line information to GRBL to excute
        time.sleep(0.1)                     # Wait 100ms to send next line 

### Safety check that homing is complete
while True:
    pos = grblpos()                         # Check GRBL status
    if checkII in pos:                      # Comparing current position with desired at CheckII
        homing = 1                          # Set homing to 1 when actual and desired are the same
        break                               # Exit while loop

### Set initial parameters for diff_off and diff_on settings using the neuromorphic drivers module
configuration = nd.prophesee_evk4.Configuration(
    biases=nd.prophesee_evk4.Biases(
        diff_off=255,                       #73  default
        diff_on=255,                        #102 default
    )
)

####################################################################################################################
### STATE_MACHINE ###
####################################################################################################################

# Open connection with camera recording using RAW data
with nd.open(raw=True) as device:
    # Contine in loop until finished or error * can set custom end points cahnging the configuration bias
    while configuration.biases.diff_on >= 0 and error == 0 and done == 0:       
        try:
            status, packet = device.__next__()              # Load status and event packet information from camera
            pos = grblpos()                                 # Check position of camera within the XY plane

            if recording == 1:                              # If recording is set
                output.write(packet)                        # Write packet data to current open output file
                
            if save == 1:                                   # If save is set    
                configuration.biases.diff_on -= 1           # Decrease diff_on bias (Increase sensitivity)
                device.update_configuration(configuration)  # Send new bias configuration to camera 
                print(configuration.biases.diff_on)         # Print new bias value in terminal
                save = 0                                    # Reset save 

            if checkI in pos and moving == 1:               # Check camera is at the end position and that it has moved 
                with open('WorkingFolderV3\gcode\c800.gcode', 'r') as f:
                                                            # Open start position file 
                    for line in f:                          # Read each line consecutively from gcode file
                        print('Sending: ' + line)           # Print in terminal line sent
                        ser.write((line + "\n").encode())   # Send line information to GRBL to excute
                        time.sleep(0.5)                     # Wait 500ms to send next line 
                
                output.close()                              # End connection with recording file
                output = None                               # Clear output
                recording = 0                               # Reset recording 
                move800 = 1                                 # Set move800 (move to start)
                move200 = 0                                 # Reset move200 
                moving = 0                                  # Reset moving 
                save = 1                                    # Set save

            if checkII in pos and moving == 1:              # Check camera is at the start position and it has moved
                ser.write(("G01 F3000 X200" +"\n").encode())# Send sinle line command to GRBL to move camera to X200  
                time.sleep(0.5)                             # Wait 500ms before continuing

                assert output is None                       # Confirm output has been reset before opening new file
                output = open(f"off_{configuration.biases.diff_off}_on_{configuration.biases.diff_on}", "wb")
                                                            # Open new file in current directory with name reflecting current bias settings writing in bytes 
                recording = 1                               # Set recording                             
                move800 = 0                                 # Reset move800
                move200 = 1                                 # Set move200(move to finish)
                moving = 0                                  # Reset moving 

            if checkI not in pos and move800 == 1:          # Check camera has left end position and move to start (move800) has been sent
                moving = 1                                  # Set moving

            if checkII not in pos and move200 == 1:         # Check camera has left start position and move to end (move200) has been sent
                moving = 1                                  # Set moving

            if homing == 1 and checkII in pos:              # Check camera has reached starting position after homing completed 
                moving = 1                                  # Set moving
                homing = 2                                  # Set homing to 2 so this statement cannot force moving to set
                
        except RuntimeError:                                # In the event that the camera experiences excessive events causing excess time in the USB transfer a timeout error will occur
            print('error')                                  # Print that recording entered into error state 

    print('done')                                           # Programed finished

