import glob
from revision import Revision


class RevisionMap(object):
    def __init__(self):
        self.last = None
        self.map = {}

    def insert(self, revision):
        self.map[revision.revision] = revision

        if self.last is None or revision.revision > self.last.revision:
            self.last = revision

    def head(self):
        return self.map[0] if not self.map else None

    def next(self):
        return self.last.revision + 1 if self.last is not None else 0

    def __str__(self):
        if self.head is None:
            return "<EMPTY>"
        rev_str = ""

        for rev in range(self.next()):
            rev_str += str(self.map[rev])
            rev_str += "\n"
        return rev_str

    @staticmethod
    def create(path):
        rev_map = RevisionMap()
        for file_ in glob.glob("%s/*.py" % path):
            revision = Revision(path, file_)
            rev_map.insert(revision)
        return rev_map