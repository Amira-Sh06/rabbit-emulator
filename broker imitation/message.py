import base64
import os
import json

def create_pdf_msg(event, sender, receiver, filepath):
    with open(filepath, "rb") as f:
        encoded = base64.b64encode(f.read().decode('utf-8'))
        return json.dumps({
            "event": event,
            "from": sender,
            "to": receiver,
            "pdf_data": filepath
        })
    
def decode_pdf_msg(body, save_dir = "pdfs/restored"):
    msg = json.loads(body)
    os.makedirs("pdfs", exist_ok=True)
    output_path = f"{save_dir}{msg['from']}{msg['filename']}"
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(msg["pdf_data"]))
    print(f"Saved PDF to {output_path}")
    return msg 