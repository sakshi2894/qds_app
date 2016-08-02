"""First Migration

Revision ID: 1
Create Date: 2016/07/16

"""

# revision identifiers, used by Mojave.
revision = 0


def upgrade(context):
    context["revisions.upgraded"].append(0)


def downgrade(context):
    context["revisions.downgraded"].append(0)
