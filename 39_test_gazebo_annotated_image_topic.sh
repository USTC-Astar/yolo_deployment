#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e
# 上一行开启遇错停止，任何命令失败都会让脚本立即退出。
source /opt/ros/noetic/setup.bash
# 上一行加载 ROS Noetic 环境，让脚本能启动 Gazebo、ROS 节点和话题工具。
export ROS_MASTER_URI="http://127.0.0.1:11330"
# 上一行为本次 Gazebo 带框图像测试指定独立 ROS master 端口。
export GAZEBO_MASTER_URI="http://127.0.0.1:11331"
# 上一行为本次 Gazebo 带框图像测试指定独立 Gazebo master 端口。
mkdir -p outputs
# 上一行创建 outputs 目录，用于保存日志和带框仿真图像。
gazebo_pid=""
# 上一行先创建 Gazebo 进程组编号变量，避免清理函数访问未定义变量。
detector_pid=""
# 上一行先创建 YOLO 带框节点进程编号变量，避免清理函数访问未定义变量。
cleanup() {
# 上一行定义清理函数，用于脚本退出时关闭后台进程。
    if [ -n "${detector_pid}" ]; then
# 上一行判断 YOLO 带框节点进程编号是否已经存在。
        kill "${detector_pid}" 2>/dev/null || true
# 上一行尝试关闭 YOLO 带框节点；如果它已经退出就忽略错误。
    fi
# 上一行结束 YOLO 带框节点清理判断。
    if [ -n "${gazebo_pid}" ]; then
# 上一行判断 Gazebo 进程组编号是否已经存在。
        kill -TERM -- "-${gazebo_pid}" 2>/dev/null || true
# 上一行尝试关闭整个 Gazebo 进程组；如果它已经退出就忽略错误。
    fi
# 上一行结束 Gazebo 清理判断。
}
# 上一行结束 cleanup 清理函数定义。
trap cleanup EXIT
# 上一行注册退出钩子，让脚本正常结束或报错退出时都执行 cleanup。
setsid ./30_run_gazebo_camera_world.sh > outputs/gazebo_annotated_world.log 2>&1 &
# 上一行用新会话在后台启动 Gazebo 相机世界，并把日志写入文件。
gazebo_pid=$!
# 上一行记录 Gazebo 新会话进程组编号，方便后面关闭整组进程。
sleep 12
# 上一行等待 Gazebo、相机插件和 /sim_camera/image_raw 话题完成启动注册。
./37_run_ros_yolo_detector_publish_annotated.sh /sim_camera/image_raw /yolo_course/detections /yolo_course/annotated_image > outputs/gazebo_annotated_detector.log 2>&1 &
# 上一行启动 YOLO 带框节点，订阅 Gazebo 相机图像并发布 JSON 和带框图像。
detector_pid=$!
# 上一行记录 YOLO 带框节点进程编号，方便后面关闭。
sleep 5
# 上一行等待 YOLO 权重加载、订阅者和发布者注册完成。
timeout 20 ./33_run_save_one_ros_image.sh /yolo_course/annotated_image outputs/gazebo_annotated_image.jpg > outputs/gazebo_annotated_save_frame.log 2>&1
# 上一行从带框图像话题保存一帧图片，最多等待 20 秒，避免异常时一直卡住。
echo "Gazebo 带框图像保存节点日志："
# 上一行打印说明文字，提示下面输出来自保存图像节点。
sed -n '1,20p' outputs/gazebo_annotated_save_frame.log
# 上一行显示保存图像节点日志前 20 行，用于确认图片是否保存成功。
echo "YOLO 带框节点日志："
# 上一行打印说明文字，提示下面输出来自 YOLO 带框节点。
sed -n '1,30p' outputs/gazebo_annotated_detector.log
# 上一行显示 YOLO 带框节点日志前 30 行，用于确认检测和带框图像发布状态。
echo "Gazebo 带框图片信息："
# 上一行打印说明文字，提示下面输出保存后的图片文件信息。
file outputs/gazebo_annotated_image.jpg
# 上一行使用 file 命令查看保存图片格式和分辨率。
