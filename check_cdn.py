import requests
import csv

cdn_headers = [
    'X-Cache', 'Via', 'X-CDN', 'CF-RAY', 'X-Edge-IP',
    'X-Edge-Location', 'X-hw', 'X-Amz-Cf-Id', 'X-Cache-Hits',
    'X-Sucuri-ID', 'X-Sucuri-Cache', 'Server', 'X-CDN-Geo',
    'X-CDN-Provider', 'Content-Delivery-Network'
]

def is_using_cdn(url):
    try:
        response = requests.get(url, timeout=12)
        headers = response.headers

        for header in cdn_headers:
            if header in headers:
                # Return the header and its value if found
                return True, f"{header}: {headers[header]}"
        return False, ""

    except requests.RequestException as e:
        return False, f"Error making request: {e}"

def highlight_urls(urls):
    results = []
    for url in urls:
        result, message = is_using_cdn(url)
        if result:
            print("\033[94m{}\033[00m".format(url))  # Blue for CDN
            if message:  # Check if message is not empty
                print(f"\t{message}")
            results.append({"website": url, "cdn-used": message})
        else:
            print(url)
            results.append({"website": url, "cdn-used": "No CDN detected"})
    return results

def export_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["website", "cdn-used"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

urls = [""]

# Highlight URLs and collect results
results = highlight_urls(urls)

# Define the CSV file name
csv_filename = 'cdn_usage.csv'

# Export results to CSV
export_to_csv(results, csv_filename)

print(f"Data exported to {csv_filename}")
