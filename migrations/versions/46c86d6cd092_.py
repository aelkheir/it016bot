"""empty message

Revision ID: 46c86d6cd092
Revises: 806513400cf6
Create Date: 2022-07-24 03:32:09.245276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46c86d6cd092'
down_revision = '806513400cf6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat_data', schema=None) as batch_op:
        batch_op.alter_column('chat_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=False)

    with op.batch_alter_table('user_data', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=False)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('telegram_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=True)
        batch_op.alter_column('chat_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('chat_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=True)
        batch_op.alter_column('telegram_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=True)

    with op.batch_alter_table('user_data', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    with op.batch_alter_table('chat_data', schema=None) as batch_op:
        batch_op.alter_column('chat_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###