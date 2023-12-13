import asyncio
from datetime import datetime
import time
import os
from typing import List, Optional
from continuedev.libs.util.paths import getGlobalFolderPath
from openai import OpenAIError
import openai
import sqlite3


from continuedev.libs.util.count_tokens import CONTEXT_LENGTH_FOR_MODEL
from openai import OpenAI
from pydantic import validator
from continuedev.core.main import ChatMessage, SetStep
from .base import LLM
from ...libs.util.logging import getLogger
from .proxy_server import ProxyServer


logger = getLogger("OpenAIProxy")


class OpenAIProxy(LLM):
    """
    With the `OpenAIProxy` you use OpenAi's Proxys.



    ```python title="~/.continue/config.py"
    from continuedev.libs.llm.openai_proxy import OpenAIProxy
    API_KEY = "<API_KEY>"
    config = ContinueConfig(
        disable_summaries=True,
        ...
        models=Models(
            default=OpenAI(
                api_key="EMPTY",
                model="gpt35turbo",
                api_base="http://localhost:8000", # change to your server
            )
        )
    )
    ```

    The `OpenAIFreeTrial` class will automatically switch to using your API key instead of ours. If you'd like to explicitly use one or the other, you can use the `ProxyServer` or `OpenAI` classes instead.

    These classes support any models available through the OpenAI API, assuming your API key has access, including "gpt-4", "gpt-3.5-turbo", "gpt-3.5-turbo-16k", and "gpt-4-32k".

    """

    api_key: Optional[str] = None
    assistant_id: Optional[str] = None
    llm: Optional[LLM] = None
    project_dir: Optional[str] = None

    _name: Optional[str] = None

    _conn: Optional[sqlite3.connect] = None
    _session_2_thread_map: dict = {}

    @validator("context_length")
    def context_length_for_model(cls, v, values):
        return CONTEXT_LENGTH_FOR_MODEL.get(values["model"], 128000)

    def start(self, unique_id: Optional[str] = None):
        super().start(unique_id=unique_id)
        self._name = f"agt_{unique_id[-6:]}"

       

    async def _stream_complete(self, prompt, options):
        return

    async def _stream_chat(self, messages: List[ChatMessage], options):
        if options.session_id is None:
            logger.error(f"{self._name}:session_id is None")
            return

        message = messages[-1]
      
        logger.info(
            f"{self._name}: REQUEST {message.role} - {message.content}"
        )

        # This is where we can pass the runner to the soon to be built OpenAIFunction Step
        from continuedev.plugins.steps.openai_agency import OpenAIAgency

        yield OpenAIAgency(
            api_key=self.api_key,
            user_input= message.content,
            name=self._name,
            content="",
        )

       # yield ChatMessage(role="assistant", content="done", summary="done")
     



        
        
     


