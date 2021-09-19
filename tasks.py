from celery import Celery, bootsteps
from kombu.common import QoS

app = Celery('tasks', broker='amqp://guest:guest@localhost:5672/')
app.config_from_object('celeryconfig')


class NoChannelGlobalQoS(bootsteps.StartStopStep):
    requires = {'celery.worker.consumer.tasks:Tasks'}

    def start(self, c):
        qos_global = False

        # This is where we enforce per-client QoS, the rest is just copypaste from celery
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
