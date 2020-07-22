from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='shamrock_ui',
            executable='user_interface',
            name='GUI'
        ),
        # Node(
        #     package='shamrock_teleop',
        #     executable='remote_control',
        #     name='remote'
        # ),
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource([ThisLaunchFileDir(), '../../ydlidar_ros2/launch/ydlidar.py'])
        # )
    ])