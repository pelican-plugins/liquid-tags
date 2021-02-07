import importlib
import logging

from pelican import signals

from .mdx_liquid_tags import LT_CONFIG, LT_HELP, LiquidTags

logger = logging.getLogger(__name__)


def addLiquidTags(gen):
    if not gen.settings.get("MARKDOWN"):
        from pelican.settings import DEFAULT_CONFIG

        gen.settings["MARKDOWN"] = DEFAULT_CONFIG["MARKDOWN"]

    if gen.settings.get("LIQUID_CONFIGS"):
        for param, default, helptext in gen.settings.get("LIQUID_CONFIGS"):
            LT_CONFIG[param] = default
            LT_HELP[param] = helptext

    if LiquidTags not in gen.settings["MARKDOWN"]:
        configs = dict()
        for key, value in LT_CONFIG.items():
            configs[key] = value
        for key, value in gen.settings.items():
            if key in LT_CONFIG:
                configs[key] = value
        gen.settings["MARKDOWN"].setdefault("extensions", []).append(
            LiquidTags(configs)
        )

    tags_to_import = gen.settings.get("LIQUID_TAGS", [])
    for tag in tags_to_import:
        try:
            importlib.import_module(f".{tag}", "pelican.plugins.liquid_tags")
        except ModuleNotFoundError:
            logger.warn(f"Could not load liquid_tag '{tag}'")


def register():
    signals.initialized.connect(addLiquidTags)
