from pathlib import Path  # 导入 Path 类，用于组织模型、输入图片和输出图片的路径。
from ultralytics import YOLO  # 从 Ultralytics 软件包导入 YOLO 类，用于加载模型和执行检测。

weights_path = Path("models") / "yolo26n.pt"  # 指定已经下载完成的 YOLO Nano 权重文件路径。
image_path = Path("images") / "bus.jpg"  # 指定本次目标检测使用的输入图片路径。
output_root = Path("outputs").resolve()  # 把输出根目录转换成绝对路径，避免 Ultralytics 改写相对保存位置。
output_directory = output_root / "first_detection"  # 在绝对输出根目录下指定本次检测结果的子目录。
model = YOLO(str(weights_path))  # 加载本地模型权重并创建可用于推理的 YOLO 模型对象。
results = model.predict(source=str(image_path), device="cpu", conf=0.25, save=True, project=str(output_root), name="first_detection", exist_ok=True)  # 使用绝对输出路径执行 CPU 检测，并保存置信度不低于 0.25 的结果。
first_result = results[0]  # 从结果列表中取出第一张也是唯一一张图片的检测结果。
output_path = output_directory / image_path.name  # 根据输出目录和原图片文件名组合出结果图片路径。
print(f"检测到的目标数量：{len(first_result.boxes)}")  # 统计检测框集合中的元素数量并打印出来。
print(f"结果图片路径：{output_path.resolve()}")  # 打印带有检测框的结果图片绝对路径。
print(f"结果图片是否存在：{output_path.exists()}")  # 检查结果图片是否已经成功写入磁盘。
