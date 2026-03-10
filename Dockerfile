# 1. Usamos la imagen oficial de ROS 2 Humble (la versión "base" es más liviana)
FROM ros:humble-ros-base

# 2. Instalamos dependencias del sistema, pip, y los paquetes clave de ROS 2 para visión
RUN apt-get update && apt-get install -y \
    python3-pip \
    libgl1 \
    libglib2.0-0 \
    ros-humble-cv-bridge \
    ros-humble-sensor-msgs \
    && rm -rf /var/lib/apt/lists/*

# 3. Definimos la carpeta de trabajo
WORKDIR /app

# 4. Copiamos el requirements e instalamos YOLO
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 5. Copiamos tu nodo (main.py)
COPY . .

# 6. El truco de ROS: Siempre hay que hacer "source" del entorno antes de correr algo.
# Usamos ENTRYPOINT para inyectar el source antes de ejecutar tu script de Python.
ENTRYPOINT ["/bin/bash", "-c", "source /opt/ros/humble/setup.bash && exec python3 main.py"]