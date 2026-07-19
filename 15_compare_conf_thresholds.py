from pathlib import Path  # 导入 Path 类，用于管理模型权重和输入图片路径。
from ultralytics import YOLO  # 导入 YOLO 类，用于加载模型并执行检测。

weights_path = Path("models") / "yolo26n.pt"  # 指定本地 YOLO26 Nano 权重文件路径。
image_path = Path("images") / "bus.jpg"  # 指定用于比较置信度阈值的测试图片路径。
confidence_thresholds = [0.25, 0.50, 0.80, 0.90, 0.95]  # 定义需要依次测试的置信度阈值列表。
model = YOLO(str(weights_path))  # 加载模型权重并创建 YOLO 模型对象。
for confidence_threshold in confidence_thresholds:  # 遍历每一个置信度阈值并分别执行检测。
    results = model.predict(source=str(image_path), device="cpu", conf=confidence_threshold, save=False, verbose=False)  # 使用当前阈值检测图片，不保存图片和默认日志。
    first_result = results[0]  # 取出第一张图片对应的检测结果对象。
    detection_boxes = first_result.boxes  # 读取当前阈值下保留下来的检测框集合。
    class_counts = {}  # 创建空字典，用于统计每个类别名称出现的次数。
    for detection_box in detection_boxes:  # 遍历当前阈值下的每一个检测框。
        class_id = int(detection_box.cls.item())  # 从类别张量中取出类别编号，并转换成整数。
        class_name = first_result.names[class_id]  # 使用类别编号查询类别名称。
        class_counts[class_name] = class_counts.get(class_name, 0) + 1  # 把当前类别的计数加 1，首次出现时从 0 开始。
    print(f"conf={confidence_threshold:.2f}：总数={len(detection_boxes)}，类别统计={class_counts}")  # 打印当前阈值下的检测总数和分类统计。
