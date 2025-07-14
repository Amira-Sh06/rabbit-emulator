from rabbitmq import RabbitMQ
from message import create_pdf_msg, decode_pdf_msg

def crm_logic():
    rabbit = RabbitMQ()
    msg = create_pdf_msg("invoice.created", "crm", "1c", "pdfs/sample.pdf")
    rabbit.publish("1c_queue", msg)
    rabbit.close()

    def callback(ch, method, properties, body):
        msg = decode_pdf_msg(body)
        print(f"CRM received: {msg['event']} from {msg['from']}")
        ch.basic_ack(delivery_tag = method.delivery_tag)

    consumer = RabbitMQ()
    consumer.consume("crm_queue", callback)

if __name__ == "_main_":
    crm_logic()