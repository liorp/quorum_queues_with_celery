from kombu import Queue

task_queues = [Queue(name="add_queue", queue_arguments={"x-queue-type": "quorum"})]

task_routes = {
    'tasks.add': 'add_queue',
}