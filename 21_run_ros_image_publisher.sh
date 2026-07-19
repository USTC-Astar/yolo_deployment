#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e # 开启遇错停止，任意命令失败时立即停止脚本。
source /opt/ros/noetic/setup.bash # 加载 ROS Noetic 环境，让脚本能找到 ROS 命令和 ROS Python 包。
source .venv/bin/activate # 激活课程虚拟环境，让 Python 能使用 OpenCV 等课程依赖。
python -u 21_ros_image_publisher.py _image_topic:="${1:-/yolo_course/image_raw}" _rate:="${2:-1.0}" # 用无缓冲模式启动图片发布节点，并允许用命令行参数覆盖话题和频率。
