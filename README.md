# Hey! Are you seeing this? Space-based object detection optimisation with neuromorphic cameras 

## Design, Hardware and Control
This experiment aims to track the effects manipulating a neuromorphic camera's biases has on object detection. The concept was to have a neuromorphic camera move across a replicated star cluster or vice versa in a controlled low-light environment. The initial proposal for this design had a fixed camera mounted in the centre of two rings, as seen below in Figure 1 (Left). The concept's inner ring would have a star pattern drilled into it. Two light sources are mounted between the first and second rings and are orientated to illuminate the area between the rings in line with the camera. The inner ring would then be driven to create events across the camera sensor. Due to its complexity of recreating an accurate star map on the curved surface and the limitation of the room being restricted by the size of the inner ring, this design was inadequate.

A redesign of the original concept led to the final design. The design allowed for versatility in mounting options and adjustable heights. These improvements also allowed the star map to be projected from a flat surface, making recreation much more straightforward.


<p align="center">
  <img src="ImagePlots/FirstDesign.JPG" alt="Image 1" style="height: 300px;">
  <img src="ImagePlots/FinalDesign.JPG" alt="Image 2" style="height: 300px;">
</p>


One of the techniques taught in the neuromorphic sensing unit was lens selection and Field of View (FOV). Below is a table covering three lenses at three different rudimentary distances from the star map. As the camera would be passing over the "stars" in the y direction, it was necessary to tune the physical dimensions to this. Ideally, the single stand light should show as a single pixel. With this assumption, using the stand thickness of 0.4mm, a desired FOV in the y direction is calculated by multiplying 0.4 by 720 (sensor pixel height), returning 288mm. The distance between the lens and lights could not be tuned to achieve a measurement as close to this. The actual FOV achieved on the y-axis using a 12mm lens was 259mm due to the constraints in the fixed point height adjustments.

| Lens | Distance(mm) | Height(mm) | Width(mm) |
|------|--------------|------------|-----------|
| 8mm  |     500      |    267     |    356    |
| 8mm  |     1000     |    534     |    712    |
| 8mm  |     1500     |    801     |    1068   |
| 10mm |     500      |    213     |    285    |
| 10mm |     1000     |    427     |    570    |
| 10mm |     1500     |    641     |    855    |
| 12mm |     500      |    178     |    237    |
| 12mm |     1000     |    356     |    475    |
| 12mm |     1500     |    534     |    712    |

