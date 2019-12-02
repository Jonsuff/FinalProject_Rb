#!/home/robot/.pyenv/versions/project1_365/bin/python


import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher
        self.count = 30
        self.turtle_vel = Twist()
        self.lds_right = None
        # self.past_lds = None
        # self.mode = "wait"

    def Delay(self, data):
        self.rate = rospy.Rate(data)
        self.rate.sleep()

    def lds_callback(self, scan):
        print("front : ", scan.ranges[0])
        print("210 : ", scan.ranges[210])
        print("270 : ", scan.ranges[270])
        print("330 : ", scan.ranges[330])
        self.lds_right = scan.ranges[270]

        if scan.ranges[0] < 0.45 and scan.ranges[0] > 0:
            self.turn_left()
        elif scan.ranges[0] > 0.45 and (scan.ranges[270] > 0.23 and scan.ranges[270] <0.28):
            self.adjust()
        else:
            self.go_straight()
            print("else init")

    def go_straight(self):
        self.turtle_vel.linear.x = 0.18
        self.turtle_vel.angular.z = 0.0
        self.publisher.publish(self.turtle_vel)
        print("go straight")

    def turn_left(self):
        self.turtle_vel.linear.x = 0.15
        self.turtle_vel.angular.z = 1.086
        self.publisher.publish(self.turtle_vel)
        if self.lds_right > 0.28 and self.lds_right <= 0.32:
            self.turtle_vel.linear.x = 0.15
            self.turtle_vel.angular.z = 0.0
        print("turn left")

    def adjust(self):
        self.turtle_vel.linear.x = 0.15
        self.turtle_vel.angular.z = -0.32
        self.publisher.publish(self.turtle_vel)
        print("adjusted")




def main():
    rospy.init_node('self_drive')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    driver = SelfDrive(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.lds_callback(scan))

    rospy.spin()


if __name__ == "__main__":
    main()
