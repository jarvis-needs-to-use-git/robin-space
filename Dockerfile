FROM condaforge/mambaforge:latest

# Set working directory
WORKDIR /app

# Copy environment file
COPY environment.yml .

# Install dependencies using mamba (much faster than conda)
RUN mamba env create -f environment.yml && \
    mamba clean --all -f -y

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "robin-space-env", "/bin/bash", "-c"]

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run the application
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "robin-space-env", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
