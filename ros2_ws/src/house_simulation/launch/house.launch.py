import os

from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch import LaunchDescription
from launch.actions import ExecuteProcess


def generate_launch_description():

    pkg_dir = get_package_share_directory('house_simulation')
    world_file = os.path.join(pkg_dir, 'worlds', 'house.sdf')

    gazebo = ExecuteProcess(
        cmd=[
            'gz', 'sim',
            '-r',
            world_file
        ],
        output='screen'
    )

    bridge = ExecuteProcess(
        cmd=[
            'ros2', 'run', 'ros_gz_bridge', 'parameter_bridge',
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'
        ],
        output='screen'
    )

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    turtlebot3_launch_dir = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'launch'
    )

    robot_state_publisher = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(turtlebot3_launch_dir, 'robot_state_publisher.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    return LaunchDescription([
        gazebo,
        bridge,
        robot_state_publisher
    ])