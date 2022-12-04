"""
Youtube Tag
-----------
This implements a Liquid-style youtube tag for Pelican,
based on the jekyll / octopress youtube tag [1]_

Configuration
-------------

- Embedding Thumbnail Only

  If you do not want to add 1+ megabyte of JS code to your page, you can embed a
  linked thumbnail instead. To do so, set a `YOUTUBE_THUMB_ONLY` variable in your
  settings file. The `YOUTUBE_THUMB_SIZE` variable controls thumbnail dimensions,
  with four sizes available:

  ======  ======  ======
  name    xres    yres
  ======  ======  ======
  maxres  1280    720
  sd      640     480
  hq      480     360
  mq      320     180
  ======  ======  ======

  Embedded thumbnails have CSS class `youtube_video`, which can be used to add a Play button.

- Using alternative YouTube frontend

  If you want to use an invidious.io instance as alternative frontend to YouTube's,
  you can set a `YOUTUBE_INVIDIOUS_INSTANCE` variable to the domain of the chosen instance.

Syntax
------
{% youtube id [width height] %}

Example
-------
{% youtube dQw4w9WgXcQ 640 480 %}

Output
------

<span class="videobox">
    <iframe
        width="640" height="480"
        src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0"
        webkitAllowFullScreen mozallowfullscreen allowFullScreen>
    </iframe>
</span>

[1] https://gist.github.com/jamieowen/2063748
"""
import re

from .mdx_liquid_tags import LiquidTags

SYNTAX = "{% youtube id [width height] %}"

YOUTUBE = re.compile(r"([\S]+)(\s+([\d%]+)\s([\d%]+))?")


@LiquidTags.register("youtube")
def youtube(preprocessor, tag, markup):
    width = 640
    height = 390
    youtube_id = None

    config_thumb_only = preprocessor.configs.getConfig("YOUTUBE_THUMB_ONLY")
    config_thumb_size = preprocessor.configs.getConfig("YOUTUBE_THUMB_SIZE")
    config_invidious = preprocessor.configs.getConfig("YOUTUBE_INVIDIOUS_INSTANCE")

    thumb_sizes = {
        "maxres": [1280, 720],
        "sd": [640, 480],
        "hq": [480, 360],
        "mq": [320, 180],
    }

    if config_thumb_only:
        if not config_thumb_size:
            config_thumb_size = "sd"

        try:
            width = thumb_sizes[config_thumb_size][0]
            height = thumb_sizes[config_thumb_size][1]
        except KeyError:
            pass

    match = YOUTUBE.search(markup)
    if match:
        groups = match.groups()
        youtube_id = groups[0]
        width = groups[2] or width
        height = groups[3] or height

    if youtube_id:
        youtube_frontend = _get_youtube_frontend(config_invidious)
        if config_thumb_only:
            thumb_url = _get_thumb_url(youtube_id, config_invidious)

            youtube_out = f"""<a
                    href="{youtube_frontend}/watch?v={youtube_id}"
                class="youtube_video" alt="YouTube Video"
                title="Click to view on YouTube"
                target="_blank" rel="noopener noreferrer">
                    <img width="{width}" height="{height}"
                        src="{thumb_url}/{config_thumb_size}default.jpg">
                </a>"""

        else:
            youtube_out = f"""
                <span class="videobox">
                    <iframe width="{width}" height="{height}"
                        src='{youtube_frontend}/embed/{youtube_id}'
                        frameborder='0' webkitAllowFullScreen
                        mozallowfullscreen allowFullScreen>
                    </iframe>
                </span>
            """.strip()
    else:
        raise ValueError(f"Error processing input, expected syntax: {SYNTAX}")

    return youtube_out


def _get_youtube_frontend(config_invidious):
    if config_invidious:
        return config_invidious
    return "https://www.youtube.com"


def _get_thumb_url(youtube_id, config_invidious):
    yt_frontend = "https://img.youtube.com"
    if config_invidious:
        yt_frontend = config_invidious
    return f"{yt_frontend}/vi/{youtube_id}"


# ---------------------------------------------------
# This import allows youtube tag to be a Pelican plugin
from .liquid_tags import register  # noqa
