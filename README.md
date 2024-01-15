## Hey! Is this thing on?
### Space-based object detection optimisation with neuromorphic cameras

This experiment aimed to track the effects manipulating a neuromorphic camera's biases had on object detection in an adverse lighting simulation replicating a star cluster in the night sky.
The set-up placed a neuromorphic camera on a GRBL-controlled carriage driven by stepper motors, which was then programmed to sweep over a simulated star field in a "Darkroom."

<p align="center">
  <img src="ImagePlots/ExperimentSetup.jpg" alt="Experimental Setup" style="width:400px;" />
</p>

The starfield consisted of fibre optic strands to replicate stars. To add variance in sizes and illumination of the "stars", different-sized holes were drilled into a plywood board. The hole configurations with corresponding stands were:
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

<p align="center">
  <img src="ImagePlots/Undersizeoptics.jpg" alt="Under side of plywood showing lighting configuration" style="width:400px;" />
</p>

<p align="center">
  <img src="ImagePlots/SimulatedStarfield.jpg" alt="Simulated starfield" style="width:400px;" />
</p>

A piece of 13mm thick plywood supported the strands as they were fed into the holes. This support held the fibres perpendicular to the top face of the board and parallel with the lens on the camera.

### Prototye code
The prototype file located in the "Old Work V1" folder was used for initial testing. This file required an operator to sit in the room, manually increase/decrease bias settings, start/stop recordings, and send GRBL commands. These manual operations were not efficient or consistent, as the lighting from the computer monitor constantly altered the illumination levels in the room. This change caused irregularities in the recordings. Though as a proof of concept, the design operated as desired with minimal/no effect from the stepper motors during operation seen in the camera. The code for the prototye was built on the PSEE413 platform and used threads to monitor and accept input changes. In the example below while the connection to the camera was live the "6" button could be pressed and providing the th_off bias was greater than 1 it would be reduced. 
```
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
```
This code did evolve to incorpirate some automation which allowed by pushing the "g" button the system would start recording, move, finish recording after the count condition was met and reset. Each time the "g" button was pressed the bias would also shift by 1 as seen below.
```
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
The code is programmed to do a single bias recording at a time (diff_off or diff_on) and starting at the greatest threshold for both (255) the bias of interest is reduced by 1 each pass untill either the bias reached 1 or a timeout error would occur. The timeout error is caused by excess data too large for the usb to transfer. This error would always flag as the biases approached 1 as each bias reducion would result in pixels becoming more and more sensitive often causing hot pixels. Below the file sizes relative to bias can be seen. 

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
  <img src="ImagePlots/Diff_Off_File_Size_155_43.png" alt="Experimental Setup" style="width:100%;" />
</p>





















### Dataset

.ES and csv files are avaliable using the link below. There are files for both Diff_On and Diff_Off in raw form and also as a zipped file.

https://westernsydneyedu.sharepoint.com/:f:/r/sites/MoNE2022/Shared%20Documents/General/SimulatedStarRecordings?csf=1&web=1&e=SZCRum
