from pathlib import Path  # 导入 Path 类，用于管理 YOLO 权重文件路径。
import sys  # 导入 sys 模块，用于在程序运行时追加 Python 模块搜索路径。
import cv2  # 先导入虚拟环境里的 OpenCV，避免后续系统路径中的 cv2 覆盖它。
from ultralytics import YOLO  # 导入 Ultralytics YOLO 类，用于加载模型并执行检测。

sys.path.append("/usr/lib/python3/dist-packages")  # 把系统 Python 包目录追加到搜索路径末尾，让 rospy 能找到 rospkg 等依赖。
import rospy  # 导入 ROS Python 客户端库，用于创建节点、订阅话题和打印 ROS 日志。
from sensor_msgs.msg import Image  # 导入 ROS 图像消息类型，用于接收相机图像。
from ros_image_utils import image_message_to_bgr_array  # 导入课程自定义转换函数，用于把 ROS Image 转成 OpenCV BGR 数组。

model = None  # 创建全局模型变量，稍后在 main 函数中加载 YOLO 权重。
processed_frames = 0  # 创建全局计数器，用于统计已经完成 YOLO 检测的帧数。


def image_callback(image_message):  # 定义图像回调函数，每收到一帧 ROS 图像就会自动执行一次。
    global processed_frames  # 声明函数内部要修改外部的 processed_frames 变量。
    try:  # 开始尝试执行可能失败的图像转换。
        cv_image = image_message_to_bgr_array(image_message)  # 把 ROS Image 消息转换成 OpenCV BGR 图像数组。
    except ValueError as error:  # 如果图像编码不支持或数据形状不合法，就捕获转换异常。
        rospy.logerr(f"图像转换失败：{error}")  # 使用 ROS 错误日志输出转换失败原因。
        return  # 转换失败时结束本次回调，不继续做 YOLO 检测。
    results = model.predict(source=cv_image, device="cpu", conf=0.25, save=False, verbose=False)  # 把当前 OpenCV 图像数组送入 YOLO，并使用 CPU 执行检测。
    first_result = results[0]  # 取出当前帧对应的检测结果对象。
    detection_boxes = first_result.boxes  # 读取当前帧中所有检测框对象。
    class_counts = {}  # 创建空字典，用于统计当前帧里每个类别出现次数。
    for detection_box in detection_boxes:  # 遍历当前帧中的每一个检测框。
        class_id = int(detection_box.cls.item())  # 从类别张量中取出类别编号，并转换成 Python 整数。
        class_name = first_result.names[class_id]  # 使用类别编号查询对应的类别名称。
        class_counts[class_name] = class_counts.get(class_name, 0) + 1  # 更新类别计数，类别首次出现时从 0 开始。
    processed_frames = processed_frames + 1  # 当前帧检测完成后，把已处理帧数加 1。
    rospy.loginfo(f"YOLO 第 {processed_frames} 帧：目标总数={len(detection_boxes)}，类别统计={class_counts}")  # 打印当前帧的检测统计结果。


def main():  # 定义程序入口函数，用于组织 ROS 节点初始化、模型加载和话题订阅。
    global model  # 声明 main 函数要修改全局 model 变量。
    rospy.init_node("yolo_course_detector")  # 初始化 ROS 节点，并设置节点名称。
    image_topic = rospy.get_param("~image_topic", "/yolo_course/image_raw")  # 读取私有参数 image_topic，未设置时订阅课程测试图像话题。
    weights_path_text = rospy.get_param("~weights", "models/yolo26n.pt")  # 读取私有参数 weights，未设置时使用本地 YOLO26 Nano 权重。
    weights_path = Path(weights_path_text)  # 把权重路径字符串转换成 Path 对象，方便检查和显示。
    rospy.loginfo(f"正在加载 YOLO 权重：{weights_path.resolve()}")  # 打印即将加载的权重文件绝对路径。
    model = YOLO(str(weights_path))  # 加载 YOLO 权重并创建模型对象，后续每帧复用同一个模型。
    rospy.Subscriber(image_topic, Image, image_callback, queue_size=1)  # 订阅 ROS 图像话题，收到图像时调用 image_callback。
    rospy.loginfo(f"YOLO 检测节点正在订阅：{image_topic}")  # 打印当前订阅的图像话题。
    rospy.spin()  # 让节点持续运行并等待图像回调，直到用户停止程序或 ROS 关闭。


if __name__ == "__main__":  # 判断当前文件是否作为主程序直接运行。
    main()  # 直接运行本文件时调用 main 函数启动 YOLO 检测节点。
