#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e
# 上一行开启遇错停止，任何命令失败都会让脚本立即退出。
source /opt/ros/noetic/setup.bash
# 上一行加载 ROS Noetic 环境，让脚本能启动 roscore、ROS 节点和话题工具。
export ROS_MASTER_URI="http://127.0.0.1:11329"
# 上一行为本次测试指定独立 ROS master 端口，避免影响其他 ROS 程序。
mkdir -p outputs
# 上一行创建 outputs 目录，用于保存日志和带框图像。
roscore -p 11329 > outputs/annotated_roscore.log 2>&1 &
# 上一行在后台启动临时 roscore，并把日志写入文件。
roscore_pid=$!
# 上一行记录 roscore 进程编号，方便脚本结束时关闭它。
detector_pid=""
# 上一行先创建 YOLO 带框节点进程编号变量，避免清理函数访问未定义变量。
publisher_pid=""
# 上一行先创建图片发布节点进程编号变量，避免清理函数访问未定义变量。
cleanup() {
# 上一行定义清理函数，用于脚本退出时关闭后台进程。
    if [ -n "${publisher_pid}" ]; then
# 上一行判断图片发布节点进程编号是否已经存在。
        kill "${publisher_pid}" 2>/dev/null || true
# 上一行尝试关闭图片发布节点；如果它已经退出就忽略错误。
    fi
# 上一行结束图片发布节点清理判断。
    if [ -n "${detector_pid}" ]; then
# 上一行判断 YOLO 带框节点进程编号是否已经存在。
        kill "${detector_pid}" 2>/dev/null || true
# 上一行尝试关闭 YOLO 带框节点；如果它已经退出就忽略错误。
    fi
# 上一行结束 YOLO 带框节点清理判断。
    kill "${roscore_pid}" 2>/dev/null || true
# 上一行尝试关闭临时 roscore；如果它已经退出就忽略错误。
}
# 上一行结束 cleanup 清理函数定义。
trap cleanup EXIT
# 上一行注册退出钩子，让脚本正常结束或报错退出时都执行 cleanup。
sleep 3
# 上一行等待 roscore 完成启动。
./37_run_ros_yolo_detector_publish_annotated.sh /yolo_course/image_raw /yolo_course/detections /yolo_course/annotated_image > outputs/annotated_detector.log 2>&1 &
# 上一行在后台启动 YOLO 带框节点，订阅原始图像并发布 JSON 和带框图像。
detector_pid=$!
# 上一行记录 YOLO 带框节点进程编号，方便后面关闭。
sleep 4
# 上一行等待 YOLO 权重加载、订阅者和发布者注册完成。
./21_run_ros_image_publisher.sh /yolo_course/image_raw 1.0 > outputs/annotated_source_publisher.log 2>&1 &
# 上一行在后台启动本地图片发布节点，以每秒 1 帧发布原始图像。
publisher_pid=$!
# 上一行记录图片发布节点进程编号，方便后面关闭。
sleep 2
# 上一行等待 YOLO 节点收到原始图像并发布带框图像。
timeout 15 ./33_run_save_one_ros_image.sh /yolo_course/annotated_image outputs/annotated_image_from_topic.jpg > outputs/annotated_save_frame.log 2>&1
# 上一行从带框图像话题保存 1 帧图片，最多等待 15 秒，避免话题异常时一直卡住。
echo "带框图像保存节点日志："
# 上一行打印说明文字，提示下面输出来自保存图像节点。
sed -n '1,20p' outputs/annotated_save_frame.log
# 上一行显示保存图像节点日志前 20 行，用于确认是否保存成功。
echo "YOLO 带框节点日志："
# 上一行打印说明文字，提示下面输出来自 YOLO 带框节点。
sed -n '1,25p' outputs/annotated_detector.log
# 上一行显示 YOLO 带框节点日志前 25 行，用于确认是否发布了带框图像。
echo "带框图片信息："
# 上一行打印说明文字，提示下面输出保存后的图片文件信息。
file outputs/annotated_image_from_topic.jpg
# 上一行使用 file 命令查看保存图片格式和分辨率。
