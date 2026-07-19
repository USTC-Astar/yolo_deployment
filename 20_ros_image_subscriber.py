import sys  # 导入 sys 模块，用于在程序运行时追加 Python 模块搜索路径。
import cv2  # 先导入虚拟环境里的 OpenCV，避免后续系统路径中的 cv2 覆盖它。

sys.path.append("/usr/lib/python3/dist-packages")  # 把系统 Python 包目录追加到搜索路径末尾，让 rospy 能找到 rospkg 等依赖。
import rospy  # 导入 ROS Python 客户端库，用于创建节点、订阅话题和保持程序运行。
from sensor_msgs.msg import Image  # 导入 ROS 图像消息类型，用于接收相机发布的图片帧。
from ros_image_utils import image_message_to_bgr_array  # 导入课程自定义转换函数，用于把 ROS Image 转成 OpenCV BGR 数组。

received_frames = 0  # 创建全局计数器，用于统计已经收到多少帧图像。


def image_callback(image_message):  # 定义图像话题回调函数，每收到一帧图像就会自动执行一次。
    global received_frames  # 声明函数内部要修改外部的 received_frames 计数器。
    try:  # 开始尝试执行可能失败的图像转换代码。
        cv_image = image_message_to_bgr_array(image_message)  # 把 ROS 图像消息转换成 OpenCV 使用的 BGR 图像数组。
    except ValueError as error:  # 如果图像编码不支持或数据形状不合法，就捕获转换异常。
        rospy.logerr(f"图像转换失败：{error}")  # 通过 ROS 日志输出错误信息。
        return  # 转换失败时直接结束本次回调，不继续处理这一帧。
    received_frames = received_frames + 1  # 转换成功后，把已接收帧数加 1。
    height, width = cv_image.shape[:2]  # 从 OpenCV 图像数组形状中读取高度和宽度。
    rospy.loginfo(f"收到第 {received_frames} 帧：宽={width}，高={height}，编码={image_message.encoding}")  # 通过 ROS 日志打印当前帧尺寸和原始编码。


def main():  # 定义程序入口函数，用于组织节点初始化和订阅逻辑。
    rospy.init_node("yolo_course_image_subscriber")  # 初始化 ROS 节点，并设置节点名称。
    image_topic = rospy.get_param("~image_topic", "/camera/rgb/image_raw")  # 读取私有参数 image_topic，未设置时使用默认图像话题。
    rospy.Subscriber(image_topic, Image, image_callback, queue_size=1)  # 订阅图像话题，收到 Image 消息时调用 image_callback。
    rospy.loginfo(f"正在订阅图像话题：{image_topic}")  # 输出当前订阅的图像话题名称。
    rospy.spin()  # 让节点持续运行并等待回调，直到用户停止程序或 ROS 关闭。


if __name__ == "__main__":  # 判断当前文件是否作为主程序直接运行。
    main()  # 直接运行本文件时，调用 main 函数启动 ROS 图像订阅节点。
