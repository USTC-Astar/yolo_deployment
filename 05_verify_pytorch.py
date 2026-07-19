import torch  # 导入 PyTorch 软件包，并在当前文件中使用名称 torch 访问它。

print(f"PyTorch 版本：{torch.__version__}")  # 读取并打印当前安装的 PyTorch 版本号。
input_tensor = torch.tensor([[1.0, 2.0], [3.0, 4.0]])  # 创建一个包含两行两列浮点数的 PyTorch 张量。
output_tensor = input_tensor * 2  # 让张量中的每个数都乘以 2，并把结果保存到新变量中。
print(f"输入张量：\n{input_tensor}")  # 打印计算前的输入张量，\n 表示先换行再显示内容。
print(f"计算结果：\n{output_tensor}")  # 打印张量乘以 2 后的计算结果。
print(f"CUDA 是否可用：{torch.cuda.is_available()}")  # 调用 PyTorch 的 CUDA 检查函数并打印布尔结果。
print(f"PyTorch 对应的 CUDA 版本：{torch.version.cuda}")  # 打印当前 PyTorch 构建所对应的 CUDA 版本，CPU 版应显示 None。
