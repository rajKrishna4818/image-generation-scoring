# Use the official Python image from the Docker Hub
FROM python:3.13.1-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8501

# Command to run the Streamlit application
CMD ["streamlit", "run", "frontend_ui.py"]