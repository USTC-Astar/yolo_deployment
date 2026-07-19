#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e # 开启遇错停止，任何命令失败都会立即终止脚本。
source /opt/ros/noetic/setup.bash # 加载 ROS Noetic 的环境变量，让终端能找到 ROS 命令和 ROS Python 包。
source .venv/bin/activate # 激活课程虚拟环境，让 python 优先使用 .venv 中安装的 YOLO 相关软件包。
python 19_verify_ros_python_imports.py # 使用当前虚拟环境的 Python 运行 ROS Python 导入验证程序。
deactivate # 退出课程虚拟环境，恢复脚本执行前的 Python 环境。
