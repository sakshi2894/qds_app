import datetime
import inspect
import logging
import os
import string
import tempfile
from mako.template import Template
from mako import exceptions
from revision_map import RevisionMap


class Migrations(object):
    def __init__(self, path):
        self.path = path
        self.base_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        self.revision_map = RevisionMap.create(path)

    def generate(self, message):
        revision = self.revision_map.next()
        template = Template(filename="%s/script.py.mako" % self.base_path)
        destination_name = args.message[:15] if len(message) > 15 else message
        destination_name = string.replace(destination_name, ' ', '_')
        destination_path = "%s/%s_%s.py" % (self.path, revision, destination_name)

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
            with open(destination_path, 'wb') as f:
                f.write(output)
        logging.info("Created new migration `%s` " % destination_path)

    def list(self):
        return self.revision_map.list()
