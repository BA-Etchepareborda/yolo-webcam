import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from ultralytics import YOLO

class YoloNode(Node):
    def __init__(self):
        # Nombramos el nodo
        super().__init__('yolo_detector')
        
        # Creamos el publicador en el tópico '/vision/detections'
        self.publisher_ = self.create_publisher(Image, '/vision/detections', 10)
        
        # Un timer que llame a la función callback 10 veces por segundo (0.1s)
        self.timer = self.create_timer(0.1, self.timer_callback) 
        
        # Inicializamos hardware y modelo
        self.cap = cv2.VideoCapture(0)
        self.model = YOLO('yolov8n.pt')
        self.bridge = CvBridge()
        
        self.get_logger().info("Nodo YOLO inicializado y publicando en /vision/detections")

    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            # 1. Hacemos la inferencia
            resultados = self.model(frame, stream=True, verbose=False)
            
            # 2. Obtenemos el frame pintado
            for r in resultados:
                frame_anotado = r.plot()
            
            # 3. Traducimos de OpenCV a ROS y publicamos
            msg = self.bridge.cv2_to_imgmsg(frame_anotado, encoding="bgr8")
            self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    nodo = YoloNode()
    
    try:
        # spin() mantiene el nodo vivo y escuchando eventos/timers
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        pass
    finally:
        # Limpieza cuando apagamos el nodo con Ctrl+C
        nodo.cap.release()
        nodo.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()