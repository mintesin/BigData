FROM python:3.11-slim-bullseye

# Install OpenJDK 17 and system dependencies
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME for OpenJDK 17
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Set working directory
WORKDIR /bigdata

# Copy all project files into container
COPY . .

# Install PySpark (compatible with Java 17)
RUN pip install --timeout=120 pyspark

# Default command
CMD ["python", "DataPreprocessor.py"]
