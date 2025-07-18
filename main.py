import threading
import time
from rabbitmq import RabbitMQ # Для доступа к RabbitMQ._stop_event
from crm import crm_logic
from one_c import one_c_logic
from dms import dms_logic

def run_all_systems():
    """
   Runs all business systems (CRM, 1C, DMS) in separate threads within a single process.
    """
    print("Starting all messaging system components...")

    # Run each logic in a separate thread
    crm_rabbit, crm_thread = crm_logic()
    one_c_consumer, one_c_thread = one_c_logic()
    dms_consumer, dms_thread = dms_logic()

    # Collect all threads to wait for their completion
    all_threads = [crm_thread, one_c_thread, dms_thread]

    print("\nAll systems are running. Press Ctrl+C to stop.")

    try:
        # Keep the main thread alive so that background consumer threads can run.
        # In a real application, this could be the main server or UI logic.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping all messaging system components...")
        # Signal all consumers to stop via a common _stop_event
        RabbitMQ._stop_event.set()
        # Waiting for all the consumer streams to complete
        for t in all_threads:
            t.join(timeout = 5) 
            if t.is_alive():
                print(f"Warning: Thread {t.name} did not terminate gracefully.")
        print("All messaging system components stopped.")

if __name__ == "__main__":
    run_all_systems()

