import sys
import unittest

import pytest

from . import youtube

if "nosetests" in sys.argv[0]:
    raise unittest.SkipTest("Those tests are pytest-compatible only")


class configs:
    def __init__(self):
        self.config = {}

    def setConfig(self, name, value):
        self.config[name] = value

    def getConfig(self, name):
        try:
            out = self.config[name]
        except KeyError:
            out = ""

        return out


class fake_proc:
    def __init__(self):
        self.configs = configs()


@pytest.mark.parametrize(
    "input,expected,thumb_only,invidious",
    [
        (
            "v78_WujMnVk",
            """<a
                    href="https://www.youtube.com/watch?v=v78_WujMnVk"
                class="youtube_video" alt="YouTube Video"
                title="Click to view on YouTube"
                target="_blank" rel="noopener noreferrer">
                    <img width="1280" height="720"
                        src="https://img.youtube.com/vi/v78_WujMnVk/maxresdefault.jpg">
                </a>""",
            True,
            "",
        ),
        (
            "v78_WujMnVk",
            """<span class="videobox">
                    <iframe width="640" height="390"
                        src='https://www.youtube.com/embed/v78_WujMnVk'
                        frameborder='0' webkitAllowFullScreen
                        mozallowfullscreen allowFullScreen>
                    </iframe>
                </span>""",
            False,
            "",
        ),
        (
            "v78_WujMnVk",
            """<a
                    href="https://inv.example.com/watch?v=v78_WujMnVk"
                class="youtube_video" alt="YouTube Video"
                title="Click to view on YouTube"
                target="_blank" rel="noopener noreferrer">
                    <img width="1280" height="720"
                        src="https://inv.example.com/vi/v78_WujMnVk/maxresdefault.jpg">
                </a>""",
            True,
            "https://inv.example.com",
        ),
        (
            "v78_WujMnVk",
            """<span class="videobox">
                    <iframe width="640" height="390"
                        src='https://inv.example.com/embed/v78_WujMnVk'
                        frameborder='0' webkitAllowFullScreen
                        mozallowfullscreen allowFullScreen>
                    </iframe>
                </span>""",
            False,
            "https://inv.example.com",
        ),
    ],
)
def test_youtube(input, expected, thumb_only, invidious):
    fake_preproc = fake_proc()

    fake_preproc.configs.setConfig("YOUTUBE_THUMB_ONLY", thumb_only)
    fake_preproc.configs.setConfig("YOUTUBE_THUMB_SIZE", "maxres")
    fake_preproc.configs.setConfig("YOUTUBE_INVIDIOUS_INSTANCE", invidious)

    print(fake_preproc.configs.config)

    out = youtube.youtube(fake_preproc, "", input)

    assert out == expected
