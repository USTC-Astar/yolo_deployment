import cv2  # 导入 OpenCV，用于在 RGB、BGR 和灰度图之间转换颜色格式。
import numpy as np  # 导入 NumPy，用于把 ROS 图像字节数据转换成图像数组。
from sensor_msgs.msg import Image  # 导入 ROS 图像消息类型，用于创建和解析 Image 消息。


def image_message_to_bgr_array(image_message):  # 定义函数，把 ROS Image 消息转换成 OpenCV BGR 图像数组。
    supported_encodings = {"bgr8", "rgb8", "mono8"}  # 定义本课程当前支持的三种常见图像编码。
    if image_message.encoding not in supported_encodings:  # 判断输入图像编码是否在支持列表中。
        raise ValueError(f"暂不支持图像编码：{image_message.encoding}")  # 编码不支持时抛出异常，避免错误解释图像数据。
    channels = 1 if image_message.encoding == "mono8" else 3  # 灰度图只有 1 个通道，彩色图有 3 个通道。
    expected_step = image_message.width * channels  # 计算每行有效图像数据应该占用的字节数。
    raw_array = np.frombuffer(image_message.data, dtype=np.uint8)  # 把 ROS 消息中的原始字节数据转换成一维 uint8 数组。
    row_array = raw_array.reshape(image_message.height, image_message.step)  # 按 ROS 消息记录的行宽 step 把一维数组还原成二维行数据。
    useful_array = row_array[:, :expected_step]  # 去掉每行末尾可能存在的对齐填充字节，只保留真实像素数据。
    if image_message.encoding == "mono8":  # 判断当前图像是否是单通道灰度图。
        mono_image = useful_array.reshape(image_message.height, image_message.width)  # 把有效数据整理成高度乘宽度的灰度图数组。
        bgr_image = cv2.cvtColor(mono_image, cv2.COLOR_GRAY2BGR)  # 把灰度图转换成三通道 BGR 图像，方便 YOLO 统一处理。
    else:  # 当前图像不是灰度图时，按三通道彩色图处理。
        color_image = useful_array.reshape(image_message.height, image_message.width, channels)  # 把有效数据整理成 HWC 彩色图数组。
        if image_message.encoding == "rgb8":  # 判断当前彩色图是否是 RGB 顺序。
            bgr_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR)  # 把 RGB 顺序转换成 OpenCV 常用的 BGR 顺序。
        else:  # 当前彩色图已经是 BGR 顺序。
            bgr_image = color_image  # 直接复用当前图像数组，不做颜色转换。
    return np.ascontiguousarray(bgr_image)  # 返回连续内存排列的 BGR 图像数组，方便 OpenCV 和 YOLO 后续处理。


def bgr_array_to_image_message(bgr_image, frame_id):  # 定义函数，把 OpenCV BGR 图像数组转换成 ROS Image 消息。
    contiguous_image = np.ascontiguousarray(bgr_image)  # 把输入图像整理成连续内存排列，保证 tobytes 按行正确输出。
    height, width, channels = contiguous_image.shape  # 从 HWC 图像数组中读取高度、宽度和通道数。
    if channels != 3:  # 判断输入图像是否是三通道彩色图。
        raise ValueError(f"BGR 图像必须有 3 个通道，当前通道数：{channels}")  # 通道数不符合要求时抛出异常。
    image_message = Image()  # 创建一个空的 ROS Image 消息对象。
    image_message.header.frame_id = frame_id  # 设置图像所属坐标系名称，模拟或标记相机坐标系。
    image_message.height = height  # 写入图像高度，单位是像素。
    image_message.width = width  # 写入图像宽度，单位是像素。
    image_message.encoding = "bgr8"  # 声明图像数据采用 8 位 BGR 彩色编码。
    image_message.is_bigendian = 0  # 声明图像字节序为小端；uint8 图像通常不受字节序影响。
    image_message.step = width * channels  # 写入每一行图像数据占用的字节数。
    image_message.data = contiguous_image.tobytes()  # 把连续内存图像数组转换成 ROS Image 需要的字节数据。
    return image_message  # 返回填充完成的 ROS Image 消息。
