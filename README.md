# rabbit-emulator
This repository contains a simplified implementation of a messaging system, simulating interaction between various business systems (CRM, 1C, DMS) using a message queue concept similar to RabbitMQ. The system demonstrates how different components can publish messages to queues and consume them, reacting to specific events and transferring data (in this case, PDF files) between each other. This updated version runs all components within a single Python process, leveraging threading for concurrent execution.

**Project Structure**
The project consists of six main files, each performing its specific role:
rabbitmq.py: Emulates the functionality of a message broker.
message_utilits.py: Provides utilities for creating and decoding messages, including Base64 encoding/decoding of PDF data.
crm_.py: Represents the logic of the CRM system.
one_c.py: Represents the logic of the 1C system.
dms.py: Represents the logic of the Document Management System (DMS).
main.py: The central entry point that orchestrates the execution of all business system logics concurrently using Python threads.

**Core Components**
<ins>rabbitmq.py (Message Broker Emulator)</ins>
This file defines the RabbitMQ class, which serves as a simplified message broker emulator. It does not connect to a real RabbitMQ server but instead uses an internal queues dictionary (shared across all class instances within the same process) to store messages in memory.

queues: A static class dictionary where keys are queue names (e.g., crm_queue, 1c_queue, dms_queue), and values are lists of messages awaiting processing. Dead Letter Queues (DLQ) are also supported for messages that fail processing.

declare_queue(queue_name, dead_letter_queue=None): A method that ensures the existence of the specified queue and, if necessary, its associated DLQ.

publish(queue_name, message): Adds a message to the specified queue.

consume(queue_name, callback, dead_letter_queue=None): Starts an infinite loop for consuming messages from the specified queue in a separate thread. Each received message is passed to a callback function for processing. If an exception occurs during processing, the message is moved to the DLQ, if specified. This method is non-blocking, allowing multiple consumers to run concurrently.

close(): Signals all consumer threads to stop gracefully.

<ins>message_utilits.py (Message Utilities)</ins>
This module contains functions for working with the message format used in the system:

create_pdf_msg(event, sender, receiver, filepath): Creates a JSON string message. It includes the event type, sender, receiver, as well as the Base64-encoded content of a PDF file, and the filename. The PDF file is read from the specified filepath.

decode_pdf_msg(body, save_dir="pdfs/restored"): Decodes a JSON string message back into a Python dictionary. It extracts the encoded PDF data, decodes it, saves the PDF file to the specified directory (pdfs/restored/), and then returns the message dictionary.

**Business System Logic Files**
The three files (crm.py, one_c.py, dms.py) define functions that encapsulate the logic for each business system. Each function creates its own RabbitMQ instance (which shares the global queues dictionary) and sets up its publishing and consuming behaviors.

<ins>crm.py (Initiator)</ins>
Role: Initiates the invoice creation process.

Actions:
Creates an "invoice.created" message with "crm" as sender and "1c" as receiver, attaching sample.pdf.
Publishes this message to the 1c_queue.
Then starts consuming messages from the crm_queue, awaiting responses.

<ins>one_c.py (Invoice Processor)</ins>
Role: Processes incoming invoices and, if successful, approves them.

Actions:
Continuously consumes messages from the 1c_queue.
Upon receiving a message with the "invoice.created" event:
Prints information about the received message.
Creates a new "invoice.approved" message with "1c" as sender and "dms" as receiver, again attaching sample.pdf.
Publishes this message to the dms_queue.

<ins>dms.py (Document Archiver)</ins>
Role: Processes approved invoices and initiates contract archiving.

Actions:
Continuously consumes messages from the dms_queue.
Upon receiving a message with the "invoice.approved" event:
Prints information about the received message.
Creates a new "contract.archived" message with "dms" as sender and "crm" as receiver, attaching sample.pdf.
Publishes this message to the crm_queue.

main.py (System Orchestrator)
This new file serves as the central entry point for the entire messaging system.
Role: Coordinates the simultaneous execution of all business system logics.

Actions:

Imports the logic functions from crm.py, one_c.py, and dms.py.
Launches each of these logic functions in a separate threading.Thread. This ensures that all components run concurrently within the same Python process, allowing them to share the RabbitMQ.queues static dictionary and thus communicate effectively.
Keeps the main thread alive to allow the consumer threads to operate.
Handles KeyboardInterrupt (Ctrl+C) to gracefully signal all consumer threads to stop before exiting.

**Overall Message Flow (Concurrent Scenario)**
The main.py script starts all three business logic functions (crm, one_c, dms) as concurrent threads.

CRM (crm thread) immediately creates an "invoice.created" message and publishes it to 1c_queue. It then starts consuming from crm_queue.
1C (one_c thread), which is already consuming from 1c_queue, receives the "invoice.created" message.
1C processes the invoice, saves the received PDF, and publishes an "invoice.approved" message to dms_queue.
DMS (dms thread), which is already consuming from dms_queue, receives the "invoice.approved" message.
DMS archives the contract, saves the received PDF, and publishes a "contract.archived" message back to crm_queue.
CRM (crm thread) receives the "contract.archived" confirmation from crm_queue, saves the final PDF, and completes its part of the cycle.
All messages and PDF data are passed successfully through the emulated queues within the single running process.
