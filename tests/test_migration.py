import pytest
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