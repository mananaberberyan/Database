from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('equipment', sa.Column('new_column', sa.String(), nullable=True))

def downgrade():
    op.drop_column('equipment', 'new_column')