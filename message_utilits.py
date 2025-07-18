import base64
import os
import json

def create_pdf_msg(event, sender, receiver, filepath):
    """
    Creates a JSON message containing information about the event, 
    sender, recipient, encoded PDF data and file name.
    """
    with open(filepath, "rb") as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')
        return json.dumps({
            "event": event,
            "from": sender,
            "to": receiver,
            "pdf_data": encoded,
            "filename": os.path.basename(filepath)
        })

def decode_pdf_msg(body, save_dir="pdfs/restored"):
    """
    Decodes the JSON message, extracts the PDF data, 
    saves the PDF file, and returns the message dictionary.
    """
    msg = json.loads(body)
    full_save_path = os.path.join(os.getcwd(), save_dir)
    os.makedirs(full_save_path, exist_ok=True) # Create a directory if there is no directory

    output_path = os.path.join(full_save_path, f"{msg['from']}_{msg['filename']}")
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(msg["pdf_data"]))
    print(f"Saved PDF to {output_path}")
    return msg
