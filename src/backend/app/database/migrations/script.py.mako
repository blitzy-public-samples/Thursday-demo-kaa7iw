# Third-party imports
# alembic==1.7.7
# sqlalchemy==1.4.36

"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# Revision identifiers, used by Alembic
# Addresses requirement: Standardized database schema migration template
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    """Implements forward database schema changes.
    
    # Human tasks before running this migration:
    1. Backup database before applying migration
    2. Ensure no conflicting schema changes are pending
    3. Verify database connection settings in alembic.ini
    4. Schedule migration during low-traffic period
    5. Test migration in staging environment first
    """
    # Addresses requirement: Data validation and constraint enforcement
    ${upgrades if upgrades else "pass"}


def downgrade():
    """Implements backward database schema changes.
    
    # Human tasks before running this downgrade:
    1. Backup database before reverting migration
    2. Verify data integrity will be maintained after downgrade
    3. Ensure dependent migrations are reverted first
    4. Test downgrade in staging environment
    5. Have rollback plan ready
    """
    # Addresses requirement: Data validation and constraint enforcement
    ${downgrades if downgrades else "pass"}