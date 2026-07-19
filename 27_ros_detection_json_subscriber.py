import json  # 导入 json 标准库，用于把 JSON 字符串还原成 Python 字典。
import sys  # 导入 sys 模块，用于在程序运行时追加 Python 模块搜索路径。

sys.path.append("/usr/lib/python3/dist-packages")  # 把系统 Python 包目录追加到搜索路径末尾，让 rospy 能找到 ROS 依赖。
import rospy  # 导入 ROS Python 客户端库，用于创建节点、订阅话题和打印日志。
from std_msgs.msg import String  # 导入 ROS 字符串消息类型，用于接收 JSON 检测结果。


def detections_callback(message):  # 定义检测结果回调函数，每收到一条 JSON 字符串消息就会自动执行一次。
    try:  # 开始尝试解析 JSON 字符串。
        payload = json.loads(message.data)  # 把 ROS String 的 data 字段从 JSON 字符串还原成 Python 字典。
    except json.JSONDecodeError as error:  # 如果字符串不是合法 JSON，就捕获解析异常。
        rospy.logerr(f"JSON 解析失败：{error}")  # 使用 ROS 错误日志输出解析失败原因。
        return  # 解析失败时结束本次回调，不继续处理这条消息。
    frame_index = payload["frame_index"]  # 从字典中读取当前检测结果对应的帧编号。
    detections = payload["detections"]  # 从字典中读取当前帧的目标检测列表。
    class_counts = {}  # 创建空字典，用于统计当前帧中每个类别出现次数。
    for detection in detections:  # 遍历当前帧中的每一个检测目标字典。
        class_name = detection["class_name"]  # 从目标字典中读取类别名称。
        class_counts[class_name] = class_counts.get(class_name, 0) + 1  # 更新类别计数，类别首次出现时从 0 开始。
    rospy.loginfo(f"解析第 {frame_index} 帧：目标总数={len(detections)}，类别统计={class_counts}")  # 打印解析后的目标总数和类别统计。


def main():  # 定义程序入口函数，用于初始化节点并订阅检测结果话题。
    rospy.init_node("yolo_course_detection_json_subscriber")  # 初始化 ROS 节点，并设置节点名称。
    detections_topic = rospy.get_param("~detections_topic", "/yolo_course/detections")  # 读取私有参数 detections_topic，未设置时使用课程检测结果话题。
    rospy.Subscriber(detections_topic, String, detections_callback, queue_size=10)  # 订阅检测结果话题，收到 String 消息时调用 detections_callback。
    rospy.loginfo(f"正在订阅检测结果话题：{detections_topic}")  # 打印当前订阅的检测结果话题。
    rospy.spin()  # 让节点持续运行并等待回调，直到用户停止程序或 ROS 关闭。


if __name__ == "__main__":  # 判断当前文件是否作为主程序直接运行。
    main()  # 直接运行本文件时调用 main 函数启动检测结果订阅节点。
