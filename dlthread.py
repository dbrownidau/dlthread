#!/usr/bin/env python3
import sys
import requests
import os
import time
import hashlib
from pathlib import Path
from urllib.request import urlretrieve
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup as bs

def gimmeh_sha1(buffer):
    """
    Returns a SHA1 for a buffer
    """
    sha1 = hashlib.sha1()
    sha1.update(buffer) #.update(str('lol').encode('utf-8'))
    return sha1.hexdigest()

def get_all_images(url):
    """
    Returns all images as part of an dict.
    """
    print('Extracting assets from html')
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
    print('Downloading:', img['name'])
    Path(pathname).mkdir(parents=True, exist_ok=True)
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    if os.path.exists(pathname + '/' + img['name']):
        alt = str(int(time.time())) + '--' + img['name']
        print('Duplicate file, saving as:', alt)
        urlretrieve(img['url'], pathname + '/' + alt) # gimmeh_sha1() - todo
        return
    urlretrieve(img['url'], pathname + '/' + img['name'])

def main(url):
    print('Hello World')
    imgs = get_all_images(url)
    for img in imgs:
        download(imgs[img], 'downloads')

if len(sys.argv) < 2:
    print('Requires target URL.')
    exit(0)
main(sys.argv[1])
