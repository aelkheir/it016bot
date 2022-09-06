"""empty message

Revision ID: 8e9c1b692420
Revises: 949c1f5e0487
Create Date: 2022-09-03 14:36:00.786416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e9c1b692420'
down_revision = '949c1f5e0487'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tutorials',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tutorial_number', sa.Integer(), nullable=True),
    sa.Column('published', sa.Boolean(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], name=op.f('fk_tutorials_course_id_courses')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_tutorials'))
    )
    with op.batch_alter_table('documents', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tutorial_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_documents_tutorial_id_tutorials'), 'tutorials', ['tutorial_id'], ['id'])

    with op.batch_alter_table('videos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tutorial_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_videos_tutorial_id_tutorials'), 'tutorials', ['tutorial_id'], ['id'])

    with op.batch_alter_table('youtube_links', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tutorial_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_youtube_links_tutorial_id_tutorials'), 'tutorials', ['tutorial_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('youtube_links', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_youtube_links_tutorial_id_tutorials'), type_='foreignkey')
        batch_op.drop_column('tutorial_id')

    with op.batch_alter_table('videos', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_videos_tutorial_id_tutorials'), type_='foreignkey')
        batch_op.drop_column('tutorial_id')

    with op.batch_alter_table('documents', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_documents_tutorial_id_tutorials'), type_='foreignkey')
        batch_op.drop_column('tutorial_id')

    op.drop_table('tutorials')
    # ### end Alembic commands ###
