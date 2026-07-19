from pathlib import Path  # 导入 Path 类，用于管理模型权重和输入图片路径。
from ultralytics import YOLO  # 导入 YOLO 类，用于加载模型并执行目标检测。

weights_path = Path("models") / "yolo26n.pt"  # 指定本地 YOLO26 Nano 权重文件路径。
image_path = Path("images") / "bus.jpg"  # 指定需要检测的公交车测试图片路径。
model = YOLO(str(weights_path))  # 加载本地权重并创建 YOLO 模型对象。
results = model.predict(source=str(image_path), device="cpu", conf=0.25, save=False, verbose=False)  # 使用 CPU 检测图片，并关闭图片保存和默认日志。
first_result = results[0]  # 取出第一张图片对应的检测结果对象。
class_names = first_result.names  # 读取类别编号到类别名称的映射表。
detection_boxes = first_result.boxes  # 读取当前图片中的全部检测框对象。
print(f"检测目标总数：{len(detection_boxes)}")  # 打印当前图片中检测到的目标数量。
for detection_index, detection_box in enumerate(detection_boxes, start=1):  # 遍历每个检测框，并让显示编号从 1 开始。
    class_id = int(detection_box.cls.item())  # 从类别张量中取出单个类别编号，并转换成整数。
    class_name = class_names[class_id]  # 使用类别编号查询对应的人类可读类别名称。
    confidence = float(detection_box.conf.item())  # 从置信度张量中取出单个置信度，并转换成浮点数。
    x_min, y_min, x_max, y_max = detection_box.xyxy[0].tolist()  # 读取检测框左上角和右下角坐标。
    box_width = x_max - x_min  # 使用右边界减左边界，计算检测框宽度。
    box_height = y_max - y_min  # 使用下边界减上边界，计算检测框高度。
    center_x = x_min + box_width / 2  # 使用左边界加半个宽度，计算检测框中心点 x 坐标。
    center_y = y_min + box_height / 2  # 使用上边界加半个高度，计算检测框中心点 y 坐标。
    box_area = box_width * box_height  # 使用宽度乘高度，计算检测框面积。
    print(f"目标 {detection_index}：{class_name}，置信度={confidence:.3f}，宽={box_width:.1f}，高={box_height:.1f}，中心=({center_x:.1f}, {center_y:.1f})，面积={box_area:.1f}")  # 打印当前目标的几何信息。
