import requests
import concurrent.futures

URLS = ['http://upload.wikimedia.org/wikipedia/commons/9/9c/Image-Porkeri_001.jpg']


def download_images(urls):
    img_bytes = requests.get(urls).content
    img_name = urls.split('/')[-1]
    with open(img_name, 'wb') as img_file:
        img_file.write(img_bytes)
        print(f'{img_name} was downloaded...')


with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(download_images, URLS)
