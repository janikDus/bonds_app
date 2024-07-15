FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Copy project files
COPY . /code/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# For running our application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]