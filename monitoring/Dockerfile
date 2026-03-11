# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /opt/tricorder/monitor

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

# Preparing the environment to run Decision_Tree application
COPY applications/decision_tree/bootstrap.sh decision_tree_bootstrap.sh
COPY applications/decision_tree/requirements.txt decision_tree_requirements.txt

RUN chmod +x decision_tree_bootstrap.sh && ./decision_tree_bootstrap.sh
RUN pip3 install --no-cache-dir -r decision_tree_requirements.txt

# Preparing the environment to run Network_Telemetry application
# RUN mkdir -p applications/network-telemetry
# RUN cd applications/network-telemetry
COPY applications/network_telemetry/bootstrap.sh network_telemetry_bootstrap.sh
RUN chmod +x network_telemetry_bootstrap.sh && ./network_telemetry_bootstrap.sh

# Preparing the environment to run the Java_Sort application
COPY applications/java_sort/bootstrap.sh java_sort_bootstrap.sh
RUN chmod +x java_sort_bootstrap.sh && ./java_sort_bootstrap.sh

# Preparing the environment to run Defects4J
COPY applications/defects4j/bootstrap.sh defects4j_bootstrap.sh
COPY applications/defects4j/setup.json setup.json
COPY applications/defects4j/run.sh run.sh

RUN chmod +x defects4j_bootstrap.sh && ./defects4j_bootstrap.sh

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the Flask app will run on
EXPOSE 5100

ENV FLASK_APP=app
ENV FLASK_RUN_PORT=5100
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=1

# Run the Flask app
CMD ["python3", "-m" , "flask", "run"]