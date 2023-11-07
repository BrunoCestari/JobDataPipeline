# Use the official Selenium standalone Chrome image as the base image
FROM selenium/standalone-chrome:latest

# Switch to root user to perform system-level installations
USER root

# Install Xvfb and other dependencies for running Chrome in headless mode
RUN apt-get update && apt-get install -y python python3-pip xvfb

# Set the DISPLAY environment variable for Xvfb
ENV DISPLAY=:99

# Create a directory for your Python scripts and set it as the working directory
WORKDIR /tmp

# Copy your Python scripts and requirements into the container
COPY Bot.py webscrape.py requirements.txt ./

# Install Python dependencies
RUN pip3 install -r requirements.txt


RUN echo "Webscrape container ready to extract data."


CMD ["sleep", "infinity"]
