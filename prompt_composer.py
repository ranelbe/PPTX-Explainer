
PROMPT_SUFFIX = """provide a detailed explanation for this presentation slide, 
you may include the following: 
title, main message, key points, related concepts, supporting evidence, implications, 
and any additional examples or illustrations to help understand the content better.
"""


class PromptComposer:
    """ Composes a prompt suffix for each slide. """

    def __init__(self, slides_text: list):
        """ initialization.
            :param slides_text: list of slides text.
        """
        self.slides_text = slides_text

    def compose(self) -> list:
        """
        Composes a prompt suffix for each slide.
        :return: list of composed slides text.
        """
        composed_slides_text = list(
            map(lambda slide_text: f"{slide_text}{PROMPT_SUFFIX}", self.slides_text)
        )
        return composed_slides_text
