import ultralytics  # 导入完整的 Ultralytics 软件包，以便读取软件包版本等信息。
from ultralytics import YOLO  # 只从 Ultralytics 软件包中导入后续要使用的 YOLO 类。

print(f"Ultralytics 版本：{ultralytics.__version__}")  # 打印当前安装的 Ultralytics 版本号。
print(f"成功导入的类：{YOLO.__name__}")  # 读取 YOLO 类自身的名称，用于确认导入操作成功。
