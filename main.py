import subprocess
import argparse
import shutil

# Comprueba si python está disponible, si no, usa python3
python_bin = "python" if shutil.which("python") else "python3"

def invoke_scraper(mode, id, debug):
    command = [python_bin, "scraper.py", mode, str(id)]
    if debug:
        command.append("--debug")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el scraper: {e}")

def main(mode, start_id, end_id, debug):
    if mode == 'ediciones':
        try:
            start_id = int(start_id)
            end_id = int(end_id) if end_id is not None else start_id  # If end_id is None, use start_id
        except ValueError:
            print("start_id y end_id deben ser números enteros.")
            return
        for id in range(start_id, end_id + 1):
            invoke_scraper(mode, id, debug)
    elif mode == 'comics':
        invoke_scraper(mode, start_id, debug)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape a Whakoom page.')
    parser.add_argument('mode', choices=['ediciones', 'comics'], help='The type of page to scrape.')
    parser.add_argument('start_id', help='The ID of the page to start scraping.')
    parser.add_argument('end_id', nargs='?', default=None, help='The ID of the page to end scraping. If not provided, it will be the same as start_id.')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode.')
    args = parser.parse_args()

    main(args.mode, args.start_id, args.end_id, args.debug)