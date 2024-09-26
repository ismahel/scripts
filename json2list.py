import json
import requests
import sys

def extract_cidr_blocks(json_data):
    """
    Extracts CIDR blocks from a JSON payload, adapting to different formats.

    Args:
        json_data: The JSON data (as a Python dictionary).

    Returns:
        A list of extracted CIDR blocks.
    """

    cidr_blocks = []

    if 'prefixes' in json_data:  # Handle zia.json format
        return json_data['prefixes']
    elif 'content' in json_data:  # Handle zpa.json format
        for item in json_data['content']:
            if 'IPs' in item:
                cidr_blocks.extend(item['IPs'])

    return cidr_blocks

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        print("Usage: python script.py <input> [output_filename]")
        print("  <input> can be either a URL or a local file path")
        sys.exit(1)

    input_source = sys.argv[1]
    output_filename = sys.argv[2] if len(sys.argv) == 3 else None

    try:
        if input_source.startswith("http://") or input_source.startswith("https://"):
            response = requests.get(input_source)
            response.raise_for_status()
            json_data = response.json()
        else:
            with open(input_source, "r") as f:
                json_data = json.load(f)
    except (requests.exceptions.RequestException, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading JSON data: {e}")
        sys.exit(1)

    cidr_blocks = extract_cidr_blocks(json_data)

    if output_filename:
        with open(output_filename, "w") as f:
            for cidr in cidr_blocks:
                f.write(cidr + "\n")
        print(f"CIDR blocks extracted and saved to {output_filename}")
    else:
        for cidr in cidr_blocks:
            print(cidr)
