import requests
import threading
from multiprocessing import Process
import asyncio
import aiohttp
import time
import argparse

urls = ['https://img.freepik.com/free-vector/happy-small-dog-set-cute-funny-puppy-practicing-different-activities-hunting-playing-eating-sleeping_74855-10796.jpg?size=626&ext=jpg&ga=GA1.1.1467479332.1688841074&semt=sph',
        'https://img.freepik.com/free-vector/cute-cat-cartoon-character_1308-134571.jpg?w=1380&t=st=1688841076~exp'
         '=1688841676~hmac=80dc8d5d97f799179922db4e1b5972f78f2cfd0c71856aebc10a08960fef117d',
        'https://img.freepik.com/free-vector/set-of-six-fish_23-2147799967.jpg?size=626&ext=jpg&ga=GA1.2.1467479332.1688841074&semt=sph',
        'https://img.freepik.com/free-vector/collection-of-flat-tropical-animal_23-2148219696.jpg?w=1380&t=st=1688841306~exp=1688841906~hmac=e70fde79076617931f81d24b3b7b8a2b88319580a442091971ec9f88fdc1205a',
         'https://img.freepik.com/free-vector/brown-bears-set_74855-15326.jpg?w=1380&t=st=1688841325~exp=1688841925'
         '~hmac=29c074fb7e0a35f28d7bf4aedd20bf73ad979a30ec3d1204605b00c837d5560b',
        'https://img.freepik.com/free-vector/cute-giraffe-in-flat-style_1308-114113.jpg?w=740&t=st=1688841373~exp=1688841973~hmac=e765385ad20acc1444a3af7805989cd51a8e713b3a9a176afb38a2851ca7be91']


def save_image(url):
    start_time = time.time()
    response = requests.get(url)
    filename = f'{url.split("/")[-1]}'
    with open(f'{filename}.jpg', 'wb') as f:
        f.write(response.content)

    downloaded_time = time.time() - start_time
    print(f"Downloaded {url} {downloaded_time} seconds")


async def save_image_async(url):
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
            filename = f'{url.split("/")[-1]}'
            with open(f'{filename}.jpg', 'wb') as f:
                f.write(content)
    downloaded_time = time.time() - start_time
    print(f"Downloaded {url} {downloaded_time} seconds")


def download_images_with_threading():
    threads = []
    for url in urls:
        thread = threading.Thread(target=save_image, args=[url])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def download_images_with_process():
    processes = []
    for url in urls:
        process = Process(target=save_image, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


async def download_images_with_async():
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(save_image_async(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download images from urls.")
    parser.add_argument("--urls", nargs="*")
    args = parser.parse_args()
    if args.urls:
        urls = args.urls

    print("Downloading images using threading...")
    download_images_with_threading()
    print('*' * 20 + ' END ' + '*' * 20)
    print("Downloading images using multiprocessing...")
    download_images_with_process()
    print('*' * 20 + ' END ' + '*' * 20)
    print("Downloading images using asyncio...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(download_images_with_async())
    print('*' * 20 + ' END ' + '*' * 20)