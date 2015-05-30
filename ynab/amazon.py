#!/usr/bin/env python

import csv
import sys

def parse_price(price):
    assert price[0] == "$"
    return float(price[1:])

writer = csv.writer(sys.stdout)
writer.writerow(["Date", "Payee", "Category", "Outflow"])
for row in csv.DictReader(sys.stdin):
    writer.writerow([
        row["Order Date"],
        row["Title"],
        row["Category"],
        (parse_price(row["Item Subtotal"]) +
         parse_price(row["Item Subtotal Tax"]))])
