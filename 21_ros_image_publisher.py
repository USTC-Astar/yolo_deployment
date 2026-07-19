from pathlib import Path  # 导入 Path 类，用于管理需要发布的图片路径。
import cv2  # 导入 OpenCV，用于读取本地图片文件。
import sys  # 导入 sys 模块，用于在程序运行时追加 Python 模块搜索路径。

sys.path.append("/usr/lib/python3/dist-packages")  # 把系统 Python 包目录追加到搜索路径末尾，让 rospy 能找到 rospkg 等依赖。
import rospy  # 导入 ROS Python 客户端库，用于创建节点和发布话题。
from sensor_msgs.msg import Image  # 导入 ROS 图像消息类型，用于发布相机图像。
from ros_image_utils import bgr_array_to_image_message  # 导入课程自定义转换函数，用于把 OpenCV BGR 图像转成 ROS Image。


def main():  # 定义程序入口函数，用于组织节点初始化和循环发布逻辑。
    rospy.init_node("yolo_course_image_publisher")  # 初始化 ROS 节点，并设置节点名称。
    image_path_text = rospy.get_param("~image_path", "images/bus.jpg")  # 读取私有参数 image_path，未设置时使用公交车测试图片。
    image_topic = rospy.get_param("~image_topic", "/yolo_course/image_raw")  # 读取私有参数 image_topic，未设置时发布到课程测试图像话题。
    publish_rate_hz = rospy.get_param("~rate", 1.0)  # 读取私有参数 rate，未设置时每秒发布 1 帧。
    image_path = Path(image_path_text)  # 把字符串路径转换成 Path 对象，便于后续检查和显示。
    cv_image = cv2.imread(str(image_path))  # 使用 OpenCV 读取本地图片，得到 BGR 图像数组。
    if cv_image is None:  # 检查图片是否读取成功，失败时 OpenCV 会返回 None。
        raise FileNotFoundError(f"无法读取图片：{image_path}")  # 抛出文件不存在异常并停止程序。
    publisher = rospy.Publisher(image_topic, Image, queue_size=1)  # 创建图像发布者，消息类型为 Image，队列长度为 1。
    rate = rospy.Rate(publish_rate_hz)  # 创建 ROS 循环频率控制器，用于控制每秒发布多少帧。
    frame_index = 0  # 创建帧编号计数器，用于给发布的每帧图像编号。
    rospy.loginfo(f"正在发布图片：{image_path.resolve()}")  # 通过 ROS 日志输出当前发布的图片绝对路径。
    rospy.loginfo(f"图像话题：{image_topic}，频率：{publish_rate_hz} Hz")  # 通过 ROS 日志输出发布话题和频率。
    while not rospy.is_shutdown():  # 只要 ROS 没有关闭，就持续循环发布图像。
        frame_index = frame_index + 1  # 每发布一帧前，把帧编号加 1。
        image_message = bgr_array_to_image_message(cv_image, "yolo_course_camera")  # 把 OpenCV BGR 图像数组转换成 ROS 图像消息。
        image_message.header.stamp = rospy.Time.now()  # 给图像消息填入当前 ROS 时间戳。
        publisher.publish(image_message)  # 把图像消息发布到指定 ROS 话题。
        rospy.loginfo(f"已发布第 {frame_index} 帧")  # 输出当前已经发布的帧编号。
        rate.sleep()  # 按设置频率休眠，保证循环不会无限高速运行。


if __name__ == "__main__":  # 判断当前文件是否作为主程序直接运行。
    main()  # 直接运行本文件时，调用 main 函数启动图片发布节点。
