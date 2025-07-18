from rabbitmq import RabbitMQ
from message_utilits import create_pdf_msg, decode_pdf_msg

def dms_logic():
    """
    Logic for DMS system.
    Consumes messages from dms_queue and publishes to crm_queue.
    """
    consumer = RabbitMQ()
    # Create a single RabbitMQ instance for all operations in this thread

    def callback(body):
        """
        Message Handler for dms
        """
        msg = decode_pdf_msg(body)
        print(f"DMS received: {msg['event']} from {msg['from']}")
        if msg['event'] == "invoice.approved":
            response = create_pdf_msg("contract.archived", "dms", "crm", "pdfs/sample.pdf")
            consumer.publish("crm_queue", response)
            print("DMS published 'contract.archived' to crm_queue.")
            
    consumer_thread = consumer.consume("dms_queue", callback, dead_letter_queue="dms_dlq")
    return consumer, consumer_thread