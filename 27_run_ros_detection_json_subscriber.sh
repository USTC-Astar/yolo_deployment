#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e
# 上一行开启遇错停止，任意命令失败时立即终止脚本。
source /opt/ros/noetic/setup.bash
# 上一行加载 ROS Noetic 环境，让脚本能找到 ROS 命令和 ROS Python 包。
source .venv/bin/activate
# 上一行激活课程虚拟环境，让 Python 使用课程环境。
python -u 27_ros_detection_json_subscriber.py _detections_topic:="${1:-/yolo_course/detections}"
# 上一行用无缓冲模式启动 JSON 检测结果订阅节点，并允许命令行参数覆盖检测结果话题。
