# Intruder Detector

## Introduction
The project aims to simulate a Smart Home alarm based using a motion sensor placed near the house door. Whenever  the motion sensor detects a movement,  sends a notify email to  the owner and a picture of the door situation via Telegram.

For the purpose of demonstrating the project, the sensor sending data will be simulated by using Node-RED. Sensor will send the output to a serverless function; the servlerless function, once triggered, will send an email by using IFTTT. Another serverless function, called SendPicture, will send a picture of "intruder" via Telegram by using IFTTT too.

## Architecture
