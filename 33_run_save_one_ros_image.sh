#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e
# 上一行开启遇错停止，任意命令失败时立即终止脚本。
source /opt/ros/noetic/setup.bash
# 上一行加载 ROS Noetic 环境，让脚本能连接 ROS master 并使用 ROS Python 包。
source .venv/bin/activate
# 上一行激活课程虚拟环境，让 Python 使用课程安装的 OpenCV 和 NumPy。
python -u 33_save_one_ros_image.py _image_topic:="${1:-/sim_camera/image_raw}" _output_path:="${2:-outputs/gazebo_camera_frame.jpg}"
# 上一行用无缓冲模式启动保存单帧图像节点，并允许命令行参数覆盖图像话题和输出路径。
