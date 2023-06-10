
PROMPT_SUFFIX = """provide a detailed explanation for this presentation slide, 
you may include the following: 
title, main message, key points, related concepts, supporting evidence, implications, 
and any additional examples or illustrations to help understand the content better.
"""

class PromptComposer:
    """ Composes a prompt suffix for each slide. """

    @staticmethod
    def compose(slides_text: list) -> list:
        """
        Composes a prompt suffix for each slide.
        :return: List of composed slides text.
        """
        composed_slides_text = list(
            map(lambda slide_text: f"{slide_text}{PROMPT_SUFFIX}", slides_text)
        )
        return composed_slides_text
