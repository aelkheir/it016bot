from logging import getLogger
from collections import defaultdict
from typing import Dict, Tuple, Any, Callable, Optional

from telegram.ext import DictPersistence, PicklePersistence
from telegram.utils.helpers import (
    encode_conversations_to_json,
    decode_conversations_from_json,
)

from flaskr import db
import json
from flaskr.models import ChatData, Conversation, UserData  # type: ignore[no-redef]


class PostgresPersistence(DictPersistence):
    """Using Postgresql database to make user/chat/bot data persistent across reboots.
    Attributes:
        store_user_data (:obj:`bool`): Whether user_data should be saved by this
            persistence class.
        store_chat_data (:obj:`bool`): Whether chat_data should be saved by this
            persistence class.
        store_bot_data (:obj:`bool`): Whether bot_data should be saved by this
            persistence class.
    Args:
        url (:obj:`str`, Optional) the postgresql database url.
        session (:obj:`scoped_session`, Optional): sqlalchemy scoped session.
        on_flush (:obj:`bool`, optional): if set to :obj:`True` :class:`PostgresPersistence`
            will only update bot/chat/user data when :meth:flush is called.
        **kwargs (:obj:`dict`): Arbitrary keyword Arguments to be passed to
            the DictPersistence constructor.
    """

    def __init__(
        self,
        on_flush: bool = False,
        **kwargs: Any,
    ) -> None:

        self._session = db.create_scoped_session()

        self.logger = getLogger(__name__)
        super().__init__(**kwargs)

        self.on_flush = on_flush
        self.__load_database()

    def __load_user_data(self):
        user_data = {}
        data = self._session.query(UserData).all()
        for record in data:
            user_data[record.user_id] = json.loads(record.data)
        
        return user_data

    def __load_chat_data(self):
        chat_data = {}
        data = self._session.query(ChatData).all()
        for record in data:
            chat_data[record.chat_id] = json.loads(record.data)
        
        return chat_data

    def __load_conversations(self):
        conversations = {}
        data = self._session.query(Conversation).order_by(Conversation.name).all()
        handler_name = ''
        for record in data:
            if handler_name != record.name:
                handler_name = record.name
                conversations[handler_name] = {}
            tuple_key = tuple(json.loads(record.key))
            conversations[handler_name][tuple_key] = record.new_state
        return conversations
        
    def __load_database(self) -> None:
        try:
            self.logger.info("Loading database....")
            self._chat_data = defaultdict(dict, self.__load_chat_data())
            self._user_data = defaultdict(dict, self.__load_user_data())
            self._conversations = defaultdict(dict, self.__load_conversations())
            # self._bot_data = data.get("bot_data", {})
            self.logger.info("Database loaded successfully!")

        finally:
            pass

    def update_conversation(
        self, name: str, key: Tuple[int, ...], new_state: Optional[object]
    ) -> None:
        """Will update the conversations for the given handler.
        Args:
            name (:obj:`str`): The handler's name.
            key (:obj:`tuple`): The key the state is changed for.
            new_state (:obj:`tuple` | :obj:`any`): The new state for the given key.
        """
        super().update_conversation(name, key, new_state)
        json_key = json.dumps(key)
        conv = self._session.query(Conversation) \
            .filter((Conversation.name==name) & (Conversation.key==json_key)) \
            .one_or_none()
        if conv:
            if conv.new_state == new_state:
                return
            conv.new_state = new_state
            self._session.commit()
        else:
            conv = Conversation(name=name, key=json_key, new_state=new_state)
            self._session.add(conv)
            self._session.commit()

    def update_user_data(self, user_id: int, data: Dict) -> None:
        """Will update the user_data (if changed).
        Args:
            user_id (:obj:`int`): The user the data might have been changed for.
            data (:obj:`dict`): The :attr:`telegram.ext.Dispatcher.user_data` ``[user_id]``.
        """
        super().update_user_data(user_id, data)
        user_data = self._session.query(UserData) \
            .filter(UserData.user_id==user_id) \
            .one_or_none()

        if user_data is None:
            user_data = UserData(user_id=user_id, data=json.dumps({}))
            self._session.add(user_data)
            self._session.commit()

        if user_data.data == json.dumps(data):
            return

        user_data.data = json.dumps(data)
        self._session.commit()

    def update_chat_data(self, chat_id: int, data: Dict) -> None:
        """Will update the chat_data (if changed).
        Args:
            chat_id (:obj:`int`): The chat the data might have been changed for.
            data (:obj:`dict`): The :attr:`telegram.ext.Dispatcher.chat_data` ``[chat_id]``.
        """
        super().update_chat_data(chat_id, data)
        chat_data = self._session.query(ChatData) \
            .filter(ChatData.chat_id==chat_id) \
            .one_or_none()

        if chat_data is None:
            chat_data = ChatData(chat_id=chat_id, data=json.dumps({}))
            self._session.add(chat_data)
            self._session.commit()

        if chat_data.data == json.dumps(data):
            return

        chat_data.data = json.dumps(data)
        self._session.commit()

    def update_bot_data(self, data: Dict) -> None:
        """Will update the bot_data (if changed).
        Args:
            data (:obj:`dict`): The :attr:`telegram.ext.Dispatcher.bot_data`.
        """
        super().update_bot_data(data)
