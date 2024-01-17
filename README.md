# Hey! Is this thing on? Space-based object detection optimisation with neuromorphic cameras

## Design, Hardware and Control
This experiment aims to track the effects manipulating a neuromorphic camera's biases has on object detection. The concept was to have a neuromorphic camera move across a replicated star cluster or vice versa in a controlled low-light environment. The initial proposal for this design had a fixed camera mounted in the centre of two rings, as seen below in Figure 1 (Left). The concept's inner ring would have a star pattern drilled into it. Two light sources are mounted between the first and second rings and are orientated to illuminate the area between the rings in line with the camera. The inner ring would then be driven to create events across the camera sensor. Due to its complexity of recreating an accurate star map on the curved surface and the limitation of the room being restricted by the size of the inner ring, this design was inadequate.

A redesign of the original concept led to the final design. The design allowed for versatility in mounting options and adjustable heights. These improvements also allowed the star map to be projected on a flat surface, meaning recreation was much more straightforward.

<figure>
  <p align="center">
    <img src="ImagePlots/FirstDesign.JPG" alt="Image 1" style="height: 350px;">
    <img src="ImagePlots/FinalDesign.JPG" alt="Image 2" style="height: 350px;">
  </p>
  <figcaption align="center">Figure 1: Left: Initial concept. Right: Final Design.</figcaption>
</figure>

.

One of the techniques taught in the neuromorphic sensing unit was lens selection and Field of View (FOV). Below is a table covering three different lenses at three different rudimentary distances from the star map. As the camera would be passing over the "stars" in the y direction, it was necessary to tune the physical dimensions to this. Ideally, the single stand light should show as a single pixel. With this assumption, using the stand thickness of 0.4mm, a desired FOV in the y direction is calculated by multiplying 0.4 by 720 (sensor pixel height), returning 288mm. The distance between the lens and lights could not be tuned to achieve a measurement as close to this. The actual FOV achieved on the y-axis using a 12mm lens was 259mm due to the constraints in the fixed point height adjustments.

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

