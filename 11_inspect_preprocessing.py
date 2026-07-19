from pathlib import Path  # 导入 Path 类，用于管理输入图片和输出图片的文件路径。
import cv2  # 导入 OpenCV，用于解码、缩放、填充和转换图片颜色。
import numpy as np  # 导入 NumPy，用于调整像素数组的维度和内存排列。
import torch  # 导入 PyTorch，用于把 NumPy 数组转换成模型使用的张量。

image_path = Path("images") / "bus.jpg"  # 指定需要观察预处理过程的公交车图片路径。
output_path = Path("outputs") / "preprocessing" / "letterbox_bus.jpg"  # 指定 Letterbox 图片的保存路径。
bgr_image = cv2.imread(str(image_path))  # 解码 JPEG 文件，得到采用 HWC 排列和 BGR 颜色顺序的 NumPy 数组。
if bgr_image is None:  # 检查 OpenCV 是否成功读取图片，读取失败时变量会是 None。
    raise FileNotFoundError(f"无法读取图片：{image_path}")  # 抛出文件不存在异常并立即停止程序。
original_height, original_width = bgr_image.shape[:2]  # 从数组形状中读取原图高度和宽度，忽略最后的颜色通道维度。
target_height = 640  # 设置本次演示要求的目标高度为 640 像素。
target_width = 640  # 设置本次演示要求的目标宽度为 640 像素。
scale = min(target_width / original_width, target_height / original_height)  # 选择不会超出目标画布的最小缩放比例。
resized_width = round(original_width * scale)  # 根据统一缩放比例计算保持原图比例的新宽度。
resized_height = round(original_height * scale)  # 根据统一缩放比例计算保持原图比例的新高度。
resized_bgr = cv2.resize(bgr_image, (resized_width, resized_height), interpolation=cv2.INTER_LINEAR)  # 使用双线性插值缩放图片但不改变宽高比例。
padding_width = target_width - resized_width  # 计算缩放后距离目标宽度还缺少多少像素。
padding_height = target_height - resized_height  # 计算缩放后距离目标高度还缺少多少像素。
left_padding = padding_width // 2  # 使用整除计算左侧需要填充的像素数量。
right_padding = padding_width - left_padding  # 把剩余的宽度填充放到图片右侧。
top_padding = padding_height // 2  # 使用整除计算上方需要填充的像素数量。
bottom_padding = padding_height - top_padding  # 把剩余的高度填充放到图片下方。
padded_bgr = cv2.copyMakeBorder(resized_bgr, top_padding, bottom_padding, left_padding, right_padding, cv2.BORDER_CONSTANT, value=(114, 114, 114))  # 使用灰色像素把缩放图片填充为 640×640。
rgb_image = cv2.cvtColor(padded_bgr, cv2.COLOR_BGR2RGB)  # 把 OpenCV 使用的 BGR 颜色顺序转换成模型常用的 RGB 顺序。
chw_array = np.ascontiguousarray(rgb_image.transpose(2, 0, 1))  # 把数组从 HWC 调整为 CHW，并整理成连续内存排列。
image_tensor = torch.from_numpy(chw_array).float() / 255.0  # 把 NumPy 数组转换成浮点张量，并把像素归一化到 0.0 至 1.0。
batch_tensor = image_tensor.unsqueeze(0)  # 在最前面添加批次维度，把 CHW 张量变成 NCHW 张量。
output_path.parent.mkdir(parents=True, exist_ok=True)  # 创建输出目录，并允许目录已经存在。
cv2.imwrite(str(output_path), padded_bgr)  # 保存仍采用 BGR 顺序的 Letterbox 图片，便于直接观察填充效果。
print(f"解码后 HWC/BGR：{bgr_image.shape}，数据类型：{bgr_image.dtype}")  # 打印原始像素数组的形状和整数数据类型。
print(f"等比例缩放后：{resized_bgr.shape}，缩放比例：{scale:.4f}")  # 打印缩放后形状，并把比例保留四位小数。
print(f"填充量 左/右/上/下：{left_padding}/{right_padding}/{top_padding}/{bottom_padding}")  # 打印图片四个方向各自的填充量。
print(f"Letterbox 后 HWC/BGR：{padded_bgr.shape}")  # 打印缩放并填充后的 HWC 数组形状。
print(f"转换后 CHW/RGB：{chw_array.shape}")  # 打印颜色和维度顺序转换后的数组形状。
print(f"最终 NCHW 张量：{tuple(batch_tensor.shape)}，数据类型：{batch_tensor.dtype}")  # 打印模型输入张量的形状和浮点数据类型。
print(f"张量数值范围：{batch_tensor.min().item():.4f} 至 {batch_tensor.max().item():.4f}")  # 打印归一化后张量中的最小值和最大值。
print(f"Letterbox 图片：{output_path.resolve()}")  # 打印演示图片保存后的绝对路径。
