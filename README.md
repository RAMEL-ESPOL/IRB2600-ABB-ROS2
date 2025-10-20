# IRB2600-ABB-ROS2 (ROS 2 Jazzy)

Repositorio para conectar el robot ABB **IRB-2600** del Laboratorio de Mecatrónica con **ROS 2 (Jazzy)**. Incluye la descripción del robot, configuraciones de `ros2_control`, archivos de lanzamiento y utilidades para visualizarlo en **RViz**, planificar con **MoveIt** y comunicarse con el controlador real (**RWS/EGM**). Está pensado como una base **mínima y práctica** para docencia, investigación y proyectos en el laboratorio.

---

## Requisitos

- **Ubuntu 24.04** (recomendado)  
- **ROS 2 Jazzy**
- **colcon**, **rosdep**, **vcstool**
- Git

> Si usas otra *shell*, ajusta `setup.bash` por `setup.zsh` o equivalente.

---

## Instalación

### 1) Crear workspace

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

### 2) Clonar este repositorio

```bash
git clone https://github.com/RAMEL-ESPOL/IRB2600-ABB-ROS2.git
```

### 3) Importar dependencias con vcstool (usa `abb.repos` del repo)

> Si no tienes vcstool: `sudo apt install -y python3-vcstool`

```bash
vcs import < IRB2600-ABB-ROS2/abb.repos
```

### 4) Cargar ROS 2 Jazzy

```bash
source /opt/ros/jazzy/setup.bash
```

### 5) Instalar dependencias del sistema de todos los paquetes

```bash
cd ~/ros2_ws
sudo apt update
rosdep update
rosdep install -r --from-paths src --ignore-src --rosdistro jazzy -y
```

### 6) Compilar

```bash
cd ~/ros2_ws
colcon build --symlink-install
```

### 7) Cargar el environment del workspace

```bash
source install/setup.bash
```

---

## Uso (simulación con *fake hardware*)

Para esta simulación, ROS 2 ejecuta los controladores del robot en **modo fake hardware**. No necesitas RobotStudio ni un robot físico.

### 1) Lanzar controladores y descripción del IRB2600

```bash
ros2 launch abb_bringup abb_control.launch.py
```

### 2) Lanzar MoveIt para planificar sobre el modelo simulado

```bash
ros2 launch abb_bringup abb_moveit.launch.py
```

---

## Notas

- Si vas a trabajar con controlador real (RWS/EGM), revisa la configuración de red, permisos RWS y los parámetros del `ros2_control` en tu `xacro/urdf` y *launch* correspondientes.
- Para sesiones nuevas, recuerda **volver a hacer**:
  ```bash
  source /opt/ros/jazzy/setup.bash
  source ~/ros2_ws/install/setup.bash
  ```

---

## Licencia

Este proyecto se distribuye con fines académicos. Revisa el archivo `LICENSE` si está disponible o define la licencia de tu preferencia.

