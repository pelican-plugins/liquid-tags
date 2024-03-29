# import filecmp
import os
from shutil import rmtree
from tempfile import mkdtemp
import unittest

from pelican import Pelican
from pelican.settings import read_settings

PLUGIN_DIR = os.path.dirname(__file__)
TEST_DATA_DIR = os.path.join(PLUGIN_DIR, "test_data")


class TestFullRun(unittest.TestCase):
    """Test running Pelican with the Plugin"""

    def setUp(self):
        """Create temporary output and cache folders"""
        self.temp_path = mkdtemp(prefix="pelicantests.")
        self.temp_cache = mkdtemp(prefix="pelican_cache.")
        os.chdir(TEST_DATA_DIR)

    def tearDown(self):
        """Remove output and cache folders"""
        rmtree(self.temp_path)
        rmtree(self.temp_cache)
        os.chdir(PLUGIN_DIR)

    def test_generic_tag_with_config(self):
        """Test generation of site with a generic tag that reads in a config file."""

        base_path = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(base_path, "test_data")
        content_path = os.path.join(base_path, "content")
        # output_path = os.path.join(base_path, "output")
        settings_path = os.path.join(base_path, "pelicanconf.py")
        settings = read_settings(
            path=settings_path,
            override={
                "PATH": content_path,
                "OUTPUT_PATH": self.temp_path,
                "CACHE_PATH": self.temp_cache,
            },
        )

        pelican = Pelican(settings)
        pelican.run()

        assert os.path.exists(
            os.path.join(self.temp_path, "test-generic-config-tag.html")
        )

        assert (
            "Tester"
            in open(os.path.join(self.temp_path, "test-generic-config-tag.html")).read()
        )
        # test differences
        # assert filecmp.cmp(os.path.join(output_path,
        #                                'test-ipython-notebook-v3.html'),
        #                   os.path.join(self.temp_path,
        #                                'test-ipython-notebook.html'))
