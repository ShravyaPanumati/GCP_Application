# Use official Python runtime as a parent image
FROM python:3.12-slim
# Set environment variables to ensure Streamlit runs properly
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set the working directory in the container
WORKDIR /app
# Copy the current directory contents into the container
COPY . /app
# Install system dependencies for pyodbc (for SQL Server)
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    build-essential \
    curl \
    && apt-get clean
# Install the ODBC Driver 17 for SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get clean

COPY strategic-reef-435523-j1-9400b4c6c369.json /app/service-account-file.json
# Install any needed packages specified in requirements.txtdock
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py ./

# Expose the port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
