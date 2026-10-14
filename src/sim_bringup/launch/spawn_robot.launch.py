import math
from pathlib import Path

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def spawn(context):
    pose = {key: LaunchConfiguration(key).perform(context) for key in ('x', 'y', 'yaw')}
    if not all(math.isfinite(float(value)) for value in pose.values()):
        raise ValueError('x, y and yaw must be finite numbers')
    package = Path(get_package_share_directory('sim_bringup'))
    description = xacro.process_file(str(package / 'urdf/omni_base.urdf.xacro')).toxml()
    return [
        Node(
            package='robot_state_publisher', executable='robot_state_publisher',
            parameters=[{'robot_description': description, 'use_sim_time': True}],
            output='screen',
        ),
        Node(
            package='gazebo_ros', executable='spawn_entity.py',
            arguments=[
                '-entity', 'omni_base', '-topic', 'robot_description',
                '-x', pose['x'], '-y', pose['y'], '-Y', pose['yaw'],
                '-z', '0.01', '-timeout', '60',
            ],
            output='screen',
        ),
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('x', default_value='0.0', description='World x in metres.'),
        DeclareLaunchArgument('y', default_value='0.0', description='World y in metres.'),
        DeclareLaunchArgument('yaw', default_value='0.0', description='World yaw in radians.'),
        OpaqueFunction(function=spawn),
    ])
