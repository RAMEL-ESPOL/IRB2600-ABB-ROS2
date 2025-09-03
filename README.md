# 1) Crea el workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# 2) Clona este repositorio
git clone https://github.com/RAMEL-ESPOL/IRB2600-ABB-ROS2.git

# 3) Importa dependencias (usa el archivo abb.repos incluido en este repo)
vcs import < IRB2600-ABB-ROS2/abb.repos

# En una terminal con ROS 2 cargado (source /opt/ros/jazzy/setup.bash)
cd ~/ros2_ws
sudo apt update
rosdep update
rosdep install -r --from-paths src --ignore-src --rosdistro jazzy -y

cd ~/ros2_ws
colcon build --symlink-install
# Cargar el overlay
source install/setup.bash

