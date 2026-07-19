#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e
# 上一行开启遇错停止，任何命令失败都会让脚本立即退出。
source /opt/ros/noetic/setup.bash
# 上一行加载 ROS Noetic 环境，让脚本能启动 Gazebo 并使用 rostopic。
export ROS_MASTER_URI="http://127.0.0.1:11323"
# 上一行为本次 Gazebo 测试指定独立 ROS master 端口，避免影响其他 ROS 程序。
export GAZEBO_MASTER_URI="http://127.0.0.1:11324"
# 上一行为本次 Gazebo 测试指定独立 Gazebo master 端口，避免和正在运行的其他 Gazebo 实例冲突。
mkdir -p outputs
# 上一行创建 outputs 目录，用于保存 Gazebo 和话题发现日志。
setsid ./30_run_gazebo_camera_world.sh > outputs/gazebo_camera_world.log 2>&1 &
# 上一行用新会话在后台启动最小 Gazebo 相机世界，并把日志写入文件。
gazebo_launch_pid=$!
# 上一行记录新会话进程组编号，方便脚本结束时关闭整组 Gazebo 进程。
cleanup() {
# 上一行定义清理函数，用于脚本退出时关闭后台仿真。
    kill -TERM -- "-${gazebo_launch_pid}" 2>/dev/null || true
# 上一行尝试关闭整个 Gazebo 进程组；如果它已经退出，就忽略错误。
}
# 上一行结束 cleanup 清理函数定义。
trap cleanup EXIT
# 上一行注册退出钩子，让脚本正常结束或出错时都尝试关闭 Gazebo。
sleep 10
# 上一行等待 10 秒，让 Gazebo、相机插件和 ROS 话题完成启动注册。
./29_find_ros_image_topics.sh > outputs/gazebo_image_topics.log 2>&1
# 上一行运行图像话题发现脚本，并把结果保存到日志文件。
echo "Gazebo 图像话题发现结果："
# 上一行打印说明文字，提示下面输出来自图像话题发现脚本。
sed -n '1,80p' outputs/gazebo_image_topics.log
# 上一行显示图像话题发现日志前 80 行，用于确认是否找到相机图像话题。
echo "Gazebo 启动日志摘要："
# 上一行打印说明文字，提示下面输出来自 Gazebo 启动日志。
sed -n '1,40p' outputs/gazebo_camera_world.log
# 上一行显示 Gazebo 启动日志前 40 行，便于排查启动失败原因。
