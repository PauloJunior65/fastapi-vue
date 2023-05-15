# Start from the official Python base image.
FROM python:3.9

# Set the current working directory to /code.
WORKDIR /code

# Copy the ./ directory inside the /code directory.
COPY ./ /code

# Install the package dependencies in the requirements file.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Set the command to run the uvicorn server.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]