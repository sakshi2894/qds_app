import datetime
import inspect
import logging
import os
import string
import tempfile
from mako.template import Template
from mako import exceptions
from revision_map import RevisionMap


class Migration(object):
    @classmethod
    def setup_parsers(cls, sub_parser):
        cls.parser = sub_parser.add_parser("migration",
                                           help="Function for Mojave migrations")

        cls.sub_parser = cls.parser.add_subparsers()

        cls.generate_parser = cls.sub_parser.add_parser("generate",
                                                        help="Generate a new migration")
        cls.generate_parser.add_argument("-m", "--message", required=True,
                                         help="Provide a message describing the migration")
        cls.generate_parser.set_defaults(func=cls.generate_cmd)

        cls.list_parser = cls.sub_parser.add_parser("list",
                                                    help="List all migrations")
        cls.list_parser.set_defaults(func=cls.list_cmd)

    @classmethod
    def generate_cmd(cls, config, args):
        migration = Migration(config, args)
        migration.generate()

    @classmethod
    def list_cmd(cls, config, args):
        migration = Migration(config, args)
        print str(migration.revision_map)

    def __init__(self, config, args):
        self.config = config
        self.args = args
        self.base_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        self.revision_map = RevisionMap.create("%s/../../migrations/" % self.base_path)

    def generate(self):
        revision = self.revision_map.next()
        template = Template(filename="%s/script.py.mako" % self.base_path)
        destination_name = args.message[:15] if len(self.args.message) > 15 else self.args.message
        destination_name = string.replace(destination_name, ' ', '_')
        destination_path = "%s/../../migrations/%s_%s.py" % (self.base_path, revision, destination_name)

        try:
            output = template.render_unicode(up_revision=revision,
                                             create_date=datetime.datetime.now(),
                                             message=self.args.message).encode("utf-8")
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
