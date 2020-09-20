# Update your twitter bio to show your root-me.org rank

Default format :

```text
Root-me rank : xxx/xxxx (xxx pts)
```

## Setup
### Install dependencies

```
pip install --user -r requirements.txt
```

### Get a twitter API key

Go to [developer.twitter.com](https://developer.twitter.com/en/docs) and request an API access.

### Give your credentials

Open and fill `main.py` whith your credentials

### Setup a cronjob

To update every 10 minutes :

```
*/10 * * * * python3 /path/to/script/main.py
```

## What's next ?

* Do not update if rank hasn't changed
* Better DOM parsing (I know)
* Better error handling
* Might release docker image
