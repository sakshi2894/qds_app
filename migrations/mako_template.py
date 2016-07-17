"""${message}

Revision ID: ${up_revision}
Create Date: ${create_date}

"""

# revision identifiers, used by Mojave.
revision = ${up_revision}

${imports if imports else ""}

def upgrade():
    ${upgrades if upgrades else "pass"}


def downgrade():
    ${downgrades if downgrades else "pass"}
