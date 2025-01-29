FROM tensorflow/tensorflow:latest-gpu

WORKDIR /tf-neural

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y git

# Install Graphviz at the system level
RUN apt-get update && apt-get install -y graphviz

# Install Python package for Graphviz
RUN pip install graphviz

EXPOSE 8888

ENTRYPOINT [ "jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser" ]
