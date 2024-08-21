import requests
import argparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}

def get_and_process_url_data(input_url, output_file):
    try:
        # Making a GET request with headers
        r = requests.get(input_url, headers=HEADERS)

        # Check status code for response received
        if r.status_code == 200:
            print("Request was successful")

            # Filter out empty lines and process content directly
            lines = [line for line in r.text.splitlines() if line.strip() != ""]

            # Keep lines from 595 to 3671 (0-based indexing)
            lines_to_write = lines[593:3671]

            # Write the filtered content to the output file
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.writelines("\n".join(lines_to_write))
                
            print(f"Successfully kept lines 595 to 3671. Output written to {output_file}")
        else:
            print(f"Request failed with status code {r.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Fetch content from a URL and process it.')
    parser.add_argument('input_url', type=str, help='The URL to fetch content from')
    parser.add_argument('output_file', type=str, help='The file to write the processed content to')

    # Parse arguments
    args = parser.parse_args()

    # Call the function with arguments
    get_and_process_url_data(args.input_url, args.output_file)