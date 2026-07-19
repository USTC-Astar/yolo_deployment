from pathlib import Path  # 导入 Path 类，用于管理输出图片保存路径。
import sys  # 导入 sys 模块，用于在程序运行时追加 Python 模块搜索路径。
import cv2  # 导入 OpenCV，用于把收到的图像帧保存成图片文件。

sys.path.append("/usr/lib/python3/dist-packages")  # 把系统 Python 包目录追加到搜索路径末尾，让 rospy 能找到 ROS 依赖。
import rospy  # 导入 ROS Python 客户端库，用于创建节点、订阅话题和关闭节点。
from sensor_msgs.msg import Image  # 导入 ROS 图像消息类型，用于订阅相机图像。
from ros_image_utils import image_message_to_bgr_array  # 导入课程自定义转换函数，用于把 ROS Image 转成 OpenCV BGR 数组。

saved_image = False  # 创建全局标记，用于记录是否已经保存过一帧图片。


def image_callback(image_message):  # 定义图像回调函数，每收到一帧 ROS 图像就会自动执行一次。
    global saved_image  # 声明函数内部要修改外部的 saved_image 标记。
    if saved_image:  # 如果已经保存过图片，就不再重复处理后续帧。
        return  # 直接结束本次回调。
    output_path_text = rospy.get_param("~output_path", "outputs/gazebo_camera_frame.jpg")  # 读取输出路径参数，未设置时保存到默认文件。
    output_path = Path(output_path_text)  # 把输出路径字符串转换成 Path 对象，方便创建目录和显示路径。
    output_path.parent.mkdir(parents=True, exist_ok=True)  # 创建输出目录，目录已经存在时不报错。
    cv_image = image_message_to_bgr_array(image_message)  # 把 ROS Image 消息转换成 OpenCV BGR 图像数组。
    cv2.imwrite(str(output_path), cv_image)  # 把 OpenCV BGR 图像数组保存成图片文件。
    saved_image = True  # 标记已经成功保存图片，避免后续帧重复写入。
    rospy.loginfo(f"已保存 Gazebo 相机画面：{output_path.resolve()}")  # 打印保存后的图片绝对路径。
    rospy.signal_shutdown("已经保存一帧图像")  # 主动请求关闭当前 ROS 节点。


def main():  # 定义程序入口函数，用于初始化节点并订阅图像话题。
    rospy.init_node("yolo_course_save_one_image")  # 初始化 ROS 节点，并设置节点名称。
    image_topic = rospy.get_param("~image_topic", "/sim_camera/image_raw")  # 读取图像话题参数，未设置时订阅 Gazebo 相机话题。
    rospy.Subscriber(image_topic, Image, image_callback, queue_size=1)  # 订阅图像话题，收到 Image 消息时调用 image_callback。
    rospy.loginfo(f"正在等待图像话题：{image_topic}")  # 打印当前等待的图像话题名称。
    rospy.spin()  # 让节点持续运行并等待回调，直到保存图片后主动关闭。


if __name__ == "__main__":  # 判断当前文件是否作为主程序直接运行。
    main()  # 直接运行本文件时调用 main 函数启动保存图像节点。
