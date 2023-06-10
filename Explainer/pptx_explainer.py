from pptx_parser import PPTXParser
from prompt_composer import PromptComposer
from gpt_api_manager import GptAPIManager
from utils import UPLOADS_FOLDER, PROCESSED_FOLDER,\
    OUTPUTS_FOLDER, make_directories
import asyncio
import json
import os
import shutil
import time


WAIT_TIME = 10
pptxParser = PPTXParser()
promptComposer = PromptComposer()
api_manager = GptAPIManager()


async def create_json_file(pptx_path: str, output_path: str):
    """
    Create an output json file.
    :param pptx_path: Path to the PowerPoint presentation.
    :param output_path: Path to the output json file.
    """
    result_list = await explain(pptx_path)
    with open(output_path, 'w') as file:
        json.dump(result_list, file)


async def explain(pptx_path: str) -> list:
    """
    Generate a list of explanations from the API.
    :param pptx_path: Path to the PowerPoint presentation.
    :return: Explanation results for each slide.
    """
    slides_text = pptxParser.extract_slides_text(pptx_path)
    prompted_slides_text = promptComposer.compose(slides_text)
    tasks = []
    for prompt in prompted_slides_text:
        task = asyncio.create_task(api_manager.generate_answer(prompt))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


async def process_uploads():
    """
    Process files in the uploads folder.
    If new file was uploaded, process it and create an output file.
    Files that were started to be processed will be moved to the processed folder.
    (This is to prevent processing the same file multiple times).
    """
    while True:
        for filename in os.listdir(UPLOADS_FOLDER):
            try:
                file_path = os.path.join(UPLOADS_FOLDER, filename)
                if not os.path.isdir(file_path):
                    print(f"processing file: {filename}")
                    new_file_path = os.path.join(PROCESSED_FOLDER, filename)
                    output_filename = os.path.splitext(filename)[0] + '.json'
                    output_path = os.path.join(OUTPUTS_FOLDER, output_filename)
                    shutil.move(file_path, new_file_path)
                    await create_json_file(new_file_path, output_path)
                    print(f"file {output_filename} created successfully")
            except Exception as e:
                print(f"Error: {e}")
        time.sleep(WAIT_TIME)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )
    make_directories()
    asyncio.run(process_uploads())
