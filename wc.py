#!/usr/bin/env python3

import sys
import os

def count_stream(stream):
    lines = 0
    words = 0
    bytes_count = 0

    for chunk in stream:
        lines += chunk.count(b'\n')
        words += len(chunk.split())
        bytes_count += len(chunk)

    return lines, words, bytes_count


def count_file(filename):
    with open(filename, 'rb') as f:   
        return count_stream(f)


def main():
    if len(sys.argv) == 1:
        lines, words, bytes_count = count_stream(sys.stdin.buffer)
        print(f"<html><body><center><h1>{lines:7} {words:7} {bytes_count:7}</h1></center></body></html>")
    else:
        total_lines = total_words = total_bytes = 0

        for filename in sys.argv[1:]:
            try:
                lines, words, bytes_count = count_file(filename)
                total_lines += lines
                total_words += words
                total_bytes += bytes_count
                print(f"{lines:7} {words:7} {bytes_count:7} {filename}")
            except FileNotFoundError:
                print(f"mywc: {filename}: No such file or directory", file=sys.stderr)

        if len(sys.argv) > 2:
            print(f"{total_lines:7} {total_words:7} {total_bytes:7} total")


if __name__ == "__main__":
    main()