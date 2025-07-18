import time

class RabbitMQ:
    queues = {
        "crm_queue": [],
        "1c_queue": [],
        "dms_queue": [],
        "crm_dlq": [],
        "1c_dlq": [],
        "dms_dlq": []
    }

    def _init_(self):
        self.connected = True

    def declare_queue(self, queue_name, dead_letter_queue=None):
        if queue_name not in self.queues:
            self.queues[queue_name] = []
        if dead_letter_queue and dead_letter_queue not in self.queues:
            self.queues[dead_letter_queue] = []

    def publish(self, queue_name, message):
        self.declare_queue(queue_name)
        self.queues[queue_name].append(message)
        print(f"Message sent to queue '{queue_name}'")

    def consume(self, queue_name, callback, dead_letter_queue=None):
        self.declare_queue(queue_name, dead_letter_queue)
        print(f"Consuming messages from '{queue_name}'...")

        while True:
            if self.queues[queue_name]:
                message = self.queues[queue_name].pop(0)
                try:
                    callback(None, type('MockMethod' (object,), {'delivery_tag': 1}), None, message)
                except Exception as e:
                    print(f"Ошибка обработки: {e}")
                    if dead_letter_queue:
                        self.queues[dead_letter_queue].append(message)
                    else:
                        time.sleep(3)

    def close(self):
        print("Emulator session closed")