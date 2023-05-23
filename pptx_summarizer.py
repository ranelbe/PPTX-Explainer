import json

from pptx_parser import PPTXParser
from prompt_composer import PromptComposer
from api_manager import APIManager
import asyncio

OUTPUT_FILE_NAME = 'result.json'


class PPTXSummarizer:
    """ A class to summarize a PowerPoint presentation using GPT-3. """

    def __init__(self, pptx_path: str):
        """
        initialization.
        :param pptx_path: the path to the PowerPoint presentation.
        """
        self.pptx_path = pptx_path

    async def generate_result_list(self) -> list:
        """
        Generate a list of results from the API.
        :return: a list of results.
        """
        slides_text = PPTXParser(self.pptx_path).extract_slides_text()
        prompted_slides_text = PromptComposer(slides_text).compose()
        api_manager = APIManager()
        tasks = []
        for prompt in prompted_slides_text:
            task = asyncio.create_task(api_manager.generate_answer(prompt))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results

    async def create_result_file(self):
        """
        Create a result json file.
        """
        with open(OUTPUT_FILE_NAME, 'w') as file:
            result_list = await self.generate_result_list()
            file.write(json.dumps(result_list))
