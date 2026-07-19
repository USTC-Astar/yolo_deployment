# YOLO Deployment Course

这是一个面向初学者的 YOLO 部署与仿真验证课程项目。

项目从 Python 虚拟环境开始，逐步完成图片检测、视频检测、ROS 图像话题接入、Gazebo 相机仿真，以及 YOLO 检测结果的 JSON 和带框图像发布。

## 项目特点

- 采用分步骤脚本，文件名前缀按照学习顺序编号。
- 每个教学脚本都尽量使用逐行中文注释，便于理解每一行代码的作用。
- 默认使用 CPU 版 PyTorch，方便没有 NVIDIA 显卡的电脑运行。
- 支持 ROS Noetic 图像话题输入，适合机器人视觉入门。
- 支持 Gazebo 11 仿真相机验证，完成从仿真画面到 YOLO 检测结果的闭环。

## 已验证环境

- Ubuntu 20.04
- Python 3.8
- ROS Noetic
- Gazebo 11
- PyTorch 2.4.1 CPU
- Ultralytics 8.4.96

说明：本课程默认不要求 CUDA。若机器有 NVIDIA GPU，可以额外安装 CUDA 版 PyTorch，并把相关推理代码中的 `device="cpu"` 改为 `device=0` 或 `device="cuda"`。

## 系统依赖

运行基础 YOLO 图片和视频检测，需要系统中已有 Python 3。

运行 ROS 和 Gazebo 仿真部分，需要提前安装 ROS Noetic、Gazebo 11 和 `gazebo_ros` 相关插件。

## 目录结构

```text
yolo_deployment_course/                 # 课程项目根目录
├── 01_create_venv.sh                    # 创建 Python 虚拟环境
├── 04_install_pytorch_cpu.sh            # 安装 CPU 版 PyTorch
├── 06_install_ultralytics.sh            # 安装 Ultralytics YOLO
├── 10_detect_image.py                   # 图片目标检测示例
├── 17_detect_video.py                   # 视频目标检测示例
├── 18_detect_video_stream.py            # 视频逐帧流式检测示例
├── 20_ros_image_subscriber.py           # ROS 图像订阅示例
├── 21_ros_image_publisher.py            # ROS 图像发布示例
├── 25_ros_yolo_detector_publish_json.py # YOLO 检测结果 JSON 发布节点
├── 27_ros_detection_json_subscriber.py  # YOLO JSON 检测结果订阅节点
├── 37_ros_yolo_detector_publish_annotated.py # YOLO JSON 与带框图像发布节点
├── ros_image_utils.py                   # ROS Image 与 OpenCV 图像转换工具
├── images/                              # 测试图片目录
├── videos/                              # 测试视频目录
├── models/                              # YOLO 权重与 Gazebo 模型目录
├── worlds/                              # Gazebo world 文件目录
└── outputs/                             # 检测图片、日志和验证结果输出目录
```

## 快速开始

进入项目目录：

```bash
cd yolo_deployment_course # 进入课程项目目录。
```

创建虚拟环境：

```bash
./01_create_venv.sh # 使用 python3 -m venv 创建 .venv 虚拟环境。
```

检查虚拟环境：

```bash
./02_activate_venv.sh # 激活 .venv 并显示当前 Python 与 pip 路径。
```

升级 pip：

```bash
./03_upgrade_pip.sh # 在 .venv 中升级并固定 pip 版本。
```

安装 PyTorch CPU 版：

```bash
./04_install_pytorch_cpu.sh # 安装 CPU 版 torch 和 torchvision。
```

也可以使用 `requirements.txt` 一次性安装 Python 依赖：

```bash
source .venv/bin/activate # 激活当前项目的 Python 虚拟环境。
python -m pip install -r requirements.txt # 按 requirements.txt 安装 PyTorch CPU、Ultralytics、OpenCV 和 requests。
deactivate # 退出当前 Python 虚拟环境。
```

验证 PyTorch：

```bash
source .venv/bin/activate # 激活当前项目的 Python 虚拟环境。
python 05_verify_pytorch.py # 检查 PyTorch 是否安装成功以及 CUDA 是否可用。
deactivate # 退出当前 Python 虚拟环境。
```

安装 Ultralytics：

```bash
./06_install_ultralytics.sh # 安装 YOLO 推理所需的 ultralytics 软件包。
```

验证 Ultralytics：

```bash
source .venv/bin/activate # 激活当前项目的 Python 虚拟环境。
python 07_verify_ultralytics.py # 检查 ultralytics 是否能被 Python 正常导入。
deactivate # 退出当前 Python 虚拟环境。
```

## 基础 YOLO 推理

加载模型：

```bash
source .venv/bin/activate # 激活当前项目的 Python 虚拟环境。
python 08_load_model.py # 加载 models/yolo26n.pt 并显示模型信息。
deactivate # 退出当前 Python 虚拟环境。
```

下载测试图片：

```bash
source .venv/bin/activate # 激活当前项目的 Python 虚拟环境。
python 09_download_test_image.py # 下载 bus.jpg 到 images 目录。
deactivate # 退出当前 Python 虚拟环境。
```

执行图片检测：

```bash
source .venv/bin/activate # 激活当前项目的 Python 虚拟环境。
python 10_detect_image.py # 对 images/bus.jpg 执行 YOLO 检测并保存带框结果。
deactivate # 退出当前 Python 虚拟环境。
```

