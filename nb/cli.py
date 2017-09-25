#!/usr/bin/env python3

import argparse
import os

import nb.api


def parse_and_run():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument(
        'markdown_file', type=str, nargs=1,
        help='The file to add upload and convert into a medium draft')
    parser.add_argument(
        "--api_key", type=str, default=None,
        help="Your medium API key")
    args = parser.parse_args()

    api_key = args.api_key if args.api_key is not None else os.environ["MEDIUM_API_KEY"]
    api = nb.api.MediumUser(api_key)
    api.convert_upload_md(args.markdown_file[0])

if __name__ == "__main__":
    parse_and_run()
