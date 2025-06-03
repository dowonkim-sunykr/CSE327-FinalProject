import os
import requests
import random
import time
import threading
from PIL import Image
import hmac
import hashlib
import base64
from urllib.parse import urlencode

# Google Maps API Key and Signing Secret (replace with your actual API key and secret)
API_KEY = "" # 2nd account
SIGNING_SECRET = "" # 2nd account

CURRENT_CITY = "seoul"
print('City:', CURRENT_CITY)

CITIES = {
    "seoul": (37.516413, 127.011039),
    "tokyo": (35.680108, 139.762194),
    "new_york": (40.743323, -73.925452),
    "london": (51.504747, -0.116251),
    "paris": (48.858781, 2.343672),
}

# Output folder for images
OUTPUT_FOLDER = "test_images/" + CURRENT_CITY
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Number of images to collect
STARTING_INDEX = 0
TARGET_IMAGES = 5
NUM_IMAGES = TARGET_IMAGES - STARTING_INDEX

ORIG_SIZE = 256
FINAL_SIZE = 256

# Google Maps API URLs
STREETVIEW_URL = "https://maps.googleapis.com/maps/api/streetview"
METADATA_URL = "https://maps.googleapis.com/maps/api/streetview/metadata"

# Function to get a random location
def get_random_location():
    (lat, lon) = CITIES[CURRENT_CITY]
    lat += random.uniform(-0.04, 0.04)
    lon += random.uniform(-0.04, 0.04)
    return lat, lon

# Function to check if Street View is available
def check_streetview_availability(lat, lon):
    # print('check street avail')
    params = {"location": f"{lat},{lon}", "key": API_KEY}
    response = requests.get(METADATA_URL, params=params)
    data = response.json()
    # print('data:', data)

    # ONLY fetch google liscened photos (streetview), and not some random people's photos
    if data.get("status") == "OK" and data.get("copyright") == '© Google':
        pano_id = data.get("pano_id")
        return True, pano_id
    return False, None

# Function to generate the signed URL
def sign_url(url, secret):
    # print('sign url')
    # Remove domain from URL — only sign path and query
    url_to_sign = url.replace("https://maps.googleapis.com", "")
    
    # Convert web-safe base64 key to standard base64
    secret = secret.replace('-', '+').replace('_', '/')
    
    # Pad the secret if necessary
    missing_padding = len(secret) % 4
    if missing_padding:
        secret += '=' * (4 - missing_padding)
    
    # Decode the key
    decoded_key = base64.b64decode(secret)
    
    # Create a signature using the decoded key and URL
    signature = hmac.new(decoded_key, url_to_sign.encode('utf-8'), hashlib.sha1)
    encoded_signature = base64.b64encode(signature.digest()).decode('utf-8')

    # Convert to web-safe base64
    web_safe_signature = encoded_signature.replace('+', '-').replace('/', '_')
    
    # Add the signature to the original URL
    return f"https://maps.googleapis.com{url_to_sign}&signature={web_safe_signature}"


# Function to download a Street View image
def download_streetview_image(pano_id, index):
    # print('download street img')
    # Build the dynamic URL for Street View request
    params = {
        "size": f"{ORIG_SIZE}x{ORIG_SIZE}",  # Image size for download
        "pano": pano_id,
        "heading": 0,
        "pitch": 0,
        "fov": 90,
        "radius": 500,
        "source": "outdoor",
        "return_error_code": "false",
        "key": API_KEY
    }
    dynamic_url = f"{STREETVIEW_URL}?{urlencode(params)}"
    
    # Generate the signed URL
    signed_url = sign_url(dynamic_url, SIGNING_SECRET)
    
    # Make the request with the signed URL
    response = requests.get(signed_url)

    if response.status_code == 200:
        filename = os.path.join(OUTPUT_FOLDER, f"streetview_{index}.jpg")

        # Save original image
        with open(filename, "wb") as file:
            file.write(response.content)

        # Open and resize the image to 32x32
        try:
            with Image.open(filename) as img:
                resized_img = img.resize((FINAL_SIZE, FINAL_SIZE), Image.Resampling.LANCZOS)
                resized_img.save(filename)
            print(f"Downloaded & resized: {filename}")
        except Exception as e:
            print(f"Error resizing image {filename}: {e}")
    else:
        print(f"Failed to download image at index {index}, status code: {response.status_code}")

# Threaded function to speed up downloads
def fetch_streetview_image(index):
    # print('fetch street img')
    while True:
        lat, lon = get_random_location()
        if lat and lon:
            available, pano_id = check_streetview_availability(lat, lon)
            if available:
                download_streetview_image(pano_id, index)
                return

# Start multiple threads to speed up downloads
threads = []
for i in range(NUM_IMAGES):
    thread = threading.Thread(target=fetch_streetview_image, args=(i + STARTING_INDEX,))
    thread.start()
    threads.append(thread)
    time.sleep(0.1)  # Slight delay to prevent hitting API rate limits

# Wait for all threads to finish
for thread in threads:
    thread.join()

print(f"✅ Completed downloading {NUM_IMAGES} Street View images!")