查看模型预处理流程：

```bash
source .venv/bin/activate # 激活当前项目的 Python 虚拟环境。
python 11_inspect_preprocessing.py # 展示图片缩放、填充、通道转换和张量转换过程。
deactivate # 退出当前 Python 虚拟环境。
```

查看检测框信息：

```bash
source .venv/bin/activate # 激活当前项目的 Python 虚拟环境。
python 12_inspect_detections.py # 读取 xyxy 坐标、类别编号、类别名称和置信度。
deactivate # 退出当前 Python 虚拟环境。
```

导出 CSV 检测结果：

```bash
source .venv/bin/activate # 激活当前项目的 Python 虚拟环境。
python 14_save_detections_csv.py # 将检测结果保存为 CSV 表格。
deactivate # 退出当前 Python 虚拟环境。
```

## 视频检测

生成测试视频：

```bash
source .venv/bin/activate # 激活当前项目的 Python 虚拟环境。
python 16_generate_test_video.py # 使用测试图片生成一个简单视频。
deactivate # 退出当前 Python 虚拟环境。
```

普通视频检测：

```bash
source .venv/bin/activate # 激活当前项目的 Python 虚拟环境。
python 17_detect_video.py # 对 videos/bus_demo.avi 执行视频检测。
deactivate # 退出当前 Python 虚拟环境。
```

流式视频检测：

```bash
source .venv/bin/activate # 激活当前项目的 Python 虚拟环境。
python 18_detect_video_stream.py # 使用 stream=True 逐帧返回 YOLO 检测结果。
deactivate # 退出当前 Python 虚拟环境。
```

## ROS 图像话题接入

加载 ROS 与 Python 环境：

```bash
./19_setup_ros_python_env.sh # 加载 ROS Noetic 环境并验证 rospy、sensor_msgs 与 YOLO 相关依赖。
```

测试 ROS 图像发布和订阅：

```bash
./22_test_ros_image_pipeline.sh # 启动 roscore、图像发布节点和图像订阅节点完成闭环测试。
```

测试 ROS 图像进入 YOLO：

```bash
./24_test_ros_yolo_pipeline.sh # 将 ROS Image 话题输入 YOLO 节点并输出检测统计。
```

测试 YOLO JSON 话题：

```bash
./26_test_ros_yolo_json_topic.sh # 将 YOLO 检测结果整理成 JSON 字符串并发布到 ROS 话题。
```

测试完整 JSON 订阅链路：

```bash
./28_test_full_ros_json_pipeline.sh # 发布图像、YOLO 检测、JSON 订阅解析三个 ROS 节点串联测试。
```

## Gazebo 仿真验证

查找 Gazebo 图像话题：

```bash
./31_test_gazebo_image_topics.sh # 启动 Gazebo 相机世界并查找 sensor_msgs/Image 类型话题。
```

测试 Gazebo 图像进入 YOLO：

```bash
./32_test_gazebo_yolo_pipeline.sh # 将 /sim_camera/image_raw 输入 YOLO 并输出检测结果。
```

保存 Gazebo 相机帧：

```bash
./34_test_save_gazebo_camera_frame.sh # 从 Gazebo 相机话题保存一帧原始图像。
```

测试带框图像发布：

```bash
./39_test_gazebo_annotated_image_topic.sh # 从 Gazebo 图像检测目标并保存 YOLO 带框图像。
```

成功后可以查看：

```text
outputs/gazebo_annotated_image.jpg # Gazebo 相机画面经过 YOLO 检测后的带框图片。
```

## 关键 ROS 话题

| 话题名 | 消息类型 | 作用 |
| --- | --- | --- |
| `/sim_camera/image_raw` | `sensor_msgs/Image` | Gazebo 相机发布的原始图像 |
| `/yolo_course/detections` | `std_msgs/String` | YOLO 检测结果 JSON 字符串 |
| `/yolo_course/annotated_image` | `sensor_msgs/Image` | 已画好检测框的图像 |

## 检测结果 JSON 示例

```json
{
  "frame_id": "sim_camera",
  "stamp": 1720000000.0,
  "detections": [
    {
      "class_id": 5,
      "class_name": "bus",
      "confidence": 0.86,
      "xyxy": [120.0, 80.0, 430.0, 310.0]
    }
  ]
}
```


## 学习顺序建议

1. 先运行 `01` 到 `10`，确认最小 YOLO 图片检测可用。
2. 再运行 `11` 到 `15`，理解预处理、检测框和结果保存。
3. 再运行 `16` 到 `18`，理解视频和流式推理。
4. 再运行 `19` 到 `28`，理解 ROS 图像话题与 JSON 检测结果。
5. 最后运行 `29` 到 `39`，完成 Gazebo 仿真相机验证。

## 课程目标

完成本项目后，应能理解并实现：

- YOLO 模型如何加载和推理。
- 图片如何变成模型输入张量。
- 检测框坐标、类别、置信度如何读取。
- 视频为什么可以看作连续图片帧。
- ROS 图像话题如何进入 YOLO。
- YOLO 检测结果如何通过 ROS 话题发布。
- Gazebo 仿真相机如何用于视觉算法验证。
