#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e # 开启遇错停止选项，安装失败时不继续执行后续命令。
source .venv/bin/activate # 激活项目虚拟环境，确保软件包安装到 .venv 中。
python -m pip install "torch==2.4.1" "torchvision==0.19.1" --index-url "https://download.pytorch.org/whl/cpu" # 从 PyTorch 官方 CPU 软件源安装固定版本的 torch 和 torchvision。
python -m pip show torch # 显示 torch 的版本、位置和依赖信息，用于确认安装结果。
python -m pip show torchvision # 显示 torchvision 的版本、位置和依赖信息，用于确认安装结果。
deactivate # 退出虚拟环境并恢复执行脚本前的环境变量。
