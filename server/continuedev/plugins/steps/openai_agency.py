import os

from agency_swarm import set_openai_key


from agency_swarm.tools import BaseTool
from continuedev.core import ContinueSDK
from pydantic import Field
from datetime import datetime
import pytz

class MyCustomTool(BaseTool):
    """
    get the current time
    """

    # Define the fields with descriptions using Pydantic Field
    timezone_str: str = Field(
        ..., description="The timezone you want the time in."
    )

    # Additional fields as required
    # ...

    def run(self):
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method should utilize the fields defined above to perform its task.
        Doc string description is not required for this method.
        """
        try:
            # Create a timezone object using the pytz library
            timezone = pytz.timezone(self.timezone_str)
            
            # Get the current time in UTC
            utc_dt = datetime.now(pytz.utc)
            
            # Convert the UTC time to the specified timezone
            dt = utc_dt.astimezone(timezone)
            
            # Print the current time in the specified timezone
            print(f"The current time in {self.timezone_str} is {dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
            return dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')
            
        except pytz.exceptions.UnknownTimeZoneError:
            print(f"Unknown timezone: {self.timezone_str}")
        
        return f"Unknown timezone: {self.timezone_str}"
    
from agency_swarm import Agent

ceo = Agent(name="CEO",
            description="Responsible for client communication, task planning and management.",
            instructions="You must converse with other agents to ensure complete task execution.", # can be a file like ./instructions.md
            files_folder=None,
            tools=[MyCustomTool])

dev = Agent(name="DEV",
            description="Responsible for client communication, task planning and management.",
            instructions="You must converse with other agents to ensure complete task execution.", # can be a file like ./instructions.md
            files_folder=None,
            tools=[MyCustomTool])
va = Agent(name="Virtual Assitant",
            description="Responsible for client communication, task planning and management.",
            instructions="You must converse with other agents to ensure complete task execution.", # can be a file like ./instructions.md
            files_folder=None,
            tools=[MyCustomTool])

from agency_swarm import Agency
from continuedev.core.main import ChatMessage, SetStep, Step
from continuedev.core.sdk import ContinueSDK, Models

class OpenAIAgency(Step):
    api_key: str
    user_input: str
    name: str
    content: str

    def __init__(self):         
        set_openai_key(os.getenv(self.api_key))
        if not OpenAIAgency.agency:
            OpenAIAgency.agency = Agency([
                ceo,  # CEO will be the entry point for communication with the user
                [ceo, dev],  # CEO can initiate communication with Developer
                [ceo, va],   # CEO can initiate communication with Virtual Assistant
                [dev, va]    # Developer can initiate communication with Virtual Assistant
            ], shared_instructions='agency_manifesto.md') # shared instructions for all agents



    async def describe(self, models: Models):
        return f"`OpenAI Agency`."

    async def run(self, sdk: ContinueSDK):    
        gen= (OpenAIAgency.agency.get_completion(self.user_input))
       
        try:
            # Yield each message from the generator
            for bot_message in gen:
                if bot_message.sender_name.lower() == "user":
                    continue

                msg = bot_message.get_sender_emoji() + " " + bot_message.get_formatted_content()
                print(msg)
                yield ChatMessage(
                    role=bot_message.sender_name,
                    content= bot_message.content,
                    summary= bot_message.content,
                )              
        except StopIteration:
            # Handle the end of the conversation if necessary
            pass