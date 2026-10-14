from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    launch = Path(get_package_share_directory('sim_bringup')) / 'launch'
    return LaunchDescription([
        DeclareLaunchArgument('gui', default_value='true'),
        DeclareLaunchArgument('software_rendering', default_value='true'),
        DeclareLaunchArgument('x', default_value='0.0'),
        DeclareLaunchArgument('y', default_value='0.0'),
        DeclareLaunchArgument('yaw', default_value='0.0'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(str(launch / 'world.launch.py')),
            launch_arguments={
                'gui': LaunchConfiguration('gui'),
                'software_rendering': LaunchConfiguration('software_rendering'),
            }.items(),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(str(launch / 'spawn_robot.launch.py')),
            launch_arguments={key: LaunchConfiguration(key) for key in ('x', 'y', 'yaw')}.items(),
        ),
    ])
