import asyncio
import argparse
from pptx_summarizer import PPTXSummarizer


def cli_configuration():
    """ Configure the command line interface. """
    parser = argparse.ArgumentParser(
        prog='pptx_summarize',
        description='a python script to summarize a PowerPoint presentation using GPT-3.',
        epilog='the result will be extracted to the file result.json.'
    )
    parser.add_argument("pptx_path", help="path to the PowerPoint presentation")
    return parser.parse_args()


async def main():
    """ Main function.
    The result will be extracted to the file result.json.
    """
    try:
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy()
        )
        cli = cli_configuration()
        await PPTXSummarizer(cli.pptx_path).create_result_file()
        print("your summary is ready! check the result.json file.")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    asyncio.run(main())
