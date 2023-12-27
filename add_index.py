from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_index('idx_equipment_name', 'equipment', ['equipment_name'], unique=False)

def downgrade():
    op.drop_index('idx_equipment_name', table_name='equipment')