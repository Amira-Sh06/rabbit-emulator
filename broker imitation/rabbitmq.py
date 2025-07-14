import pika
import os

class RabbitMQ:
    def __init__(self):
        self.user = os.getenv('RABBITMQ_USER', 'guest')
        self.password = os.getenv('RABBITMQ_PASSWORD', 'guest')
        self.host = os.getenv('RABBITMQ_HOST', 'localost')
        self.port = int(os.getenv('RABBITMQ_PORT', 5672))
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()

    def declare_queue(self, queue_name, dead_letter_queue):
        args = {}
        if dead_letter_queue:
            args['x-dead-letter-exchange'] = ''
            args['x-dead-letter-routing-key'] = dead_letter_queue
        self.channel.queue_declare(queue=queue_name, durable=True, arguments=args)

    def consume(self, queue_name, callback, dead_letter_queue = None):
        self.declare_queue(queue_name, dead_letter_queue)
        def wrapped_callback(ch, method, properties, body):
            try:
                callback(ch, method, properties, body)
            except Exception as e:
                print(f"[\u26a0\ufe0f] Error processing message: {e}. Sending to DLQ.")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                
        if not self.channel:   
            raise Exception("Connection is not established.")
        self.channel.basic_consume(queue=queue_name, on_message_callback=wrapped_callback, auto_ack=False)
        self.channel.start_consuming()
        try:
            self.channel.start_consuming()
        except:
            print("Consumption is stopped by user")

    def publish(self, queue_name, message):
        self.declare_queue(queue_name)
        if not self.channel:
            raise Exception("Connection is not established.")
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_publish(exchange='',
                                   routing_key=queue_name,
                                   body=message,
                                   properties=pika.BasicProperties(
                                       delivery_mode=2,  # make message persistent
                                   ))
        print(f"Sent message to queue {queue_name}: {message}")