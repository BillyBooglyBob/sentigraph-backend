FROM python:3.12-slim

WORKDIR /usr/src/sentigraph_backend

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install netcat for the entrypoint file
# This is used to wait for the database to be ready
# before starting the Django server
RUN apt-get update && apt-get install -y netcat-openbsd

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Execute the entrypoint file
COPY ./entrypoint.sh .

# Copy the rest of the application code
COPY . .

RUN sed -i 's/\r$//g' /usr/src/sentigraph_backend/entrypoint.sh
RUN chmod +x /usr/src/sentigraph_backend/entrypoint.sh

ENTRYPOINT [ "/usr/src/sentigraph_backend/entrypoint.sh" ]