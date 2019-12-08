# **Self-Driving Car**
# **Capstone Project: Programming A Self Driving Car**

## MK

## Traffic Light Detection and Classification

Overview

Discussion and details about the Object Detection and Classification performed as part of the Capstone Project: Programming A Self Driving Car.

As the car traverses along the test track inside the simulator, it has to detect traffic-lights and classify the light state of the detected traffic-light. This is performed using images from the front camera. Depending on the light state, the car stops at the traffic-light stop-line if it is "Red" or moves forward if it is either "Green or Yellow".

[//]: # (Image References)

[image1]: ./Writeup_IV/SpeedAccuracy_COD.png "SpeedAccuracy_COD"
[image2]: ./Writeup_IV/TFV_1p13p2.png "TFV_1p13p2"


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

All the training was performed on [Google Colab](https://colab.research.google.com/notebooks/welcome.ipynb) using a GPU (GPU is usually a NVIDIA Tesla P100). However, all the preliminary or preprocessing work was performed locally on windows machine.

Some of the preliminary and preprocessing work was performed based on this [tutorial](https://medium.com/object-detection-using-tensorflow-and-coco-pre/object-detection-using-tensorflow-and-coco-pre-trained-models-5d8386019a8) at medium.com

Important Notes:
- Installed Anconda for windows [Link](https://www.anaconda.com/distribution/). Did not use Anconda GUI for this project, but rather the most useful tool from Anconda installation was the use of "Conda Environments". Using "Conda Environments" it was easy to maintain different Tensor Flow versions and its associated dependencies.
- The TensorFlow models repository's code (which contains the object detection API) is continuously updated by the developers. Sometimes they make changes that break functionality with old versions of TensorFlow [Link](https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10).
- In addtion, the older TensorFlow models repositories do not have all the latest object detection models (pre-trained classifiers with specific neural network architectures).
- In this work, instead of using the latest Tensor Flow models, training was performed using Tensor Flow models based on [version 1.13](https://github.com/tensorflow/models/tree/r1.13.0), one version below the latest version as of 12/07/2019. For a complete guide on Tensor Flow models based on various versions of Tensor Flow refer to this [work](https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10).
- Tensor Flow version 1.13.2 and the necessary packages to run the object detection API are shown below
![][image2]
- Once the necessary environment has been created with the packages listed above, follow the below set of steps sequentially
  - `set PYTHONPATH=C:/Users/???/Desktop/CarND/MyOD6_GCL/models`
  - `set PYTHONPATH=C:/Users/???/Desktop/CarND/MyOD6_GCL/models/research`
  - `set PYTHONPATH=C:/Users/???/Desktop/CarND/MyOD6_GCL/models/research/slim`
  -  `set PATH=%PATH%;PYTHONPATH`
  - `echo %PATH%`
  - `echo %PYTHONPATH%`
  - `cd C:/Users/???/Desktop/CarND/MyOD6_GCL/models/research`
  - `for /f %i in ('dir /b object_detection\protos\*.proto') do protoc object_detection\protos\%i --python_out=.`
  - `python setup.py build`
  - `python setup.py install`
  - `cd object_detection`
  - ``

- Furthermore, Udacity supplied Ubuntu image with ROS installation uses Tensor Flow version 1.3.0

