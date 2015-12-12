# Liquid-style Tags
*Author: Jake Vanderplas <jakevdp@cs.washington.edu>*

This plugin allows liquid-style tags to be inserted into Markdown within
Pelican documents via tags bounded by `{% ... %}`, a convention also used
to extend Markdown in other publishing platforms such as Octopress.

This set of extensions does not actually interface with liquid, but allows
users to define their own liquid-style tags which will be inserted into
the Markdown preprocessor stream. There are several built-in tags, which
can be added as follows.

First, in your pelicanconf.py file, add the plugins you want to use:

    PLUGIN_PATH = '/path/to/pelican-plugins'
    PLUGINS = ['liquid_tags.img', 'liquid_tags.video',
               'liquid_tags.youtube', 'liquid_tags.vimeo',
               'liquid_tags.include_code', 'liquid_tags.notebook']

Following below is more information about these and other tags.

## Image Tag
To insert a sized and labeled image in your document, enable the
`liquid_tags.img` plugin and use the following:

    {% img [class name(s)] path/to/image [width [height]] [title text | "title text" ["alt text"]] %}

### Base64 Image (inline image) tag

`b64img` is based on the`img` tag, but instead of inserting a link to the image it encodes it as base64 text and inserts it into a`<img src=` attribute.

To use it:

1. Enable `liquid_tags.b64img`
1. Insert a tag as follows: `{% b64img [class name(s)] path/to/image [width [height]] [title text | "title text" ["alt text"]] %}`

Images are encoded at generation time, so you can use any local path (just be sure that the image will remain in the same location for subsequent site generations).

## Instagram Tag
To insert a sized and labeled Instagram image in your document by its shortcode (such as `pFI0CAIZna`), enable the `liquid_tags.gram` plugin and use the following:

    {% gram shortcode [size] [width] [class name(s)] [title text | "title text" ["alt text"]] %}

You can specify a size with `t`, `m`, or `l`.

## Flickr Tag
To insert a Flickr image to a post, follow these steps:

