FROM condaforge/miniforge3:latest

# Set working directory
WORKDIR /app

# 1. Install MEEP and core system dependencies (The Heavy Lift)
# We do this FIRST and ALONE to minimize solver memory usage.
RUN mamba create -n robin-space-env -c conda-forge pymeep python=3.10 -y && \
    mamba clean --all -f -y

# 2. Activate environment for subsequent commands
SHELL ["conda", "run", "-n", "robin-space-env", "/bin/bash", "-c"]

# 3. Install Python UI dependencies via PIP (Much lower memory usage than Conda)
# We explicitly avoid Conda for these to prevent re-triggering the heavy solver.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run the application
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "robin-space-env", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
