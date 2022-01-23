# bltool

## bltool.py

```
usage: bltool.py [-h] {list,delete,add,reset,next} ...

Command the blinkytile.

positional arguments:
  {list,delete,add,reset,next}
    list                List files
    delete              Delete file
    add                 Add file
    reset               Reset the blinkytile
    next                Show the next animation

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
- `next` Run the next animation

## animation.py

This defines a very simple Animation class which can write out animation files which can be added to the Lightbuddy using `bltool.py add`

## openocd-blinkytile.cfg

This is an OpenOCD configuration file for debugging the Lightbuddy (or
programming it).

## Reading flash

To dump the internal flash, use
```
openocd -f openocd-blinkytile.cfg
```
and then connect to the telnet port 4444 with nc.
```
nc -t localhost 4444
```

Issue the command
```
dump_image firmware.bin 0 0x10000
```
which will write `firmware.bin` in the same directory that you ran `openocd`
from.

## Writing flash

I haven't tried writing flash, but I suspect it should work using standard
tools. The commented out configuration regarding `verify` may be an issue.
