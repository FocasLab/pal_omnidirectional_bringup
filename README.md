# PAL Omni-directional Bringup

## 1. Introduction

This package launches a PAL Omni-directional drive robot in an empty Gazebo world and lets you add one static cylindrical obstacle. The robot’s spawn position and the obstacle’s position and radius can be configured through terminal commands.

## 2. System Requirements

- Ubuntu 22.04
- ROS 2 Humble
- Gazebo Classic 11

## 3. Setup

> **Using an existing workspace?** Make sure it has an `src` directory, and replace **`~/pal_ws`** in the commands below with the path to your workspace.

### Step 1: Create a ROS 2 workspace

```bash
mkdir -p ~/pal_ws/src
```

**If** you are using an existing workspace, **skip** this step.

### Step 2: Clone the package

Go to the workspace root:

```bash
cd ~/pal_ws
```

Clone the package into the `src` directory:

```bash
git clone https://github.com/FocasLab/pal_omnidirectional_bringup.git src/sim_bringup
```


### Step 3: Install missing dependencies

```bash
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
```

`rosdep` installs dependencies declared by the package that are missing from your system.

### Step 4: Build the workspace

Run the build command from the workspace root:

```bash
cd ~/pal_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install
```

## 4. Usage

### Terminal 1: Launch the world and robot

Open a terminal and source the workspace:

```bash
cd ~/pal_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
```

Launch the empty world and the robot :

```bash
ros2 launch sim_bringup simulation.launch.py
```

This places the robot at the origin: `x=0`, `y=0`, `yaw=0`.

**Optionally**, launch the robot at a desired position and orientation:

```bash
ros2 launch sim_bringup simulation.launch.py x:=2.0 y:=1.0 yaw:=1.57
```

`x` and `y` are in metres. `yaw` is in radians. Run either the default or optional  launch command, **not both**.

### Terminal 2: Spawn the obstacle

Keep Terminal 1 running. Open a second terminal and source the workspace:

```bash
cd ~/pal_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
```

Spawn a cylindrical obstacle:

```bash
ros2 run sim_bringup spawn_obstacle 1,2,0.3
```

The argument format is **`x,y,radius`**. This example places the obstacle at `(1, 2)` metres with a radius of `0.3` metres. Its height is fixed at 1 metre, and it rests on the ground. Running the command again replaces the existing obstacle.

## 5. Topics

| Topic | Message type | Purpose |
| --- | --- | --- |
| `/cmd_vel` | `geometry_msgs/msg/Twist` | Publish commands to move and turn the robot. |
| `/odom` | `nav_msgs/msg/Odometry` | Read the robot’s position, orientation, and velocity. The pose uses the `world` frame. |
| `/obstacle` | `sim_bringup/msg/Obstacle` | Read the obstacle’s centre position and radius. |
| `/scan` | `sensor_msgs/msg/LaserScan` | Read distance measurements from the robot’s LiDAR. |
