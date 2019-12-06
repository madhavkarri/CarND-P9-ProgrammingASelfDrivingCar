#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from geometry_msgs.msg import PoseStamped, Pose
from styx_msgs.msg import TrafficLightArray, TrafficLight
from styx_msgs.msg import Lane
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from light_classification.tl_classifier import TLClassifier
from scipy.spatial import KDTree
import tf
import cv2
import yaml

# import time
import datetime
import os

STATE_COUNT_THRESHOLD = 3
# ODC_COUNT_THRESHOLD = 5 # classification on every fifth image from camera feed, skips in between frames
#                         # every fifth must also meet below criteria for classification

# optimum distance for object detection classification
# is about 10-35 waypoints
diff_cpsl_lb = 5 # lower bound
diff_cpsl_ub = 75 # upper bound

class TLDetector(object):
    def __init__(self):
        rospy.init_node('tl_detector')

        self.pose = None
        self.base_waypoints = None
        self.waypoints_2d = None
        self.waypoint_tree = None
        self.camera_image = None
        self.lights = []

        self.bridge = CvBridge()

        self.light_classifier = TLClassifier()
        self.listener = tf.TransformListener()

        self.state = TrafficLight.UNKNOWN
        self.last_state = TrafficLight.UNKNOWN
        self.last_wp = -1
        self.state_count = 0
        
        self.tl_id = 0
        self.my_lwi = 292
        self.first_lwi = 292
        self.prev_lwi = 292

        self.diff_cpsl = None # waypoint index difference between car current pose and traffic light stop line
        self.classification_prev = 0 # previous classification state

        config_string = rospy.get_param("/traffic_light_config")
        self.config = yaml.load(config_string)

        sub1 = rospy.Subscriber('/current_pose', PoseStamped, self.pose_cb)
        sub2 = rospy.Subscriber('/base_waypoints', Lane, self.waypoints_cb)
        sub3 = rospy.Subscriber('/vehicle/traffic_lights', TrafficLightArray, self.traffic_cb)
        sub6 = rospy.Subscriber('/image_color', Image, self.image_cb)
        self.upcoming_red_light_pub = rospy.Publisher('/traffic_waypoint', Int32, queue_size=1)        

        '''
        /vehicle/traffic_lights provides you with the location of the traffic light in 3D map spacle and
        helps you acquire an accurate ground truth data source for the traffic light
        classifier by sending the current color state of all traffic lights in the
        simulator. When testing on the vehicle, the color state will not be available. You'll need to
        rely on the position of the light and the camera image to predict it.
        '''

        rospy.spin()

    def pose_cb(self, msg):
        self.pose = msg

    def waypoints_cb(self, waypoints):
        self.base_waypoints = waypoints
        if not self.waypoints_2d:
            self.waypoints_2d = [[waypoint.pose.pose.position.x, waypoint.pose.pose.position.y] for waypoint in waypoints.waypoints]
            self.waypoint_tree = KDTree(self.waypoints_2d)

    def traffic_cb(self, msg):
        self.lights = msg.lights

    def image_cb(self, msg):
        """Identifies red lights in the incoming camera image and publishes the index
            of the waypoint closest to the red light's stop line to /traffic_waypoint

        Args:
            msg (Image): image from car-mounted camera

        """
        self.has_image = True
        self.camera_image = msg
        light_wp, state = self.process_traffic_lights()

        '''
        Publish upcoming red lights at camera frequency.
        Each predicted state has to occur `STATE_COUNT_THRESHOLD` number
        of times till we start using it. Otherwise the previous stable state is
        used.
        '''
        if self.state != state:
            self.state_count = 0
            self.state = state
        elif self.state_count >= STATE_COUNT_THRESHOLD:
            self.last_state = self.state
            light_wp = light_wp if state == TrafficLight.RED else -1
            self.last_wp = light_wp
            self.upcoming_red_light_pub.publish(Int32(light_wp))
        else:
            self.upcoming_red_light_pub.publish(Int32(self.last_wp))
        self.state_count += 1

    def get_closest_waypoint(self, x, y):
        """Identifies the closest path waypoint to the given position
            https://en.wikipedia.org/wiki/Closest_pair_of_points_problem
        Args:
            pose (Pose): position to match a waypoint to
            Note: chnaged from 2 inputs (self, pose) to 3 inputs (self, x, y)

        Returns:
            int: index of the closest waypoint in self.waypoints

        """
        #TODO implement
    	return self.waypoint_tree.query([x, y], 1)[1]


    def get_light_state(self, light):
        """Determines the current color of the traffic light

        Args:
            light (TrafficLight): light to classify

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """

        '''        
        if(not self.has_image):
            self.prev_light_loc = None
            return False
        '''

        # cv_image = self.bridge.imgmsg_to_cv2(self.camera_image, "bgr8")

        # execute this code prior to classification 
        # save/capture  image files to determine optimum distance for image capture
        # image capture using optimum distance (not too far or not too close from/to traffic light) 
        # will increase accuracy/precision of Classifier

        if self.my_lwi == self.first_lwi:
            self.tl_id = 0
        elif self.my_lwi != self.prev_lwi:
            self.prev_lwi= self.my_lwi            
            self.tl_id += 1
        else:
            self.prev_lwi= self.my_lwi

        rospy.logwarn("Next Traffic Light ID: {0}".format(self.tl_id))
        rospy.logwarn("Light State (Ground Truth): {0}".format(light.state))

        if self.diff_cpsl >= diff_cpsl_lb and self.diff_cpsl <= diff_cpsl_ub:

            cv_image = self.bridge.imgmsg_to_cv2(self.camera_image, "bgr8")

            # capture camera images for classification training

            # execute this code prior to classification 
            # save/capture  image files to determine optimum distance for image capture
            # image capture using optimum distance (not too far or not too close from/to traffic light) 
            # will increase accuracy/precision of Classifier

            # my_ct1 = datetime.datetime.now()
            # my_ct2 = '%s_%s_%s_%s' % (str(my_ct1.hour).zfill(2),str(my_ct1.minute).zfill(2), str(my_ct1.second).zfill(2), str(my_ct1.microsecond)[:3].zfill(3))
            
            # file_name = 'imgs/'+my_ct2+'_'+str(self.tl_id).zfill(2)+'_'+str(self.diff_cpsl).zfill(2)+'_'+str(light.state)+'.jpg'
            # # cv2.imwrite(file_name, cv_image)

            # # put text optimum image capture distance
            # position = (10,50)
            # cv2.putText(
            #     cv_image, # numpy array on which text is written
            #     'Opt_ICD:'+str(self.diff_cpsl), # text
            #     position, # position at which writing has to start
            #     cv2.FONT_HERSHEY_SIMPLEX, # font family
            #     1, # font size
            #     (255, 255, 255), # font color
            #     1) # font stroke

            # # put text traffic ligh id
            # position = (600,50)
            # cv2.putText(
            #     cv_image, # numpy array on which text is written
            #     'TL_ID:'+str(self.tl_id), # text
            #     position, # position at which writing has to start
            #     cv2.FONT_HERSHEY_SIMPLEX, # font family
            #     1, # font size
            #     (255, 255, 255), # font color
            #     1) # font stroke

            # # changing folder to save for images with text
            # file_name = 'imgs_txt/'+my_ct2+'_'+str(self.tl_id).zfill(2)+'_'+str(self.diff_cpsl).zfill(2)+'_'+str(light.state)+'.jpg'
            # # cv2.imwrite(file_name, cv_image)

            # Get classification
            # classification =  self.light_classifier.get_classification(cv_image)
            # rospy.logwarn("Light State (classification): {0}".format(classification))


        return light.state



    def process_traffic_lights(self):
        """Finds closest visible traffic light, if one exists, and determines its
            location and color

        Returns:
            int: index of waypoint closes to the upcoming stop line for a traffic light (-1 if none exists)
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        closest_light = None
        light_wp_idx = -1
        state = TrafficLight.UNKNOWN        

        # List of positions that correspond to the line to stop in front of a given intersection
        stop_line_positions = self.config['stop_line_positions']
        if(self.pose):
            car_wp_idx = self.get_closest_waypoint(self.pose.pose.position.x, self.pose.pose.position.y)

        #TODO find the closest visible traffic light (if one exists)
        diff = len(self.base_waypoints.waypoints)
        for i, light in enumerate(self.lights):
            # Get stop line waypoint index
            line = stop_line_positions[i]
            temp_wp_idx = self.get_closest_waypoint(line[0], line[1])
            # Find closest wapoint stopline index
            d = temp_wp_idx - car_wp_idx
            if d >= 0 and d < diff:
                diff = d
                closest_light = light
                light_wp_idx = temp_wp_idx
                self.my_lwi = light_wp_idx

        if closest_light == None:
            line = stop_line_positions[0]
            light_wp_idx = self.get_closest_waypoint(line[0], line[1])
            self.my_lwi = light_wp_idx
            closest_light = self.lights[0]

        # distance (waypoint difference) between car current pose/waypoint and traffic ligth stop line waypoint
        self.diff_cpsl = diff
        if closest_light:
            state = self.get_light_state(closest_light)
            return light_wp_idx, state

if __name__ == '__main__':
    try:
        TLDetector()
    except rospy.ROSInterruptException:
        rospy.logerr('Could not start traffic node.')
