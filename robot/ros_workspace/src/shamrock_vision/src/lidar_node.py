#!/usr/bin/python3

import rospy

from geometry_msgs.msg import Point32
from sensor_msgs.msg import LaserScan, PointCloud

# Point Cloud Publisher
point_cloud_pub = rospy.Publisher("/point_cloud", PointCloud, queue_size=1)

def lidar_callback(scan_msg):
    idx = 0
    angle = scan_msg.angle_min
    point_cloud = PointCloud()

    # Run through all the angles
    while angle < scan_msg.angle_max:
        dist = ranges[idx]

        # Only consider real readings
        if dist >= scan_msg.range_min and dist <= scan_msg.range_max:
            x = dist * cos(angle)
            y = dist * sin(angle)
            point = Point32(x = x, y = y, z = 0)
            tmp_point_cloud.points.append(point)

        # Update angle and index
        angle += scan_msg.angle_increment
        idx += 1

    # Publish the local point cloud
    point_cloud_pub.publish(point_cloud)

def main():
    # Init node.
    rospy.init_node("lidar_node")

    # Subscribe to the LiDAR.
    lidar_sub = rospy.Subscriber("/scan", LaserScan, lidar_callback, queue_size=1)

    # Spin
    rospy.spin()

if __name__ == "__main__":
    main()