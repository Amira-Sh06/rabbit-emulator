import sys
print("sys.path:", sys.path)

from rabbitmq import RabbitMQ
from message_utilits import create_pdf_msg, decode_pdf_msg

def crm_logic():
    rabbit = RabbitMQ()
    msg = create_pdf_msg("invoice.created", "crm", "1c", "pdfs/sample.pdf")
    rabbit.publish("1c_queue", msg)

    def callback(body):
        msg = decode_pdf_msg(body)
        print(f"CRM received: {msg['event']} from {msg['from']}")

    rabbit.consume("crm_queue", callback, dead_letter_queue="crm_dlq")
    rabbit.close()

if __name__ == "_main_":
    crm_logic()
