FROM python:3.10

WORKDIR /app

COPY ./Blogapp /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y tzdata

RUN cd Blogapp

# Install Python packages using pip
RUN pip install -r requirements.txt


# Command to run when the container starts
ENTRYPOINT ["python3", "manage.py"]

CMD ["runserver", "0.0.0.0:8000"]