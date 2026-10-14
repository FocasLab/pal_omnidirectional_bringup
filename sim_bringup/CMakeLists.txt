cmake_minimum_required(VERSION 3.8)
project(sim_bringup)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Obstacle.msg"
  "srv/SetObstacle.srv"
  DEPENDENCIES std_msgs geometry_msgs
)

install(DIRECTORY launch urdf meshes worlds models
  DESTINATION share/${PROJECT_NAME}
)
install(PROGRAMS scripts/spawn_obstacle scripts/obstacle_server
  DESTINATION lib/${PROJECT_NAME}
)
install(FILES README.md LICENSE DESTINATION share/${PROJECT_NAME})

ament_export_dependencies(rosidl_default_runtime)
ament_package()
