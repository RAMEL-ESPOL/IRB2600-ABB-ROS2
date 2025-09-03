IRB2600-ABB-ROS2 (ROS 2 Jazzy)
Descripción

Este repositorio fue creado para conectar el robot ABB IRB-2600 del Laboratorio de Mecatrónica con ROS 2 (Jazzy). Incluye la descripción del robot, configuraciones de ros2_control, archivos de lanzamiento y utilidades para visualizarlo en RViz, simularlo y comunicarte con el controlador real (RWS/EGM). Está pensado como una base mínima y práctica para docencia, investigación y proyectos en el laboratorio.
1) Requisitos

ROS 2 Jazzy 
# 1) Crear workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# 2) Clonar este repositorio
git clone https://github.com/RAMEL-ESPOL/IRB2600-ABB-ROS2.git

# 3) Importar dependencias con vcstool (usa el archivo abb.repos del repo)
vcs import < IRB2600-ABB-ROS2/abb.repos
# Carga ROS 2 Jazzy (ajusta si usas otra shell)
source /opt/ros/jazzy/setup.bash

# Instalar dependencias del sistema de todos los paquetes del workspace
cd ~/ros2_ws
sudo apt update
rosdep update
rosdep install -r --from-paths src --ignore-src --rosdistro jazzy -y
cd ~/ros2_ws
colcon build --symlink-install

# Source enviroment
source install/setup.bash

Para esta simulación, ROS 2 ejecuta los controladores del robot (modo fake hardware). No necesitas RobotStudio ni un robot físico.
# 1) Lanzar controladores (fake hardware) y descripción del IRB2600
ros2 launch abb_bringup abb_control.launch.py \
  description_package:=abb_irb2600_support \
  description_file:=irb2600_main.xacro \
  launch_rviz:=false \
  moveit_config_package:=abb_irb2600_moveit_config \
  use_fake_hardware:=true
Después de lanzar los controladores, inicia MoveIt:
# 2) Lanzar MoveIt para planificar sobre el modelo simulado
ros2 launch abb_bringup abb_moveit.launch.py \
  robot_xacro_file:=irb2600_main.xacro \
  support_package:=abb_irb2600_support \
  moveit_config_package:=abb_irb2600_12_185_moveit_config \
  moveit_config_file:=abb_irb2600_12_185.srdf.xacro



