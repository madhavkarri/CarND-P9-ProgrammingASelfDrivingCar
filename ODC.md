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
Tensorflow Object Detection API and Tensorflow detection model zoo

The traffic light detection and classification was performed using Tensorflow Object Detection API [Link](https://github.com/tensorflow/models/tree/master/research/object_detection). 

Tensorflow Object Detection API

Creating accurate machine learning models capable of localizing and identifying multiple objects in a single image remains a core challenge in computer vision. The TensorFlow Object Detection API is an open source framework built on top of TensorFlow that makes it easy to construct, train, and deploy object detection models

Tensorflow detection model zoo

A collection of detection models pre-trained on the [COCO
dataset](http://mscoco.org), the [Kitti dataset](http://www.cvlibs.net/datasets/kitti/),
the [Open Images dataset](https://github.com/openimages/dataset), the
[AVA v2.1 dataset](https://research.google.com/ava/) and the
[iNaturalist Species Detection Dataset](https://github.com/visipedia/inat_comp/blob/master/2017/README.md#bounding-boxes).
These models can be useful for out-of-the-box inference if you are interested in
categories already in those datasets. They are also useful for initializing your
models when training on novel datasets.
