from rabbitmq import RabbitMQ
from message_utilits import create_pdf_msg, decode_pdf_msg

def crm_logic():
    """
    Logic for CRM system.
    Initiates the process by publishing a message to 1c_queue, then consumes messages from crm_queue.
    """
    rabbit = RabbitMQ()
    # CRM initiates the process by publishing a message
    msg = create_pdf_msg("invoice.created", "crm", "1c", "pdfs/sample.pdf")
    rabbit.publish("1c_queue", msg)

    def callback(body):
        """
        Message Handler for 1C.
        """
        msg = decode_pdf_msg(body)
        print(f"CRM received: {msg['event']} from {msg['from']}")

    
    consumer_thread = rabbit.consume("crm_queue", callback, dead_letter_queue="crm_dlq")
    return rabbit, consumer_thread