The driving hardware selected for this project is an ACRO 1500mm x 1500mm CNC Kit (https://www.makerstore.com.au/product/kit-acro-1515-s/) and an Arduino CNC shield with DRV8825 High Current Drivers. The CNC steppers are controlled using GRBL, sending G-code commands within the python recorder.py scripts. These commands could be sent as a single line in code or called a multi-line g-code file.

Below is an example of a single-line instruction. In this example, the carriage is sent the command over serial using ser. write to move from its current position to using G01, a linear (straight line movement), at a feed rate (Speed) of F3000 mm/min to location X200. No Y position is included in this command, so the current Y value is held.

```py
    ser.write(("G01 F3000 X200" +"\n").encode())# Send single line command to GRBL to move camera to X200  
```
In order to send a multi-line g-code file over GRBL, the file needs to be opened and read line by line. While running each line, the command is sent using the same user. Write as the example above. A brief wait of 100ms occurs between each line, allowing the Arduino to process and send the command. Below is the code from recorder.py, which runs the homing cycle for the CNC.
```py
# Open homing gcode file as a read only file and assign it to variable f
with open('WorkingFolderV3\gcode\homing.gcode', 'r') as f:
    for line in f:                          # Read each line consecutively from gcode file
        print('Sending: ' + line)           # Print in terminal line sent
        ser.write((line + "\n").encode())   # Send line information to GRBL to excute
        time.sleep(0.1)                     # Wait 100ms to send next line 
```
Below is the homing. gcode file called above. 4 commands are saved, which prepare the CNC once the script is first run. These commands reset the limits and positioning of the carriage and set it to its "Ready" state.
```
$H            % Start homing cycle
G92 X0 Y0     % Set work-coordinate offset
G90           % Absolute values
G00 X750Y700  % move to starting location
```
  
The image below shows preliminary testing once the frame was set up.

<p align="center">
  <img src="ImagePlots/workingdesign.jpg" alt="Working Design" style="width:550px;" />
</p>

## Star Field
The star field for this concept is designed on previously captured ground truth data of the star Mu Velorum and its surroundings. The reconstructed starfield consists of fibre optic strands inserted into plywood to replicate the same star pattern. In order to add variance in sizes and illumination of the "stars" to better match the example, different-sized holes were drilled into the plywood board. These holes allowed multiple strands to be inserted, giving the impression of larger/brighter stars. During this step, it was necessary to replicate the ground truth as closely as possible to ensure the best chance of optimal optimisation. 

The hole configurations with corresponding stands are outlined in the table below:

| Hole Size | Strands |
|----------|----------|
| 0.7mm    |     1    |
| 0.9mm    |     2    |
| 1.0mm    |     3    |
| 1.3mm    |     4    |
| 1.5mm    |     5    |
| 2.0mm    |     6    |
| 2.2mm    |     7    |
| 3.2mm    |     8    |
| 3.75mm   |     9    |

A piece of 13mm thick plywood supported the strands as they were fed into the holes. This support held the fibres perpendicular to the top face of the board, holding the lighting surface parallel to the lens on the camera, reducing visual errors. The following images show the underside and top of the plywood housing the optic strands. The ply's underside on the left shows the holes' distribution sizing and strand placement. The right shows the final "Star" layout used in the experiments. 

<figure>
  <p align="center">
    <img src="ImagePlots/Undersizeoptics.jpg" alt="Underside plywood" style="height: 275px;">
    <img src="ImagePlots/SimulatedStarfield.jpg" alt="Finished replication" style="height: 275px;">
  </p>
  <figcaption align="center">Figure 1: Left: Underside of plywood, strand distribution. Right: Final "Star" result.</figcaption>
</figure>

In order to test the accuracy of the replication compared to the ground truth, both images were run through astrometry.net (https://nova.astrometry.net/). This website takes an uploaded image and locates its origin in the sky. As expected, the ground truth image was positioned in the origin location in the sky. The replication search time was longer when processing, but it was located and copied to the original location. Side by side, these images can be told apart from the replication, which lacks the environmental noise that the original has. The following three images show the origin with the authentic and fake overlays and one of the origins by itself.

<p align="center">
  <img src="ImagePlots/realorigin.JPG" alt="Image 1" style="height: 275px;">
  <img src="ImagePlots/fakeorigin.JPG" alt="Image 2" style="height: 275px;">
</p>


<p align="center">
  <img src="ImagePlots/origin.JPG" alt="Image 1" style="height: 300px;">
</p>


## Camera
The camera used for recordings was a Prophesee EVK4. The EVK4 is a neuromorphic camera with a Sony IMX636 HD (720x1280 pixel) sensor. Neuromorphic cameras are unique in how they record data. They detect illumination changes asynchronously at a pixel level and return an "event" with a polarity of either 0 or 1. These polarities tell if the pixel had an off event (0), which occurs when light across the pixel is reduced or an on event (1), which is an increase of light across the pixel. 

In a neuromorphic camera, each pixel has a stored log intensity (Image below left as ln(i)) a current baseline value for illumination. The baseline resets as the log intensity reaches the set threshold depicted as the dotted line in the image below on the right (upper diagram). This baseline is then used by the comparators (ON and OFF) to compare itself against their threshold values. These thresholds are user-defined by the diff_on and diff_off Bias, where larger values in these biases would require more significant light variance across the pixel before breaching the threshold and registering an event. The greater the bias value (255 max), the less sensitive (detail) the pixel, resulting in fewer events. As sensitivity is increased, data size and rate follow. This experiment aims to find this "happy medium" between sensitivity and data rate. 

<p align="center">
  <img src="ImagePlots/simplepixel.JPG" alt="Image 1" style="height: 200px;">
  <img src="ImagePlots/eventdia.JPG" alt="Image 2" style="height: 200px;">
</p>

<p align="center"><i>Lichtsteiner, P, Posch, C & Delbruck, T 2008, ‘A 128 x 128 120 dB 15 us Latency Asynchronous Temporal Contrast Vision Sensor’, IEEE Journal of Solid-State Circuits, vol. 43, no. 2, pp. 566–576.</i></p>




## Prototype code
### V1 Code
The prototype file located in the "Old Work V1" folder was used for initial testing. This file required an operator to sit in the room and manually increase/decrease bias settings, start/stop recordings, and send GRBL commands. This manual operation was not efficient or consistent. The lighting from the backlit buttons as they were pushed and the computers monitor were constantly altering the illumination levels in the room causing irregularities in the recordings. Though as a proof of concept, the design operated as desired with minimal/no effect from the stepper motors during operation seen in the camera as viabrations causing the pixels to oscillilate on and off constantly. 

The code for the prototye was built on the PSEE413 platform and used threads to monitor for inputs from the operator. One of these inputs is seen in the example below. This code was avaliable to be used whn the camera was in a real time live view state. During this time providing no other instructions were running pressing the "6" button would execute the commands providing th_off was greater than 1. The commands would reduce th_off by 1 then set the updated diff_off value by acessing the bias parameters in PSEE413. 
```py
if c == ord("6") and th_off > 1:          # "Look" for an input command from the 6 button and confirm th_off is greater than 1 
        th_off -= 1                       # Reduce th_off by 1
        camera.set_parameters(            # Set the camera parameters to:
            psee413.Parameters(           #     - access from psee413 parameters and biases of the of the camera 
                biases = psee413.Biases( 
                    diff_on = th_on,      #     - refresh changes in biases 
                    diff = diff,
                    diff_off = th_off,
                )
            )
        )
```

Following the proof of concept an attempt was made to incorpirate some automation into this script. This automation allowed an operator to push the "g" button and the system would increase th_off by 1, create and name an .es file, start recording data to es file and start running gcode command from the CNC controller via GRBL. 

```py
  if c == ord("g"):                              # "Look" for an input command from the g button
    #ser.write(("G00 X10Y10" + "\n").encode())   # This line was commented out as the move instruction was repositioned during the automation process 
    th_off += 1                                  # increase th_off by 1
    name = f'{datetime.datetime.now(tz=datetime.timezone.utc).isoformat().replace("+00:00", "Z"+ str(th_off) + "OFF" + str(th_on)+"ON").replace(":", "-")}.es'          # create es file name
    camera.start_recording_to(name)              # start recording data to the es file 
    recording = True                             # set recording flag
    print("Recording to " + name)                # print to terminal "recording to "name""
    time.sleep(0.5)                              # wait es file to be created/formatted
    with open('C:\\Users\\Josh.F\\Desktop\\19317377\\PG\\Frame design\\Python\\startest.gcode', 'r') as f: # Open startest gcode file as a read only file and assign it to variable f
    for line in f:                               # Read each line consecutively from gcode file
        print('Sending: ' + line)                # Print in terminal line sent
        ser.write((line + "\n").encode())        # Send line information to GRBL to excute
        time.sleep(0.1)                          # Wait 100ms to send next line 
    
    count = 0                                    # reset counter to 0
```
This semi automated process still had the on going flaws requiring human interaction each iteration and the negative impacts from the illumination noise caused by the keyboard and monitor. This testing also outlined an effency issue with the code. Often the code would become interlocked between 2 steps or would run instructions out of order. Processing the recording was also cumbersome on the script and would often cause premature timeout errors on large thresholds. The problem with timeout errors is that the camera would need to be reset. This would in turn also reset the saved log intensity value which had been conditioned to the room. From testing the first 1-2 recording post rest would have additional noise as pixels returned to a normalised state. 

### V2 Code
Moving forward it was important to incorpirate a full automation process and improved efficency in both recording consistancy and reduced time to complete a full data set (from 255 > 0). To achieve this a new code was developed using the design of a state machine which also in itself operates ascyronusly. The state machine allowed the program to constantly run looking only for boolean changes in variable flags that would be 1 or 0 depending on what stage the process the system was in. 

Communication via the camera was now done via the neuromorphic_drivers module (https://github.com/neuromorphicsystems/neuromorphic-rs) which when recording packets from the camera would be stored in an array with each coloumn allocated to a different bias reading. when the script finished (met final condition or timedout) each coloumn of the array would be writtten to a unique csv file. This was done to minimise impact on the running of the script during recordings.

The code is designed to do a single bias recording at a time (diff_off or diff_on) and starting at the greatest threshold (255), the Bias is reduced by 1 each pass untill either it reaches one (this is user defined) or a timeout error would occur. The timeout error is caused by excess data too large for the usb to transfer. This error would always flag as the biases approached 1 as each bias reducion would result in pixels becoming more and more sensitive causing hot pixels. 

The code below shows a small portion (2 states) of the state machine where the script continusly rolls over each of the if statements waiting for the the corresponding flag to be raised. For instance during the recording phase the flag recording will be equal to 1. Therefore each time the script runs over the first line "if recording == 1:" the packets are then loaded into the array "packetdata". The point of this code is for the machine to not have heavy operations to carry out so as much processing can be put into the transfer of data. Thought the writing of events to an array then to a list would become expontionaly more burdensome because of the increasing data filling "reclist" each iteration.

```py
    if recording == 1:                                    # check recording status 
        if 'dvs_events' in packet:                        # check camera has events to upload
            packetdata.extend(packet['dvs_events'])       # load event data into the packetdata array onto the end of anything already present 
        
    if save == 1:                                         # check save status
        fname = f"off_{configuration.biases.diff_off}_on_{configuration.biases.diff_on}"  # create file name
        reclist[fname] = packetdata                       # add packet data array into reclist

        configuration.biases.diff_on -= 1                 # reduce diff_on by 1 
        device.update_configuration(configuration)        # apply new diff_on changes to camera
        print(configuration.biases.diff_on)               # confirmation printed to terminal of newly written bias value
        save = 0                                          # reset save 
```

### Current working files
In an effert to further impove efficency, the v2 code was modified to to save data straight from the camera in a RAW format. By exporting the data in this way negates the need to process the data (parsing) from raw into readable events.  This allowed an additional 4 recordings prior to the timeout error. Another benifit of this change is that it further simplified the script by removing the need to process the event data straight away. The removal of the csv conversion functions reduced the lines of code by approximatly 30 and saved hours of post processing unwanted data. 

The final code can be broken into 2 sections. The first is the setup phase which is used to perform single use tasks that do not need to be iterated over each time. Such tasks are establishing connections and loading defualt values to the camera and the CNC controller, Homing the camera carrige and setting initial flag states. The excption to the booklean flags are the variables checki and checkii which are strings used as comparators for determining the position of the carrige by requesting the location status through GRBL. 

The second section of the script is the state machine consisting of 7 elements that could be occuring in the process: 
1. Recording
2. Save
3. Checki and has moved (at end position)
4. Checkii and has moved  (at Start position)
5. Checki and move to 800 is set
6. Checkii and move to 200 is set
7. homing

```py
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
```
## Interesting Data

























The file sizes relative to Bias can be seen below. 

### Diff_off File size (MB) vs Bias
<p align="center">
  <img src="ImagePlots/Diff_Off_File_Size_255_156.png" alt="Experimental Setup" style="width:100%;" />
</p>
<p align="center">
  <img src="ImagePlots/Diff_Off_File_Size_155_48.png" alt="Experimental Setup" style="width:100%;" />
</p>

### Diff_on File size (MB) vs Bias
<p align="center">
  <img src="ImagePlots/Diff_On_File_Size_255_156.png" alt="Experimental Setup" style="width:100%;" />
</p>
<p align="center">
  <img src="ImagePlots/Diff_On_File_Size_155_43.png" alt="Experimental Setup" style="width:100%;" />
</p>

### Plot Discussion Points
- In both plots the first file size is quite large compared to the subsequent files. This is due to the pixels still leveling out after ambient light being let     into the room with the door being open and closed by the operator.
- In Diff_off the file size interestingly continues to decresases to a bias of 136 before it begins to increase again.
- When diff_off Bias reaches 55, the sharp spike is caused by a single hot pixel. These hot pixels continue to grow in the remianing files.
- The diff_on file size depicts what would be expected as the threshold is reduced each run. The file size can be seen to be growing constantly until the Bias reaches 58 at which point file size starts to grow exponetioaly.
The plots above offer some intersting insights into how the bias effect file size. Under these conditions diff_off has an interesting occurance where less data is generated than at 255 which should be the largest threshold. Aditionally the hot pixel scenario comes in with immediate effect with no warning. Diff_on on the other hand has a nice linear data growth until 58 where the data size become more exponential, interestingly the hot pixel started at 70.




















### Dataset

.ES and csv files are avaliable using the link below. There are files for both Diff_On and Diff_Off in raw form and also as a zipped file.

https://westernsydneyedu.sharepoint.com/:f:/r/sites/MoNE2022/Shared%20Documents/General/SimulatedStarRecordings?csf=1&web=1&e=SZCRum
