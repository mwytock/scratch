#!/usr/bin/env python

import ofxclient.util
import ofxclient.config

def download_ofx():
    config = ofxclient.config.OfxConfig()
    data = ofxclient.util.combined_download(config.accounts())
    f = open("data.ofx", "w")
    f.write(data.read())

download_ofx()
