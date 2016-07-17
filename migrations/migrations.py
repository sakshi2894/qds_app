import datetime
import glob
import inspect
import io
import logging
import os
import string
import tempfile
from mako.template import Template
from mako import exceptions
from revision import Revision


class Migrations(object):
    def __init__(self, path):
        self.last = None
        self.map = {}

        self.path = path
        self.base_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

        for file_ in glob.glob("%s/*.py" % path):
            revision = Revision(path, file_)
            self.insert(revision)

    def insert(self, revision):
        self.map[revision.revision] = revision

        if self.last is None or revision.revision > self.last.revision:
            self.last = revision

    def head(self):
        return self.map[0] if not self.map else None

    def next(self):
        return self.last.revision + 1 if self.last is not None else 0

    def list(self):
        revisions = []
        for rev in range(self.next()):
            revisions.append(rev)

        return revisions

    def __str__(self):
        if self.head is None:
            return "<EMPTY>"
        rev_str = ""

        for rev in range(self.next()):
            rev_str += str(self.map[rev])
            rev_str += "\n"
        return rev_str

    def _generate(self, message, out_stream):
        revision = self.next()
        template = Template(filename="%s/script.py.mako" % self.base_path)

        try:
            output = template.render_unicode(up_revision=revision,
                                             create_date=datetime.datetime.now(),
                                             message=message).encode("utf-8")
        except:
            with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as ntf:
                ntf.write(
                    exceptions.text_error_template().
                    render_unicode().encode("utf-8"))
                fname = ntf.name
            raise Exception(
                "Template rendering failed; see %s for a "
                "template-oriented traceback." % fname)
        else:
            out_stream.write(output)

    def generate_str(self, message):
        out_stream = io.StringIO()
        self._generate(message, out_stream)
        return out_stream.getvalue()

    def generate(self, message):
        revision = self.next()

        destination_name = message[:15] if len(message) > 15 else message
        destination_name = string.replace(destination_name, ' ', '_')
        destination_path = "%s/%s_%s.py" % (self.path, revision, destination_name)

        out_stream = io.FileIO(destination_path, "wb")
        self._generate(message, out_stream)
        logging.info("Created new migration `%s` " % destination_path)
        return destination_path
