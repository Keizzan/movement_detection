Project Name:
    Motion Caption


Synopsis:
    Script activates default camera, and starts movement detection. At end of
    programs life cycle it creates mp4 video file with detected motion and csv file
    containing information when movement was detected and when it stopped.

Application requirement: 
    Python 3.8.10,
    pip 20.0.2,
    external python3 libraries are (you can install them, by running command 'pip install -r requirements.txt'): 
    numpy==1.21.2
    opencv-python==4.5.3.56
    pandas==1.3.3
    python-dateutil==2.8.2
    pytz==2021.3
    six==1.16.0

For End-Users
-----------------
    1. Run script with python3/py/python* app.py'
*(choose one depeding on your operating system)
    2. Press 'q' to kill program
    3. At end in the same directory will be created 2 files, 'DetectedMotion.mp4' and Active_Times.csv containing details of detected movement.


