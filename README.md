# Docker

## Clone the repository

1. Clone this repository to your **WSL2** environment:
   ```bash
   git clone https://github.com/Ssurajbalii/Tensorflow-gpu-.git
   ```

2. Change to the project directory:
   ```bash
   cd Tensorflow-gpu-
   ```

## Build and Run the Docker container

### Requirements
Ensure you have the following installed:
- Docker
- Docker Compose
- NVIDIA Docker (if using GPU)
- TensorFlow (inside the container)

### Using Docker Compose
This repository includes a `docker-compose.yml` file that simplifies the process of building and running the Docker container.

1. **Build and start** the Docker container:
   ```bash
   docker-compose up --build
   ```

2. If you just want to start the container **without rebuilding** it, you can run:
   ```bash
   docker-compose up
   ```

This will start the container, and **TensorFlow will use the GPU** if available.

### Using GPU with TensorFlow
Make sure your system has a compatible **NVIDIA GPU** and that Docker is configured to use the GPU. If you're using **WSL2 with NVIDIA GPU support**, the container should automatically use the GPU.

#### Note:
If you don’t have a GPU or don’t wish to use it, you can modify the `docker-compose.yml` to disable GPU support. Please refer to [TensorFlow’s official Docker guides](https://www.tensorflow.org/install/docker) for further details on setting up GPU support if needed.
