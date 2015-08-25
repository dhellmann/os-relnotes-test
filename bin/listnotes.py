#!/usr/bin/env python
"""Produce a list of notes, in the order they were added, by version.
"""

from __future__ import print_function

import argparse
import collections
import os
import re
import subprocess

TAG_PAT = re.compile('tag: ([\d\.]+)')

parser = argparse.ArgumentParser()
parser.add_argument('relnotesdir', nargs='?', default='releasenotes')
args = parser.parse_args()

relnotesdir = args.relnotesdir
notesdir = os.path.join(relnotesdir, 'notes')

files_and_tags = collections.OrderedDict()

# Determine the current version, which might be an unreleased or dev
# version.
current_version = subprocess.check_output(['git', 'describe', '--tags']).strip()

# FIXME(dhellmann): This might need to be more line-oriented in the
# production script.
history_results = subprocess.check_output(
    ['git', 'log', '--pretty=%x00%H %d', '--name-only', notesdir],
)
history = history_results.split('\x00')
previous_version = current_version
for i, h in enumerate(history):
    h = h.strip()
    if not h:
        continue
    print('-' * 30)
    print(i)
    hlines = h.splitlines()
    tags = TAG_PAT.findall(hlines[0])
    print(tags)
    filenames = hlines[2:]
    if not tags:
        tags = [previous_version]
    else:
        previous_version = tags[0]
    for t in tags:
        files_and_tags.setdefault(t, []).extend(filenames)
    print(filenames)
    print('-' * 30)

for t, filenames in files_and_tags.items():
    print(t, filenames)
