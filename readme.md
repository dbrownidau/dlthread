### dlthread

Dumps all the assets from posts on lynxchan imageboard threads.

### Project Directive

This script can be run sequentially against the same URL. It will only download unique media files (identified by URL initally, then SHA1 before writing to disk). 

For example, it could be setup as a crontab and would continually re-scrape, downloading the new assets from the latests posts.

There is a catalog handler, so if you send it the catalog url it will attempt to download all assets from all threads. 

You can also import an existing directory of media content, the program will sha1 each file and store them in the state as "known" (duplicate files won't be re-aqcuired in future scrapes).

If multiple instances concurrently access the same statefile, you would risk data lose. See issue [#8](https://github.com/dbrownidau/dlthread/issues/8). 

This project does not create concurrent HTTP requests.


### How to use


#### Windows (10/11)
1. Download the project code from Github as a zip file.
1. Extract the zip file.
1. Run `powershell` and change directory to the extracted folder.
1. Type `python` in powershell. If not installed, it will open Python in the Windows Store for you to install. (Type `exit` to quit python).
   - Use the command: `python -m venv .env`
   - Use the command: `.env/Scripts/activate`
   - Use the command: `pip install -r requirements.txt`
   - Use the command: `python dlthread.py https://????chan.net/???/res/???????.html`

#### Linux
```
git clone https://github.com/dbrownidau/dlthread.git
cd ./dlthread
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt
chmod +x ./dlthread.py
./dlthread.py https://????chan.net/???/res/???????.html
```
