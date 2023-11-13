import requests
import os
import concurrent.futures
import asyncio
import aiohttp
import time
import argparse

# Создаем директорию, если она не существует
DOWNLOAD_DIR = 'downloaded_images'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_image(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Извлекаем имя файла из URL
        filename = os.path.basename(url)

        filepath = os.path.join(DOWNLOAD_DIR, filename)

        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return filepath
    except Exception as e:
        return f"Failed to download {url}: {str(e)}"

async def download_image_async(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()

            # Извлекаем имя файла из URL
            filename = os.path.basename(url)

            filepath = os.path.join(DOWNLOAD_DIR, filename)

            with open(filepath, 'wb') as file:
                while chunk := await response.content.read(8192):
                    file.write(chunk)

            return filepath
    except Exception as e:
        return f"Failed to download {url}: {str(e)}"

def sync_download(urls):
    start_time = time.time()
    results = []
    for url in urls:
        result = download_image(url)
        results.append(result)
    end_time = time.time()
    print(f"Sync download time: {end_time - start_time:.2f} seconds")
    return results

def multi_process_download(urls):
    start_time = time.time()
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(download_image, urls))
    end_time = time.time()
    print(f"Multiprocess download time: {end_time - start_time:.2f} seconds")
    return results

async def async_download(urls):
    start_time = time.time()
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [download_image_async(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    end_time = time.time()
    print(f"Async download time: {end_time - start_time:.2f} seconds")
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download images from given URLs.")
    parser.add_argument("urls", metavar="URL", type=str, nargs="+", help="URLs of the images to download.")
    args = parser.parse_args()

    urls = args.urls

    sync_results = sync_download(urls)
    print(sync_results)

    multi_process_results = multi_process_download(urls)
    print(multi_process_results)

    async_results = asyncio.run(async_download(urls))
    print(async_results)
