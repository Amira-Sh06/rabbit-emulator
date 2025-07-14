from rabbitmq import RabbitMQ
from message import create_pdf_msg, decode_pdf_msg

def dms_logic():
    def callback(ch, method, properties, body):
        msg = decode_pdf_msg(body)
        print(f"DMS received: {msg['event']} from {msg['from']}")

        if msg['event'] == "invoice.approved":
            response = create_pdf_msg("contract.archived", "dms", "crm", "pdfs/sample.pdf")
            producer = RabbitMQ()
            producer.publish("crm_queue", response)
            producer.close()
        ch.basic_ack(delivery_tag=method.delivery_tag)

    consumer = RabbitMQ()
    consumer.consume("dms_queue", callback)

if __name__ == "_main_":
    dms_logic()