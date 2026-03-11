# Use the official Node.js 22 image as the base image
FROM node:22-alpine

# Set the working directory to /app
WORKDIR /opt/tricorder/frontend

# Copy the package.json file into the container
COPY package*.json ./

# Install the dependencies
RUN npm install

RUN npm install -g @angular/cli

# Copy the application code into the container
COPY . .

ARG TRICORDER_BACKEND_IP
ARG TRICORDER_BACKEND_PORT
RUN sed -i "s|TRICORDER_BACKEND_IP|$TRICORDER_BACKEND_IP|g" /opt/tricorder/frontend/src/environments/environment*.ts \
 && sed -i "s|TRICORDER_BACKEND_PORT|$TRICORDER_BACKEND_PORT|g" /opt/tricorder/frontend/src/environments/environment*.ts

# Expose the port that the application will listen on
EXPOSE 4200

# Run the application when the container starts
CMD ["ng", "serve", "--configuration=docker", "--host", "0.0.0.0"]