from pathlib import Path  # 从 Python 标准库导入 Path 类，用于安全地拼接和检查文件路径。
from ultralytics import YOLO  # 从 Ultralytics 软件包导入 YOLO 类，用于加载模型权重。

weights_path = Path("models") / "yolo26n.pt"  # 使用 / 运算符把目录名和文件名组合成模型权重路径。
model = YOLO(str(weights_path))  # 把 Path 转成字符串并交给 YOLO 类，创建已经加载权重的模型对象。
print(f"权重文件路径：{weights_path.resolve()}")  # 把相对路径转换成绝对路径并打印出来。
print(f"权重文件是否存在：{weights_path.exists()}")  # 检查权重文件是否已经保存在本地并打印布尔结果。
print(f"模型任务类型：{model.task}")  # 打印模型识别出的任务类型，目标检测模型应显示 detect。
