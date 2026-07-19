#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e
# 上一行开启遇错停止，任何命令失败都会让脚本立即退出。
source /opt/ros/noetic/setup.bash
# 上一行加载 ROS Noetic 环境，让脚本能启动 Gazebo、YOLO 节点和 rostopic。
export ROS_MASTER_URI="http://127.0.0.1:11325"
# 上一行为本次 Gazebo+YOLO 测试指定独立 ROS master 端口。
export GAZEBO_MASTER_URI="http://127.0.0.1:11326"
# 上一行为本次 Gazebo+YOLO 测试指定独立 Gazebo master 端口。
mkdir -p outputs
# 上一行创建 outputs 目录，用于保存本次测试产生的日志文件。
gazebo_pid=""
# 上一行先创建 Gazebo 启动进程编号变量，避免清理函数访问未定义变量。
detector_pid=""
# 上一行先创建 YOLO 检测节点进程编号变量，避免清理函数访问未定义变量。
echo_pid=""
# 上一行先创建 rostopic echo 进程编号变量，方便后面等待或清理。
cleanup() {
# 上一行定义清理函数，用于脚本退出时关闭后台进程。
    if [ -n "${echo_pid}" ]; then
# 上一行判断 rostopic echo 进程编号是否已经存在。
        kill "${echo_pid}" 2>/dev/null || true
# 上一行尝试关闭 rostopic echo；如果它已经退出，就忽略错误。
    fi
# 上一行结束 rostopic echo 清理判断。
    if [ -n "${detector_pid}" ]; then
# 上一行判断 YOLO 检测节点进程编号是否已经存在。
        kill "${detector_pid}" 2>/dev/null || true
# 上一行尝试关闭 YOLO 检测节点；如果它已经退出，就忽略错误。
    fi
# 上一行结束 YOLO 检测节点清理判断。
    if [ -n "${gazebo_pid}" ]; then
# 上一行判断 Gazebo 启动进程编号是否已经存在。
        kill -TERM -- "-${gazebo_pid}" 2>/dev/null || true
# 上一行尝试关闭整个 Gazebo 进程组；如果它已经退出，就忽略错误。
    fi
# 上一行结束 Gazebo 清理判断。
}
# 上一行结束 cleanup 清理函数定义。
trap cleanup EXIT
# 上一行注册退出钩子，让脚本正常结束或报错退出时都执行 cleanup。
setsid ./30_run_gazebo_camera_world.sh > outputs/gazebo_yolo_world.log 2>&1 &
# 上一行用新会话在后台启动最小 Gazebo 相机世界，并把日志写入文件。
gazebo_pid=$!
# 上一行记录新会话进程组编号，方便后面关闭整组 Gazebo 进程。
sleep 12
# 上一行等待 Gazebo、相机插件和 ROS 图像话题完成启动注册。
./25_run_ros_yolo_detector_publish_json.sh /sim_camera/image_raw /yolo_course/detections > outputs/gazebo_yolo_detector.log 2>&1 &
# 上一行启动 YOLO JSON 检测节点，让它直接订阅 Gazebo 相机图像话题。
detector_pid=$!
# 上一行记录 YOLO 检测节点进程编号，方便后面关闭。
sleep 5
# 上一行等待 YOLO 权重加载、图像订阅注册和检测结果发布者创建完成。
timeout 15 rostopic echo -n 1 /yolo_course/detections > outputs/gazebo_yolo_echo.log 2>&1 &
# 上一行启动 rostopic echo，最多等待 15 秒，只抓取 1 条 YOLO 检测结果。
echo_pid=$!
# 上一行记录 rostopic echo 进程编号，方便后面等待或清理。
wait "${echo_pid}" || true
# 上一行等待 rostopic echo 抓取消息并退出；超时失败时不让脚本直接中断。
echo "Gazebo YOLO 检测结果话题输出："
# 上一行打印说明文字，提示下面输出来自 rostopic echo。
sed -n '1,30p' outputs/gazebo_yolo_echo.log
# 上一行显示检测结果话题输出前 30 行，用于确认是否抓到 JSON 检测结果。
echo "YOLO 检测节点日志："
# 上一行打印说明文字，提示下面输出来自 YOLO 检测节点。
sed -n '1,30p' outputs/gazebo_yolo_detector.log
# 上一行显示 YOLO 检测节点日志前 30 行，用于确认检测节点状态。
echo "Gazebo 图像话题："
# 上一行打印说明文字，提示下面输出当前 Image 话题发现结果。
./29_find_ros_image_topics.sh | sed -n '1,80p'
# 上一行运行图像话题发现脚本并显示前 80 行，用于确认 /sim_camera/image_raw 仍然在线。
