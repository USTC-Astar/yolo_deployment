#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e # 开启遇错停止，任何命令失败都会立即终止脚本。
source /opt/ros/noetic/setup.bash # 加载 ROS Noetic 环境，让脚本能找到 roscore、rostopic 和 ROS Python 包。
source .venv/bin/activate # 激活课程虚拟环境，让 Python 能使用之前安装的 YOLO 和 OpenCV 包。
python -u 20_ros_image_subscriber.py _image_topic:="${1:-/camera/rgb/image_raw}" # 用无缓冲模式启动图像订阅节点，并允许用第一个命令行参数覆盖图像话题。
