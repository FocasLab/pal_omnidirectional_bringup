import os
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    package = Path(get_package_share_directory('sim_bringup'))
    gazebo = Path(get_package_share_directory('gazebo_ros'))
    return LaunchDescription([
        DeclareLaunchArgument('gui', default_value='true'),
        DeclareLaunchArgument(
            'software_rendering', default_value='true',
            description='Use Mesa software rendering instead of the GPU driver.',
        ),
        SetEnvironmentVariable(
            'LIBGL_ALWAYS_SOFTWARE', '1',
            condition=IfCondition(LaunchConfiguration('software_rendering')),
        ),
        SetEnvironmentVariable(
            '__GLX_VENDOR_LIBRARY_NAME', 'mesa',
            condition=IfCondition(LaunchConfiguration('software_rendering')),
        ),
        SetEnvironmentVariable(
            'GAZEBO_RESOURCE_PATH',
            [str(Path(os.environ.get('GAZEBO_INSTALL_PREFIX', '/usr')) / 'share/gazebo-11'),
             os.pathsep, EnvironmentVariable('GAZEBO_RESOURCE_PATH', default_value='')],
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(str(gazebo / 'launch/gazebo.launch.py')),
            launch_arguments={
                'world': str(package / 'worlds/empty.world'),
                'gui': LaunchConfiguration('gui'),
                'server_required': 'true',
                'force_system': 'false',
                'lockstep': 'true',
            }.items(),
        ),
        Node(
            package='sim_bringup', executable='obstacle_server',
            parameters=[{'use_sim_time': True}], output='screen',
        ),
    ])
