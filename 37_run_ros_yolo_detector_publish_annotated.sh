#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e
# 上一行开启遇错停止，任意命令失败时立即终止脚本。
source /opt/ros/noetic/setup.bash
# 上一行加载 ROS Noetic 环境，让脚本能找到 ROS 命令和 ROS Python 包。
source .venv/bin/activate
# 上一行激活课程虚拟环境，让 Python 能使用 Ultralytics、PyTorch 和 OpenCV。
python -u 37_ros_yolo_detector_publish_annotated.py _image_topic:="${1:-/yolo_course/image_raw}" _detections_topic:="${2:-/yolo_course/detections}" _annotated_topic:="${3:-/yolo_course/annotated_image}" _weights:="${4:-models/yolo26n.pt}"
# 上一行用无缓冲模式启动带框图像发布节点，并允许命令行参数覆盖图像话题、检测话题、带框图像话题和权重路径。
