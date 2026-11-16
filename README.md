# RoboDog

## Setup Instructions

1. Clone the repository

2. Install dependencies and initialize rosdep if necessary

```
cd RoboDog/ros2_ws

sudo apt update

sudo apt install -y \
    python3-colcon-common-extensions \
    python3-rosdep \
    build-essential \
    ros-jazzy-ros-gz \
    ros-jazzy-turtlebot3* \
    ros-jazzy-cartographer \
    ros-jazzy-cartographer-ros \
    ros-jazzy-navigation2 \
    ros-jazzy-nav2-bringup

if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then
    sudo rosdep init
fi

rosdep update
```

3. Install package dependencies
```
cd ~/RoboDog/ros2_ws

source /opt/ros/jazzy/setup.bash

rosdep install --from-paths src \
    --ignore-src \
    --rosdistro jazzy \
    -r -y
```
4. Build the workspace
```
colcon build --symlink-install
```
5. Configure the environment

Run these commands in each new terminal, or add them to your ~/.bashrc to configure them automatically:
```
source /opt/ros/jazzy/setup.bash
source ~/RoboDog/ros2_ws/install/setup.bash

export TURTLEBOT3_MODEL=waffle

export GZ_SIM_RESOURCE_PATH="/opt/ros/jazzy/share/turtlebot3_gazebo/models${GZ_SIM_RESOURCE_PATH:+:$GZ_SIM_RESOURCE_PATH}"
```



## Running SLAM

1. Terminal 1 — Gazebo
```
source /opt/ros/jazzy/setup.bash
source ~/RoboDog/ros2_ws/install/setup.bash
export TURTLEBOT3_MODEL=waffle

ros2 launch house_simulation house.launch.py
```
2. Terminal 2 — EKF
```
source /opt/ros/jazzy/setup.bash
source ~/RoboDog/ros2_ws/install/setup.bash

ros2 run robot_localization ekf_node --ros-args --params-file ~/RoboDog/ros2_ws/src/house_simulation/config/ekf.yaml
```
3. Terminal 3 — Cartographer
```
source /opt/ros/jazzy/setup.bash
source ~/RoboDog/ros2_ws/install/setup.bash

ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=True
```
4. Terminal 4 — Keyboard teleoperation
```
source /opt/ros/jazzy/setup.bash

ros2 run teleop_twist_keyboard teleop_twist_keyboard
```