The driving hardware selected for this project is an ACRO 1500mm x 1500mm CNC Kit (https://www.makerstore.com.au/product/kit-acro-1515-s/) and an Arduino CNC shield with DRV8825 High Current Drivers. The CNC steppers were controlled using GRBL, sending G-code commands within the python recorder.py scripts. These commands could be sent as a single line in code or called a multi-line g-code file.

Below is an example of a single-line instruction. In this example, the carriage is sent the command over serial using ser. write to move from its current position to using G01, a linear (straight line movement), at a feed rate (Speed) of F3000 mm/min to location X200. No Y position is included in this command, so the current Y value is held.

```py
    ser.write(("G01 F3000 X200" +"\n").encode())# Send sinle line command to GRBL to move camera to X200  
```
In order to send a multi-line g-code file over GRBL, the file needs to be opened and read line by line. While running each line, the command is sent using the same user. Write as the example above. A brief wait of 100ms occurs between each line, allowing the Arduino to process and send the command. Below is the code from recorder.py, which runs the homing cycle for the CNC.
```py
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
The star field for this concept is designed on previously captured ground truth data of the star Mu Velorum and its surroundings. The reconstructed starfield consists of fibre optic strands being inserted into plywood to replicate the same star pattern. To add variance in sizes and illumination of the "stars" to better match the example, different-sized holes were drilled into the plywood board. These holes alloed multiple strands to be inserted to giving the impression of larger/brighter stars. It was important during this step to replicate the ground truth as close as possible to ensure the best chance of optimal optimisation. 

The hole configurations with corresponding stands is outlined in the table below:

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

A piece of 13mm thick plywood supported the strands as they were fed into the holes. This support held the fibres perpendicular to the top face of the board, holding the lighting surface parallel with the lens on the camera reducing visual errors. The following images show the underside and top of the plywood housing the optic strands. On the left, the underside of the ply shows the distribution and sizing of the holes and stand placement. The right shows the final "Star" layout used in the experiments.

<figure>
  <p align="center">
    <img src="ImagePlots/Undersizeoptics.jpg" alt="Underside plywood" style="height: 300px;">
    <img src="ImagePlots/SimulatedStarfield.jpg" alt="Finished replication" style="height: 300px;">
  </p>
  <figcaption align="center">Figure 1: Left: Underside of plywood, strand distribution. Right: Final "Star" result.</figcaption>
</figure>

In order to test the accuracy of the replication compared to the ground truth both images were run through astrometry.net (https://nova.astrometry.net/), a website that takes an uploaded image and locates its origin in the sky. As expected the ground truth capture positioned in the expected origin location. When processing the replication search time was longer but it was located and copies the location of orginial. Side by side these images can be told apart with the replecation lacking the enviromental noise that the original has. The next three images show the orgin with the real and fake overlayed and one of the origin by itself.

<figure>
  <p align="center">
    <img src="ImagePlots/realorigin.JPG" alt="Image 1" style="height: 350px;">
    <img src="ImagePlots/fakeorigin.JPG" alt="Image 2" style="height: 350px;">
  </p>
  <figcaption align="center">Figure 1: Left: Ground truth. Right: Replicated "Star" field.</figcaption>
</figure>


<figure>
  <p align="center">
    <img src="ImagePlots/origin.JPG" alt="Image 1" style="height: 400px;">
  </p>
  <figcaption align="center">Figure 1: Origin in the sky.</figcaption>
</figure>

## Camera
The camera used for recordings was a Prophesee EVK4. The EVK4 is a neuromorphic camera with a sony IMX636 HD (720x1280 pixel) sensor. Neuromorphic cameras are unique in the way they record data as they detect illuminaton changes aschroynsly at a pixel level and return an event with a polarity of either 0 or 1. thes polarities tell if the pixel had a off event (0) where the light on the pixel was reduced frim its current baseline or a on event (1) which is an increase of light acriss the oixel. 

The thresholds that determin if the change in light intensity at the pixel warrants an on/;off event are able to be customised. These settings are refered to as Diff_on and Diff_off bias settings, by reducing the threshold the sensor/pixel become increasingly more sensitive as a smaller differene in illumination now causes an event to occur.

## Prototype code
### V1 Code
The prototype file located in the "Old Work V1" folder was used for initial testing. This file required an operator to sit in the room and manually increase/decrease bias settings, start/stop recordings, and send GRBL commands. This manual operation was not efficient or consistent, as the lighting from the computer monitor constantly altered the illumination levels in the room causing irregularities in the recordings. Though as a proof of concept, the design operated as desired with minimal/no effect from the stepper motors during operation seen in the camera. The code for the prototye was built on the PSEE413 platform and used threads to monitor and accept input changes. In the example below, providing the connection to the camera was live the "6" button could be pressed and providing the th_off Bias was larger than one, it would be reduced. 
```py
if c == ord("6") and th_off > 1:          # "Look" for an input command from the 6 buttoon and th_off is greater than 1 
        th_off -= 1                       # Reduce th_off by 1
        camera.set_parameters(            # Open the camera and psee413 parameters of the of the camera and load new th_off values
            psee413.Parameters(
                biases = psee413.Biases(
                    diff_on = th_on,
                    diff = diff,
                    diff_off = th_off,
                )
            )
        )
```
This code did evolve to incorpirate some automation which allowed by pushing the "g" button the system would start recording, move, finish recording after the count condition was met and reset. Each time the "g" button was pressed, the Bias would shift by 1 as seen below.
```py
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
```

### V2 Code
Moving forward it was important to incorpirate a full automation process and improved efficency. To achieve this the new code incorpirated a state machine. the state machine allowed the program to constantly run looking only for changes in variable flags that would be set/reset depending on what stage the process the system was in.

Communication via the camera was now done via the neuromorphic_drivers module (https://github.com/neuromorphicsystems/neuromorphic-rs) which when recording packets from the camera would be stored in an array then written to a csv file while at the same time the sytem was returning to its home location ready for another recording. 

The code is programmed to do a single bias recording at a time (diff_off or diff_on) and starting at the greatest threshold for both (255), the Bias of interest is reduced by 1 each pass untill either the Bias reaches one or a timeout error would occur. The timeout error is caused by excess data too large for the usb to transfer. This error would always flag as the biases approached 1 as each bias reducion would result in pixels becoming more and more sensitive often causing hot pixels. 

The code below shows a snippet of the state machine where the script will just continue to roll over the if statements waiting for the the corresponding flag to be raised. For instance during the recording phase the flag recording will be equal to 1. Therefore each time the script runs over "if recording == 1:" the packets are then loaded into the array "packetdata". The point of this code is for the machine to not have heavy operations to carry out. Instead multiple easy tasks are provided. 

```py
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
```


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

### Current working files
In an effert to further impove efficency the v2 code was modified to to save data straight from the camera in a RAW format. This allowed an additional 4 recordings prior to the timeout error. The benifit of this code is that it further simplified the script reducing the lines of code by approximatly 30. The script during the recording phase seen below is now simply writes the packet data straight to the RAW file then when recording is done closes the output. A new file is then generated and data can be written again. This has removed the need to fill an array, then convert the array to csv.

```py
    if recording == 1:                          # If recording is set
    output.write(packet)                        # Write packet data to current open output file
```


















### Dataset

.ES and csv files are avaliable using the link below. There are files for both Diff_On and Diff_Off in raw form and also as a zipped file.

https://westernsydneyedu.sharepoint.com/:f:/r/sites/MoNE2022/Shared%20Documents/General/SimulatedStarRecordings?csf=1&web=1&e=SZCRum
