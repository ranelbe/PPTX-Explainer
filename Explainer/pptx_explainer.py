import asyncio
import json
import time
from datetime import datetime
from sqlalchemy import or_
from sqlalchemy.orm import Session
from DB.database import engine, Upload
from gpt_api_manager import GptAPIManager
from pptx_parser import PPTXParser
from prompt_composer import PromptComposer
from utils import make_directories
from utils import UploadStatus

WAIT_TIME = 10
pptxParser = PPTXParser()
promptComposer = PromptComposer()
api_manager = GptAPIManager()


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


async def create_json_file(upload: Upload):
    """
    Create a JSON file with the explanation results.
    :param upload: the Upload object.
    """
    result_list = await explain(upload.upload_path)
    with open(upload.output_path, 'w') as file:
        json.dump(result_list, file)


async def process_uploads():
    """
    Process all pending/failed uploads.
    Create a JSON file with the explanation results.
    Update the status of the upload accordingly.
    """
    while True:
        with Session(engine) as session:
            # Find pending/failed uploads in the DB
            pending_uploads = session.query(Upload).filter(
                or_(Upload.status == UploadStatus.PENDING,
                    Upload.status == UploadStatus.FAILED)).all()

            # Process each upload
            for upload in pending_uploads:
                if isinstance(upload, Upload):
                    try:
                        upload.status = UploadStatus.PROCESSING
                        session.commit()
                        print(f"processing file: {upload.upload_name}")
                        await create_json_file(upload)
                        upload.status = UploadStatus.DONE
                        upload.finish_time = datetime.now()
                        session.commit()
                        print(f"file {upload.output_name} created successfully")
                    except Exception as e:
                        upload.status = UploadStatus.FAILED
                        session.commit()
                        print(f"Error: {e}")

            # wait some time before checking again pending uploads
            time.sleep(WAIT_TIME)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )
    make_directories()
    asyncio.run(process_uploads())
