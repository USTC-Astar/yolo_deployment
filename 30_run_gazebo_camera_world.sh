#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e
# 上一行开启遇错停止，任何命令失败都会让脚本立即退出。
source /opt/ros/noetic/setup.bash
# 上一行加载 ROS Noetic 环境，让脚本能使用 roslaunch、Gazebo 和 gazebo_ros 插件。
world_path="$(pwd)/worlds/minimal_camera.world"
# 上一行把最小相机世界文件转换成绝对路径，避免 roslaunch 在别的目录中找不到它。
export GAZEBO_MODEL_PATH="$(pwd)/models:${GAZEBO_MODEL_PATH}"
# 上一行把课程 models 目录加入 Gazebo 模型搜索路径，让 Gazebo 能找到 bus_billboard。
roslaunch gazebo_ros empty_world.launch world_name:="${world_path}" gui:=false paused:=false use_sim_time:=true
# 上一行启动 Gazebo 空世界启动器，加载我们的相机世界，关闭 GUI，并启用仿真时间。
