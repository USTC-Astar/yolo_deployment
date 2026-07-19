from pathlib import Path  # 导入 Path 类，用于管理模型权重、输入图片和输出图片路径。
import cv2  # 导入 OpenCV，用于保存带检测框的图像。
from ultralytics import YOLO  # 导入 YOLO 类，用于加载模型并执行目标检测。

weights_path = Path("models") / "yolo26n.pt"  # 指定本地 YOLO26 Nano 模型权重路径。
image_path = Path("images") / "bus.jpg"  # 指定需要检测并绘制检测框的输入图片路径。
output_path = Path("outputs") / "annotated" / "bus_annotated.jpg"  # 指定带检测框图片的保存路径。
model = YOLO(str(weights_path))  # 加载模型权重并创建 YOLO 模型对象。
results = model.predict(source=str(image_path), device="cpu", conf=0.25, save=False, verbose=False)  # 使用 CPU 检测图片，但不让 Ultralytics 自动保存结果。
first_result = results[0]  # 取出第一张图片对应的检测结果对象。
annotated_image = first_result.plot()  # 让 Ultralytics 把检测框、类别名和置信度画回图像数组。
output_path.parent.mkdir(parents=True, exist_ok=True)  # 创建输出目录，目录已经存在时不报错。
cv2.imwrite(str(output_path), annotated_image)  # 使用 OpenCV 把带检测框的图像数组保存成 JPG 文件。
print(f"检测目标总数：{len(first_result.boxes)}")  # 打印当前图片中检测到的目标数量。
print(f"标注图片路径：{output_path.resolve()}")  # 打印带检测框图片保存后的绝对路径。
