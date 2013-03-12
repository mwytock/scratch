#!/bin/bash -eu
# Copyright 2012 Google Inc. All Rights Reserved.
# Author: mwytock@google.com (Matt Wytock)
#
# Push the app to prod

blaze build -c opt apphosting/tools:appcfg_over_stubby

blaze-bin/apphosting/tools/appcfg_over_stubby update \
experimental/users/mwytock/meds

