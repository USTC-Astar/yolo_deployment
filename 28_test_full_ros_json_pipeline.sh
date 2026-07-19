#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e
# 上一行开启遇错停止，任何命令失败都会让脚本立即退出。
source /opt/ros/noetic/setup.bash
# 上一行加载 ROS Noetic 环境，让脚本能使用 roscore 和 ROS 通信变量。
export ROS_MASTER_URI="http://127.0.0.1:11322"
# 上一行把本次测试的 ROS master 固定到 11322 端口，避免影响其他 ROS 程序。
mkdir -p outputs
# 上一行创建 outputs 目录，用于保存本次测试产生的日志文件。
roscore -p 11322 > outputs/full_pipeline_roscore.log 2>&1 &
# 上一行在后台启动临时 roscore，并把输出写入日志文件。
roscore_pid=$!
# 上一行记录 roscore 后台进程编号，方便脚本结束时关闭它。
detector_pid=""
# 上一行先创建 YOLO 检测节点进程编号变量，避免清理函数访问未定义变量。
subscriber_pid=""
# 上一行先创建 JSON 解析订阅节点进程编号变量，避免清理函数访问未定义变量。
cleanup() {
# 上一行定义清理函数，用于脚本退出时关闭后台进程。
    if [ -n "${subscriber_pid}" ]; then
# 上一行判断 JSON 解析订阅节点进程编号是否已经存在。
        kill "${subscriber_pid}" 2>/dev/null || true
# 上一行尝试关闭 JSON 解析订阅节点，如果它已经退出就忽略错误。
    fi
# 上一行结束 JSON 解析订阅节点清理判断。
    if [ -n "${detector_pid}" ]; then
# 上一行判断 YOLO 检测节点进程编号是否已经存在。
        kill "${detector_pid}" 2>/dev/null || true
# 上一行尝试关闭 YOLO 检测节点，如果它已经退出就忽略错误。
    fi
# 上一行结束 YOLO 检测节点清理判断。
    kill "${roscore_pid}" 2>/dev/null || true
# 上一行尝试关闭临时 roscore，如果它已经退出就忽略错误。
}
# 上一行结束 cleanup 清理函数定义。
trap cleanup EXIT
# 上一行注册退出钩子，让脚本正常结束或报错退出时都执行 cleanup。
sleep 3
# 上一行等待 roscore 完成启动。
./25_run_ros_yolo_detector_publish_json.sh /yolo_course/image_raw /yolo_course/detections > outputs/full_pipeline_detector.log 2>&1 &
# 上一行在后台启动 YOLO JSON 检测节点，订阅图像话题并发布检测结果话题。
detector_pid=$!
# 上一行记录 YOLO 检测节点进程编号，方便后面关闭。
sleep 4
# 上一行等待 YOLO 权重加载、图像订阅注册和检测结果发布者创建完成。
./27_run_ros_detection_json_subscriber.sh /yolo_course/detections > outputs/full_pipeline_json_subscriber.log 2>&1 &
# 上一行在后台启动 JSON 解析订阅节点，用于订阅并解析 YOLO 检测结果。
subscriber_pid=$!
# 上一行记录 JSON 解析订阅节点进程编号，方便后面关闭。
sleep 2
# 上一行等待 JSON 解析订阅节点完成订阅注册，避免错过检测结果消息。
timeout 8 ./21_run_ros_image_publisher.sh /yolo_course/image_raw 1.0 > outputs/full_pipeline_publisher.log 2>&1 || true
# 上一行以每秒 1 帧发布图片，最多运行 8 秒；timeout 退出属于预期结果。
sleep 2
# 上一行等待 YOLO 检测节点和 JSON 解析节点处理最后几条消息并写入日志。
echo "JSON 解析订阅节点日志："
# 上一行打印说明文字，提示下面输出来自 JSON 解析订阅节点。
sed -n '1,25p' outputs/full_pipeline_json_subscriber.log
# 上一行显示 JSON 解析订阅节点日志前 25 行，用于确认是否解析到检测结果。
echo "YOLO JSON 检测节点日志："
# 上一行打印说明文字，提示下面输出来自 YOLO JSON 检测节点。
sed -n '1,25p' outputs/full_pipeline_detector.log
# 上一行显示 YOLO JSON 检测节点日志前 25 行，用于确认是否发布检测结果。
echo "图片发布节点日志："
# 上一行打印说明文字，提示下面输出来自图片发布节点。
sed -n '1,15p' outputs/full_pipeline_publisher.log
# 上一行显示图片发布节点日志前 15 行，用于确认图像是否发布。
