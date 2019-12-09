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
[image3]: ./Writeup_IV/MyOD6_GCL_TB1.png "MyOD6_GCL_TB1"
[image4]: ./Writeup_IV/MyOD6_GCL_TB2.png "MyOD6_GCL_TB2"
[image5]: ./Writeup_IV/MyOD6_GCL_TB3.png "MyOD6_GCL_TB3"


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
- In this work, instead of using the latest Tensor Flow models, training was performed using Tensor Flow models based on [version 1.13](https://github.com/tensorflow/models/tree/r1.13.0), one version below the latest version as of 12/07/2019. For a complete guide on Tensor Flow models based on various versions of Tensor Flow refer to this [work](https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10)

Training: Tools and Procedure
- Tensor Flow version 1.13.2 and the necessary packages to run the object detection API are shown below
![][image2]
- Create conda environment with the above listed packages and execute the below set of commands sequentially using Anaconda command prompt:
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
  - `python xml_to_csv.py`
  - `python generate_tfrecord.py --csv_input=images/train_labels.csv --image_dir=images/train --output_path=train.record`
  - `python generate_tfrecord.py --csv_input=images/test_labels.csv --image_dir=images/test --output_path=test.record`
  - `python legacy/train.py --logtostderr --train_dir=training/ --pipeline_config_path=training/faster_rcnn_resnet50_coco.config`
  
- To keep track of the above training process and various loss variables, open another Anaconda command prompt and execute below set of commands
  - `cd C:/Users/???/Desktop/CarND/MyOD6_GCL/models/research/object_detection/`
  - `tensorboard --logdir=training`
- Executing the above two commands would result in a http address with port 6006. The training progress and other loss variables can be viewed using a browser and the http address.

Frozen Inference Graph
- After the training is completed a frozen inference graph can be created using the below command:
  - `python export_inference_graph.py --input_type image_tensor --pipeline_config_path training/faster_rcnn_resnet50_coco.config --trained_checkpoint_prefix training/model.ckpt-???? --output_directory inference_graph`
  - `model.ckpt-????` represents one of the saved model checkpoints from the training process. Typically this model-checkpoint refers to one with the lowest total loss.

Testing Classifier
- After the inference graph has been created, test the classifier on images using the below command
- `python my_Object_detection_image.py`
- The above python code typically is written to test on a single image. If it is necessary to test the classifier on multiple images in a single session use the following python code [my_Object_detection_image.py](https://drive.google.com/open?id=1D4pAmQ_Cauqpcxp0hO5u5u3_YuXcupnk)

Google Colab
- All the training has been performed in Google Colab (Colab) because of the ease of access to GPU
- After the training has been tested on local machine, upload the working folder as a zip file to Google Drive. It is easier to upload to Google Drive and doing a transfer from Google Drive to Colab rather than uploading directly to Colab
- Training in Colab is performed in iPython notebook. iPython notebook used for this work can be accessed [here](./Writeup_IV/od6_req.ipynb). Execute the cells one at a time 

Training results from Google Colab: it shows Total Loss as a function of number of steps/iterations. The model-checkpoint for generating the inference graph was selected approximately at step number 70,000. The selected model-checkpoint was 69,544. The total loss at step number 69,544 was approximately 0.02

![][image3]

<!-- 
![][image4])
![][image5]
-->

By running the evaluation on the test and train data sets, the following mertrics were obtained:
- Train Data Set

`Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.981`

 `Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 1.000`
 
 `Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 0.997`
 
 `Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.942`
 
 `Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.997`
 
 `Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 1.000`
 
 `Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.340`
 
 `Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.984`
 
 `Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.984`
 
 `Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.953`
 
 `Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.998`
 
 `Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 1.000`
 
`INFO:tensorflow:DetectionBoxes_Precision/mAP: 0.981119`

`INFO:tensorflow:DetectionBoxes_Precision/mAP (large): 1.000000`

`INFO:tensorflow:DetectionBoxes_Precision/mAP (medium): 0.996519`

`INFO:tensorflow:DetectionBoxes_Precision/mAP (small): 0.941960`

`INFO:tensorflow:DetectionBoxes_Precision/mAP@.50IOU: 0.999881`

`INFO:tensorflow:DetectionBoxes_Precision/mAP@.75IOU: 0.996602`

`INFO:tensorflow:DetectionBoxes_Recall/AR@1: 0.339729`

`INFO:tensorflow:DetectionBoxes_Recall/AR@10: 0.984217`

`INFO:tensorflow:DetectionBoxes_Recall/AR@100: 0.984217`

`INFO:tensorflow:DetectionBoxes_Recall/AR@100 (large): 1.000000`

`INFO:tensorflow:DetectionBoxes_Recall/AR@100 (medium): 0.997663`

`INFO:tensorflow:DetectionBoxes_Recall/AR@100 (small): 0.953016`

- Test Data Set
  - PascalBoxes_PerformanceByCategory/AP@0.5IOU/b'Green': 0.887854
  - PascalBoxes_PerformanceByCategory/AP@0.5IOU/b'Red': 0.945645
  - PascalBoxes_PerformanceByCategory/AP@0.5IOU/b'Yellow': 0.938653
  - PascalBoxes_Precision/mAP@0.5IOU: 0.924051
  
- Furthermore, Udacity supplied Ubuntu image with ROS installation uses Tensor Flow version 1.3.0

