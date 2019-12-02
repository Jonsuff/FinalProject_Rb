#!/home/jon/.pyenv/versions/rospy_365/bin/python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher
        self.cosTheta = 0
        self.cosTheta_back = 0
        self.rate = None
        self.turtle_vel = Twist()
        self.scanned = []
        self.sum = 0
        self.sum_out = 0
        self.mean = 0
        
        
    def lds_callback(self, scan):
        self.scanned = scan.ranges
        self.front_obs_detect()
        if scan.ranges[90] > 0.40:
            if scan.ranges[330] != 0:
                self.cosTheta = scan.ranges[270] / scan.ranges[330]
            if self.mean <= 0.45:
                self.turn_left()
            elif scan.ranges[0] > 0.30:
                self.go_straight()
                if self.cosTheta < 0.48:
                    self.adjust_to_right()
            elif scan.ranges[0] == 0:
                pass
        elif scan.ranges[90] <= 0.40:
            if scan.ranges[45] < 0.28 and scan.ranges[90] < 0.28:
                self.go_straight()
            elif scan.ranges[30] < 0.36:
                self.adjust_to_right() 
            else:
                self.turn_left_smooth()
      
        
    def Delay(self, data):
        self.rate = rospy.Rate(data)
        self.rate.sleep()
        
    def go_straight(self):
        self.turtle_vel.linear.x = 0.16
        self.turtle_vel.angular.z = 0.0
        self.publisher.publish(self.turtle_vel)
        
    def go_back(self):
        self.turtle_vel.linear.x = -0.08
        self.publisher.publish(self.turtle_vel)
        
    def turn_left(self):
        self.turtle_vel.linear.x = 0.12
        self.turtle_vel.angular.z = 1.35
        self.publisher.publish(self.turtle_vel)
        
    def turn_left_smooth(self):
        self.turtle_vel.linear.x = 0.15
        self.turtle_vel.angular.z = 0.65
        self.publisher.publish(self.turtle_vel)
        
    def turn_right(self):
        self.turtle_vel.linear.x = 0.12
        self.turtle_vel.angular.z = -1.35
        self.publisher.publish(self.turtle_vel)
        
    def adjust_to_right(self):
        self.turtle_vel.linear.x = 0.15
        self.turtle_vel.angular.z = -0.22
        self.publisher.publish(self.turtle_vel)
        print("adjust to right")
            
    def adjust_to_left(self):
        self.turtle_vel.linear.x = 0.15
        self.turtle_vel.angular.z = 0.15
        self.publisher.publish(self.turtle_vel)
        print("adjust to left")
            
    def front_obs_detect(self):
        for i in range(30):
            self.sum += self.scanned[329+i]
            print("{} : ".format(self.scanned[329+i]))
        self.mean = self.sum / 30
        self.sum = 0


def main():
    rospy.init_node('self_drive')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    driver = SelfDrive(publisher)
    driver.Delay(3)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.lds_callback(scan))
    rospy.spin()

if __name__ == "__main__":
    main()

