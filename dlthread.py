#!/usr/bin/env python3
import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse

def get_all_images(url):
    """
    Returns all images as part of an dict.
    """
    soup = bs(requests.get(url).content, "html.parser")
    imgs = {}
    for a in soup.find_all("a", class_='originalNameLink'):
        temp = {}
        temp['name'] = a['download'] #the filename
        temp['url'] =  urljoin(url, a['href']) #The lonk
        imgs[a['download']] = temp
    return imgs

def download(img, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # get the file name
    filename = img['name']
    with open(filename, "wb") as f:
        f.write(requests.get(img['url']).content)

def main(url, path):
    # get all images
    imgs = get_all_images(url)
    for img in imgs:
        # for each image, download it
        download(imgs[img], path)

main("https://16chan.xyz/pol/res/25345.html", "web-scraping")
