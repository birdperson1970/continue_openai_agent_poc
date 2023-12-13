import os
from typing import Any, List

from agency_swarm import set_openai_key

from agency_swarm import Agency
from continuedev.core.main import ChatMessage, SetStep, Step, DeltaStep
from continuedev.core.sdk import ContinueSDK, Models
from continuedev.plugins.steps.openai_agency_tools import CurrentTimeTool, GetProjectFile, GoogleSearchTool, ListProjectFiles
from continuedev.plugins.steps.shell_tool import ShellTool
from ...libs.util.logging import getLogger
from langchain.tools import YouTubeSearchTool
from agency_swarm.tools import ToolFactory

logger = getLogger('OpenAIAgency')
from agency_swarm import Agent

from langchain.agents import load_tools

# os.environ["GOOGLE_CSE_ID"] = ""
# os.environ["GOOGLE_API_KEY"] = ""

logger.info(f"GOOGLE_CSE_ID={os.getenv('GOOGLE_CSE_ID')}  GOOGLE_API_KEY={os.getenv('GOOGLE_API_KEY')}")


#tools = load_tools(["llm-math", "serpapi"])


from langchain.tools import YouTubeSearchTool
from agency_swarm.tools import ToolFactory
tools =[]
tools.append(ToolFactory.from_langchain_tool(YouTubeSearchTool))
#tools = ToolFactory.from_langchain_tool(ShellTool)


tools.append(CurrentTimeTool)
tools.append(GoogleSearchTool)
tools.append(ListProjectFiles)
tools.append(GetProjectFile)
tools.append(ShellTool)




ceo = Agent(name="CEO",
            description="Responsible for client communication, task planning and management.",
            instructions="You must converse with other agents to ensure complete task execution.", # can be a file like ./instructions.md
            files_folder=None,
            tools=tools)

dev = Agent(name="DEV",
            description="Responsible for client communication, task planning and management.",
            instructions="You must converse with other agents to ensure complete task execution.", # can be a file like ./instructions.md
            files_folder=None,
            tools=tools)

va = Agent(name="Virtual Assitant",
            description="Responsible for client communication, task planning and management.",
            instructions="You must converse with other agents to ensure complete task execution.", # can be a file like ./instructions.md
            files_folder=None,
            tools=tools)



class OpenAIAgency(Step):
    api_key: str
    user_input: str
    name: str
    content: str
    _sdk: ContinueSDK
    complete: bool = False
    _agency: Agency = None

    async def describe(self, models: Models):
        return f"`OpenAI Agency`."

    async def run(self, sdk: ContinueSDK): 
        OpenAIAgency._sdk = sdk   
        sdk.config.disable_summaries=True
        print (f" OpenAIAgency._agency={OpenAIAgency._agency}")
        print(f"Type of OpenAIAgency._agency: {type(OpenAIAgency._agency)}")

        if type(OpenAIAgency._agency) != Agency:
            OpenAIAgency._agency = Agency([
                ceo,  # CEO will be the entry point for communication with the user
                [ceo, dev],  # CEO can initiate communication with Developer
                [ceo, va],   # CEO can initiate communication with Virtual Assistant
                [dev, va]    # Developer can initiate communication with Virtual Assistant
            ], shared_instructions='docs/agents/manifesto.md') # shared instructions for all agents

        gen= (OpenAIAgency._agency.get_completion(self.user_input))
       
        try:
            # Yield each message from the generator
            for bot_message in gen:
                msg = bot_message.get_sender_emoji() + " " + bot_message.get_formatted_content()
                print(f"msg: {msg}")
                # yield ChatMessage(
                #         role="assistant",
                #         description= msg,                                                      
                # )    
                #yield ChatMessage(role="assistant", content=msg, summary=msg)
                self.chat_context.append(
                    ChatMessage(role="assistant", content=msg, summary=msg)
                    #ChatMessage(role="user", content=self.user_input, summary=self.user_input)
                )
                yield DeltaStep(description=msg)
                    
                
        except StopIteration:
            # Handle the end of the conversation if necessary
            self.complete = True
