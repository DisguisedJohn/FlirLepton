# FlirLepton
Flir Lepton image acquire and camera control
Used for practical part of Bachelors degree thesis.

video_stream.py
Raw data acquire from Flir Lepton Camera with basic transformation to video feed and object detection.

main.cpp
Communication with camera via I2C, for setting parameters. Implemented AGC disabing and performing FFC calibration.

Missing implementation of KNX BAOS communication because of inability to test code. 
