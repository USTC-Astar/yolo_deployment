from pathlib import Path  # 导入 Path 类，用于管理输入图片和输出视频路径。
import cv2  # 导入 OpenCV，用于读取图片、绘制文字和写入视频文件。

image_path = Path("images") / "bus.jpg"  # 指定用于生成测试视频的公交车图片路径。
video_path = Path("videos") / "bus_demo.avi"  # 指定生成后的测试视频保存路径。
frame_count = 20  # 设置视频总帧数为 20 帧。
frames_per_second = 5  # 设置视频帧率为每秒 5 帧。
frame_width = 640  # 设置输出视频每一帧的宽度为 640 像素。
frame_height = 480  # 设置输出视频每一帧的高度为 480 像素。
image = cv2.imread(str(image_path))  # 使用 OpenCV 解码输入图片，得到 BGR 像素数组。
if image is None:  # 检查图片是否读取成功，读取失败时 image 会是 None。
    raise FileNotFoundError(f"无法读取图片：{image_path}")  # 抛出文件不存在异常并停止程序。
resized_image = cv2.resize(image, (frame_width, frame_height))  # 把图片缩放到视频帧要求的固定宽高。
video_path.parent.mkdir(parents=True, exist_ok=True)  # 创建 videos 输出目录，目录已经存在时不报错。
fourcc = cv2.VideoWriter_fourcc(*"MJPG")  # 创建 MJPG 视频编码标识，告诉 OpenCV 用哪种方式压缩视频帧。
video_writer = cv2.VideoWriter(str(video_path), fourcc, frames_per_second, (frame_width, frame_height))  # 创建视频写入器，并设置路径、编码、帧率和画面尺寸。
if not video_writer.isOpened():  # 检查视频写入器是否成功打开。
    raise RuntimeError(f"无法创建视频文件：{video_path}")  # 如果视频写入器不可用，就抛出运行时异常并停止程序。
for frame_index in range(frame_count):  # 从 0 开始循环生成指定数量的视频帧。
    frame = resized_image.copy()  # 复制一份图片作为当前帧，避免直接修改原始缩放图片。
    label = f"frame {frame_index + 1:02d}"  # 生成当前帧编号文字，例如 frame 01。
    cv2.putText(frame, label, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)  # 在当前帧左上角绘制黄色帧编号。
    video_writer.write(frame)  # 把当前帧写入视频文件。
video_writer.release()  # 关闭视频写入器，并把缓冲区中的数据完整写入磁盘。
print(f"视频文件路径：{video_path.resolve()}")  # 打印生成视频的绝对路径。
print(f"视频帧数：{frame_count}")  # 打印视频总帧数。
print(f"视频帧率：{frames_per_second} FPS")  # 打印视频每秒播放的帧数。
print(f"视频尺寸：{frame_width}x{frame_height}")  # 打印视频画面的宽度和高度。
