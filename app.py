
""""
##############################################################################
#######             PROJECT NAME : Motion Caption                      #######
##############################################################################

                             Synopsis:
 Script activates default camera, and starts movement detection. At end of
 programs life cycle it creates mp4 video file with detected motion and csv file
 containing information when movement was detected and when it stopped.
"""

### Imports
import cv2
from datetime import datetime
import pandas as pd
import time


### Declaring Variables
first_frame = None
status_list = [None, None]
times = []
vid = 0
recording_status = False

### Data frame for csv file output
df = pd.DataFrame(columns=['Start', 'End'])

# ### Delay Start Program
time.sleep(10)


### Creating video object
video = cv2.VideoCapture(0)

### Declaring variables for video & file output
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
width= int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
writer = cv2.VideoWriter('DetectedMotion.mp4', fourcc, 20, (width,height))
while True:

### Original Frame
    check, frame = video.read()
    status = 0

### Gray Scale Frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

### Check for first caught frame
    if first_frame is None:
        first_frame = gray
        continue

### White / Black Frame
    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (cnts, _) = cv2.findContours(thresh_frame.copy(),
                                 cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

### Sensitivity
    for contour in cnts:
        if cv2.contourArea(contour) < 7500:
            continue
        status = 1
### Highlighting moving object
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

### Comments in camera feed
    if status == 1:
        text = 'Movement Detected'
    else:
        text = 'Movement Not Detected'
    cv2.putText(frame,text,(10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    time_stamp = datetime.now().strftime('%H-%M-%S')
    cv2.putText(frame,time_stamp,(500, 475),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

### Saving memory / Operating only on last 2 recent status values
    status_list.append(status)
    status_list=status_list[-2:]

### Check for changes in status values and inputting it into list + 
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
        recording_status = True
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())
        recording_status = False


### Check for recording
    if recording_status == True:
        writer.write(frame)


    ### Display video
    cv2.imshow('Live feed', frame)


    key = cv2.waitKey(1)

### Press 'q' to kill program
    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

### Save cvs file with list of times
for i in range(0, len(times), 2):
    df = df.append({'Start': times[i], 'End': times[i+1]}, ignore_index=True)

### cvs file output
df.to_csv('Active_Time.csv')

video.release()
writer.release()
cv2.destroyAllWindows()
