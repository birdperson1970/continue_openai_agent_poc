
import asyncio
from agency_swarm.tools import BaseTool
from continuedev.core.sdk import ContinueSDK
from continuedev.libs.index.chunkers.chunk_directory import get_all_filepaths

from pydantic import Field
from datetime import datetime
import pytz

class CurrentTimeTool(BaseTool):
    timezone_str: str = Field(
        ..., description="The timezone you want the time in."
    )
    def run(self):
        try:
            timezone = pytz.timezone(self.timezone_str)
            utc_dt = datetime.now(pytz.utc)
            dt = utc_dt.astimezone(timezone)
            print(f"The current time in {self.timezone_str} is {dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
            return dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')
            
        except pytz.exceptions.UnknownTimeZoneError:
            print(f"Unknown timezone: {self.timezone_str}")
        
        return f"Unknown timezone: {self.timezone_str}"
    
from langchain.utilities.google_search import GoogleSearchAPIWrapper    
class GoogleSearchTool(BaseTool):
    _api_wrapper= GoogleSearchAPIWrapper()
    # Define the fields with descriptions using Pydantic Field
    query_str: str = Field(
        ..., description="A wrapper around Google Search. Useful for when you need to answer questions about current events. Input should be a search query. Output is a JSON array of the query results"
    )

    def run(self):
        print(f"query: {self.query_str}")
        return self._api_wrapper.run(self.query_str)
    

from continuedev.plugins.context_providers.file import get_file_contents
from ...libs.util.logging import getLogger
from fuzzywuzzy import process
import os

logger = getLogger('openai_agency_tools')

class ListProjectFiles(BaseTool):

    def run(self):
        from continuedev.plugins.steps.openai_agency import OpenAIAgency
        sdk = OpenAIAgency._sdk
        loop = asyncio.get_event_loop()
        files, should_ignore =loop.run_until_complete(get_all_filepaths(sdk.ide))
        
        relative_filepaths = [os.path.relpath(path, sdk.ide.workspace_directory) for path in files]
        str = '\n'.join(relative_filepaths)
        logger.info(f' ListProjectFiles()= returned {len(files)} filenames')
        return str

        #return f'Here is where the file would be uploaded for {file_path}'

class GetProjectFile(BaseTool):
    file_path: str = Field(
        ..., file_path="Get a project file. Input should be a file path from ListProjectFiles(). Output is the contents of the file"
    )
    def run(self):
        loop = asyncio.get_event_loop()
        from continuedev.plugins.steps.openai_agency import OpenAIAgency
        sdk = OpenAIAgency._sdk
        abs_path = os.path.join(sdk.ide.workspace_directory, self.file_path)
        if os.path.exists(abs_path) == False:
            fuzzy_path = loop.run_until_complete(self.fuzzy_match_project_file(sdk, self.file_path))
            if fuzzy_path:
                logger.debug(f'GetProjectFile: get_project_file()={self.file_path} fuzzy matched to {fuzzy_path}')
                abs_path = os.path.join(sdk.ide.workspace_directory, fuzzy_path)
            else:
                logger.info(f'GetProjectFile: get_project_file()={abs_path} does not exist')
                return f'ERROR: Failed to find file: {self.file_path}'
            
        contents = loop.run_until_complete(get_file_contents(abs_path, sdk.ide))
        if len(contents) == 0:
            contents=f'file not found {abs_path}'
            logger.error(f'GetProjectFile:  get_project_file({self.file_path}) - file not found')
        else:   
            logger.info(f'GetProjectFile: get_project_file({self.file_path})={abs_path} size={len(contents)}')
        return contents
        #return f'Here is where the file would be uploaded for {file_path}'

    async def fuzzy_match_project_file(self, sdk, filename, threshold=80):
        """
        Retrieves the contents of the requested file with fuzzy match on the filename.
        
        Args:
            filename (str): The approximate name of the file to match.
            threshold (int): The matching score threshold to consider a successful match.

        Returns:
            str: The contents of the matched file or an error message.
        """
        from continuedev.plugins.steps.openai_agency import OpenAIAgency
        
        sdk = OpenAIAgency._sdk
        # Perform fuzzy matching to find the best match above a certain threshold
        files, should_ignore = await get_all_filepaths(sdk.ide)
        best_match, score = process.extractOne(filename,files )

        # Check if the matching score is above the threshold
        if score >= threshold:
            # If the score is above the threshold, fetch and return the file content
            return best_match
        else:
            # If no file is closely matched enough, return an error message
            return None

