#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e
# 上一行开启遇错停止，任何命令失败都会让脚本立即退出。
source /opt/ros/noetic/setup.bash
# 上一行加载 ROS Noetic 环境，让脚本能找到 roscore、rostopic 和 ROS Python 包。
export ROS_MASTER_URI="http://127.0.0.1:11319"
# 上一行把本次测试的 ROS master 地址固定到 11319 端口，避免影响默认 11311 端口上的其他 ROS 程序。
roscore -p 11319 > outputs/ros_pipeline_roscore.log 2>&1 &
# 上一行在后台启动临时 roscore，并把日志写入文件。
roscore_pid=$!
# 上一行记录 roscore 进程编号，方便脚本结束时关闭它。
sleep 3
# 上一行等待 3 秒，让 roscore 有时间完成启动。
./20_run_ros_image_subscriber.sh /yolo_course/image_raw > outputs/ros_pipeline_subscriber.log 2>&1 &
# 上一行在后台启动图像订阅节点，并订阅课程测试图像话题。
subscriber_pid=$!
# 上一行记录订阅节点进程编号，方便脚本结束时关闭它。
sleep 2
# 上一行等待 2 秒，让订阅节点完成注册。
timeout 6 ./21_run_ros_image_publisher.sh /yolo_course/image_raw 2.0 > outputs/ros_pipeline_publisher.log 2>&1 || true
# 上一行以每秒 2 帧启动图片发布节点，最多运行 6 秒；超时退出是预期行为。
sleep 1
# 上一行等待 1 秒，让订阅节点把最后几帧日志写完。
kill "${subscriber_pid}" 2>/dev/null || true
# 上一行关闭订阅节点；如果它已经退出，就忽略错误。
kill "${roscore_pid}" 2>/dev/null || true
# 上一行关闭临时 roscore；如果它已经退出，就忽略错误。
echo "订阅节点日志："
# 上一行打印说明文字，提示下面输出来自订阅节点。
sed -n '1,20p' outputs/ros_pipeline_subscriber.log
# 上一行显示订阅节点日志前 20 行，用于确认是否收到了 ROS 图像。
echo "发布节点日志："
# 上一行打印说明文字，提示下面输出来自发布节点。
sed -n '1,20p' outputs/ros_pipeline_publisher.log
# 上一行显示发布节点日志前 20 行，用于确认图片是否被持续发布。
