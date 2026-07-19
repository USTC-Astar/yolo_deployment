#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e # 任意命令执行失败时立即停止，避免带着错误继续运行。
python3 -m venv .venv # 使用系统 Python 在当前项目中创建名为 .venv 的虚拟环境。
.venv/bin/python -m pip --version # 使用虚拟环境自己的 Python 检查其中的 pip 是否可用。
