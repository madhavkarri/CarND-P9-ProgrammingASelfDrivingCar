# **Self-Driving Car**
# **Capstone Project: Programming A Self Driving Car**

## MK

## Object Detection and Classification: Traffic Light Detection and Classification

Overview

Discussion and details about the Object Detection and Classification performed as part of the Capstone Project: Programming A Self Driving Car.

As the car traverses along the test track inside the simulator, using images from the front camera, it has to detect traffic lights and classify the light state of the detected traffic light. Depending on the light state of the traffic light, the car stops at the traffic light stop line if it is "Red" or moves forward if it is either "Green or Yellow".

[//]: # (Image References)

[image1]: ./Writeup_IV/Carla_Architecture.png "Carla_Architecture"


#
Tensorflow Object Detection API

The traffic light detection and classification was performed using Tensorflow Object Detection API [Link](https://github.com/tensorflow/models/tree/master/research/object_detection). Creating accurate machine learning models capable of localizing and identifying multiple objects in a single image remains a core challenge in computer vision. The TensorFlow Object Detection API is an open source framework built on top of TensorFlow that makes it easy to construct, train, and deploy object detection models
