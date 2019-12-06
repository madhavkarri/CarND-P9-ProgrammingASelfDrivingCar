# **Self-Driving Car**
# **Capstone Project: Programming A Self Driving Car**

## MK

## Individual Submission

Overview

A system integration project to drive Carla, the Udacity self-driving car, around a test track. For this project, Robot Operating System (ROS) was utilized to implement core functionality of the autonomous vehicle system: traffic light detection, control, and waypoint following. 

As this was an individual submission, code testing was performed only on the simulator.

[//]: # (Image References)

[image1]: ./Writeup_IV/Carla_Architecture.png "Carla_Architecture"
[image2]: ./Writeup_IV/ROS_Graph.jpg "ROS_Graph"
[image3]: ./Writeup_IV/ROSNodes_Architecture.png "ROSNodes_Architecture"
[image4]: ./Writeup_IV/WaypointUpdater_Node.png "WaypointUpdater_Node"
[image5]: ./Writeup_IV/TLD_Node.png "TLD_Node"
[image6]: ./Writeup_IV/DBW_Node.png "DBW_Node"


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
ROS Architecture

The ROS Architecture consists of nodes (written in Python or C++), that communicate with each other via ROS messages. The nodes and their communication with each other are shown below. Oval text boxes inside rectangular boxes represent the ROS nodes and rectangular boxes represent the ROS topics that are subscribed or published to. The direction of arrows indicates direction of communication.

![][image2]

The primary control node from the above rqt-graph is the styx_server. It links the simulator and ROS by sending the car's state and surroundings (vehicle current pose/position, velocity, front camera images, etc.) and receiving control input (steering, braking, throttle). The remainder of the nodes can be associated with either of the three tasks: Perception, Planning, and Control.

Node Design

![][image3]

In this project the following packages have been built or modified to navigate the vehicle around the test track.

Waypoint Updater:

This package contains the waypoint updater node: `waypoint_updater.py`. The purpose of this node is to update the target velocity property of each waypoint based on traffic light and obstacle detection data. This node subscribes to the `/base_waypoints`, `/current_pose`, `/obstacle_waypoint`, and `/traffic_waypoint` topics, and publishes a list of waypoints ahead of the car with target velocities to the `/final_waypoints` topic

![][image4]

Traffic Light Detection:

This package contains the traffic light detection node: `tl_detector.py`. This node takes in data from the `/image_color`, `/current_pose`, and `/base_waypoints` topics and publishes the locations to stop for red traffic lights to the `/traffic_waypoint topic`.

The `/current_pose` topic provides the vehicle's current position, and `/base_waypoints` provides a complete list of waypoints the car will be following.

Built both traffic light detection node and a traffic light classification node. Traffic light detection was implemented in `tl_detector.py` and traffic light classification was implemented at `../tl_detector/light_classification_model/tl_classfier.py`.

![][image5]

DBW Node:

Carla is equipped with a drive-by-wire (dbw) system, meaning the throttle, brake, and steering have electronic control. This package consists of files responsible for control of the vehicle: the node `dbw_node.py` and the file `twist_controller.py`, along with a pid and lowpass filter. The `dbw_node` subscribes to the `/current_velocity` topic along with the `/twist_cmd` topic to receive target linear and angular velocities. Additionally, this node subscribes to `/vehicle/dbw_enabled`, which indicates if the car is under dbw or driver control. This node publishes throttle, brake, and steering commands to the `/vehicle/throttle_cmd`, `/vehicle/brake_cmd`, and `/vehicle/steering_cmd` topics.

![][image6]


#
The Project

The project was completed in the order as suggested by Udacity:

- Waypoint Updater Node (Partial): Completed a partial waypoint updater which subscribes to `/base_waypoints` and `/current_pose` and publishes to `/final_waypoints`.
- DBW Node: Once waypoint updater is publishing `/final_waypoints`, the `waypoint_follower` node starts publishing messages to the `/twist_cmd` topic. At this point, all resources are available to build the `dbw_node`. After completing this step, the car was able to drive in the simulator, ignoring the traffic lights.
- Traffic Light Detection: This was split into 2 parts:
  - Detection: Detected traffic light and its color from the `/image_color`. The topic `/vehicle/traffic_lights` contains the exact location and status of all traffic lights in simulator and was used to test against the classification output.
  - Waypoint publishing: Once the traffic light was identified and its position determined, it was converted to a waypoint index for publishing.

- Waypoint Updater (Full): Used `/traffic_waypoint` to change the waypoint target velocities before publishing to `/final_waypoints`. The car was able to stop at red traffic lights and move when they were green.

#
The Code

- src_v1: baseline code Udacity provided. Completed the following set of steps:
  - Waypoint Updater Node (Partial) (5)
  - Waypoint Updater Partial Walkthrough (6)
  - DBW Node (7)
  - DBW Walkthrough (8)
  - Yet to test dbw_test.py and functioning of dbw_enabled flag
  - The code: [Link1:github](https://github.com/madhavkarri/CarND-P9-ProgrammingASelfDrivingCar/tree/master/src_vers/src_v1) and [Link2:gdrive](https://drive.google.com/drive/folders/1Twvq2HscZP3vCLbsxgR0ZI44XCsUqjLY)

- src_v2: baseline code src_v1. Implemented dbw_enabled flag and verified its working correctly
  - The code: [Link1:github](https://github.com/madhavkarri/CarND-P9-ProgrammingASelfDrivingCar/tree/master/src_vers/src_v2) and [Link2:gdrive](https://drive.google.com/drive/folders/1nsvE3ESYdaB8IaLcJQX95OdsOMfcyf2o)

- src_v3: baseline code src_v1. Implemented dbw_test.py
  - The code: [Link1:github](https://github.com/madhavkarri/CarND-P9-ProgrammingASelfDrivingCar/tree/master/src_vers/src_v3) and [Link2:gdrive](https://drive.google.com/drive/folders/17L25dIh3zBsMBHyReZyrExgobhcmRpvB?usp=sharing)
  
- src_v4: baseline code src_v3. Completed the following set of steps:
  - Traffic Light Detection Node (9)
  - Object Detection Lab (10)
  - Detection Walkthrough (11)
  - Waypoint Updater Node (Full) (12)
  - Full Waypoint Walkthrough (13)
  - TF Classifier not yet implemented
  - The code: [Link1:github](https://github.com/madhavkarri/CarND-P9-ProgrammingASelfDrivingCar/tree/master/src_vers/src_v4) and [Link2:gdrive](https://drive.google.com/drive/folders/1ZxGtrEgPiqeWcigIer5vVmjD2L91qnj8)
  
- src_v5: baseline code src_v4
  - TF Classifier implemented
  - Implemented storing images from front camera
  - Implemented storing images within threshold distance from traffic light stop line
  - Image capture using optimum distance (not too far) will increase accuracy/precision of Classifier
  - Classification using optimum distance will lower the workload on the Classifier and consequently any lagging issues between the vehicle simulator and ROS
  - The code: [Link1:github](https://github.com/madhavkarri/CarND-P9-ProgrammingASelfDrivingCar/tree/master/src_vers/src_v5) and [Link2:gdrive](https://drive.google.com/drive/folders/13XjIzRLsiHBqiP84mFTpSlHdHY_OBMcC)

- src_v6: baseline code src_v5
  - Using Udacity provided code, the vehicle stops after finishing one lap
  - Modified code such that the vehicle can traverse indefinite number of laps
  - Looping around the simulator track, in conjunction with image capture at optimum ditance, is useful for consistent data collection used in classifier training
  - The code: [Link1:github](https://github.com/madhavkarri/CarND-P9-ProgrammingASelfDrivingCar/tree/master/src_vers/src_v6) and [Link2:gdrive](https://drive.google.com/drive/folders/1Dc4MinyycWV9zQsG0qQmZz4synBdJEK1)

- src_v7: baseline code src_v6. Classification activated
  - The code: [Link1:github](https://github.com/madhavkarri/CarND-P9-ProgrammingASelfDrivingCar/tree/master/src_vers/src_v7) and [Link2:gdrive](https://drive.google.com/drive/folders/1MHnLLm4Cw9CcQO_K9E97LsFzuVZuPic8)

- src: Final version
  - Both the Unity simulator and ROS running on Ubuntu 16.04
  - System Specifications: Intel Core i9-9900K Processor, NVIDIA GeForce RTX 2080 Super 8 GB, and 32 GB RAM
  - Activated TensorFlow GPU (version: 1.3.0)
  - Number of waypoints: 50
  - Camera publishing rate: 4 Hz
  - Final output video (Youtube): [Link](https://youtu.be/41H2Aetl3Uo)
  - The code: [Link1:github](https://github.com/madhavkarri/CarND-P9-ProgrammingASelfDrivingCar/tree/master/src_vers/src) and [Link2:gdrive](https://drive.google.com/drive/folders/1sVP7IoVzbNEzV9-uj_2On0IpJgQv9iDG)
  
Notes: 
- After launching the ROS and simulator, TensorFlow initialization takes about 4 mins before it can start performing classifcation. Therefore to overcome this issue dbw_enabled flag is not enabled or set to true until 4 mins. Prolonged TensorFlow intilization is an issue for some TensorFlow versions. However, have not spent time to address this issue.
- Link1: github and Link2: Google Drive. Large files are not supported on Github. Even if using git-lfs there is an git-lfs account limit of 1 GB.
