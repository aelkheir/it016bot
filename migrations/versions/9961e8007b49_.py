"""empty message

Revision ID: 9961e8007b49
Revises: 961602dff682
Create Date: 2022-07-24 15:09:40.221068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9961e8007b49'
down_revision = '961602dff682'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat_data', schema=None) as batch_op:
        batch_op.drop_constraint('uq_chat_data_chat_id_copy', type_='unique')
        batch_op.drop_column('chat_id_copy')

    with op.batch_alter_table('user_data', schema=None) as batch_op:
        batch_op.drop_constraint('uq_user_data_user_id_copy', type_='unique')
        batch_op.drop_column('user_id_copy')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('uq_users_chat_id_copy', type_='unique')
        batch_op.drop_constraint('uq_users_telegram_id_copy', type_='unique')
        batch_op.drop_column('telegram_id_copy')
        batch_op.drop_column('chat_id_copy')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('chat_id_copy', sa.BIGINT(), nullable=True))
        batch_op.add_column(sa.Column('telegram_id_copy', sa.BIGINT(), nullable=True))
        batch_op.create_unique_constraint('uq_users_telegram_id_copy', ['telegram_id_copy'])
        batch_op.create_unique_constraint('uq_users_chat_id_copy', ['chat_id_copy'])

    with op.batch_alter_table('user_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id_copy', sa.BIGINT(), nullable=True))
        batch_op.create_unique_constraint('uq_user_data_user_id_copy', ['user_id_copy'])

    with op.batch_alter_table('chat_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('chat_id_copy', sa.BIGINT(), nullable=True))
        batch_op.create_unique_constraint('uq_chat_data_chat_id_copy', ['chat_id_copy'])

    # ### end Alembic commands ###
