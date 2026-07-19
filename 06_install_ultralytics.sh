#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e # 开启遇错停止选项，安装失败时立即终止脚本。
source .venv/bin/activate # 激活项目虚拟环境，确保 Ultralytics 安装到 .venv 中。
python -m pip install "ultralytics==8.4.96" # 从默认 Python 软件源安装并固定 Ultralytics 版本。
python -m pip show ultralytics # 显示 Ultralytics 的版本、安装位置和依赖信息。
deactivate # 退出虚拟环境并恢复执行脚本前的环境变量。
