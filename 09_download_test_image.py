from pathlib import Path  # 导入 Path 类，用于创建目录和管理测试图片路径。
import requests  # 导入 requests 软件包，用于通过 HTTP 网络请求下载文件。

image_url = "https://ultralytics.com/images/bus.jpg"  # 保存 Ultralytics 官方测试图片的网络地址。
image_path = Path("images") / "bus.jpg"  # 组合本地图片目录和文件名，得到保存路径。
image_path.parent.mkdir(parents=True, exist_ok=True)  # 创建 images 目录，目录已存在时不报错。
response = requests.get(image_url, timeout=60)  # 发送 HTTP GET 请求下载图片，并把最长等待时间设为 60 秒。
response.raise_for_status()  # 如果服务器返回 4xx 或 5xx 错误状态码，就主动抛出异常并停止程序。
image_path.write_bytes(response.content)  # 把服务器返回的二进制图片内容写入本地文件。
print(f"测试图片路径：{image_path.resolve()}")  # 打印测试图片保存后的绝对路径。
print(f"测试图片大小：{image_path.stat().st_size} 字节")  # 读取并打印图片文件占用的字节数。
