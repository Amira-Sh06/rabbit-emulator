from rabbitmq import RabbitMQ
from message_utilits import create_pdf_msg, decode_pdf_msg
import time    

def one_c_logic():
    """
    Logic for 1C system.
    Consumes messages from 1c_queue and publishes to dms_queue.
    """
    consumer = RabbitMQ()
    def callback(body):
        """
        Message Handler fоr 1C.
        """
        msg = decode_pdf_msg(body)
        print(f"1C received: {msg['event']} from {msg['from']}")
        if msg['event'] == "invoice.created":
            response = create_pdf_msg("invoice.approved", "1c", "dms", "pdfs/sample.pdf")
            consumer.publish("dms_queue", response)
            print("1C published 'invoice.approved' to dms_queue.")

    consumer_thread = consumer.consume("1c_queue", callback, dead_letter_queue="1c_dlq")
    return consumer, consumer_thread