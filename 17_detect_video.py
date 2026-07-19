from pathlib import Path  # 导入 Path 类，用于管理模型权重、输入视频和输出目录路径。
from ultralytics import YOLO  # 导入 YOLO 类，用于加载模型并执行视频检测。

weights_path = Path("models") / "yolo26n.pt"  # 指定已经下载到本地的 YOLO26 Nano 权重文件。
video_path = Path("videos") / "bus_demo.avi"  # 指定需要进行目标检测的测试视频文件。
output_root = Path("outputs").resolve()  # 把输出根目录转换成绝对路径，确保结果保存在课程目录中。
output_name = "video_detection"  # 指定本次视频检测结果使用的子目录名称。
model = YOLO(str(weights_path))  # 加载模型权重并创建可执行推理的 YOLO 模型对象。
results = model.predict(source=str(video_path), device="cpu", conf=0.25, save=True, project=str(output_root), name=output_name, exist_ok=True)  # 对视频逐帧检测，并保存绘制检测框后的视频。
frame_results = list(results)  # 把生成器或结果序列转换成列表，便于统计实际处理的帧数。
output_directory = output_root / output_name  # 组合输出根目录和子目录，得到本次检测结果目录。
print(f"处理帧数：{len(frame_results)}")  # 打印 YOLO 实际返回的帧结果数量。
print(f"结果目录：{output_directory}")  # 打印保存检测结果的目录。
for output_file in sorted(output_directory.iterdir()):  # 遍历输出目录中的文件，并按文件名排序。
    print(f"输出文件：{output_file.name}")  # 打印每一个输出文件的名称。
