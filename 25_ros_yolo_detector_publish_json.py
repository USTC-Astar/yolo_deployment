import json  # 导入 json 标准库，用于把 Python 字典和列表转换成 JSON 字符串。
from pathlib import Path  # 导入 Path 类，用于管理 YOLO 权重文件路径。
import sys  # 导入 sys 模块，用于在程序运行时追加 Python 模块搜索路径。
import cv2  # 先导入虚拟环境里的 OpenCV，避免后续系统路径中的 cv2 覆盖它。
from ultralytics import YOLO  # 导入 Ultralytics YOLO 类，用于加载模型并执行目标检测。

sys.path.append("/usr/lib/python3/dist-packages")  # 把系统 Python 包目录追加到搜索路径末尾，让 rospy 能找到 ROS 依赖。
import rospy  # 导入 ROS Python 客户端库，用于创建节点、订阅话题和发布话题。
from sensor_msgs.msg import Image  # 导入 ROS 图像消息类型，用于接收相机图像。
from std_msgs.msg import String  # 导入 ROS 字符串消息类型，用于发布 JSON 格式的检测结果。
from ros_image_utils import image_message_to_bgr_array  # 导入课程自定义转换函数，用于把 ROS Image 转成 OpenCV BGR 数组。

model = None  # 创建全局模型变量，稍后在 main 函数中加载 YOLO 权重。
detections_publisher = None  # 创建全局发布者变量，稍后在 main 函数中创建 ROS 结果发布者。
processed_frames = 0  # 创建全局计数器，用于统计已经完成检测并发布结果的帧数。


def image_callback(image_message):  # 定义图像回调函数，每收到一帧 ROS 图像就会自动执行一次。
    global processed_frames  # 声明函数内部要修改外部的 processed_frames 变量。
    try:  # 开始尝试执行可能失败的 ROS 图像转换。
        cv_image = image_message_to_bgr_array(image_message)  # 把 ROS Image 消息转换成 OpenCV BGR 图像数组。
    except ValueError as error:  # 如果图像编码不支持或数据形状不合法，就捕获转换异常。
        rospy.logerr(f"图像转换失败：{error}")  # 使用 ROS 错误日志输出转换失败原因。
        return  # 转换失败时结束本次回调，不继续执行 YOLO 检测。
    results = model.predict(source=cv_image, device="cpu", conf=0.25, save=False, verbose=False)  # 把当前帧送入 YOLO，并使用 CPU 执行检测。
    first_result = results[0]  # 取出当前帧对应的检测结果对象。
    detections = []  # 创建空列表，用于保存当前帧的所有检测目标。
    for detection_box in first_result.boxes:  # 遍历当前帧中的每一个检测框。
        class_id = int(detection_box.cls.item())  # 从类别张量中取出类别编号，并转换成 Python 整数。
        class_name = first_result.names[class_id]  # 使用类别编号查询对应的类别名称。
        confidence = float(detection_box.conf.item())  # 从置信度张量中取出数值，并转换成 Python 浮点数。
        x_min, y_min, x_max, y_max = detection_box.xyxy[0].tolist()  # 读取检测框左上角和右下角坐标。
        detection = {"class_id": class_id, "class_name": class_name, "confidence": round(confidence, 6), "xyxy": [round(x_min, 2), round(y_min, 2), round(x_max, 2), round(y_max, 2)]}  # 把一个目标整理成 JSON 友好的字典。
        detections.append(detection)  # 把当前目标字典加入当前帧检测结果列表。
    processed_frames = processed_frames + 1  # 当前帧处理完成后，把帧计数加 1。
    payload = {"frame_index": processed_frames, "stamp": image_message.header.stamp.to_sec(), "frame_id": image_message.header.frame_id, "detections": detections}  # 把当前帧编号、时间戳、坐标系和检测列表整理成消息载荷。
    detections_publisher.publish(json.dumps(payload, ensure_ascii=False))  # 把载荷转换成 JSON 字符串并发布到 ROS 检测结果话题。
    rospy.loginfo(f"已发布第 {processed_frames} 帧检测结果：目标总数={len(detections)}")  # 打印当前帧检测结果已经发布的日志。


def main():  # 定义程序入口函数，用于组织 ROS 节点初始化、模型加载、发布者创建和订阅者创建。
    global model  # 声明 main 函数要修改全局 model 变量。
    global detections_publisher  # 声明 main 函数要修改全局 detections_publisher 变量。
    rospy.init_node("yolo_course_detector_json")  # 初始化 ROS 节点，并设置节点名称。
    image_topic = rospy.get_param("~image_topic", "/yolo_course/image_raw")  # 读取私有参数 image_topic，未设置时订阅课程测试图像话题。
    detections_topic = rospy.get_param("~detections_topic", "/yolo_course/detections")  # 读取私有参数 detections_topic，未设置时发布到课程检测结果话题。
    weights_path_text = rospy.get_param("~weights", "models/yolo26n.pt")  # 读取私有参数 weights，未设置时使用本地 YOLO26 Nano 权重。
    weights_path = Path(weights_path_text)  # 把权重路径字符串转换成 Path 对象，方便检查和显示。
    rospy.loginfo(f"正在加载 YOLO 权重：{weights_path.resolve()}")  # 打印即将加载的权重文件绝对路径。
    model = YOLO(str(weights_path))  # 加载 YOLO 权重并创建模型对象，后续每帧复用同一个模型。
    detections_publisher = rospy.Publisher(detections_topic, String, queue_size=10)  # 创建检测结果发布者，消息类型为 String，队列长度为 10。
    rospy.Subscriber(image_topic, Image, image_callback, queue_size=1)  # 订阅 ROS 图像话题，收到图像时调用 image_callback。
    rospy.loginfo(f"正在订阅图像话题：{image_topic}")  # 打印当前订阅的图像话题。
    rospy.loginfo(f"正在发布检测话题：{detections_topic}")  # 打印当前发布的检测结果话题。
    rospy.spin()  # 让节点持续运行并等待图像回调，直到用户停止程序或 ROS 关闭。


if __name__ == "__main__":  # 判断当前文件是否作为主程序直接运行。
    main()  # 直接运行本文件时调用 main 函数启动 JSON 检测结果发布节点。
