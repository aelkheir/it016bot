"""empty message

Revision ID: df9911c04389
Revises: 501fcb5eb349
Create Date: 2022-02-12 20:38:28.311068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df9911c04389'
down_revision = '501fcb5eb349'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('current_semester',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('semester_id', sa.Integer(), nullable=True),
    sa.CheckConstraint('id = 1', name=op.f('ck_current_semester_only_one_row')),
    sa.ForeignKeyConstraint(['semester_id'], ['semesters.id'], name=op.f('fk_current_semester_semester_id_semesters')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_current_semester'))
    )

    with op.batch_alter_table('semesters', schema=None) as batch_op:
        batch_op.drop_column('archived')


    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    with op.batch_alter_table('semesters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('archived', sa.BOOLEAN(), nullable=True))


    op.drop_table('current_semester')
    # ### end Alembic commands ###
