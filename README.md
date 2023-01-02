# Intruder Detector

## Introduction
The project aims to simulate a Smart Home alarm based on a motion sensor placed near the house door. Whenever  the motion sensor detects a movement,  sends a notify email to  the owner and a picture of the door situation via Telegram.

For the purpose of demonstrating the project, the sensor sending data will be simulated by using Node-RED. Sensor will send the output to a serverless function; the servlerless function, once triggered, will send an email by using IFTTT. Another serverless function, called SendPicture, will send a picture of "intruder" via Telegram by using IFTTT too.

## Architecture
![image](https://user-images.githubusercontent.com/51193421/210285006-b4df8cb8-f832-4d95-8eec-7ccdcbde8e84.png)


Two function are used in this project:

<ul>
  <li><code>MovementHandler</code>: sends email notification to the owner when a movement is detected.</li>
  <li><code>PictureHandler</code>: sends the picture of intruder on the Telegram chat with the owner.</li>
  <li><code>SendPicture</code>: ESP32 function installed on arduino board which take the picture and send it using mqtt protocol to the
      serverless function <code>PictureHandler</code>.</li>
</ul>

All of that is achieved by using RabbitMQ, Node-RED, Nuclio, Arduino IDE, IFTTT, Docker.

## Docker
Docker is a tool designed to make it easier to create, deploy, and run applications by using containers. Containers allow developers to package up an application with all of the parts it needs, such as libraries and other dependencies, and ship it all out as one package.
Docker containers use the same Linux kernel as the system that they're running on, which results in a significant performance boost.

Docker is used in the architecture to deploy functions in application containers and each of the functions is a Docker container that is listening on a socket port and can be invoked by any of the configurable triggers. We will containerize all of our components, such as Node-RED, Nuclio and RabbitMQ.

To get Docker on your pc, follow this [guide](https://docs.docker.com/get-docker/)

## RabbitMQ
RabbitMQ supports multiple messaging protocols and can be deployed to meet high-scale and high-availability requirements.

The default protocol is AMQP and the library used to interact with it is AMQP .

### How to use
To start a RabbitMQ instance with Docker:
```
$ docker run -p 9000:15672  -p 1883:1883 -p 5672:5672  cyrilix/rabbitmq-mqtt 
```
Then, browse to http://localhost:9000, and login using <b>'guest'</b> as username and <b>'guest'</b> as password, in order to access to the RabbitMQ console.
If you want to customize user permissions, you can create it on admin tab in the RabbitMQ dashboard.

For our purposes, in this project we'll use mqtt protocol.

## Nuclio
Nuclio is High-Performance Serverless event and data processing platform.

To start a Nuclio instance with Docker:
```
$ docker run -p 8070:8070 -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp nuclio/dashboard:stable-amd64
```

### How to use
After your Nuclio instance has been successfully started, browse to http://localhost:8070 to access to Nuclio dashboard. Then, simply follow these steps:

Create a new project named MovementHandler
Click on <b>Create Function<b> and then on <b>Import</b> to upload "MovementHandler" and "PictureHandler" functions by using <code>motion-alert.yaml</code>, <code>send-picture.yaml</code> files respectively. You can find these files in <code>./yaml-function</code> folder.
Click on <b>Create Function</b> and then on <b>Deploy</b>


## IFTTT
If This Then That (IFTTT) is an online service that automates Web-based tasks so that when user-specified events occur, follow-up tasks are triggered and handled.

### How to use
Register on IFTTT and create a new applet by adding on IF clause WebHooks service > Receive a web request with the following parameter:

![IFTTT_trigger](https://user-images.githubusercontent.com/51193421/210283487-a2d3e078-5f7d-436f-8381-6da30d00858b.png)

and with a <code>THEN</code> clause Telegram > Send Message with the following parameters:

![IFTTT_gmail](https://user-images.githubusercontent.com/51193421/210283394-81a1f3d4-493d-4e4e-ba9d-ba915f33f31d.png)

You can repeat this steps in order to create a second trigger with the same <code>IF</code> clause(web request) and the Telegram <code>THEN</code> clause.
  
## ESP32 Module

