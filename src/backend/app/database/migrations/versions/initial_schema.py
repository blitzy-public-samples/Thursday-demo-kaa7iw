"""Initial database migration that creates the core tables.

Human Tasks:
1. Verify PostgreSQL extensions for UUID support are enabled
2. Review database audit logging configuration
3. Confirm row-level security policies are properly configured
4. Check database user permissions for CRUD operations
5. Verify PostgreSQL version supports all used features (14+)
"""

# External imports - versions specified as per requirements
from alembic import op  # version: 1.7+
import sqlalchemy as sa  # version: 1.4+
from sqlalchemy.dialects import postgresql

# Internal imports
from ....models.base import metadata

# Revision identifiers
revision = 'initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    """Creates all initial database tables and relationships.
    
    Requirement: 1.2 Scope/4. Data Management - Initial database schema setup
    Requirement: 2.2.2 Database Schema - Implementation of core tables
    """
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                 server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('last_login', sa.TIMESTAMP(timezone=True)),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        
        # Constraints
        sa.UniqueConstraint('email', name='uq_users_email'),
        sa.CheckConstraint("email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
                          name='ck_users_email_format')
    )
    
    # Create projects table
    op.create_table(
        'projects',
        sa.Column('project_id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                 server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                 server_default=sa.text('CURRENT_TIMESTAMP'),
                 onupdate=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        
        # Constraints
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'],
                              name='fk_projects_user_id',
                              ondelete='CASCADE'),
        sa.CheckConstraint("LENGTH(TRIM(title)) > 0",
                          name='ck_projects_title_not_empty')
    )
    
    # Create specifications table
    op.create_table(
        'specifications',
        sa.Column('spec_id', sa.Integer(), primary_key=True),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                 server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                 server_default=sa.text('CURRENT_TIMESTAMP'),
                 onupdate=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        
        # Constraints
        sa.ForeignKeyConstraint(['project_id'], ['projects.project_id'],
                              name='fk_specifications_project_id',
                              ondelete='CASCADE'),
        sa.CheckConstraint("LENGTH(TRIM(content)) > 0",
                          name='ck_specifications_content_not_empty')
    )
    
    # Create bullet_items table
    op.create_table(
        'bullet_items',
        sa.Column('item_id', sa.Integer(), primary_key=True),
        sa.Column('spec_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                 server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                 server_default=sa.text('CURRENT_TIMESTAMP'),
                 onupdate=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        
        # Constraints
        sa.ForeignKeyConstraint(['spec_id'], ['specifications.spec_id'],
                              name='fk_bullet_items_spec_id',
                              ondelete='CASCADE'),
        sa.CheckConstraint('order >= 0 AND order < 10',
                          name='ck_bullet_items_order_range'),
        sa.CheckConstraint("LENGTH(TRIM(content)) > 0",
                          name='ck_bullet_items_content_not_empty'),
        sa.UniqueConstraint('spec_id', 'order',
                           name='uq_bullet_items_spec_order')
    )
    
    # Create indexes for performance optimization
    op.create_index('idx_projects_user_id', 'projects', ['user_id'],
                    postgresql_where=sa.text('NOT is_deleted'))
    op.create_index('idx_specifications_project_id', 'specifications', ['project_id'],
                    postgresql_where=sa.text('NOT is_deleted'))
    op.create_index('idx_bullet_items_spec_id', 'bullet_items', ['spec_id'],
                    postgresql_where=sa.text('NOT is_deleted'))
    op.create_index('idx_bullet_items_order', 'bullet_items', ['spec_id', 'order'],
                    postgresql_where=sa.text('NOT is_deleted'))
    
    # Create full text search indexes
    op.execute(
        """
        CREATE INDEX idx_projects_title_search ON projects 
        USING gin(to_tsvector('english', title)) 
        WHERE NOT is_deleted
        """
    )
    op.execute(
        """
        CREATE INDEX idx_specifications_content_search ON specifications 
        USING gin(to_tsvector('english', content)) 
        WHERE NOT is_deleted
        """
    )
    
    # Enable row-level security
    op.execute("ALTER TABLE projects ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE specifications ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE bullet_items ENABLE ROW LEVEL SECURITY")
    
    # Create row-level security policies
    op.execute(
        """
        CREATE POLICY projects_access_policy ON projects
        FOR ALL
        TO authenticated
        USING (user_id = current_user_id())
        """
    )
    op.execute(
        """
        CREATE POLICY specifications_access_policy ON specifications
        FOR ALL
        TO authenticated
        USING (project_id IN (
            SELECT project_id FROM projects 
            WHERE user_id = current_user_id()
        ))
        """
    )
    op.execute(
        """
        CREATE POLICY bullet_items_access_policy ON bullet_items
        FOR ALL
        TO authenticated
        USING (spec_id IN (
            SELECT spec_id FROM specifications 
            WHERE project_id IN (
                SELECT project_id FROM projects 
                WHERE user_id = current_user_id()
            )
        ))
        """
    )

def downgrade():
    """Removes all created tables in correct order respecting foreign key constraints.
    
    Requirement: 1.2 Scope/4. Data Management - Database schema rollback
    """
    # Drop row-level security policies
    op.execute("DROP POLICY IF EXISTS bullet_items_access_policy ON bullet_items")
    op.execute("DROP POLICY IF EXISTS specifications_access_policy ON specifications")
    op.execute("DROP POLICY IF EXISTS projects_access_policy ON projects")
    
    # Drop search indexes
    op.execute("DROP INDEX IF EXISTS idx_specifications_content_search")
    op.execute("DROP INDEX IF EXISTS idx_projects_title_search")
    
    # Drop performance indexes
    op.drop_index('idx_bullet_items_order', table_name='bullet_items')
    op.drop_index('idx_bullet_items_spec_id', table_name='bullet_items')
    op.drop_index('idx_specifications_project_id', table_name='specifications')
    op.drop_index('idx_projects_user_id', table_name='projects')
    
    # Drop tables in reverse order to respect foreign key constraints
    op.drop_table('bullet_items')
    op.drop_table('specifications')
    op.drop_table('projects')
    op.drop_table('users')