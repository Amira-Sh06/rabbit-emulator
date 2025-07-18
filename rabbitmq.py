import time
import queue
import threading

class RabbitMQ:
    queues = {
        "crm_queue": [],
        "1c_queue": [],
        "dms_queue": [],
        "crm_dlq": [],
        "1c_dlq": [],
        "dms_dlq": []
    }
    _stop_event = threading.Event()

    def __init__(self):
        self.connected = True

    def declare_queue(self, queue_name, dead_letter_queue=None):
        """
        Declares a queue if it does not already exist.
        Also declares a dead mail queue (DLQ) if specified.
        """
        if queue_name not in self.queues:
            self.queues[queue_name] = []
            print(f"Queue '{queue_name}' declared.")
        if dead_letter_queue and dead_letter_queue not in self.queues:
            self.queues[dead_letter_queue] = []
            print(f"Dead Letter Queue '{dead_letter_queue}' declared.")

    def publish(self, queue_name, message):
        """
        Publishes the message to the specified queue.
        """
        self.declare_queue(queue_name)
        self.queues[queue_name].append(message)
        print(f"Message sent to queue '{queue_name}'")

    def consume_thread_function(self, queue_name, callback, dead_letter_queue):
        """
        Work function for the consumer thread.
        Constantly retrieves messages from the queue and calls callback.
        """
        print(f"Consuming messages from '{queue_name}' in a new thread...")

        while not self._stop_event.is_set():
            if self.queues[queue_name]:
                message = self.queues[queue_name].pop(0)
                try:
                    callback(message)
                except Exception as e:
                    print(f"Processing error: {e}")
                    if dead_letter_queue:
                        self.queues[dead_letter_queue].append(message)
                        print(f"Message moved to DLQ '{dead_letter_queue}'.")

    def consume(self, queue_name, callback, dead_letter_queue=None):
        """
        Starts the consumer for the specified queue in a separate thread.
        """
        self.declare_queue(queue_name, dead_letter_queue)
        consumer_thread = threading.Thread(
            target = self.consume_thread_function,
            args = (queue_name, callback, dead_letter_queue),
            daemon = True)
        consumer_thread.start()
        return consumer_thread

    def close(self):
        self._stop_event.set()
        print("Emulator session closed")