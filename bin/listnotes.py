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

versions = []
earliest_seen = collections.OrderedDict()

# Determine the current version, which might be an unreleased or dev
# version.
current_version = subprocess.check_output(['git', 'describe', '--tags']).strip()

# FIXME(dhellmann): This might need to be more line-oriented in the
# production script.
history_results = subprocess.check_output(
    ['git', 'log', '--pretty=%x00%H %d', '--name-only', notesdir],
)
history = history_results.split('\x00')
current_version = current_version
for i, h in enumerate(history):
    h = h.strip()
    if not h:
        continue
    print('-' * 30)
    print(h)

    hlines = h.splitlines()
    tags = TAG_PAT.findall(hlines[0])
    print(tags)
    filenames = hlines[2:]

    if not tags:
        tags = [current_version]
    else:
        current_version = tags[0]

    if current_version not in versions:
        versions.append(current_version)

    for f in filenames:
        # Updated as older tags are found, handling edits to release
        # notes.
        earliest_seen[f] = tags[0]

# Invert earliest_seen to make a list for each version.
files_and_tags = collections.OrderedDict()
for v in versions:
    files_and_tags[v] = []
for filename, version in earliest_seen.items():
    files_and_tags[version].append(filename)

for t, filenames in files_and_tags.items():
    print(t, filenames)
