import sys
print("sys.path:", sys.path)

from rabbitmq import RabbitMQ
from message_utilits import create_pdf_msg, decode_pdf_msg

def dms_logic():
    def callback(body):
        msg = decode_pdf_msg(body)
        print(f"DMS received: {msg['event']} from {msg['from']}")
        if msg['event'] == "invoice.approved":
            response = create_pdf_msg("contract.archived", "dms", "crm", "pdfs/sample.pdf")
            producer = RabbitMQ()
            producer.publish("crm_queue", response)
            producer.close()

    consumer = RabbitMQ()
    consumer.consume("dms_queue", callback, dead_letter_queue="dms_dlq")
    consumer.close()

if __name__ == "_main_":
    dms_logic()