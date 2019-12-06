
import os
import cv2
import numpy as np
import tensorflow as tf
import sys

import label_map_util

from styx_msgs.msg import TrafficLight

class TLClassifier(object):
    def __init__(self):
        #TODO load classifier
        # pass

		# light state
		self.cur_ls = TrafficLight.UNKNOWN

		# This is needed since file is stored in
		sys.path.append("..")

		# Name of the directory containing the object detection module we're using
		MODEL_NAME = 'light_classification/inference_graph'

		# Grab path to current working directory
		CWD_PATH = os.getcwd()

		# Path to frozen detection graph .pb file, which contains the model that is used
		# for object detection.
		PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

		# Path to label map file
		PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,'labelmap.pbtxt')

		# Number of classes the object detector can identify
		NUM_CLASSES = 3

		# Load the label map.
		# Label maps map indices to category names, so that when our convolution
		# network predicts `1`, we know that this corresponds to `Red`.
		# Here we use internal utility functions, but anything that returns a
		# dictionary mapping integers to appropriate string labels would be fine
		label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
		categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
		category_index = label_map_util.create_category_index(categories)

		# Load the Tensorflow model into memory.
		detection_graph = tf.Graph()
		with detection_graph.as_default():
		    od_graph_def = tf.GraphDef()
		    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
				serialized_graph = fid.read()
				od_graph_def.ParseFromString(serialized_graph)
				tf.import_graph_def(od_graph_def, name='')

		    self.sess = tf.Session(graph=detection_graph)

		# Define input and output tensors (i.e. data) for the object detection classifier

		# Input tensor is the image
		self.image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

		# Output tensors are the detection boxes, scores, and classes
		# Each box represents a part of the image where a particular object was detected
		self.detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

		# Each score represents level of confidence for each of the objects.
		# The score is shown on the result image, together with the class label.
		self.detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
		self.detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

		# Number of objects detected
		self.num_detections = detection_graph.get_tensor_by_name('num_detections:0')


    def get_classification(self, image):
    	"""Determines the color of the traffic light in the image

    	Args:
    		image (cv::Mat): image containing the traffic light

		Returns:
			int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """

        # TODO implement light color prediction
        # return TrafficLight.UNKNOWN

        # Load image using OpenCV and
        # expand image dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
        # image = cv2.imread(PATH_TO_IMAGE)

        image_expanded = np.expand_dims(image, axis=0)

        # Perform the actual detection by running the model with the image as input
        (boxes, scores, classes, num) = self.sess.run(
        [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
        feed_dict={self.image_tensor: image_expanded})

        # assign classified light state to current light sate
        if scores[0,0]>0.80:
        	if (classes[0,0]==3.0):
        		self.cur_ls = 2
    		elif (classes[0,0]==2.0):
    			self.cur_ls = 1
    		elif (classes[0,0]==1.0):
    			self.cur_ls = 0
    		else:
    			self.cur_ls = 4


		return self.cur_ls

