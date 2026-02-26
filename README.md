# FastFetchProject
Used GenAI to Produce README, but understand all parts

Downloads 100 images in parallel using Python threads. Much faster than downloading one at a time.

## What This Does

Downloads 100 random images from picsum.photos. Compares:
- **Serial**: Download 1 image at a time (~30 seconds)
- **Parallel**: Download 5 images at once (~4 seconds)

## Setup

1. Clone the repo:
```bash
git clone <your-repo-url>
cd FastFetch
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install libraries:
```bash
pip install requests certifi
```

## How to Run

```bash
python3 main.py
```

The program will:
1. Download 100 images serially and show time
2. Download 100 images in parallel and show time
3. Log everything to `logger.txt`

## Serial vs Parallel

**Serial**: Downloads one image, waits for it to finish, then downloads the next one. Slow.

**Parallel**: Downloads 5 images at the same time. While one is waiting for the server, others download. Much faster.

**Results**:
- Serial: 30 seconds
- Parallel: 4 seconds
- **7x faster!**

## How It Works

**Threading**: Uses 5 worker threads that run at the same time.

**Locks**: A lock prevents multiple threads from writing to the log file at once (prevents corruption).

**Retries**: If a download fails, try again up to 3 times before giving up.

**Timeout**: If a download takes more than 3 seconds, skip it and move on.

**Logging**: Every download attempt is recorded in `logger.txt` with a timestamp and status.

## Files

```
main.py         - The program
logger.txt      - Log of all downloads
image_1.jpg ... - Downloaded images
```

## Log File

The `logger.txt` file records every download attempt:

```
2026-03-01 10:15:22 | https://picsum.photos/301 | image_1.jpg | SUCCESS
2026-03-01 10:15:23 | https://picsum.photos/302 | image_2.jpg | RETRY 1
2026-03-01 10:15:24 | https://picsum.photos/303 | image_3.jpg | TIMEOUT
2026-03-01 10:15:25 | https://picsum.photos/304 | image_4.jpg | FAILED
```

Status values:
- `SUCCESS` - Downloaded successfully
- `RETRY 1/2/3` - Retry attempt
- `TIMEOUT` - Download took too long
- `FAILED` - Failed after 3 retries

## What You Learn

- Threading in Python
- Using locks to prevent race conditions
- Error handling and retry logic
- Performance optimization
- Logging best practices

## Troubleshooting

**SSL Warning**: If you see a `NotOpenSSLWarning`, you can ignore it. Your code will still work fine.

**Some downloads fail**: This is normal. The retry logic handles it. Check `logger.txt` to see what happened.
