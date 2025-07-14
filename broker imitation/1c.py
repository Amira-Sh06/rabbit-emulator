from rabbitmq import RabbitMQ
from message import create_pdf_msg, decode_pdf_msg

def one_c_logic():
    def callback(ch, method, properties, body):
        msg = decode_pdf_msg(body)
        print(f"1C received: {msg['event']} from {msg['from']}")

        if msg['event'] == "invoice.created":
            response = create_pdf_msg("invoice.approved", "1c", "dms", "pdfs/sample.pdf")
            producer = RabbitMQ()
            producer.publish("dms_queue", response)
            producer.close()
        ch.basic_ack(delivery_tag = method.delivery_tag)

    consumer = RabbitMQ()
    consumer.consume("1c_queue", callback)

if __name__ == "_main_":
    one_c_logic()