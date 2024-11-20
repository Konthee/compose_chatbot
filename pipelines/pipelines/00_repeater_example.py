from typing import List, Union, Generator, Iterator, Optional
import uuid

class Pipeline:
    def __init__(self):
        self.name = "00 Repeater Example"
        self.section_id = None  # Initialize section_id as None

    async def on_startup(self):
        # print(f"on_startup: {__name__}")
        pass

    async def on_shutdown(self):
        # print(f"on_shutdown: {__name__}")
        pass

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        print('inlet')
        return body

    async def outlet(self, body: dict, user: Optional[dict] = None) -> dict:
        print('outlet')
        return body

    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict,__user__:Optional[dict]=None) -> Union[str, Generator, Iterator]:
        
        # If you'd like to check for title generation, you can add the following check
        if body.get("stream") == True:
            if len(messages) == 1:
                self.section_id = str(uuid.uuid4())  # Generate a new section_id
                print(f"New section_id generated: {self.section_id}")

        print('body: \n', body)
        print('messages: \n', messages)
        print(f"section_id: {self.section_id}")
        print(f"received message from user: {user_message}")

        return f"received message from user: {user_message}"
