"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# Revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: str | None = ${repr(down_revision)}
branch_labels: tuple[str] | None = ${repr(branch_labels)}
depends_on: tuple[str] | None = ${repr(depends_on)}


def upgrade() -> None:
    """Apply migration changes (upgrade schema)."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Revert migration changes (downgrade schema)."""
    ${downgrades if downgrades else "pass"}
