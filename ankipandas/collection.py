#!/usr/bin/env python3

# std
from pathlib import Path
import shutil
import tempfile

import ankipandas.paths
import ankipandas.raw as raw
from ankipandas.ankidf import AnkiDataFrame


class Collection(object):
    def __init__(self, path, user=None):
        path = ankipandas.paths.db_path_input(path, user=user)

        #: Path to currently loaded database
        self.path = path

        self._working_dir = tempfile.TemporaryDirectory()
        self._working_path = Path(self._working_dir.name) / "collection.anki2"
        shutil.copy2(str(self.path), str(self._working_path))

        #: Opened Anki database (:class:`sqlite3.Connection`)
        self.db = raw.load_db(self._working_path)

        self.notes = AnkiDataFrame.init_with_table(self, "notes")
        self.cards = AnkiDataFrame.init_with_table(self, "cards")
        self.revs = AnkiDataFrame.init_with_table(self, "revs")

    def __del__(self):
        if self._working_dir is not None:
            self._working_dir.cleanup()

    def empty_notes(self):
        return AnkiDataFrame.init_with_table(self, "notes", empty=True)

    def empty_cards(self):
        return AnkiDataFrame.init_with_table(self, "cards", empty=True)

    def empty_revs(self):
        return AnkiDataFrame.init_with_table(self, "revs", empty=True)