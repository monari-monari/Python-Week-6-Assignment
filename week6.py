
import requests
import os
import hashlib
import mimetypes
from urllib.parse import urlparse

# Global set to track downloaded images and prevent duplicates (Challenge 3)
downloaded_hashes = set()

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    # Enhanced: Support both single URL and multiple URLs (Challenge 1)
    url_input = input("Please enter the image URL(s) [separate multiple URLs with commas]: ")
    
    # Handle multiple URLs if comma-separated
    if ',' in url_input:
        urls = [url.strip() for url in url_input.split(',') if url.strip()]
        print(f"\nProcessing {len(urls)} URLs...")
        
        successful = 0
        for i, url in enumerate(urls, 1):
            print(f"\n--- Processing URL {i}/{len(urls)} ---")
            if download_single_url(url):
                successful += 1
        
        print(f"\n✓ Successfully downloaded {successful}/{len(urls)} images")
        print("Connection strengthened. Community enriched.")
        
    else:
        # Single URL processing (following your original structure)
        url = url_input.strip()
        download_single_url(url)

def download_single_url(url):
    """Download a single URL following the starter structure with enhancements"""
    try:
        # Challenge 2: Security precaution - URL validation
        if not url.startswith(('http://', 'https://')):
            print(f"✗ Invalid URL format: {url}")
            print("Please use http:// or https:// URLs only")
            return False
        
        # Create directory if it doesn't exist
        os.makedirs("Fetched_Images", exist_ok=True)
        
        # Enhanced: Security headers for responsible downloading
        headers = {
            'User-Agent': 'Ubuntu-Image-Fetcher/1.0 (Educational Purpose)'
        }
        
        # Fetch the image
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Challenge 4: Check important HTTP headers before saving
        content_type = response.headers.get('content-type', '').lower()
        content_length = response.headers.get('content-length')
        
        # Security check: Verify it's actually an image
        if not content_type.startswith('image/'):
            print(f"✗ Security check failed: Not an image file (content-type: {content_type})")
            return False
        
        # Security check: File size limit (50MB max for safety)
        if content_length:
            size_mb = int(content_length) / (1024 * 1024)
            if size_mb > 50:
                print(f"✗ File too large: {size_mb:.1f}MB (max 50MB for security)")
                return False
        
        # Challenge 3: Duplicate prevention using content hash
        content_hash = hashlib.md5(response.content).hexdigest()
        if content_hash in downloaded_hashes:
            print("✗ Duplicate image detected - already downloaded this content")
            return False
        downloaded_hashes.add(content_hash)
        
        # Extract filename from URL or generate one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        if not filename or '.' not in filename:
            # Generate appropriate filename using content type
            extension = mimetypes.guess_extension(content_type) or '.jpg'
            filename = f"downloaded_image_{content_hash[:8]}{extension}"
        
        # Ensure unique filename to prevent overwrites
        base_name, extension = os.path.splitext(filename)
        counter = 1
        original_filename = filename
        while os.path.exists(os.path.join("Fetched_Images", filename)):
            filename = f"{base_name}_{counter}{extension}"
            counter += 1
            
        # Save the image
        filepath = os.path.join("Fetched_Images", filename)
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
            
        print(f"✓ Successfully fetched: {filename}")
        if filename != original_filename:
            print(f"  (Renamed from {original_filename} to avoid conflicts)")
        print(f"✓ Image saved to {filepath}")
        
        # Display file info
        size_kb = len(response.content) / 1024
        print(f"✓ File size: {size_kb:.1f} KB")
        print(f"✓ Content type: {content_type}")
        
        print("\nConnection strengthened. Community enriched.")
        return True
        
    except requests.exceptions.Timeout:
        print("✗ Connection timeout - server took too long to respond")
    except requests.exceptions.ConnectionError:
        print("✗ Connection error - check your internet connection")
    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP error: {e.response.status_code} - {e.response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Request error: {e}")
    except PermissionError:
        print("✗ Permission denied - cannot write to Fetched_Images directory")
    except Exception as e:
        print(f"✗ An unexpected error occurred: {e}")
        
    return False

if __name__ == "__main__":
    main()