# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 8501 for the Streamlit app
EXPOSE 8501

# Set the entry point and command for the container
ENTRYPOINT ["streamlit", "run"]
CMD ["src/app.py"]