1. Enable `liquid_tags.flickr`
2. [Get an API key from Flickr](https://www.flickr.com/services/apps/create/apply)
3. Add FLICKR_API_KEY to your settings file
4. Add this to your source document:

    {% flickr image_id [small|medium|large] ["alt text"|'alt text'] %}

## Giphy Tag
To insert a GIF from Giphy in your document by its ID (such as `aMSJFS6oFX0fC`), enable the `liquid_tags.giphy` plugin and use the following:

    {% giphy gif_id ["alt text"|'alt text'] %}

**Important:** You must [request a production API key](https://api.giphy.com/submit) from Giphy.
If you just want to try it out, you can use the public beta key contained within the [GiphyAPI](https://github.com/giphy/GiphyAPI) README file.

## Soundcloud Tag
To insert a Soundcloud widget in your content, follow these steps:

1. Enable `liquid_tags.soundcloud`
2. Add this to your source document:

    {% soundcloud track_url %}

## YouTube Tag
To insert a YouTube video into your content, enable the
`liquid_tags.youtube` plugin and add the following to your source document:

    {% youtube youtube_id [width] [height] %}

The width and height are in pixels and are optional. If they
are not specified, then the dimensions will be 640 (wide) by 390 (tall).

If you experience issues with code generation (e.g., missing closing tags),
add `SUMMARY_MAX_LENGTH = None` to your settings file.

## Vimeo Tag
To insert a Vimeo video into your content, enable the `liquid_tags.vimeo`
plugin and add the following to your source document:

    {% vimeo vimeo_id [width] [height] %}

The width and height are in pixels and are optional. If they
are not specified, then the dimensions will be 640 (wide) by 390 (tall).

If you experience issues with code generation (e.g., missing closing tags),
add `SUMMARY_MAX_LENGTH = None` to your settings file.

## Video Tag
To insert HTML5-friendly video into your content, enable the `liquid_tags.video`
plugin and add the following to your source document:

    {% video /url/to/video.mp4 [width] [height] [/path/to/poster.png] %}

The width and height are in pixels and are optional. If they are not specified,
then the native video size will be used. The poster image is a preview image
that is shown prior to initiating video playback.

To link to a video file, make sure it is in a static directory, transmitted
to your server, and available at the specified URL.

## Audio Tag
To insert HTML5 audio into a post, enable the `liquid_tags.audio` plugin
and add the following to your source document:

    {% audio url/to/audio [url/to/audio] [url/to/audio] %}

This tag supports up to three audio URL arguments so you can add different
audio file versions, as different browsers support different file formats.

To link to a audio file, make sure it is in a static directory, transmitted
to your server, and available at the specified URL.

## Include Code
To include code from a file in your document with a link to the original
file, enable the ``liquid_tags.include_code`` plugin, and add to your
document:

    {% include_code /path/to/code.py [lang:python] [lines:X-Y] [:hidefilename:] [title] %}

All arguments are optional but their order must be kept. `:hidefilename:` is
only allowed if a title is also given.

    {% include_code /path/to/code.py lines:1-10 :hidefilename: Test Example %}

This example will show the first 10 lines of the file while hiding the actual
filename.

The script must be in the ``code`` subdirectory of your content folder:
this default location can be changed by specifying

    CODE_DIR = 'code'

within your configuration file. Additionally, in order for the resulting
hyperlink to work, this directory must be listed under the STATIC_PATHS
setting, e.g.:

    STATIC_PATHS = ['images', 'code']

## IPython notebooks

To insert an [IPython][] notebook into your post, enable the
``liquid_tags.notebook`` plugin and add to your document:

    {% notebook filename.ipynb %}

The file should be specified relative to the ``notebooks`` subdirectory of the
content directory.  Optionally, this subdirectory can be specified in the
config file:

    NOTEBOOK_DIR = 'notebooks'

Because the conversion and rendering of notebooks is rather involved, there
are a few extra steps required for this plugin:

- First, you will need to install IPython:

      pip install ipython==2.4.1

- After typing "make html" when using the notebook tag, a file called
  ``_nb_header.html`` will be produced in the main directory.  The content
  of the file should be included in the header of the theme.  An easy way
  to accomplish this is to add the following lines within the header template
  of the theme you use:

      {% if EXTRA_HEADER %}
      {{ EXTRA_HEADER }}
      {% endif %}

  and in your configuration file, include the line:

      EXTRA_HEADER = open('_nb_header.html').read().decode('utf-8')

  this will insert the proper css formatting into your document.

### Optional Arguments for Notebook Tags

The notebook tag also has two optional arguments: ``cells`` and ``language``.

- You can specify a slice of cells to include:

  ``{% notebook filename.ipynb cells[2:8] %}``

- You can also specify the name of a language which Pygments should use for
  highlighting code cells. A list of the short names for languages that Pygments
  will highlight can be found [here](http://www.pygments.org/docs/lexers/).

  ``{% notebook filename.ipynb language[julia] %}``

  This may be helpful for those using [IJulia](https://github.com/JuliaLang/IJulia.jl)
  or notebooks in any other language, especially as the IPython project [broadens its
  scope](https://github.com/ipython/ipython/wiki/Roadmap:-IPython) of [language
  compatibility](http://jupyter.org/). By default, the language for highlighting
  will be ``ipython``.

- These options can be used separately, together, or not at all. However,
  if both tags are used then ``cells`` must come before ``language``:

  ``{% notebook filename.ipynb cells[2:8] language[julia] %}``

### Collapsible Code in IPython Notebooks

The plugin also enables collapsible code input boxes. For this to work
you first need to copy the file ``pelicanhtml_3.tpl`` (for IPython
3.x, ``pelicanhtml_2.tpl`` (for IPython 2.x)...) to the top level of your
Pelican blog. Notebook input cells containing the comment line ``#
<!-- collapse=True -->`` will be collapsed when the html page is
loaded and can be expanded by clicking on them. Cells containing the
comment line ``# <!-- collapse=False -->`` will be open on load but
can be collapsed by clicking on their header. Cells without collapse
comments are rendered as standard code input cells.

## Testing

To test the plugin in multiple environments we use [tox](http://tox.readthedocs.org/en/latest/), to run the entire test suite, just type:

```
cd path/to/liquid_tags
tox
```

[IPython]: http://ipython.org/
