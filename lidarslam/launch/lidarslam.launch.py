import os

import launch
import launch_ros.actions

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    main_param_dir = launch.substitutions.LaunchConfiguration(
        'main_param_dir',
        default=os.path.join(
            get_package_share_directory('lidarslam'),
            'param',
            'lidarslam.yaml'))
    
    rviz_param_dir = launch.substitutions.LaunchConfiguration(
        'rviz_param_dir',
        default=os.path.join(
            get_package_share_directory('lidarslam'),
            'rviz',
            'mapping.rviz'))

    mapping = launch_ros.actions.Node(
        package='scanmatcher',
        executable='scanmatcher_node',
        parameters=[main_param_dir],
        remappings=[('/input_cloud','/lexus3/os_center/points')],
        output='screen'
        )

    tf__ = launch_ros.actions.Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0','0','0','0','0','0','1','base_link','velodyne']
        )
    ## ros2 bag play /mnt/c/bag/slam_campus_thome01_lexus3_2025-02-07_13-52_0.mcap --clock --remap /tf:=/tf_devnull
    ## issue command also: ros2 run tf2_ros static_transform_publisher --x 0.75 --y 0.0 --z 1.91 --yaw 0.0 --pitch 0.0 --roll 0.0 --frame-id base_link --child-frame-id lexus3/os_center_a_laser_data_frame
    tf = launch_ros.actions.Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='center1_os_front_tf_publisher',
        output='screen',
        arguments=[
            '--x',     '0.75',
            '--y',     '0.0',
            '--z',     '1.91',
            '--yaw',   '0.0',
            '--pitch', '0.0',
            '--roll',  '0.0',

            '--frame-id',       'base_link',
            '--child-frame-id', 'lexus3/os_center_a_laser_data_frame'
        ],
    )

    graphbasedslam = launch_ros.actions.Node(
        package='graph_based_slam',
        executable='graph_based_slam_node',
        parameters=[main_param_dir],
        output='screen'
        )
    
    rviz = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_param_dir]
        )


    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            'main_param_dir',
            default_value=main_param_dir,
            description='Full path to main parameter file to load'),
        mapping,
        tf,
        graphbasedslam,
        rviz,
            ])