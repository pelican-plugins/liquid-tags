"""
Image Tag
---------
This implements a Liquid-style image tag for Pelican,
based on the octopress image tag [1]_

Syntax
------
{% img [class name(s)] [http[s]:/]/path/to/image [lazy | eager] [width [height]] [title text | "title text" ["alt text"]] %}

Configuration
-------------

The configuration variable `IMG_DEFAULT_LOADING` can change the default beahavior
of the plugin. `lazy` setting takes precendence over the default `eager`.
If `lazy` is set, all the images will receive the attribute. This is not the case
with `eager` because it's the default behavior of browsers when faced with an image.
Explicit parameters specified in liquid-tags `img` will always take precedence
and will always be translated into attributes.

Examples
--------
{% img /images/ninja.png %}
{% img left half http://site.com/images/ninja.png Ninja Attack! %}
{% img left half http://site.com/images/ninja.png 150 150 "Ninja Attack!" "Ninja in attack posture" %}
{% img left half http://site.com/images/ninja.png eager 150 150 "Ninja Attack!" "Ninja in attack posture" %}
{% img left half http://site.com/images/ninja.png 150 150 "Ninja Attack!" "Ninja in attack posture" %}

Output
------
<img src="/images/ninja.png">
<img class="left half" src="http://site.com/images/ninja.png" title="Ninja Attack!" alt="Ninja Attack!">
<img class="left half" src="http://site.com/images/ninja.png" width="150" height="150" title="Ninja Attack!" alt="Ninja in attack posture">
<img class="left half" src="http://site.com/images/ninja.png" loading="eager" width="150" height="150" title="Ninja Attack!" alt="Ninja in attack posture">
<img class="left half" src="http://site.com/images/ninja.png" width="150" height="150" title="Ninja Attack!" loading="lazy" alt="Ninja in attack posture">

[1] https://github.com/imathis/octopress/blob/master/plugins/image_tag.rb
"""
import re

from .mdx_liquid_tags import LiquidTags

SYNTAX = '{% img [class name(s)] [http[s]:/]/path/to/image [lazy | eager] [width [height]] [title text | "title text" ["alt text"]] %}'

# Regular expression to match the entire syntax
ReImg = re.compile(
    r"""(?P<class>\S.*\s+)?(?P<src>(?:https?:\/\/|\/|\S+\/)\S+)(?:\s+(?P<loading>lazy|eager))?(?:\s+(?P<width>\d+))?(?:\s+(?P<height>\d+))?(?P<title>\s+.+)?"""
)

# Regular expression to split the title and alt text
ReTitleAlt = re.compile(
    r"""(?:"|')(?P<title>[^"']+)?(?:"|')\s+(?:"|')(?P<alt>[^"']+)?(?:"|')"""
)


@LiquidTags.register("img")
def img(preprocessor, tag, markup):
    attrs = None

    # Parse the markup string
    match = ReImg.search(markup)
    if match:
        attrs = {key: val.strip() for key, val in match.groupdict().items() if val}
    else:
        raise ValueError(
            "Error processing input. " "Expected syntax: {}".format(SYNTAX)
        )

    # If loading setting is modified but not at the image scale
    # If so, apply the global setting
    loading = preprocessor.configs.getConfig("IMG_DEFAULT_LOADING")
    if "loading" not in attrs and loading != "eager":
        attrs["loading"] = loading

    # Check if alt text is present -- if so, split it from title
    if "title" in attrs:
        match = ReTitleAlt.search(attrs["title"])
        if match:
            attrs.update(match.groupdict())
        if not attrs.get("alt"):
            attrs["alt"] = attrs["title"]

    # Return the formatted text
    return "<img {}>".format(
        " ".join('{}="{}"'.format(*item) for item in attrs.items())
    )


# ----------------------------------------------------------------------
# This import allows image tag to be a Pelican plugin
from .liquid_tags import register  # noqa
