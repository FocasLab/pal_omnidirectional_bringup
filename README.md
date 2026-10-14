# PAL Omni-directional Bringup

## 1. Introduction

This package launches a PAL Omni-directional drive robot in an empty Gazebo world and lets you add one static cylindrical obstacle. The robot’s spawn position and the obstacle’s position and radius can be configured through terminal commands.

## 2. System Requirements

- Ubuntu 22.04
- ROS 2 Humble
- Gazebo Classic 11

## 3. Terminal Commands

After cloning **`src`** into a ROS 2 workspace, open a terminal at the workspace root and build it:

```bash
source /opt/ros/humble/setup.bash
colcon build --symlink-install
```

### Terminal 1: Launch the world and robot

From the workspace root, source the environment:

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
```

Launch the empty world and robot together:

```bash
ros2 launch sim_bringup simulation.launch.py
```

This places the robot at the origin: `x=0`, `y=0`, `yaw=0`.

**Optionally**, to launch the robot at a desired position and orientation:

```bash
ros2 launch sim_bringup simulation.launch.py x:=2.0 y:=1.0 yaw:=1.57
```

`x` and `y` are in metres. `yaw` is in radians. Run either commands , **not both**.

### Terminal 2: Spawn the obstacle

Keep Terminal 1 running. Open another terminal at the workspace root and source the environment:

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
```

Spawn a cylindrical obstacle:

```bash
ros2 run sim_bringup spawn_obstacle 1,2,0.3
```

The argument format is **`x,y,radius`**. This example places the obstacle at `(1, 2)` metres with a radius of `0.3` metres. Its height is fixed at 1 metre, and it rests on the ground. Running the command again replaces the existing obstacle.

## 4. Topics

| Topic | Message type | Purpose |
| --- | --- | --- |
| `/cmd_vel` | `geometry_msgs/msg/Twist` | Publish commands to move and turn the robot. |
| `/odom` | `nav_msgs/msg/Odometry` | Read the robot’s position, orientation, and velocity. The pose uses the `world` frame. |
| `/obstacle` | `sim_bringup/msg/Obstacle` | Read the obstacle’s centre position and radius. |
| `/scan` | `sensor_msgs/msg/LaserScan` | Read distance measurements from the robot’s LiDAR. |
