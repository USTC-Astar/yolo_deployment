#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e # 任意命令失败时立即停止脚本。
source .venv/bin/activate # 修改当前脚本的环境变量，让 python 优先指向 .venv 中的解释器。
which python # 显示激活环境后实际使用的 Python 路径。
python --version # 显示当前虚拟环境使用的 Python 版本。
python -m pip --version # 显示当前 Python 对应的 pip 路径和版本。
deactivate # 退出虚拟环境并恢复原来的环境变量。
