import requests
from datetime import datetime
import threading
import time

#making locks
log_lock = threading.Lock()
counter_lock = threading.Lock()
DOWNLOAD_COUNTER = 0
SUCCESSFUL_DOWNLOADS_PARALLEL = 0

def generate_images():
    urls = []
    for i in range(1, 101):
        url = f"https://picsum.photos/{300+i}"
        urls.append(url)
    return urls

#initializing logger.txt
def init_logger():
    with open("logger.txt", "w") as f:
        f.write("") #writing blank bc nothing to add yet

#what to log in the logger.txt
def log(url, filename, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_lock:  # Thread-safe logging
        with open("logger.txt", "a") as f:
            f.write(f"{timestamp} | {url} | {filename} | {status}\n")

def increment_counter(success=False):
    global DOWNLOAD_COUNTER, SUCCESSFUL_DOWNLOADS_PARALLEL #need to have this to modify the values
    with counter_lock:
        DOWNLOAD_COUNTER += 1
        if success:
            SUCCESSFUL_DOWNLOADS_PARALLEL += 1
        print(f"Downloaded: {DOWNLOAD_COUNTER} / 100")


def serial_downloader(urls):
    count = 1
    successful_downloads = 0

    start = time.perf_counter()
    for url in urls:
        output_file = f"image_{count}.jpg"
        max_retries = 3
        retries = 0

        while retries < max_retries:
            try:
                response = requests.get(url, timeout=3)
                with open(output_file, "wb") as f:
                    f.write(response.content)
                log(url, output_file, "SUCCESS")
                successful_downloads += 1
                break
            except requests.exceptions.Timeout:
                log(url, output_file, "TIMEOUT")
                break
            except Exception:
                retries += 1
                if retries < max_retries:
                    log(url, output_file, f"RETRY {retries}")
                else:
                    log(url, output_file, "FAILED")
        
        count += 1

    end = time.perf_counter()
    print(f"Serial time: {end-start:.2f} seconds (s)")
    print(f"Serial successful downloads: {successful_downloads}")

#making download function that does what is done in the serial but need to call in parallel, could've used in serial but didnt think that far
def single_download(url, image_num):
    output_file = f"image_{image_num}.jpg"
    max_retries = 3
    retries = 0
    
    while retries < max_retries:
        try:
            response = requests.get(url, timeout=3)
            with open(output_file, "wb") as f:
                f.write(response.content)
            log(url, output_file, "SUCCESS")
            increment_counter(success=True)
            break
        except requests.exceptions.Timeout:
            log(url, output_file, "TIMEOUT")
            increment_counter(success=False)
            break  # Don't retry on timeout
        except Exception as e:
            retries += 1
            if retries < max_retries:
                log(url, output_file, f"RETRY {retries}")
            else:
                log(url, output_file, "FAILED")
                increment_counter(success=False)

#making parallel version that handles max 5 workers
def parallel_downloader(urls):
    global DOWNLOAD_COUNTER, SUCCESSFUL_DOWNLOADS_PARALLEL #need to have this to modify the values
    DOWNLOAD_COUNTER = 0
    SUCCESSFUL_DOWNLOADS_PARALLEL = 0
    
    start = time.perf_counter()
    max_workers = 5
    threads = []

    for i, url in enumerate(urls, 1):
        thread = threading.Thread(target=single_download, args=(url, i))
        threads.append(thread)
        thread.start()

        if len(threads) >= max_workers:
            threads[0].join()
            threads.pop(0)

    for thread in threads:
        thread.join()

    end = time.perf_counter()
    print(f"Parallel time: {end-start:.2f} seconds (s)")
    print(f"Parallel successful downloads: {SUCCESSFUL_DOWNLOADS_PARALLEL}")


if __name__ == "__main__":
    init_logger()  #make logger
    urls = generate_images()
    serial_downloader(urls)

    print("\nNow running parallel\n")
    parallel_downloader(urls)
