import sys  # 导入 sys 模块，用于在程序运行时追加 Python 模块搜索路径。
import cv2  # 先导入虚拟环境里的 OpenCV，避免后续系统路径中的 cv2 覆盖它。

sys.path.append("/usr/lib/python3/dist-packages")  # 把系统 Python 包目录追加到搜索路径末尾，让 rospy 能找到 rospkg 等依赖。
import rospy  # 导入 ROS Python 客户端库，用于后续创建 ROS 节点、订阅话题和发布话题。
from sensor_msgs.msg import Image  # 导入 ROS 标准图像消息类型，Gazebo 相机通常会发布这种消息。
from ultralytics import YOLO  # 导入 Ultralytics 的 YOLO 类，确认同一个 Python 环境也能使用 YOLO。
from ros_image_utils import image_message_to_bgr_array  # 导入课程自定义图像转换函数，避免 cv_bridge 和 OpenCV 版本冲突。

print(f"rospy 路径：{rospy.__file__}")  # 打印 rospy 的实际加载路径，确认它来自 ROS Noetic。
print(f"cv2 路径：{cv2.__file__}")  # 打印 cv2 的实际加载路径，确认它来自课程虚拟环境。
print(f"Image 消息类型：{Image.__name__}")  # 打印图像消息类名，确认 sensor_msgs 可以正常导入。
print(f"YOLO 类名：{YOLO.__name__}")  # 打印 YOLO 类名，确认 Ultralytics 仍然可以正常导入。
print(f"图像转换函数：{image_message_to_bgr_array.__name__}")  # 打印课程图像转换函数名称，确认自定义桥接工具可以正常导入。
