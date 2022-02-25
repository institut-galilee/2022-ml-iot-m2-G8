# 2021-ExamMonitoringSystem

The subject is based on the implementation of an exam monitoring system, this by developing two applications: mobile and desktop which will allow a good functioning of the system.
The candidate will have a phone attached to his forehead which will monitor all of these activities as well as the objects around him, the machine where he will take the exam will have a direct connection with this phone, and his camera will try to detect the set of objects and people located in the space of the candidate. Any suspicious attempt at cheating will prevent the candidate from continuing to pass his exam by issuing a warning message.
Before establishing the possible scenarios, a very good analysis has been put in place by establishing all the actors who will intervene in our system.
In order to pass the exam the candidate should

• Identify yourself by facial recognition.

• Attach the phone to his forehead and place it properly.

• Begin to pass the exam.

During its examination, the system will try to detect any possible cheating attempt for this, a set of scenarios will therefore be possible.

• When connecting, the system will try to recognize the person authorized to take the exam, if it does not detect it, the connection will not be established.

• The candidate begins to take his exam,

if the candidate tries to cheat either:

      - To leave

      - Presence of an unauthorized person
      
      - Presence of an unauthorized object

The system will detect the cheating attempt

otherwise the candidate could continue to take their exam.


# How to run the application

1/ Install requirements

> pip install requirements.txt

2/ Deploy the android app in your mobile located in directory: \android

3/ Activate Hotspot from your Computer then connect your phone to the hotspot wifi

4/ - Add your pictures with your name on it in the path desktop\Mutiprocessing\pictures 
   - Add the name of pictures in desktop\Mutiprocessing\main.py line 32 "known_face_names"

5/ Start main.py application in python in "\desktop\MultiProcessing\main.py"

6/ stay still until you get connected

7/ start the mobile app when the system tells you to do so


## Requirements
For python, all requirements can be found in the `requirements.txt` file located in desktop\MultiProcessing.

> cd .\desktop\MultiProcessing

> pip install requirements.txt

For the mobile application, take a look at the Gradle files.

## Contribute
Please feel free to report any bug that you encounter while using the system. You have solely to create a new issue in the `Issues` tab.
Feel free also to provide suggestions for improvement or additional features that you want to see in the system. Again, simply create a new issue.

## Credits
* BENDIMRAD Mehdi (bendimrad.mehdi@edu.univ-paris13.fr)
* BENSAID Mohammed (bensaid.mohammed@edu.univ-paris13.fr)

## License
