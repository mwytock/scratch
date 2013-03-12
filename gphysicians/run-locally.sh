#!/bin/bash -eu
# Copyright 2012 Google Inc. All Rights Reserved.
# Author: mwytock@google.com (Matt Wytock)
#
# Runs the app locally, port 8080

blaze-bin/apphosting/tools/dev_appserver_internal_main \
--address=0.0.0.0 \
experimental/users/mwytock/meds \
$*
