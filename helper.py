#!/usr/bin/env python

import json
import sys

import xmltodict

with open(sys.argv[1], "rb") as inputf:
    print(json.dumps(xmltodict.parse(inputf), indent=2))
