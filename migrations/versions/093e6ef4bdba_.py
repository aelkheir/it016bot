"""empty message

Revision ID: 093e6ef4bdba
Revises: 3fd80a5c9d9f
Create Date: 2021-09-10 03:41:07.699916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '093e6ef4bdba'
down_revision = '3fd80a5c9d9f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('labs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lab_number', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], name=op.f('fk_labs_course_id_courses')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_labs'))
    )
    with op.batch_alter_table('documents', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lab_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_documents_lab_id_labs'), 'labs', ['lab_id'], ['id'])

    with op.batch_alter_table('videos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lab_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_videos_lab_id_labs'), 'labs', ['lab_id'], ['id'])

    with op.batch_alter_table('youtube_links', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lab_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_youtube_links_lab_id_labs'), 'labs', ['lab_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('youtube_links', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_youtube_links_lab_id_labs'), type_='foreignkey')
        batch_op.drop_column('lab_id')

    with op.batch_alter_table('videos', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_videos_lab_id_labs'), type_='foreignkey')
        batch_op.drop_column('lab_id')

    with op.batch_alter_table('documents', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_documents_lab_id_labs'), type_='foreignkey')
        batch_op.drop_column('lab_id')

    op.drop_table('labs')
    # ### end Alembic commands ###
