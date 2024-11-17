import uuid
import psycopg
import pandas as pd
from langchain_postgres import PostgresChatMessageHistory
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from typing import List, Dict, Any, Union

# Mapping roles to message classes
ROLE_MAP = {
    "system": SystemMessage,
    "user": HumanMessage,
    "assistant": AIMessage,
}

# Reverse mapping message classes to roles
MESSAGE_ROLE_MAP = {v: k for k, v in ROLE_MAP.items()}

def convert_messages(messages: List[Dict[str, Any]]) -> List[Union[SystemMessage, HumanMessage, AIMessage]]:
    """Convert list of message dicts to message class instances."""
    return [
        ROLE_MAP[msg["role"]](content=msg["content"])
        for msg in messages if msg["role"] in ROLE_MAP
    ]

def convert_messages_back(messages: List[Union[SystemMessage, HumanMessage, AIMessage]]) -> List[Dict[str, str]]:
    """Convert message class instances back to list of message dicts."""
    return [
        {"role": MESSAGE_ROLE_MAP.get(type(msg)), "content": msg.content}
        for msg in messages
    ]

class PostgresHelper:
    """Helper class for PostgreSQL database interaction."""
    def __init__(self, connection_string, schema=None):
        self.connection_string = connection_string
        self.options = f"-c search_path={schema}" if schema else None

    def execute_query(self, query: str):
        """Execute a SQL query."""
        with psycopg.connect(self.connection_string, options=self.options) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()

    def read_sql(self, query: str) -> pd.DataFrame:
        """Read SQL query into a pandas DataFrame."""
        with psycopg.connect(self.connection_string, options=self.options) as conn:
            return pd.read_sql(query, conn)

class LangchainPostgresChatHistory:
    """Manages chat history storage in a PostgreSQL database."""
    def __init__(self, connection_string, table_name="chat_history", session_id=None, schema=None):
        self.connection_string = connection_string
        self.options = f"-c search_path={schema}" if schema else None
        self.table_name = table_name
        self.session_id = session_id or str(uuid.uuid4())

    def create_table(self):
        """Create the chat history table."""
        with psycopg.connect(self.connection_string, options=self.options) as conn:
            PostgresChatMessageHistory.create_tables(conn, self.table_name)
        print(f"Table {self.table_name} created successfully in schema.")

    def add_messages(self, messages: List[Dict[str, Any]]):
        """Add messages to the chat history."""
        converted_messages = convert_messages(messages)
        with psycopg.connect(self.connection_string, options=self.options) as conn:
            chat_history = PostgresChatMessageHistory(
                self.table_name, self.session_id, sync_connection=conn
            )
            chat_history.add_messages(converted_messages)

    def get_messages(self) -> List[Dict[str, str]]:
        """Retrieve messages from the chat history."""
        with psycopg.connect(self.connection_string, options=self.options) as conn:
            chat_history = PostgresChatMessageHistory(
                self.table_name, self.session_id, sync_connection=conn
            )
            messages = chat_history.get_messages()
        return convert_messages_back(messages)

    def clear_history(self):
        """Delete all chat history for the current session."""
        with psycopg.connect(self.connection_string, options=self.options) as conn:
            with conn.cursor() as cur:
                delete_query = f"""
                DELETE FROM {self.table_name}
                WHERE session_id = %s;
                """
                cur.execute(delete_query, (self.session_id,))
                conn.commit()


