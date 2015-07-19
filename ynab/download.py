#!/usr/bin/env python

import argparse

import ofxclient.util
import ofxclient.config

parser = argparse.ArgumentParser()
parser.add_argument("--days", default=40, type=int)
args = parser.parse_args()

def download_ofx():
    config = ofxclient.config.OfxConfig()
    data = ofxclient.util.combined_download(config.accounts(), days=args.days)
    f = open("data.ofx", "w")
    f.write(data.read())

download_ofx()
