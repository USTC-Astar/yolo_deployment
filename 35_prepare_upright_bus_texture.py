from pathlib import Path  # 导入 Path 类，用于管理输入纹理和输出纹理路径。
import cv2  # 导入 OpenCV，用于读取、旋转和保存图片。

input_path = Path("models") / "bus_billboard" / "materials" / "textures" / "bus.jpg"  # 指定原始公交车纹理图片路径。
output_path = Path("models") / "bus_billboard" / "materials" / "textures" / "bus_upright.jpg"  # 指定旋转修正后的纹理图片路径。
image = cv2.imread(str(input_path))  # 使用 OpenCV 读取原始公交车纹理图片。
if image is None:  # 检查图片是否读取成功，读取失败时 image 会是 None。
    raise FileNotFoundError(f"无法读取纹理图片：{input_path}")  # 抛出文件不存在异常并停止程序。
rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)  # 把纹理顺时针旋转 90 度，用来抵消 Gazebo 平面贴图的方向旋转。
cv2.imwrite(str(output_path), rotated_image)  # 把修正后的纹理图片保存到 Gazebo 模型纹理目录。
print(f"修正纹理路径：{output_path.resolve()}")  # 打印修正后纹理图片的绝对路径。
print(f"修正纹理尺寸：{rotated_image.shape[1]}x{rotated_image.shape[0]}")  # 打印修正后纹理的宽度和高度。
