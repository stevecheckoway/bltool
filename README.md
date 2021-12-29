# bltool

## bltool.py

```
usage: bltool.py [-h] {list,delete,add,reset} ...

Command the blinkytile.

positional arguments:
  {list,delete,add,reset}
    list                List files
    delete              Delete file
    add                 Add file
    reset               Reset the blinkytile

optional arguments:
  -h, --help            show this help message and exit
```

Files are named by the starting sector. E.g.,

```
$ ./bltool.py list
1 files
0: 18
```
The file at sector 0 has type 18 (animation; the only type defined).

Subcommands
- `list` List all of the files on the Lightbuddy
- `add file` Add the file to the Lightbuddy
- `delete sector` Delete the file starting at `sector` from the Lightbuddy
- `reset` Reloads the animations and starts playing the first file

## animation.py

This defines a very simple Animation class which can write out animation files which can be added to the Lightbuddy using `bltool.py add`
