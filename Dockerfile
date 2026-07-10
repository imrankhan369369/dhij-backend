FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /code

# Copy only requirements first - this is a caching trick.
# Docker rebuilds layers from the first line that changed.
# If your code changes but requirements.txt doesn't, this layer
# stays cached and Docker skips reinstalling everything.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of your actual application code
COPY . .

# Tell Docker this container listens on port 8000
EXPOSE 8000

# The command that runs when the container starts
# --host 0.0.0.0 is required so the app is reachable from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
