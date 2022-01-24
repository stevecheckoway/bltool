# bltool

## bltool.py

```
usage: bltool.py [-h] {list,delete,add,add-script,reset,next} ...

Command the blinkytile.

positional arguments:
  {list,delete,add,add-script,reset,next}
    list                List files
    delete              Delete file
    add                 Add file
    add-script          Add script file
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
- `add-script file` Add the script file to the Lightbuddy
- `delete sector` Delete the file starting at `sector` from the Lightbuddy
- `reset` Reloads the animations and starts playing the first file
- `next` Run the next animation

## animation.py

This defines a very simple Animation class which can write out animation files which can be added to the Lightbuddy using `bltool.py add`

# firmware

The firmware in `firmware` is a modified version of the normal BlinkyTile firmware for the Lightbuddy.

Modifications include
- A new "next animation" command serial command
- Animation scripts (extremely basic)

## Animation scripts

An animation script is a new file format that lets you control how long each
regular animation plays. See `script.py` for details and example scripts.

If any animation scripts are in flash, then the "next animation" button (and
serial command) will move to the next script rather than the next animation.

Since animation scripts refer to animations in order, you'll probably want to
delete all files and then add normal animations in the order you want and then
the scripts that will talk to them.

# OpenOCD

`openocd-blinkytile.cfg` is an OpenOCD configuration file for debugging the
Lightbuddy (or programming it).

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
