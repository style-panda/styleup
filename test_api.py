import requests
import base64
import json
import os

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def test_analyze_images():
    # Replace with paths to your test images
    image_paths = [
        "path/to/image1.jpg",
        "path/to/image2.jpg"
    ]
    
    # Check if images exist
    for path in image_paths:
        if not os.path.exists(path):
            print(f"Image not found: {path}")
            return
    
    # Encode images
    encoded_images = [encode_image(path) for path in image_paths]
    
    # Prepare request
    url = "http://localhost:5000/api/analyze-images"
    payload = {
        "images": encoded_images
    }
    
    # Send request
    response = requests.post(url, json=payload)
    
    # Print response
    print(f"Status code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_analyze_images()