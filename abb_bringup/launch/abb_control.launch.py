from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.conditions import IfCondition
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def launch_setup(context, *args, **kwargs):
    # Evaluar argumentos para validación
    use_fake_hardware_val = LaunchConfiguration("use_fake_hardware").perform(context).lower()
    rws_ip_val = LaunchConfiguration("rws_ip").perform(context)

    # === Regla: si NO se usa fake hardware => exigir rws_ip ===
    if use_fake_hardware_val in ("false", "0", "no"):
        if (rws_ip_val is None) or (rws_ip_val.strip() == "") or (rws_ip_val.strip().lower() == "none"):
            raise RuntimeError(
                "[abb_control.launch.py] use_fake_hardware:=false (hardware real) requiere definir rws_ip "
                "(ejemplo: rws_ip:=192.168.0.10)."
            )

    # Re-crear LaunchConfigurations (para usarlas como Substitutions)
    runtime_config_package = LaunchConfiguration("runtime_config_package")
    controllers_file = LaunchConfiguration("controllers_file")
    description_package = LaunchConfiguration("description_package")
    moveit_config_package = LaunchConfiguration("moveit_config_package")
    description_file = LaunchConfiguration("description_file")
    prefix = LaunchConfiguration("prefix")
    use_fake_hardware = LaunchConfiguration("use_fake_hardware")
    fake_sensor_commands = LaunchConfiguration("fake_sensor_commands")
    rws_ip = LaunchConfiguration("rws_ip")
    rws_port = LaunchConfiguration("rws_port")
    configure_via_rws = LaunchConfiguration("configure_via_rws")
    initial_joint_controller = LaunchConfiguration("initial_joint_controller")
    launch_rviz = LaunchConfiguration("launch_rviz")

    # Construir robot_description vía xacro
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare(description_package), "urdf", description_file]
            ),
            " ",
            "prefix:=",
            prefix,
            " ",
            "use_fake_hardware:=",
            use_fake_hardware,
            " ",
            "fake_sensor_commands:=",
            fake_sensor_commands,
            " ",
            "rws_ip:=",
            rws_ip,
            " ",
            "rws_port:=",
            rws_port,
            " ",
            "configure_via_rws:=",
            configure_via_rws,
            " ",
        ]
    )
    robot_description = {
        "robot_description": ParameterValue(robot_description_content, value_type=str)
    }

    robot_controllers = PathJoinSubstitution(
        [FindPackageShare(runtime_config_package), "config", controllers_file]
    )

    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare(moveit_config_package), "rviz", "moveit.rviz"]
    )

    # Nodos
    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_description, robot_controllers],
        output="both",
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )

    rviz_node = Node(
        package="rviz2",
        condition=IfCondition(launch_rviz),
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
    )

    initial_joint_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[initial_joint_controller, "-c", "/controller_manager"],
    )

    return [
        control_node,
        robot_state_publisher_node,
        rviz_node,
        joint_state_broadcaster_spawner,
        initial_joint_controller_spawner,
    ]


def generate_launch_description():
    declared_arguments = []

    # === Defaults IRB-2600 ===
    declared_arguments.append(
        DeclareLaunchArgument(
            "runtime_config_package",
            default_value="abb_bringup",
            description='Package con configuración de controllers en "config".',
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "controllers_file",
            default_value="abb_controllers.yaml",
            description="YAML con la configuración de controllers.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "description_package",
            default_value="abb_irb2600_support",
            description="Paquete con URDF/Xacro del robot.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "moveit_config_package",
            default_value="abb_irb2600_moveit_config",
            description="Paquete de configuración de MoveIt del robot.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "description_file",
            default_value="irb2600_main.xacro",
            description="Archivo URDF/Xacro del robot.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "prefix",
            default_value='""',
            description="Prefijo de joints (para multi-robot).",
        )
    )

    # Por defecto: simulación (no requiere rws_ip)
    declared_arguments.append(
        DeclareLaunchArgument(
            "use_fake_hardware",
            default_value="true",
            description="Si false (hardware real), se exigirá rws_ip.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "rws_ip",
            default_value="None",
            description="IP de RWS (requerida solo si use_fake_hardware==false).",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "rws_port",
            default_value="80",
            description="Puerto de RWS.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "configure_via_rws",
            default_value="true",
            description="Si false, la descripción se genera desde ros2_control xacro.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "fake_sensor_commands",
            default_value="false",
            description="Comandos falsos para sensores (simples).",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "initial_joint_controller",
            default_value="joint_trajectory_controller",
            description="Controller inicial del robot.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "launch_rviz",
            default_value="false",
            description="¿Lanzar RViz?",
        )
    )

    return LaunchDescription(declared_arguments + [OpaqueFunction(function=launch_setup)])
