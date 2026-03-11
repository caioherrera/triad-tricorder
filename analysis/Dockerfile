# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /opt/tricorder/analysis

# Set up the zip file for damicore-python3
COPY damicore-python3-main.zip .

# Run bootstrap.sh script
COPY bootstrap.sh .
RUN chmod +x bootstrap.sh && ./bootstrap.sh

# Copy the requirements files into the container
COPY requirements.txt .

# Install the dependencies
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

# Copy the DAMICORE requirements file into the container
COPY damicore_requirements.txt .

# Install the DAMICORE dependencies
RUN pip3 install --no-cache-dir -r damicore_requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the Flask app will run on
EXPOSE 5200

ENV FLASK_APP=app
ENV FLASK_RUN_PORT=5200
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=1

# Run the Flask app
CMD ["python3", "-m" , "flask", "run"]