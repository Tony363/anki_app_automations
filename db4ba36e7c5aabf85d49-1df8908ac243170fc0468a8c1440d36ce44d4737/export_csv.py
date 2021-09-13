# -*- coding: utf-8 -*-
"""Anki add-on which adds "Notes in CSV format" option of Export desc dialog.

Copyright (c) 2015 Alex Chekunkov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""
import csv

from anki.exporting import Exporter
from anki.hooks import addHook
from anki.lang import _
from anki.utils import  ids2str, splitFields


class CSVNoteExporter(Exporter):

    key = _("Notes in CSV format")
    ext = ".csv"
    db_query = """
    select guid, flds, tags from notes
    where id in
    (select nid from cards
    where cards.id in %s)
    """

    def __init__(self, col):
        super(CSVNoteExporter, self).__init__(col)
        self.includeID = False
        self.includeTags = True

    def doExport(self, file):
        writer = csv.writer(file)
        cardIds = self.cardIds()
        self.count = 0
        for _id, flds, tags in self.col.db.execute(self.db_query % ids2str(cardIds)):
            row = []
            # note id
            if self.includeID:
                row.append(str(_id))
            # fields
            row.extend([self.escapeText(f) for f in splitFields(flds)])
            # tags
            if self.includeTags:
                row.append(tags.strip())
            self.count += 1
            writer.writerow([x.encode("utf-8") for x in row])


def _id(obj):
    return ("%s (*%s)" % (obj.key, obj.ext), obj)

def update_exporters_list(exps):
	exps.append(_id(CSVNoteExporter))

addHook("exportersList", update_exporters_list)