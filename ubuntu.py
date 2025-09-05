import requests
import os
import hashlib
from urllib.parse import urlparse

def get_filename_from_url(url, content):
    """Extract filename from URL or generate one using a hash."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)

    # If no filename in URL, generate one
    if not filename:
        file_hash = hashlib.md5(content).hexdigest()[:10]  # shorten hash
        filename = f"image_{file_hash}.jpg"

    return filename

def download_image(url, folder="Fetched_Images"):
    """Download an image from the given URL into the folder."""

    try:
        os.makedirs(folder, exist_ok=True)

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Check content type (important precaution)
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ Skipping {url} — not an image (Content-Type: {content_type})")
            return

        # Generate safe filename
        filename = get_filename_from_url(url, response.content)
        filepath = os.path.join(folder, filename)

        # Prevent duplicates (precaution)
        if os.path.exists(filepath):
            print(f"⚠ Duplicate detected: {filename} already exists, skipping download.")
            return

        # Save file in binary mode
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error fetching {url}: {e}")
    except Exception as e:
        print(f"✗ An unexpected error occurred: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Allow multiple URLs (comma or space separated)
    urls_input = input("Please enter one or more image URLs (separated by spaces or commas): ")
    urls = [u.strip() for u in urls_input.replace(",", " ").split() if u.strip()]

    if not urls:
        print("✗ No valid URLs entered.")
        return

    for url in urls:
        download_image(url)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
