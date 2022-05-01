from celery import Celery, bootsteps
from kombu.common import QoS

app = Celery('tasks', broker='amqp://guest:guest@localhost:5672/')
app.config_from_object('celeryconfig')


class NoChannelGlobalQoS(bootsteps.StartStopStep):
    requires = {'celery.worker.consumer.tasks:Tasks'}  # Required for the step to be run after Tasks has been run

    def start(self, c):
        # In this context, `c` is the consumer (celery worker)
        qos_global = False

        # This is where we enforce per-client QoS, the rest is just copypaste from celery
        # Note that we set to prefetching size to be 0, so the exact value of `c.initial_prefetch_count` is not important
        c.connection.default_channel.basic_qos(
            0, c.initial_prefetch_count, qos_global,
        )

        def set_prefetch_count(prefetch_count):
            return c.task_consumer.qos(
                prefetch_count=prefetch_count,
                apply_global=qos_global,
            )
        c.qos = QoS(set_prefetch_count, c.initial_prefetch_count)


app.steps['consumer'].add(NoChannelGlobalQoS)


@app.task
def add(x, y):
    return x + y
