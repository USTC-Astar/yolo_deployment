#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e
# 上一行开启遇错停止，任何命令失败都会让脚本立即退出。
source /opt/ros/noetic/setup.bash
# 上一行加载 ROS Noetic 环境，让脚本能启动 Gazebo 和 ROS 节点。
export ROS_MASTER_URI="http://127.0.0.1:11327"
# 上一行为本次保存相机画面测试指定独立 ROS master 端口。
export GAZEBO_MASTER_URI="http://127.0.0.1:11328"
# 上一行为本次保存相机画面测试指定独立 Gazebo master 端口。
mkdir -p outputs
# 上一行创建 outputs 目录，用于保存日志和相机画面。
gazebo_pid=""
# 上一行先创建 Gazebo 进程编号变量，避免清理函数访问未定义变量。
cleanup() {
# 上一行定义清理函数，用于脚本退出时关闭后台 Gazebo。
    if [ -n "${gazebo_pid}" ]; then
# 上一行判断 Gazebo 进程编号是否已经存在。
        kill -TERM -- "-${gazebo_pid}" 2>/dev/null || true
# 上一行尝试关闭整个 Gazebo 进程组；如果它已经退出就忽略错误。
    fi
# 上一行结束 Gazebo 进程清理判断。
}
# 上一行结束 cleanup 清理函数定义。
trap cleanup EXIT
# 上一行注册退出钩子，让脚本正常结束或报错退出时都执行 cleanup。
setsid ./30_run_gazebo_camera_world.sh > outputs/save_frame_gazebo.log 2>&1 &
# 上一行用新会话在后台启动最小 Gazebo 相机世界，并把日志写入文件。
gazebo_pid=$!
# 上一行记录新会话进程组编号，方便后面关闭整组 Gazebo 进程。
sleep 12
# 上一行等待 Gazebo、相机插件和图像话题完成启动注册。
timeout 15 ./33_run_save_one_ros_image.sh /sim_camera/image_raw outputs/gazebo_camera_frame.jpg > outputs/save_frame_node.log 2>&1
# 上一行启动保存单帧图像节点，最多等待 15 秒，防止没有图像时一直卡住。
echo "保存节点日志："
# 上一行打印说明文字，提示下面输出来自保存图像节点。
sed -n '1,20p' outputs/save_frame_node.log
# 上一行显示保存图像节点日志前 20 行，用于确认图片是否保存成功。
echo "保存图片信息："
# 上一行打印说明文字，提示下面输出是保存后的图片文件信息。
file outputs/gazebo_camera_frame.jpg
# 上一行使用 file 命令查看保存图片的格式和分辨率。
