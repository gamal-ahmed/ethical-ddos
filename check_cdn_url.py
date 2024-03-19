import requests
import sys  # Import sys to access command-line arguments

# Define CDN-related headers that could indicate the use of a CDN
cdn_headers = [
    'X-Cache', 'Via', 'X-CDN', 'CF-RAY', 'X-Edge-IP',
    'X-Edge-Location', 'X-hw', 'X-Amz-Cf-Id', 'X-Cache-Hits',
    'X-Sucuri-ID', 'X-Sucuri-Cache', 'Server', 'X-CDN-Geo',
    'X-CDN-Provider', 'Content-Delivery-Network'
]

def is_using_cdn(url):
    try:
        # Make a request to the given URL
        response = requests.get(url, timeout=12)
        headers = response.headers

        # Check each CDN-related header in the response
        for header in cdn_headers:
            if header in headers:
                # Print a descriptive message about the CDN in use
                print(f"CDN Detected: {header} indicating the use of a CDN. Header value: {headers[header]}")
                return

        # If no CDN-related headers are found, indicate no CDN detected
        print("No CDN detected for this URL.")

    except requests.RequestException as e:
        # Print any errors encountered during the request
        print(f"Error making request: {e}")

# Check if a URL has been passed as a command-line argument
if len(sys.argv) < 2:
    print("Usage: script.py <URL>")
    sys.exit(1)

# Extract the URL from the command-line arguments
url = sys.argv[1]

# Check and print the CDN in use for the provided URL
is_using_cdn(url)
