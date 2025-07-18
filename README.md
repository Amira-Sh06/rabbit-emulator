# rabbit-emulator
This repository contains a simplified implementation of a messaging system, simulating interaction between various business systems (CRM, 1C, DMS) using a message queue concept similar to RabbitMQ. The system demonstrates how different components can publish messages to queues and consume them, reacting to specific events and transferring data (in this case, PDF files) between each other.

**Project Structure**
The project consists of five main files, each performing its specific role:

rabbitmq.py: Emulates the functionality of a message broker.
message_utilits.py: Provides utilities for creating and decoding messages containing PDF data.
crm_logic.py: Represents the logic of the CRM system, initiating the process.
one_c_logic.py: Represents the logic of the 1C system, processing incoming messages.
dms_logic.py: Represents the logic of the Document Management System (DMS), completing the process.

**Core Components**
rabbitmq.py (Message Broker Emulator)
This file defines the RabbitMQ class, which serves as a simplified message broker emulator. It does not connect to a real RabbitMQ server but instead uses an internal queues dictionary (shared across all class instances) to store messages in memory.

queues: A static class dictionary where keys are queue names (e.g., crm_queue, 1c_queue, dms_queue), and values are lists of messages awaiting processing. Dead Letter Queues (DLQ) are also supported for messages that fail processing.
declare_queue(queue_name, dead_letter_queue=None): A method that ensures the existence of the specified queue and, if necessary, its associated DLQ.
publish(queue_name, message): Adds a message to the specified queue.
consume(queue_name, callback, dead_letter_queue=None): Starts an infinite loop for consuming messages from the specified queue. Each received message is passed to a callback function for processing. If an exception occurs during processing, the message is moved to the DLQ, if specified.
close(): In this emulation, this method simply prints a message indicating the session is closed.
message_utilits.py (Message Utilities)
This module contains functions for working with the message format used in the system:
create_pdf_msg(event, sender, receiver, filepath): Creates a JSON string message. It includes the event type, sender, receiver, as well as the Base64-encoded content of a PDF file, and the filename. The PDF file is read from the specified filepath.
decode_pdf_msg(body, save_dir="pdfs/restored"): Decodes a JSON string message back into a Python dictionary. It extracts the encoded PDF data, decodes it, saves the PDF file to the specified directory (pdfs/restored/), and then returns the message dictionary.

**Business System Logic**
The three files (crm_logic.py, one_c_logic.py, dms_logic.py) represent separate "services" or "modules," each with its own logic for interacting via message queues.

crm_logic.py (Initiator)
Role: Initiates the invoice creation process.

Actions:

Creates an "invoice.created" message with "crm" as sender and "1c" as receiver, attaching sample.pdf.
Publishes this message to the 1c_queue.
Then starts consuming messages from the crm_queue, awaiting responses.

one_c_logic.py (Invoice Processor)
Role: Processes incoming invoices and, if successful, approves them.

Actions:

Continuously consumes messages from the 1c_queue.
Upon receiving a message with the "invoice.created" event:
Prints information about the received message.
Creates a new "invoice.approved" message with "1c" as sender and "dms" as receiver, again attaching sample.pdf.
Publishes this message to the dms_queue.

dms_logic.py (Document Archiver)
Role: Processes approved invoices and initiates contract archiving.

Actions:

Continuously consumes messages from the dms_queue.
Upon receiving a message with the "invoice.approved" event:
Prints information about the received message.
Creates a new "contract.archived" message with "dms" as sender and "crm" as receiver, attaching sample.pdf.
Publishes this message to the crm_queue.

**Overall Message Flow (Hypothetical Scenario)**
CRM (crm_logic.py) creates an "invoice.created" message and sends it to 1c_queue.
1C (one_c_logic.py) receives the "invoice.created" message from 1c_queue.
1C processes the invoice and sends an "invoice.approved" message to dms_queue.
DMS (dms_logic.py) receives the "invoice.approved" message from dms_queue.
DMS archives the contract and sends a "contract.archived" message back to crm_queue.
CRM receives the "contract.archived" confirmation from crm_queue, completing the cycle.
