cmake_minimum_required(VERSION 3.5)
project(assignment_ros2)

find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(assignment_interfaces REQUIRED)

ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  ${PROJECT_SOURCE_DIR}/assignment_ros2/assignment.py
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()