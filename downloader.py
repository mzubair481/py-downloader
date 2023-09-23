import asyncio
import os
import time
from urllib.parse import urlparse

import aiohttp
import tqdm

async def download_file(url, destination):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=None)) as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                start_time = time.time()
                
                with open(destination, 'wb') as file, tqdm.tqdm(total=total_size, unit='iB', unit_scale=True, unit_divisor=1024) as progress_bar:
                    async for chunk in response.content.iter_any():
                        if chunk:
                            file.write(chunk)
                            progress_bar.update(len(chunk))
        except aiohttp.ClientError as e:
            print(f"Error: {e}")
        except asyncio.TimeoutError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        else:
            total_time = (time.time() - start_time) / 60
            download_speed = total_size / total_time
            download_speed_mb = download_speed / (1024 * 1024)
            print(f"\nDownload complete!\nTotal Download Time: {total_time:.2f} minutes\nAverage Download Speed: {download_speed_mb:.2f} MB per second")

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def parse_url(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    return base_url

def get_file_name(url):
    return url.split('/')[-1]

async def main():
    url = parse_url(input("Enter the URL of the file to download: "))
    directory = input("Enter the directory to save the file: ")
    
    create_directory(directory)
    
    file_name = get_file_name(url)
    destination = os.path.join(directory, file_name)
    
    await download_file(url, destination)

if __name__ == "__main__":
    asyncio.run(main())
