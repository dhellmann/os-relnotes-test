#!/usr/bin/env python

import argparse
import os
import uuid

parser = argparse.ArgumentParser()
parser.add_argument('--relnotesdir', default='releasenotes')
parser.add_argument('slug')
args = parser.parse_args()

relnotesdir = args.relnotesdir
notesdir = os.path.join(relnotesdir, 'notes')

slug = args.slug.replace(' ', '-')

template = """\
---
prelude: >
    Replace this text.
critical:
  - Add critical notes here, or remove this section.
security:
  - Add security notes here, or remove this section.
other:
  - Add other notes here, or remove this section.
"""

for i in range(50):
    newid = str(uuid.uuid4())
    notefilename = os.path.join(notesdir, '%s-%s.yaml' % (newid, slug))
    if not os.path.exists(notefilename):
        if not os.path.exists(notesdir):
            os.makedirs(notesdir)
        with open(notefilename, 'w') as f:
            f.write(template)
        print newid
        break
else:
    raise ValueError('Unable to generate random id after 50 tries')
