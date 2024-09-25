# Base stage for Node.js
FROM node:18-alpine AS node_builder

# Set the working directory for Node.js
WORKDIR /usr/src/app

# Copy package.json and package-lock.json for Node.js dependencies
COPY package*.json ./

# Install Node.js dependencies
RUN npm install --production

# Copy all files into the image for the Node.js app
COPY . .

# Build the Node.js app if necessary (uncomment if needed)
# RUN npm run build

# Base stage for Python
FROM python:3.11-slim AS python_builder

# Set the working directory for Python
WORKDIR /usr/src/app

# Copy Python-related files (requirements.txt or similar)
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port for the app (adjust if necessary)
EXPOSE 3000

# Command to run both the Node.js and Python applications (adjust accordingly)
CMD [ "sh", "-c", "npm start & python app.py" ]
