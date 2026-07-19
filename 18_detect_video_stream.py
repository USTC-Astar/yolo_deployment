from pathlib import Path  # 导入 Path 类，用于管理模型权重和视频路径。
from ultralytics import YOLO  # 导入 YOLO 类，用于加载模型并执行视频流式检测。

weights_path = Path("models") / "yolo26n.pt"  # 指定本地 YOLO26 Nano 模型权重路径。
video_path = Path("videos") / "bus_demo.avi"  # 指定需要检测的测试视频路径。
model = YOLO(str(weights_path))  # 加载模型权重并创建 YOLO 模型对象。
results_stream = model.predict(source=str(video_path), device="cpu", conf=0.25, stream=True, save=False, verbose=False)  # 以流式方式逐帧产生检测结果，不把所有结果一次性堆在内存中。
processed_frames = 0  # 创建计数器，用于统计已经处理了多少帧。
for frame_result in results_stream:  # 从结果流中逐帧取出检测结果，循环会在视频结束时自动停止。
    processed_frames = processed_frames + 1  # 每成功取出一帧结果，就把已处理帧数加 1。
    detection_boxes = frame_result.boxes  # 读取当前帧中的检测框集合。
    class_counts = {}  # 创建字典，用于统计当前帧中每个类别出现了多少次。
    for detection_box in detection_boxes:  # 遍历当前帧中的每一个检测框。
        class_id = int(detection_box.cls.item())  # 从类别张量中取出类别编号，并转换成整数。
        class_name = frame_result.names[class_id]  # 使用类别编号查询当前类别名称。
        class_counts[class_name] = class_counts.get(class_name, 0) + 1  # 更新当前类别的计数，不存在时从 0 开始。
    print(f"第 {processed_frames:02d} 帧：目标总数={len(detection_boxes)}，类别统计={class_counts}")  # 打印当前帧的检测数量和类别统计。
print(f"流式处理完成，总帧数：{processed_frames}")  # 视频全部读完后，打印最终处理帧数。
