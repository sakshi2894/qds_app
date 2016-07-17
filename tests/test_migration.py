import pytest
import inspect
import os.path
from migrations import migrations


def test_empty_list(tmpdir_factory):
    path = tmpdir_factory.mktemp("empty_migrations")
    mig = migrations.Migrations(path)
    assert(len(mig.list()) == 0)


def test_generate_first_migration(tmpdir_factory):
    path = tmpdir_factory.mktemp("first_migration")
    mig = migrations.Migrations(path)
    migration_path = mig.generate("First Migration")
    assert(os.path.exists(migration_path))


def test_single_upgrade():
    path = "%s/fixtures/upgrade" % \
        os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    mig = migrations.Migrations(path)
    mig.upgrade()
    assert True


def test_single_pending():
    path = "%s/fixtures/upgrade" % \
        os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    mig = migrations.Migrations(path)
    pending = mig.pending()
    assert (len(pending) == 1)

