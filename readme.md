### dlthread

Dumps all the assets from posts on lynxchan imageboard threads.

### Project Directive

In order to maintain a useful dataset this project indexes files by checksum and stores the result hash in a dictionary.
Attached to this many-to-many relationship is the name of the file, the download URL `sys.argv[1]`, and the URL of the media asset.
In operation, the program downloads each file and computes the checksum before comparing it against the index to determine if it already exists.
Should the check_duplicate() return true the file is not saved to disk but the checksum is recorded against the download request.

The metadata anchored against the sha1 is indexed in a state object. Currently this is a json blob written to disk.
This index is read once at the beginning of a capture transaction, and is in memory for the life of the process.
The state is written back to the disk at the end of a capture and thus must be treated atomically.

If multiple instances are running concurrently, you risk data lose. https://github.com/dbrownidau/dlthread/issues/8

This project does not create concurrent HTTP requests.


### How to use

```
git clone https://github.com/dbrownidau/dlthread.git
cd ./dlthread
python -m venv .dlthread
source .dlthread/bin/activate
pip install -r requirements.txt
chmod +x ./dlthread.py
./dlthread.py https://????chan.net/???/res/???????.html
```
