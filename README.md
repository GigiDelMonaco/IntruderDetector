# Intruder Detector

## Introduction
This is a project for the exam of Serverless Computing for IoT in my Master Degree course.
The project aims to simulate a Smart Home alarm based on a motion sensor placed near the house door. Whenever  the motion sensor detects a movement,  sends a notify email to  the owner so that the owner can take a picture using a bot Telegram connected to live cam by using ESP32 module

For the purpose of demonstrating the project, the sensor sending data will be simulated by using Node-RED. Sensor will send the output to a serverless function; the servlerless function, once triggered, will send an email by using IFTTT. Another serverless function, called SendPicture, will send a picture of "intruder" via Telegram by using IFTTT too.

## Architecture
![Motion_detector_architecture](https://user-images.githubusercontent.com/51193421/210550312-730ac36b-fdc2-455b-8403-c0c7c6772b6d.png)

Three function are used in this project:

<ul>
  <li><code>SendAlert</code>: Node-RED flow that simulate the motion sensor in order to trigger the alarm.</li>
  <li><code>MovementHandler</code>: sends email notification to the owner when a movement is detected.</li>
  <li><code>intruder_detector_bot</code>: using the specific command <code>/take_picture</code> sends the picture of intruder on the Telegram chat with the owner.</li>
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
Click on <b>Create Function<b> and then on <b>Import</b> to upload "MovementHandler" function by using <code>movement-handler.yaml</code> file. You can find these files in <code>yaml-function</code> folder.
Click on <b>Create Function</b> and then on <b>Deploy</b>


## IFTTT
If This Then That (IFTTT) is an online service that automates Web-based tasks so that when user-specified events occur, follow-up tasks are triggered and handled.

### How to use
Register on IFTTT and create a new applet by adding on IF clause WebHooks service > <b>Receive a web request</b> with the following parameter:

![IFTTT_trigger](https://user-images.githubusercontent.com/51193421/210283487-a2d3e078-5f7d-436f-8381-6da30d00858b.png)

  and with a <code>THEN</code> clause Telegram > <b>Send yourself</b> an email with the following parameters:

![IFTTT_gmail](https://user-images.githubusercontent.com/51193421/210283394-81a1f3d4-493d-4e4e-ba9d-ba915f33f31d.png)

## Node-RED
Built on Node.js, Node-RED is a programming tool for wiring together hardware devices, APIs and online services in new and interesting ways.
It provides a browser-based editor that makes it easy to wire together flows using the wide range of nodes in the palette that can be deployed to its runtime in a single-click.
  
### How to use
Start Node-RED instance using docker. [Click here](https://nodered.org/docs/getting-started/docker) for the reference guide.
```
$ docker run -it -p 1880:1880 -v node_red_data:/data --name mynodered nodered/node-red
```
  
Once the container is started and running, follow these steps:
<ul>
  <li>Browse to http://localhost:1880 to open the homepage of Node-RED</li>
  <li> Import the ([flow.json])(Node-RED/flow.json)</li>
  <li> Press Manage palette and from Install tab and search for the following palette:
    <ul>
      <li> node-red-dashboard </li>
      <li >node-red-contrib-mqtt-broker </li>
    </ul>
<li>Press on one of the mqtt nodes, edit mqtt-broker node and change according with your MQTT Broker, Server and _Port in <b>Connection</b> and User and Password in <b>Security</b></li>
</ul>

## Telegram Bot
Now, you need to create the bot telegram connected with the live-camera. In order to do that, follow these steps:

- Open Telegram and search for BotFather
- Type /newBot
- Specify intruder_detector_bot as a name for your bot
- Choose a unique id by following BotFather instruction
- Copy the token it gives to you and paste it in the <b>intruder_detector_bot.py<b>

## Python 3.8
In this project i used python version 3.8
You need to install pip too; you can find instructions [here](https://phoenixnap.com/kb/install-pip-windows#:~:text=1%20Download%20PIP%20get-pip.py.%20Before%20installing%20PIP%2C%20download,Command%20Prompt%20if%20it%20isn%E2%80%99t%20already%20open.%20)

Once you've installed pip, run this command
```
pip install <module name>
```

and install these dependencies:

- urllib3
- pyTelegramBotAPI : references [here](https://github.com/eternnoir/pyTelegramBotAPI)

For my purposes i used PyCharm IDE, but you can use the IDE/Editor you prefer.

## ESP32-Cam Module
In order to install and configure ESP32-Cam i suggest you to follow this [guide](https://randomnerdtutorials.com/installing-the-esp32-board-in-arduino-ide-windows-instructions/)

Once you've completed the configuration, start <code>Arduino IDE</code> and open <code>arduino.ino</code> file.

- Connect your module with usb-c wire in the port that you've specified during installation, choosing esp32 board.
- Replace SSID and PASSWORD with your wifi credentials.
- <code>Verify</code> and <code>Upload</code> the Sketch on the ESP32 MCU board.
- Open the Serial monitor and check if connected. It will be displayed an url where the cam in streaming. Copy this url and paste it on the python script.

