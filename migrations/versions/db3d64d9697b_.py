"""empty message

Revision ID: db3d64d9697b
Revises: 9961e8007b49
Create Date: 2022-08-12 00:09:36.724870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db3d64d9697b'
down_revision = '9961e8007b49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assignments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('assignment_number', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], name=op.f('fk_assignments_course_id_courses')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_assignments'))
    )

    with op.batch_alter_table('documents', schema=None) as batch_op:
        batch_op.add_column(sa.Column('assignment_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_documents_assignment_id_assignments'), 'assignments', ['assignment_id'], ['id'])

    with op.batch_alter_table('photos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('assignment_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_photos_assignment_id_assignments'), 'assignments', ['assignment_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('photos', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_photos_assignment_id_assignments'), type_='foreignkey')
        batch_op.drop_column('assignment_id')

    with op.batch_alter_table('documents', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_documents_assignment_id_assignments'), type_='foreignkey')
        batch_op.drop_column('assignment_id')


    op.drop_table('assignments')
    # ### end Alembic commands ###
