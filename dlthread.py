#!/usr/bin/env python3
import sys
import requests
import os
import time
import hashlib
import json
from pathlib import Path
from urllib.request import urlretrieve
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup as bs

def load_state(statefile):
    print('Loading state')
    try:
        with open(statefile, 'r') as state:
            return json.load(state)
    except FileNotFoundError:
        print('No state file found.')
        temp = {}
        return temp

def save_state(statefile, state):
    print('Saving state')
    with open (statefile, 'w') as statetarget:
        json.dump(state, statetarget)

def gimmeh_sha1(buffer):
    """
    Returns a SHA1 for a buffer
    """
    sha1 = hashlib.sha1()
    sha1.update(buffer)
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
        imgs[urljoin(url, a['href'])] = temp
    return imgs

def gen_targetfile(img, pathname):
    """
    Does preflight checks, generates a path.
    """
    Path(pathname).mkdir(parents=True, exist_ok=True)
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    if os.path.exists(pathname + '/' + img['name']):
        alt = str(int(time.time())) + '--' + img['name']
        print('Existing filename:', img['name'])
        return pathname + '/' + alt #Often doesn't progress enough for this to be used.
    print('Filename:', img['name'])
    return pathname + '/' + img['name']

def download(url, name):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    print(' > Downloading:', name)
    u = requests.get(url)
    return u

def save_file(u, pathname, filename):
    """
    Writes file to disk
    """
    print(' > Writing', filename, 'to disk.')
    with open(pathname, 'wb') as f:
        f.write(u.content)

def index(state, imgs, url):
    """
    Indexes a file in the state
    """
    for img in imgs:
        if not imgs[img]['url'] in state:
            imgs[img]['target'] = url
            state[imgs[img]['url']] = imgs[img]
    return state

def bookmark_checksum(state, url, checksum):
    state[url]['sha1'] = checksum

def check_duplicate(state, checksum):
    """
    Returns true if the sha1 is known
    """
    for entity in state:
        try:
            if checksum in state[entity]['sha1']:
                print(' > Checksum already known, skipping...')
                return True
        except KeyError:
            return False
    return False

def url_known(state, img):
    """
    Returns true if the url is known in the index state and has a sha1 attached.
    """
    for entity in state:
        if img['url'] in state[entity]['url']: #img['url'] comes from main
            try:
                if 'sha1' in state[entity]:
                    print(' > Known: ', state[entity]['sha1'])
                    return True
            except KeyError:
                return False
    return False

def catalog_consumer(url):
    print('Catalog consumer attempting to find threads...')
    soup = bs(requests.get(url).content, "html.parser")
    target_threads = []
    for a in soup.find_all("a", class_='linkThumb'):
        target_threads.append(urljoin(url, a['href']))
    print('Found:', len(target_threads), "threads.")
    return target_threads

def main(url):
    print('Hello World')
    if 'catalog' in url:
        for instance in catalog_consumer(url):
            print('Downloading thread:', instance)
            main(instance)
        return
    state = load_state('dlthread.json')
    save_state('dlthread_bkp.json', state)
    imgs = get_all_images(url)
    state = index(state, imgs, url)
    for img in imgs:
        targetfile = gen_targetfile(imgs[img], 'downloads')
        if url_known(state, imgs[img]):
            continue
        u = download(imgs[img]['url'], imgs[img]['name'])
        if not check_duplicate(state, gimmeh_sha1(u.content)):
            save_file(u, targetfile, imgs[img]['name'])
        bookmark_checksum(state, imgs[img]['url'], gimmeh_sha1(u.content))
    save_state('dlthread.json', state)

if len(sys.argv) < 2:
    print('Requires target URL.')
    exit(0)
main(sys.argv[1])
