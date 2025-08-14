# Description  
Communicator of ascii messages using FSK sound : the sound produced is a series of 2 frequences, one for 0, the other one for 1. Each group of 8 frequences represents an ascii character and the final message is a group of those characters.

# Prerequisites
- 2 computers to communicate but I guess you can communicate with yourself by running both scripts on the same computer
- python with numpy and sounddevice packages installed

- notice that the 2 computers have to be close together because the project uses hearable sounds and it doesn't travel very far, btw default sounds are at 18000 Hertz, so if you are a dog or a bat, it can be unpleasnt to hear that sound, you can absolutly change the base frequency, just make sure to do it on both scripts 

# Install
- clone the repo on both computers
- on one computer run the receiver
- on the other one, run the transmitter
- there you go

# Trouble shooting
- you may have to change the default mic by uncommenting the line ```#sd.default.device = (7, None)``` at the beggining of receiver.py and set the one you want (all available mics are displayed when you run receiver.py)
- there could be a problem with the fs variable of receiver.py : try to set it to 44100 instead of 48000 if there is a lot of red errors related to the mic
