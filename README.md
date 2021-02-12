# Liquid Tags

[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/liquid-tags/build)](https://github.com/pelican-plugins/liquid-tags/actions)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-liquid-tags)](https://pypi.org/project/pelican-liquid-tags/)
![License](https://img.shields.io/pypi/l/pelican-liquid-tags?color=blue)

This Pelican plugin allows Liquid-style tags to be inserted into Markdown within
Pelican documents via tags bounded by `{% ... %}`, a convention also used
to extend Markdown in other publishing platforms such as Octopress.

This set of extensions does not actually interface with Liquid, but allows
users to define their own Liquid-style tags which will be inserted into
the Markdown pre-processor stream. There are several built-in tags, which
can be added as follows below.

## Installation

This plugin can be installed via:

    python -m pip install pelican-liquid-tags

For more detailed plugin installation instructions, please refer to the
[Pelican Plugin Documentation](https://docs.getpelican.com/en/latest/plugins.html).

## Configuration

While this plugin does provide an extensive set of built-in tags (see below),
none of them is imported and made available by default. In order to use specific
tags in your post, you need to explicitly enable them in your settings file:

    LIQUID_TAGS = ["img", "literal", "video", "youtube",
                   "vimeo", "include_code"]

### Configuration Settings in Custom Tags

Tags do not have access to the full set of Pelican settings, and instead arrange
for the variables to be passed to the tag. Tag authors who plan to add their
tag as an in-tree tag can just add the variables they need to an array in
`mdx_liquid_tags.py`. Out-of-tree tag authors can specify which variables they
need by including a tuple of (variable, default value, helptext) via the
appropriate Pelican setting:

    LIQUID_CONFIGS = (('PATH', '.', "The default path"), ('SITENAME', 'Default Sitename', 'The name of the site'))

## Tags in this Plugin

### Image Tag

To insert a sized and labeled image in your document, enable the
`img` tag and use the following:

    {% img [class name(s)] path/to/image [width [height]] [title text | "title text" ["alt text"]] %}

### Base64 Image (Inline Image) Tag

`b64img` is based on the`img` tag, but instead of inserting a link to the image, it encodes it as Base64 text and inserts it into an `<img src=` attribute.

To use it:

1. Enable `b64img`
1. Insert a tag as follows: `{% b64img [class name(s)] path/to/image [width [height]] [title text | "title text" ["alt text"]] %}`

Images are encoded at generation time, so you can use any local path (just be sure that the image will remain in the same location for subsequent site generations).

### Instagram Tag

To insert a sized and labeled Instagram image in your document by its short-code (such as `pFI0CAIZna`), enable the `gram` tag and use the following:

    {% gram shortcode [size] [width] [class name(s)] [title text | "title text" ["alt text"]] %}

You can specify a size with `t`, `m`, or `l`.

### Flickr Tag

To insert a Flickr image to a post, follow these steps:

1. Enable `flickr`
2. [Get an API key from Flickr](https://www.flickr.com/services/apps/create/apply)
3. Add `FLICKR_API_KEY` to your settings file
4. Add this to your source document:

       {% flickr image_id [small|medium|large] ["alt text"|'alt text'] %}

### Giphy Tag

To insert a GIF from Giphy in a post, follow these steps:
1. Enable `giphy`
2. [Get an API key from Giphy](https://developers.giphy.com/docs/api#quick-start-guide)
3. Add `GIPHY_API_KEY` to your settings file
4. Add this to your source document:

       {% giphy gif_id ["alt text"|'alt text'] %}

### Soundcloud Tag

To insert a Soundcloud widget in your content, follow these steps:

1. Enable `soundcloud`
2. Add this to your source document:

       {% soundcloud track_url %}

### YouTube Tag

To insert a YouTube video into your content, enable the
`youtube` plugin and add the following to your source document:

    {% youtube youtube_id [width] [height] %}

The width and height are in pixels and are optional. If they
are not specified, then the dimensions will be 640 (wide) by 390 (tall).

If you experience issues with code generation (e.g., missing closing tags),
you might need to add `SUMMARY_MAX_LENGTH = None` to your settings file.

#### Embedding Thumbnail Only

If you do not want to add 1+ megabyte of JS code to your page, you can embed a
linked thumbnail instead. To do so, set a `YOUTUBE_THUMB_ONLY` variable in your
settings file. The `YOUTUBE_THUMB_SIZE` variable controls thumbnail dimensions,
with four sizes available:

name  | xres | yres
------|------|-----
maxres| 1280 | 720
sd    |  640 | 480
hq    |  480 | 360
mq    |  320 | 180

Embedded thumbnails have CSS class `youtube_video`, which can be used to add
a *Play* button.

### Vimeo Tag

To insert a Vimeo video into your content, enable the `vimeo`
plugin and add the following to your source document:

    {% vimeo vimeo_id [width] [height] %}

The width and height are in pixels and are optional. If they
are not specified, then the dimensions will be 640 (wide) by 390 (tall).

If you experience issues with code generation (e.g., missing closing tags),
you might need to add `SUMMARY_MAX_LENGTH = None` to your settings file.

### Speakerdeck Tag

To insert a Speakerdeck viewer into your content, follow these steps:

1. Enable the `soundcloud` plugin
2. Add the following to your source document:

```html
{% speakerdeck speakerdeck_id [ratio] %}
```

Notes:

- The ratio is a decimal number and is optional.
- Ratio must be a decimal number and any digit after decimal is optional.
- If ratio is not specified, then it will be `1.33333333333333` (4/3).
- Common value for the ratio is `1.77777777777777` (16/9).

### Video Tag

To insert HTML5-friendly video into your content, enable the `video`
plugin and add the following to your source document:

    {% video /url/to/video.mp4 [width] [height] [/path/to/poster.png] %}

The width and height are in pixels and are optional. If they are not specified,
then the native video size will be used. The poster image is a preview image
that is shown prior to initiating video playback.
To link to a video file, make sure it is in a static directory, transmitted
to your server, and available at the specified URL.

### Audio Tag

To insert HTML5 audio into a post, enable the `audio` plugin
and add the following to your source document:

    {% audio url/to/audio [url/to/audio] [url/to/audio] %}

This tag supports up to three audio URL arguments so you can add different
audio file versions, as different browsers support different file formats.

To link to an audio file, make sure it is in a static directory, transmitted
to your server, and available at the specified URL.

### Include Code

To include code from a file in your document, with optional link to the original
file, enable the `include_code` plugin, and add the following to your source
document:

    {% include_code path/to/code.py [lang:python] [lines:X-Y] [:hidefilename:] [:hidelink:] [:hideall:] [title] %}

`path/to/code.py` is path to file with source code, relative to `CODE_DIR` subdirectory
in your content folder. `CODE_DIR` is `code` by default and can be changed in
your settings file:

    CODE_DIR = 'code'

Additionally, in order for the resulting hyperlink to work, this directory must
be listed in the `STATIC_PATHS` setting. For example:

    STATIC_PATHS = ['images', 'code']

All other arguments are optional but must be specified in the order shown above.
Following example will show the first ten lines of the file.

    {% include_code path/to/code.py lines:1-10 Test Example %}

To hide the filename, use `:hidefilename:`. When that flag is specified, a title
must be provided.

You can hide download links only, while leaving the filename, by adding
`:hidelink:`.

If you would like to hide all three (title, filename, and download link),
use `:hideall:`.

The following example hides the filename:

    {% include_code path/to/code.py lines:1-10 :hidefilename: Test Example %}

### IPython notebooks

To insert an [IPython][] notebook into your post, enable the
`notebook` plugin and add the following to your source document:

    {% notebook filename.ipynb %}

The file should be specified relative to the `notebooks` subdirectory of the
content directory. Optionally, this subdirectory can be specified in your
settings file:

    NOTEBOOK_DIR = 'notebooks'

Because the conversion and rendering of notebooks is rather involved, there
are a few extra steps required for this plugin. First, you must install IPython:

      pip install ipython==2.4.1

After running Pelican on content containing an IPython notebook tag, a file
called `_nb_header.html` will be generated in the main directory. The content
of this file should be included in the header of your theme. An easy way to
accomplish this is to add the following to your theme’s header template…

      {% if EXTRA_HEADER %}
      {{ EXTRA_HEADER }}
      {% endif %}

… and in your settings file, include the line:

      from io import open
      EXTRA_HEADER = open('_nb_header.html', encoding='utf-8').read()

This will insert the proper CSS formatting into your generated document.

#### Optional Arguments for Notebook Tags

The notebook tag also has two optional arguments: `cells` and `language`.

- You can specify a slice of cells to include:

  `{% notebook filename.ipynb cells[2:8] %}`

- You can also specify the name of the language that Pygments should use for
  highlighting code cells. For a list of the language short names that Pygments
  can highlight, refer to the [Pygments lexer list](https://pygments.org/docs/lexers/).

  `{% notebook filename.ipynb language[julia] %}`

  This may be helpful for those using [IJulia](https://github.com/JuliaLang/IJulia.jl)
  or notebooks in other languages, especially as the IPython project [broadens its
  scope](https://github.com/ipython/ipython/wiki/Roadmap:-IPython) to [support
  other languages](https://jupyter.org). The default language for highlighting
  is `ipython`.

- These options can be used separately, together, or not at all. However,
  if both tags are used then `cells` must come before `language`:

  `{% notebook filename.ipynb cells[2:8] language[julia] %}`

#### Collapsible Code in IPython Notebooks

The IPython plugin also enables collapsible code input boxes. For this to work
you must first copy the file `pelicanhtml_3.tpl` (for IPython 3.x) or
`pelicanhtml_2.tpl` (for IPython 2.x) to the top level of your content
directory. Notebook input cells containing the comment line `#
<!-- collapse=True -->` will be collapsed when the HTML page is
loaded and can be expanded by tapping on them. Cells containing the
comment line `# <!-- collapse=False -->` will be expanded on load but
can be collapsed by tapping on their header. Cells without collapsed
comments are rendered as standard code input cells.

## Testing

To run the plugin test suite, [set up your development environment][] and run:

    cd path/to/liquid_tags
    invoke tests

To test the plugin in multiple environments, install and use [Tox](https://tox.readthedocs.io/en/latest/):

    tox

## Contributing

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

## Gratitude

Thanks to [Jake Vanderplas](https://github.com/jakevdp) for creating this plugin, which has subsequently been enhanced by [dozens of contributors](https://github.com/pelican-plugins/liquid-tags/graphs/contributors).


[IPython]: http://ipython.org/
[set up your development environment]: https://docs.getpelican.com/en/latest/contribute.html#setting-up-the-development-environment
[existing issues]: https://github.com/pelican-plugins/liquid-tags/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html
