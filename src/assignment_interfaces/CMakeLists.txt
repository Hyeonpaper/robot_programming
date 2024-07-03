cmake_minimum_required(VERSION 3.5)
project(assignment_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/ID.msg"
  "srv/MultiplyTwoInts.srv"
  "action/AddID.action"
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()