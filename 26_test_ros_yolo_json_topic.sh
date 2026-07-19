#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e
# 上一行开启遇错停止，任何命令失败都会让脚本立即退出。
source /opt/ros/noetic/setup.bash
# 上一行加载 ROS Noetic 环境，让脚本能使用 roscore、rostopic 和 ROS 通信变量。
export ROS_MASTER_URI="http://127.0.0.1:11321"
# 上一行把本次测试的 ROS master 固定到 11321 端口，避免影响其他 ROS 程序。
mkdir -p outputs
# 上一行创建 outputs 目录，用于保存本次测试产生的日志文件。
roscore -p 11321 > outputs/ros_yolo_json_roscore.log 2>&1 &
# 上一行在后台启动临时 roscore，并把输出写入日志文件。
roscore_pid=$!
# 上一行记录 roscore 后台进程编号，方便脚本结束时关闭它。
detector_pid=""
# 上一行先创建检测节点进程编号变量，避免清理函数里访问未定义变量。
echo_pid=""
# 上一行先创建 rostopic echo 进程编号变量，方便后面等待或清理它。
cleanup() {
# 上一行定义清理函数，用于脚本退出时关闭后台进程。
    if [ -n "${echo_pid}" ]; then
# 上一行判断 rostopic echo 进程编号是否已经存在。
        kill "${echo_pid}" 2>/dev/null || true
# 上一行尝试关闭 rostopic echo；如果它已经退出，就忽略错误。
    fi
# 上一行结束 rostopic echo 清理判断。
    if [ -n "${detector_pid}" ]; then
# 上一行判断检测节点进程编号是否已经存在。
        kill "${detector_pid}" 2>/dev/null || true
# 上一行尝试关闭 YOLO JSON 检测节点；如果它已经退出，就忽略错误。
    fi
# 上一行结束检测节点清理判断。
    kill "${roscore_pid}" 2>/dev/null || true
# 上一行尝试关闭临时 roscore；如果它已经退出，就忽略错误。
}
# 上一行结束 cleanup 清理函数定义。
trap cleanup EXIT
# 上一行注册退出钩子，让脚本正常结束或报错退出时都执行 cleanup。
sleep 3
# 上一行等待 roscore 完成启动。
./25_run_ros_yolo_detector_publish_json.sh /yolo_course/image_raw /yolo_course/detections > outputs/ros_yolo_json_detector.log 2>&1 &
# 上一行在后台启动 YOLO JSON 检测节点，订阅图像话题并发布检测结果话题。
detector_pid=$!
# 上一行记录 YOLO JSON 检测节点进程编号，方便后面关闭。
sleep 4
# 上一行等待 YOLO 权重加载、检测结果发布者创建和图像订阅注册完成。
timeout 12 rostopic echo -n 1 /yolo_course/detections > outputs/ros_yolo_json_echo.log 2>&1 &
# 上一行启动 rostopic echo，最多等待 12 秒，只抓取 1 条检测结果消息。
echo_pid=$!
# 上一行记录 rostopic echo 进程编号，方便后面等待或清理。
sleep 1
# 上一行等待 rostopic echo 完成订阅注册，避免错过第一条消息。
timeout 8 ./21_run_ros_image_publisher.sh /yolo_course/image_raw 1.0 > outputs/ros_yolo_json_publisher.log 2>&1 || true
# 上一行以每秒 1 帧发布图片，最多运行 8 秒；timeout 退出属于预期结果。
wait "${echo_pid}" || true
# 上一行等待 rostopic echo 抓取消息并退出；超时失败时不让脚本直接中断。
echo "检测结果话题输出："
# 上一行打印说明文字，提示下面输出来自 rostopic echo。
sed -n '1,20p' outputs/ros_yolo_json_echo.log
# 上一行显示 rostopic echo 日志前 20 行，用于确认是否抓到了 JSON 检测结果。
echo "YOLO JSON 检测节点日志："
# 上一行打印说明文字，提示下面输出来自 YOLO JSON 检测节点。
sed -n '1,25p' outputs/ros_yolo_json_detector.log
# 上一行显示 YOLO JSON 检测节点日志前 25 行，用于确认是否发布了检测结果。
echo "图片发布节点日志："
# 上一行打印说明文字，提示下面输出来自图片发布节点。
sed -n '1,15p' outputs/ros_yolo_json_publisher.log
# 上一行显示图片发布节点日志前 15 行，用于确认图像是否发布。
