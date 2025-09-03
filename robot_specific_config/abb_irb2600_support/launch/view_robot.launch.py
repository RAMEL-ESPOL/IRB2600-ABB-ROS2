# view_robot.launch.py – Adaptado para usar el XACRO principal (irb2600_main.xacro)
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.descriptions import ParameterValue


def generate_launch_description():
    # Declarar argumento para elegir el archivo XACRO (principal) dentro de urdf/
    robot_description_file_arg = DeclareLaunchArgument(
        'robot_description_file',
        default_value='irb2600_main.xacro',
        description='Archivo XACRO principal que define <robot> con el brazo y el gripper'
    )

    # Directorio share del paquete
    pkg_share = FindPackageShare('abb_irb2600_support')

    # Comando para procesar el XACRO seleccionado
    robot_description_content = Command([
        FindExecutable(name='xacro'), ' ',  
        PathJoinSubstitution([pkg_share, 'urdf', LaunchConfiguration('robot_description_file')])
    ])

    # Parámetro robot_description para robot_state_publisher
    robot_description = {
        'robot_description': ParameterValue(
            robot_description_content,
            value_type=str
        )
    }

    # Nodo robot_state_publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    # GUI de sliders de articulaciones
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    # Nodo RViz configurado con el archivo .rviz
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', PathJoinSubstitution([pkg_share, 'rviz', 'urdf_description.rviz'])]
    )

    return LaunchDescription([
        robot_description_file_arg,
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])
