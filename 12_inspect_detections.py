from pathlib import Path  # 导入 Path 类，用于组织模型权重和输入图片的路径。
from ultralytics import YOLO  # 从 Ultralytics 软件包导入 YOLO 类，用于加载模型和执行推理。

weights_path = Path("models") / "yolo26n.pt"  # 指定已经下载到本地的 YOLO26 Nano 权重文件。
image_path = Path("images") / "bus.jpg"  # 指定需要执行目标检测的公交车测试图片。
model = YOLO(str(weights_path))  # 加载模型权重并创建 YOLO 模型对象。
results = model.predict(source=str(image_path), device="cpu", conf=0.25, save=False, verbose=False)  # 使用 CPU 执行检测，但不保存图片也不打印默认详细日志。
first_result = results[0]  # 取出结果列表中第一张图片对应的检测结果对象。
class_names = first_result.names  # 读取类别编号到类别名称的映射表。
detection_boxes = first_result.boxes  # 读取当前图片中所有目标的检测框集合。
print(f"检测目标总数：{len(detection_boxes)}")  # 打印检测框集合中的目标数量。
for detection_index, detection_box in enumerate(detection_boxes, start=1):  # 遍历每个检测框，并让显示编号从 1 开始。
    class_id = int(detection_box.cls.item())  # 从单元素张量中取出类别编号，并转换成 Python 整数。
    class_name = class_names[class_id]  # 使用类别编号从映射表中查询可读的类别名称。
    confidence = float(detection_box.conf.item())  # 从单元素张量中取出置信度，并转换成 Python 浮点数。
    x_min, y_min, x_max, y_max = detection_box.xyxy[0].tolist()  # 读取左上角和右下角坐标，并转换成 Python 数值列表。
    print(f"目标 {detection_index}：类别编号={class_id}，类别={class_name}，置信度={confidence:.3f}，坐标=({x_min:.1f}, {y_min:.1f}, {x_max:.1f}, {y_max:.1f})")  # 按固定小数位打印当前目标的完整检测信息。
