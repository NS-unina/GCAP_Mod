# Base image with ROS Noetic
FROM ros:noetic

# Install dependencies for Flask and ROS
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    ros-noetic-ros-base \
    ros-noetic-mavros \
    ros-noetic-mavros-msgs

# Install Flask
RUN pip3 install flask

# Source the ROS environment
RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc

# Copy the Flask application code to the container
COPY app.py /app/app.py

# Set the working directory
WORKDIR /app

 CMD /bin/bash -c " roscore "
# CMD /bin/bash -c " roscore & python3 app.py"



