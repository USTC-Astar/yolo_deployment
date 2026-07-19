#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e # 开启 Bash 的遇错停止选项，任意命令失败后不再继续执行。
source .venv/bin/activate # 激活项目虚拟环境，确保后续操作不会修改系统 Python。
python -m pip install --upgrade "pip==25.0.1" # 使用当前 Python 的 pip，把 pip 升级并固定到兼容 Python 3.8 的 25.0.1 版本。
python -m pip --version # 输出升级后的 pip 版本和安装路径，用于确认操作结果。
deactivate # 退出虚拟环境并恢复执行脚本前的环境变量。
