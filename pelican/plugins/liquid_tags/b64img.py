"""
Image Tag
---------
This implements a Liquid-style image tag for Pelican,
based on the liquid img tag which is based on the octopress image tag [1]_

Syntax
------
{% b64img [class name(s)] [http[s]:/]/path/to/image [width [height]] [title text | "title text" ["alt text"]] %}

Examples
--------
{% b64img /images/ninja.png Ninja Attack! %}
{% b64img left half http://site.com/images/ninja.png Ninja Attack! %}
{% b64img left half http://site.com/images/ninja.png 150 150 "Ninja Attack!" "Ninja in attack posture" %}

Output
------
<img src="data:;base64,....">
<img class="left half" src="data:;base64,..." title="Ninja Attack!" alt="Ninja Attack!">
<img class="left half" src="data:;base64,..." width="150" height="150" title="Ninja Attack!" alt="Ninja in attack posture">

[1] https://github.com/imathis/octopress/blob/master/plugins/image_tag.rb
"""
import base64
import re

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

from .mdx_liquid_tags import LiquidTags

SYNTAX = '{% b64img [class name(s)] [http[s]:/]/path/to/image [width [height]] [title text | "title text" ["alt text"]] %}'

# Regular expression to match the entire syntax
ReImg = re.compile(
    r"""(?P<class>\S.*\s+)?(?P<src>(?:https?:\/\/|\/|\S+\/)\S+)(?:\s+(?P<width>\d+))?(?:\s+(?P<height>\d+))?(?P<title>\s+.+)?"""
)

# Regular expression to split the title and alt text
ReTitleAlt = re.compile(
    r"""(?:"|')(?P<title>[^"']+)?(?:"|')\s+(?:"|')(?P<alt>[^"']+)?(?:"|')"""
)


def _get_file(src):
    """Return content from local or remote file."""
    try:
        if "://" in src or src[0:2] == "//":  # Most likely this is remote file
            response = urllib2.urlopen(src)
            return response.read()
        else:
            with open(src, "rb") as fh:
                return fh.read()
    except Exception as e:
        raise RuntimeError(f"Error generating base64image: {e}")


def base64image(src):
    """Generate base64 encoded image from srouce file."""
    return base64.b64encode(_get_file(src))


@LiquidTags.register("b64img")
def b64img(preprocessor, tag, markup):
    attrs = None

    # Parse the markup string
    match = ReImg.search(markup)
    if match:
        attrs = {key: val.strip() for (key, val) in match.groupdict().items() if val}
    else:
        raise ValueError(
            "Error processing input. " "Expected syntax: {}".format(SYNTAX)
        )

    # Check if alt text is present -- if so, split it from title
    if "title" in attrs:
        match = ReTitleAlt.search(attrs["title"])
        if match:
            attrs.update(match.groupdict())
        if not attrs.get("alt"):
            attrs["alt"] = attrs["title"]

    attrs["src"] = "data:;base64,{}".format(base64image(attrs["src"]))

    # Return the formatted text
    return "<img {}>".format(" ".join(f'{key}="{val}"' for (key, val) in attrs.items()))


# ----------------------------------------------------------------------
# This import allows image tag to be a Pelican plugin
from .liquid_tags import register  # noqa
