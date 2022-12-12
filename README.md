# Hello World

## What is this?

Its a python script that interacts with the Docker API directly to create an
HTTPd container which servers and _extremely_ cool HTML file on localhost:8080.

Personally, I love it.

## How do I make this work?

```
pip install -r requirements.txt
```

And then!

```
./go.py
```

## Problems / Future Work

So like, first off HTTPd runs as root by default, which isn't super great for 
the security of the host.  We could do better there by just switching to a non-
root user and using port 8080 in the container instead of 80.  Because of this
I didn't do any no-new-privileges or --cap-drop all tricks, since that's like
defending swiss cheese at this point.
