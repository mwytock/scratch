#!/usr/bin/python

import sys

from boto.glacier import layer2

if len(sys.argv) != 3:
    print >>sys.stderr, "Usage: ./upload.py <vault> <description>"
    sys.exit(1)

glacier = layer2.Layer2()
vault = glacier.get_vault(sys.argv[1])
archive_id = vault.create_archive_from_file(file_obj=sys.stdin,
                                            description=sys.argv[2])
print "Created archive", archive_id
