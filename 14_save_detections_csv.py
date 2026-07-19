import csv  # 导入 Python 标准库 csv，用于把结构化检测结果写成 CSV 表格文件。
from pathlib import Path  # 导入 Path 类，用于管理模型、图片和输出文件路径。
from ultralytics import YOLO  # 导入 YOLO 类，用于加载权重并执行目标检测。

weights_path = Path("models") / "yolo26n.pt"  # 指定本地 YOLO26 Nano 模型权重路径。
image_path = Path("images") / "bus.jpg"  # 指定需要检测并导出结果的测试图片路径。
csv_path = Path("outputs") / "detections" / "bus_detections.csv"  # 指定检测结果 CSV 文件的保存路径。
fieldnames = ["image", "index", "class_id", "class_name", "confidence", "x_min", "y_min", "x_max", "y_max", "width", "height", "center_x", "center_y", "area"]  # 定义 CSV 每一列的列名和输出顺序。
model = YOLO(str(weights_path))  # 加载本地模型权重并创建 YOLO 模型对象。
results = model.predict(source=str(image_path), device="cpu", conf=0.25, save=False, verbose=False)  # 使用 CPU 检测图片，不保存可视化图片，不打印默认详细日志。
first_result = results[0]  # 取出第一张图片对应的检测结果对象。
class_names = first_result.names  # 读取类别编号到类别名称的映射表。
detection_boxes = first_result.boxes  # 读取当前图片中所有检测框对象。
csv_path.parent.mkdir(parents=True, exist_ok=True)  # 创建 CSV 输出目录，目录已经存在时不报错。
with csv_path.open("w", newline="", encoding="utf-8") as csv_file:  # 以写入模式打开 CSV 文件，并指定 UTF-8 编码。
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)  # 创建按字典写入 CSV 的 writer，并指定列名顺序。
    writer.writeheader()  # 写入 CSV 表头，也就是第一行列名。
    for detection_index, detection_box in enumerate(detection_boxes, start=1):  # 遍历所有检测框，并让目标编号从 1 开始。
        class_id = int(detection_box.cls.item())  # 从类别张量中取出类别编号，并转换成 Python 整数。
        class_name = class_names[class_id]  # 使用类别编号查询对应的类别名称。
        confidence = float(detection_box.conf.item())  # 从置信度张量中取出数值，并转换成 Python 浮点数。
        x_min, y_min, x_max, y_max = detection_box.xyxy[0].tolist()  # 读取当前检测框左上角和右下角坐标。
        box_width = x_max - x_min  # 使用右边界减左边界，计算检测框宽度。
        box_height = y_max - y_min  # 使用下边界减上边界，计算检测框高度。
        center_x = x_min + box_width / 2  # 使用左边界加半个宽度，计算中心点 x 坐标。
        center_y = y_min + box_height / 2  # 使用上边界加半个高度，计算中心点 y 坐标。
        box_area = box_width * box_height  # 使用宽度乘高度，计算检测框像素面积。
        row = {"image": image_path.name, "index": detection_index, "class_id": class_id, "class_name": class_name, "confidence": round(confidence, 6), "x_min": round(x_min, 2), "y_min": round(y_min, 2), "x_max": round(x_max, 2), "y_max": round(y_max, 2), "width": round(box_width, 2), "height": round(box_height, 2), "center_x": round(center_x, 2), "center_y": round(center_y, 2), "area": round(box_area, 2)}  # 把当前检测目标整理成一行 CSV 数据。
        writer.writerow(row)  # 把当前检测目标这一行写入 CSV 文件。
print(f"CSV 文件路径：{csv_path.resolve()}")  # 打印 CSV 文件的绝对路径。
print(f"写入目标数量：{len(detection_boxes)}")  # 打印写入 CSV 的检测目标数量。
