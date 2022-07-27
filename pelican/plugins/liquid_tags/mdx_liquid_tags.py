"""
Markdown Extension for Liquid-style Tags
----------------------------------------
A markdown extension to allow user-defined tags of the form::

    {% tag arg1 arg2 ... argn %}

Where "tag" is associated with some user-defined extension.
These result in a preprocess step within markdown that produces
either markdown or html.
"""
import itertools
import re
import warnings

import markdown

# Define some regular expressions
LIQUID_TAG = re.compile(r"\{%.*?%\}", re.MULTILINE | re.DOTALL)
EXTRACT_TAG = re.compile(r"(?:\s*)(\S+)(?:\s*)")
LT_CONFIG = {
    "CODE_DIR": "code",
    "NOTEBOOK_DIR": "notebooks",
    "FLICKR_API_KEY": "flickr",
    "GIPHY_API_KEY": "giphy",
    "IMG_DEFAULT_LOADING": "eager",
    "YOUTUBE_THUMB_ONLY": False,
    "YOUTUBE_THUMB_SIZE": "",
}
LT_HELP = {
    "CODE_DIR": "Code directory for include_code subplugin",
    "NOTEBOOK_DIR": "Notebook directory for notebook subplugin",
    "FLICKR_API_KEY": "Flickr key for accessing the API",
    "GIPHY_API_KEY": "Giphy key for accessing the API",
    "IMG_DEFAULT_LOADING": "The default loading method of images (eager or lazy)",
    "YOUTUBE_THUMB_ONLY": "Embed a linked thumbnail instead 1MB of JS code",
    "YOUTUBE_THUMB_SIZE": "Thumbnail dimensions maxres/sd (default)/hq/mq",
}


class _LiquidTagsPreprocessor(markdown.preprocessors.Preprocessor):
    _tags = {}

    def __init__(self, configs):
        self.configs = configs

    def run(self, lines):
        page = "\n".join(lines)
        liquid_tags = LIQUID_TAG.findall(page)

        for i, markup in enumerate(liquid_tags):
            # remove {% %}
            markup = markup[2:-2]
            tag = EXTRACT_TAG.match(markup).groups()[0]
            markup = EXTRACT_TAG.sub("", markup, 1)
            if tag in self._tags:
                liquid_tags[i] = self._tags[tag](self, tag, markup.strip())

        # add an empty string to liquid_tags so that chaining works
        liquid_tags.append("")

        # reconstruct string
        page = "".join(itertools.chain(*zip(LIQUID_TAG.split(page), liquid_tags)))

        # resplit the lines
        return page.split("\n")


class LiquidTags(markdown.Extension):
    """Wrapper for MDPreprocessor"""

    def __init__(self, config):
        for key, value in LT_CONFIG.items():
            self.config[key] = [value, LT_HELP[key]]
        super().__init__(**config)

    @classmethod
    def register(cls, tag):
        """Decorator to register a new include tag"""

        def dec(func):
            if tag in _LiquidTagsPreprocessor._tags:
                warnings.warn("Enhanced Markdown: overriding tag '%s'" % tag)
            _LiquidTagsPreprocessor._tags[tag] = func
            return func

        return dec

    def extendMarkdown(self, md):
        self.htmlStash = md.htmlStash
        md.registerExtension(self)
        # for the include_code preprocessor, we need to re-run the
        # fenced code block preprocessor after substituting the code.
        # Because the fenced code processor is run before, {% %} tags
        # within equations will not be parsed as an include.
        i = md.preprocessors.get_index_for_name("html_block")
        priority = md.preprocessors._priority[i].priority - 5
        md.preprocessors.register(_LiquidTagsPreprocessor(self), "mdincludes", priority)


def makeExtension(configs=None):
    """Wrapper for a MarkDown extension"""
    return LiquidTags(configs=configs)
