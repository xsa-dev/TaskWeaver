from typing import Any, Generator, List


from taskweaver.llm.base import CompletionService, EmbeddingService, LLMServiceConfig
from taskweaver.llm.util import ChatMessageType

from hugchat import ChatBot
from hugchat import Login
import os


EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


class HugchatServiceConfig(LLMServiceConfig):
    def _configure(self) -> None:
        self._set_name("hugchat")
        self.chatbot = None
        self.auth()
        self.chatbot.new_conversation()


    def auth(self):
        sign = Login(EMAIL, PASSWORD)
        cookies = sign.login()
        sign.saveCookiesToDir("./fortest")
        assert cookies is not None
        self.chatbot = ChatBot(cookies=cookies.get_dict(),
                               default_llm=0)



class HugchatService(CompletionService, EmbeddingService):
    def __init__(self, config: HugchatServiceConfig):
        self.config = config

    def chat_completion(self, messages: List[ChatMessageType], use_backup_engine: bool = False, stream: bool = True, temperature: float | None = None, max_tokens: int | None = None, top_p: float | None = None, stop: List[str] | None = None, **kwargs: Any) -> Generator[ChatMessageType, None, None]:
        res = str(self.chatbot.chat("Just reply me `test_ok`"))
        assert res is not None