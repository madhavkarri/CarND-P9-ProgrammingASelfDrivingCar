# **Self-Driving Car**
# **Capstone Project: Programming A Self Driving Car**

## MK

#
Overview

A system integration project to drive Carla, the Udacity self-driving car, around a test track. For this project, Robot Operating System (ROS) was utilized to implement core functionality of the autonomous vehicle system: traffic light detection, control, and waypoint following. 

As this was an individual submission, code testing was performed only on the simulator.

[//]: # (Image References)

[image1]: ./Writeup_IV/Carla_Architecture.png "Carla_Architecture"


#
Carla Architecture

Carla is a Lincoln MKZ vehicle, modified into a self-driving car. Carla's self-driving system can be sub-dvidied into four major sub-systems: Sensors, Perception, Planning, and Control

![][image1]

Sensors

Sensors are hardware components that gathers data to observe and understand the physical world and its surroundings. Most common types of autonomous vehicle sensors are (but not limited to): Cameras, LIDAR, GPS, Radar, Ultrasonic, and IMU (Inertial Measuremnt Unit)

Perception

Consists of software to process the sensor data into structure data, to be later used in path planning and control. This is where most of the analysis and understanding of the vehicles environemnt and location are performed. Perception can be further classified into Detection and Localization

Detection

- Detection susbsystem is responsible for understanding the surrounding environment
- It includes software components/piplines such as: 
  - Lane detection 
  - Traffic sign detection and classification
  - Traffic light detection and classification
  - Object detection and tracking
  - Free space detection, etc

Localization

- Localization subsystem is responsible for using sensor and map data to determine the vehicle's precise location, with an accuracy of less than 10 cm

Planning

After the sensor data has been processed by the perception sub-system, the vehicle can use the processed data to plan its path. The planning sub-system can be further classified into:
- Route Planning: responsible for high level path of the vehicle between two points on a map. Analogous to route planning feature found on smartphones or in-car navigation systems
- Prediction: identifies which maneuver other objects on the road might take. For example, if vehicle detects presence of another vehicle in its surroundings, the prediction component would estimate its future trajectory\
- Behavior Planning: determines which maneuver the vehicle should take. For example: stopping at a traffic light or intersection, changing lanes, accelerating, or braking are various maneuvers issued by this planning component.

Trajectory Planning

Based on the desired immediate behavior, the trajectory planning component will determine which trajectory is best for executing this behavior.

Control

Contains software components  to esnure vehicle follows the path specified by the planning susbsytem. Control component takes trajectory outputs and processes them with a controller algorithm like PID or MPC (Model based predictive control) to adjust the control inputs for smooth operation of the vehicle. The control subsystem sends acceleration, braking, steering commands to the vehicle. This completes the chain of information from the sensors to actuation and allows the vehicle to drive

#
Carla Architecture

The ROS Architecture consists of different nodes (written in Python or C++) that communicate with each other via ROS messages. The nodes and their communication with each other are depicted in the picture below. The ovally outlined text boxes inside rectangular boxes represent the ROS nodes while the simple rectangular boxes represent the topics that are subscribed or published to. 

The following is a system architecture diagram showing the ROS nodes and topics used in the project. You can refer to the diagram throughout the project as needed. The ROS nodes and topics shown in the diagram are described briefly in the Code Structure section below, and more detail is provided for each node in later classroom concepts of this lesson.

#
The Project

The steps for this project:

* Waypoint Updater Node (Partial): complete a partial waypoint updater which subscribes to t/base_waypoints and /current_pose and publishes to /final_waypoints.
DBW Node: Once your waypoint updater is publishing /final_waypoints, the waypoint_follower node will start publishing messages to the/twist_cmd topic. At this point, you have everything needed to build the dbw_node. After completing this step, the car should drive in the simulator, ignoring the traffic lights.
Traffic Light Detection: This can be split into 2 parts:
Detection: Detect the traffic light and its color from the /image_color. The topic /vehicle/traffic_lights contains the exact location and status of all traffic lights in simulator, so you can test your output.
Waypoint publishing: Once you have correctly identified the traffic light and determined its position, you can convert it to a waypoint index and publish it.
Waypoint Updater (Full): Use /traffic_waypoint to change the waypoint target velocities before publishing to /final_waypoints. Your car should now stop at red traffic lights and move when they are green.

* Build a PID controller and tune the PID hyperparameters
* Test the tuned PID controller on the vehicle/race-track simulator
* Vehicle must successfully drive a lap around the track
* There is no minimum vehicle speed criteria. However, maximize vehicle speed by tuning the PID parameters
