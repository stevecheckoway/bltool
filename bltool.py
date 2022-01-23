#!/usr/bin/env python

import argparse
from struct import pack, unpack
import sys

import serial
import serial.tools.list_ports

CMD_RELOAD_ANIMATIONS = 0x02
CMD_FILE_COUNT = 0x12
CMD_FILE_TYPE = 0x14
CMD_READ_FILE = 0x1A
CMD_DELETE_FILE = 0x15
CMD_NEW_FILE = 0x18
CMD_WRITE_FILE = 0x19

CMD_NEXT_ANIMATION = 0x80

FILETYPE_ANIMATION = 0x12


def command(ser, cmd, data=None):
    buffer = bytearray(1)
    buffer[0] = cmd
    if data:
        buffer.extend(data)
    # print(f"Command: {buffer}")
    ser.write(b'\xFF' * 10 + buffer)

    # These reads will block until all bytes are read.
    response = bytearray()
    response.extend(ser.read(3))
    response_length = response[1] + 1
    if len(response) < response_length + 2:
        response.extend(ser.read(response_length + 2 - len(response)))
    # print(f"Response: {response}")
    if response[0] != b'P'[0]:
        return None

    return response[2:]


def get_file_count(ser):
    response = command(ser, CMD_FILE_COUNT)
    if response is None or len(response) != 4:
        return None
    return unpack('>I', response)[0]


def get_files(ser):
    files = []
    for sector in range(0, 100):
        response = command(ser, CMD_FILE_TYPE, pack('>I', sector))

        if response is None:
            continue
        if len(response) == 4:
            files.append((sector, unpack('>I', response)[0]))
        else:
            files.append((sector, None))
    return files


def read_file(ser, sector):
    data = bytearray()
    offset = 0
    while True:
        response = command(ser, CMD_READ_FILE, pack('>IIB', sector, offset, 255))
        if response is None:
            return data
        data.extend(response)
        offset += len(response)


def delete_file(ser, sector):
    return command(ser, CMD_DELETE_FILE, pack('>I', sector)) is not None


def new_file(ser, data):
    sector = command(ser, CMD_NEW_FILE, pack(
        '>BI', FILETYPE_ANIMATION, len(data)))
    if sector is None:
        print("Failed to create file", file=sys.stderr)
        return None
    sector = unpack('>I', sector)[0]
    for offset in range(0, len(data), 256):
        cmd_data = pack('>II', sector, offset) + data[offset:offset+256]
        if command(ser, CMD_WRITE_FILE, cmd_data) is None:
            print("Failed to write file", file=sys.stderr)
            return None
    return sector


def reload_animations(ser):
    return command(ser, CMD_RELOAD_ANIMATIONS) is not None

def next_animation(ser):
    return command(ser, CMD_NEXT_ANIMATION)

def get_serial_port():
    for port in serial.tools.list_ports.grep(r'.*usbmodem.*'):
        return port.device
    return None


def connect(port: str = None):
    if port is None:
        port = get_serial_port()
        if port is None:
            print("No serial port found", file=sys.stderr)
            sys.exit(1)
    #print(f"Using serial port: {port}")
    return serial.Serial(port, 115200)


def arg_parser():
    parser = argparse.ArgumentParser(description='Command the blinkytile.')
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('list', help='List files')

    delete_parser = subparsers.add_parser('delete', help='Delete file')
    delete_parser.add_argument('sector', type=int, help='Sector to delete')

    add_parser = subparsers.add_parser('add', help='Add file')
    add_parser.add_argument(
        'file', type=argparse.FileType('rb'), help='File to add')

    subparsers.add_parser('reset', help='Reset the blinkytile')
    subparsers.add_parser('next', help='Show the next animation')

    return parser


def main():
    parser = arg_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_usage(file=sys.stderr)
        sys.exit(1)

    with connect() as ser:
        if args.command == 'list':
            print(f"{get_file_count(ser)} files")
            for sector, file_type in get_files(ser):
                if file_type is None:
                    print(f"{sector}: empty")
                else:
                    print(f"{sector}: {file_type}")
        elif args.command == 'delete':
            if not delete_file(ser, args.sector):
                print(f"Failed to delete file {args.sector}", file=sys.stderr)
                sys.exit(1)
        elif args.command == 'add':
            data = args.file.read()
            args.file.close()
            if len(data) % 256 != 0:
                print("File must be a multiple of 256 bytes", file=sys.stderr)
                sys.exit(1)
            sector = new_file(ser, data)
            print(f"Created file at sector {sector}")
            reload_animations(ser)
        elif args.command == 'reset':
            if not reload_animations(ser):
                print("Failed to reset", file=sys.stderr)
                sys.exit(1)
        elif args.command == 'next':
            if not next_animation(ser):
                print("Failed to move to the next animation", file=sys.stderr)
                sys.exit(1)

        else:
            print(f"Unknown command: {args.command}")
            sys.exit(1)


if __name__ == '__main__':
    main()
