import json
import base64
import os

# Load the Jupyter Notebook JSON file

notebook_path = r'creating-ML-pipeline-components\2. Beginning of creating a pipeline\2.1 first steps to creating a pipeline.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook_json = json.load(f)

# Traverse the JSON structure to find base64-encoded image strings in attachments
image_count = 9
for cell in notebook_json['cells']:
    if 'attachments' in cell:
        for attachment_name, attachment_data in cell['attachments'].items():
            for mime_type, data in attachment_data.items():
                if mime_type == 'image/png':
                    # Decode the base64 string to binary data
                    image_data = base64.b64decode(data)
                    image_name = f"image_{image_count}.png"
                    # Save the binary data to an image file
                    with open(image_name, "wb") as file:
                        file.write(image_data)

                    image_count += 1