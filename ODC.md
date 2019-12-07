# **Self-Driving Car**
# **Capstone Project: Programming A Self Driving Car**

## MK

## Traffic Light Detection and Classification

Overview

Discussion and details about the Object Detection and Classification performed as part of the Capstone Project: Programming A Self Driving Car.

As the car traverses along the test track inside the simulator, it has to detect traffic-lights and classify the light state of the detected traffic-light. This is performed using images from the front camera. Depending on the light state, the car stops at the traffic-light stop-line if it is "Red" or moves forward if it is either "Green or Yellow".

[//]: # (Image References)

[image1]: ./Writeup_IV/SpeedAccuracy_COD.png "SpeedAccuracy_COD"


#
Tensorflow Object Detection API and Tensorflow detection model zoo

The traffic light detection and classification was performed using Tensorflow Object Detection API in conjunction with Tensorflow detection model zoo. 

[Tensorflow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection)

Creating accurate machine learning models capable of localizing and identifying multiple objects in a single image remains a core challenge in computer vision. The TensorFlow Object Detection API is an open source framework built on top of TensorFlow that makes it easy to construct, train, and deploy object detection models

[Tensorflow detection model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md)

A collection of detection models pre-trained on the [COCO
dataset](http://mscoco.org), the [Kitti dataset](http://www.cvlibs.net/datasets/kitti/),
the [Open Images dataset](https://github.com/openimages/dataset), the
[AVA v2.1 dataset](https://research.google.com/ava/) and the
[iNaturalist Species Detection Dataset](https://github.com/visipedia/inat_comp/blob/master/2017/README.md#bounding-boxes).
These models can be useful for out-of-the-box inference for categories already in those datasets  and also for initializing models when training on novel datasets.

#
Selection of model from Tensorflow detection model zoo

The criteria for selection of model from the Tensorflow detection model zoo was based on the work by Jonathan Huang et al.,
[Speed/accuracy trade-offs for modern convolutional object detectors](https://arxiv.org/pdf/1611.10012.pdf).
 
 A summary of results from the above work is shown below:
![][image1]

Based on the above set of results the "Faster R-CNN w/ResNet, Hi Res, 50 Proposals" model was selected for traffic light detection and classification. This model is a good trade-off between speed and accuracy. Accordingly, the [faster_rcnn_resnet50_coco](http://download.tensorflow.org/models/object_detection/faster_rcnn_resnet50_coco_2018_01_28.tar.gz) was utilized for training the dataset.

#
Train and Test Data Sets

Training Data Set

The training data set was obtained from the following source [Link](https://github.com/coldKnight/TrafficLight_Detection-TensorFlowAPI). A few modifications were performed, such that the number of images consisting of Green and Yello traffic lights are equal. In addition the images in the data set were not labled and classified. The image labeling was performed using [LabelImg](https://github.com/tzutalin/labelImg). The final data set used for training can be accessed at [Link](https://drive.google.com/open?id=1kDV6NReRehsExP-mdMYqoYGszpVZhaEp)

Test Data Set

The test data set was obtained from the following source [Link](https://github.com/alex-lechner/Traffic-Light-Classification). The final data set used for testing can be accessed at [Link](https://drive.google.com/open?id=1cg_Owcn-nXXpufHn2g6D7ElVE65ZWqag)

#
Training

All the training was performed on [Google Colab]().

