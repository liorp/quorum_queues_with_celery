# Description

A simple celery app that supports quorum queues.

# Usage

First make sure you have an instance of rabbitmq running, e.g `docker run -d --hostname my-rabbit --name some-rabbit -p 8080:15672 -p 5672:5672 rabbitmq:3-management`.  
Run `main.py` to push messages into the queue.  
Run workers with `celery -A tasks worker --loglevel=INFO`.
