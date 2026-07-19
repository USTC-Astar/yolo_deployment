#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e
# 上一行开启遇错停止，任何命令失败都会让脚本立即退出。
source /opt/ros/noetic/setup.bash
# 上一行加载 ROS Noetic 环境，让脚本能使用 roscore 和 ROS 通信变量。
export ROS_MASTER_URI="http://127.0.0.1:11320"
# 上一行把本次测试的 ROS master 固定到 11320 端口，避免影响其他 ROS 程序。
mkdir -p outputs
# 上一行创建 outputs 目录，用于保存本次测试的日志文件。
roscore -p 11320 > outputs/ros_yolo_roscore.log 2>&1 &
# 上一行在后台启动临时 roscore，并把输出写入日志文件。
roscore_pid=$!
# 上一行记录 roscore 后台进程编号，方便后面关闭。
detector_pid=""
# 上一行先创建检测节点进程编号变量，避免清理函数里访问未定义变量。
cleanup() {
# 上一行定义清理函数，用于脚本结束时关闭后台进程。
    if [ -n "${detector_pid}" ]; then
# 上一行判断检测节点进程编号是否已经存在。
        kill "${detector_pid}" 2>/dev/null || true
# 上一行尝试关闭 YOLO 检测节点，如果它已经退出就忽略错误。
    fi
# 上一行结束检测节点清理判断。
    kill "${roscore_pid}" 2>/dev/null || true
# 上一行尝试关闭临时 roscore，如果它已经退出就忽略错误。
}
# 上一行结束 cleanup 清理函数定义。
trap cleanup EXIT
# 上一行注册退出钩子，让脚本正常结束或报错退出时都执行 cleanup。
sleep 3
# 上一行等待 roscore 完成启动。
./23_run_ros_yolo_detector.sh /yolo_course/image_raw > outputs/ros_yolo_detector.log 2>&1 &
# 上一行在后台启动 YOLO 检测节点，并订阅课程测试图像话题。
detector_pid=$!
# 上一行记录 YOLO 检测节点进程编号，方便后面关闭。
sleep 4
# 上一行等待 YOLO 权重加载和订阅注册完成。
timeout 8 ./21_run_ros_image_publisher.sh /yolo_course/image_raw 1.0 > outputs/ros_yolo_publisher.log 2>&1 || true
# 上一行以每秒 1 帧发布图片，最多运行 8 秒；timeout 退出属于预期结果。
sleep 2
# 上一行等待 YOLO 检测节点处理最后收到的图像并写入日志。
echo "YOLO 检测节点日志："
# 上一行打印说明文字，提示下面输出来自 YOLO 检测节点。
sed -n '1,30p' outputs/ros_yolo_detector.log
# 上一行显示 YOLO 检测节点日志前 30 行，用于确认是否完成检测。
echo "图片发布节点日志："
# 上一行打印说明文字，提示下面输出来自图片发布节点。
sed -n '1,20p' outputs/ros_yolo_publisher.log
# 上一行显示图片发布节点日志前 20 行，用于确认图像是否发布。
