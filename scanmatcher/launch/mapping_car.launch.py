import os

import launch
import launch_ros.actions

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    mapping_param_dir = launch.substitutions.LaunchConfiguration(
        'mapping_param_dir',
        default=os.path.join(
            get_package_share_directory('scanmatcher'),
            'param',
            'mapping_car.yaml'))

    mapping = launch_ros.actions.Node(
        package='scanmatcher',
        executable='scanmatcher_node',
        parameters=[mapping_param_dir],
        remappings=[('/input_cloud','/lexus3/os_center/points')],# Autoware
        output='screen'
        )

    tf = launch_ros.actions.Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['1.2','0','2.0','0','0','0','1','base_link','velodyne']
    )

    tf_a = launch_ros.actions.Node(
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

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            'mapping_param_dir',
            default_value=mapping_param_dir,
            description='Full path to mapping parameter file to load'),
        mapping,
        tf_a
            ])