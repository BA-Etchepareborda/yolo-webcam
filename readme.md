# 🤖 ROS 2 YOLOv8 Object Detection Node (Dockerized)

Real-time object detection pipeline using **YOLOv8** and **ROS 2 Humble**, entirely encapsulated within a Docker container. 

This project captures a live webcam feed, performs bounding-box inference using Ultralytics YOLOv8 Nano, and translates the OpenCV frames into `sensor_msgs/Image` messages. The annotated video stream is published to a ROS 2 topic, allowing other nodes in a robotics stack to consume the visual data without dealing with ML dependencies.

## 🛠️ Tech Stack
* **Framework:** ROS 2 Humble
* **AI Model:** Ultralytics YOLOv8 (`yolov8n.pt`)
* **Vision:** OpenCV, `cv_bridge`
* **Infrastructure:** Docker (for environment isolation)

## 📋 Prerequisites
* Linux environment (tested on Ubuntu)
* Docker installed
* A connected webcam (mapped to `/dev/video0`)

## 🚀 Build Instructions

Clone the repository and build the Docker image. This will download the official ROS 2 Humble base image and install the necessary Python and ROS dependencies.

```bash
git clone [https://github.com/tu-usuario/cv-webcam-yolo.git](https://github.com/tu-usuario/cv-webcam-yolo.git)
cd cv-webcam-yolo
docker build -t ros-yolo-node .

💻 Usage
To run the complete pipeline, we need to spin up the publisher node and then attach a visualizer to the ROS network.

1. Start the YOLO Publisher Node
First, allow local Docker containers to access your X11 display server (needed for GUI tools in the next step):

xhost +local:

Then, run the container, passing the webcam device and starting the ROS 2 node:

docker run -it --rm \
    --name mi_robot \
    --device=/dev/video0 \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e DISPLAY=$DISPLAY \
    ros-yolo-node

The node will automatically download the YOLO weights on the first run and start publishing to /vision/detections.

2. Visualize the ROS Topic
Open a new terminal session and execute the rqt_image_view tool inside the running container to see the real-time inference:

docker exec -it mi_robot bash -c "source /opt/ros/humble/setup.bash && ros2 run rqt_image_view rqt_image_view"

Select /vision/detections from the top-left dropdown menu in the GUI.

🔮 Future Work
Integration with Safe SLAM navigation stacks for dynamic obstacle avoidance.

Export the PyTorch model to TensorRT for C++ API inference and GPU optimization.

Incorporate 3D tracking (e.g., BoT-SORT) to assign unique IDs to detected dynamic obstacles.