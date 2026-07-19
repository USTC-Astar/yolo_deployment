#!/usr/bin/env bash
# 上一行指定使用 Bash 解释执行本脚本。
set -e
# 上一行开启遇错停止，避免命令失败后继续输出误导结果。
source /opt/ros/noetic/setup.bash
# 上一行加载 ROS Noetic 环境，让脚本能使用 rostopic 命令。
echo "正在检查 ROS master：${ROS_MASTER_URI:-http://localhost:11311}"
# 上一行打印当前 ROS master 地址；如果环境变量没设置，ROS 默认使用 localhost:11311。
if ! rostopic list >/tmp/yolo_course_topics.txt 2>/tmp/yolo_course_rostopic_error.txt; then
# 上一行尝试列出 ROS 话题；如果失败，说明 roscore 或 ROS master 可能没有运行。
    echo "没有连接到 ROS master，请先启动 roscore 或 Gazebo。"
# 上一行提示用户当前没有可用的 ROS 通信中心。
    cat /tmp/yolo_course_rostopic_error.txt
# 上一行打印 rostopic 返回的错误信息，方便判断具体原因。
    exit 1
# 上一行用错误状态退出脚本，表示本次没有成功列出话题。
fi
# 上一行结束 ROS master 连接检查。
echo "当前所有 ROS 话题："
# 上一行打印说明文字，提示下面是完整话题列表。
cat /tmp/yolo_course_topics.txt
# 上一行显示当前 ROS master 中注册的所有话题。
echo "当前 Image 图像话题："
# 上一行打印说明文字，提示下面只筛选图像消息话题。
found_image_topic=0
# 上一行创建标记变量，用于记录是否找到至少一个图像话题。
while read -r topic_name; do
# 上一行逐行读取话题名称。
    topic_type="$(rostopic type "${topic_name}" 2>/dev/null || true)"
# 上一行查询当前话题的消息类型；失败时返回空字符串而不中断脚本。
    if [ "${topic_type}" = "sensor_msgs/Image" ]; then
# 上一行判断当前话题是否是 ROS 标准图像消息类型。
        echo "${topic_name}"
# 上一行打印找到的图像话题名称。
        found_image_topic=1
# 上一行把标记变量设置为 1，表示已经找到图像话题。
    fi
# 上一行结束图像话题类型判断。
done < /tmp/yolo_course_topics.txt
# 上一行把话题列表文件作为 while 循环的输入。
if [ "${found_image_topic}" = "0" ]; then
# 上一行判断是否没有找到任何图像话题。
    echo "未找到 sensor_msgs/Image 类型的话题。"
# 上一行提示当前没有标准 ROS 图像话题。
fi
# 上一行结束图像话题缺失判断。
