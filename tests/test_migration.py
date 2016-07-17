import pytest
from migrations import migrations

def test_empty_list(tmpdir_factory):
    dir = tmpdir_factory.mktemp("empty_migrations")
    mig = migrations.Migrations(dir)
    assert(len(mig.list()) == 0)
