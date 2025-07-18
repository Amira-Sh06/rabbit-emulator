import sys
print("sys.path:", sys.path)

from rabbitmq import RabbitMQ
from message_utilits import create_pdf_msg, decode_pdf_msg

def one_c_logic():
    def callback(body):
        msg = decode_pdf_msg(body)
        print(f"1C received: {msg['event']} from {msg['from']}")
        if msg['event'] == "invoice.created":
            response = create_pdf_msg("invoice.approved", "1c", "dms", "pdfs/sample.pdf")
            producer = RabbitMQ()
            producer.publish("dms_queue", response)
            producer.close()

    consumer = RabbitMQ()
    consumer.consume("1c_queue", callback, dead_letter_queue="1c_dlq")
    consumer.close()

if __name__ == "_main_":
    one_c_logic()