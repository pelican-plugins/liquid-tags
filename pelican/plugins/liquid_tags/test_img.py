import unittest

from .img import img


class MockPreprocessor:
    """Mocking _LiquidTagsPreprocessor class used for its `configs` attr"""

    def __init__(self, configs):
        self.configs = configs


class MockConfigs:
    """Mocking Configs class that store the plugin settings in a dict"""

    def __init__(self, configs):
        self.configs = configs

    def getConfig(self, key):
        return self.configs.get(key)


class TestImgTag(unittest.TestCase):
    def setUp(self):
        self.preprocessor = MockPreprocessor(
            MockConfigs({"IMG_DEFAULT_LOADING": "eager"})
        )
        self.tag = "img"

    def test_normal_relative_path(self):
        markup = "/images/ninja.png"
        expected = '<img src="/images/ninja.png">'
        actual = img(self.preprocessor, self.tag, markup)
        self.assertIn(expected, actual)

    def test_classnames_title_noalt(self):
        markup = "left half http://site.com/images/ninja.png Ninja Attack!"
        expected = (
            '<img class="left half" src="http://site.com/images/ninja.png" '
            'title="Ninja Attack!" alt="Ninja Attack!">'
        )
        actual = img(self.preprocessor, self.tag, markup)
        self.assertIn(expected, actual)

    def test_classnames_sizes_title_alt(self):
        markup = 'left half http://site.com/images/ninja.png 150 150 "Ninja Attack!" "Ninja in attack posture"'
        expected = (
            '<img class="left half" src="http://site.com/images/ninja.png" '
            'width="150" height="150" title="Ninja Attack!" alt="Ninja in attack posture">'
        )
        actual = img(self.preprocessor, self.tag, markup)
        self.assertIn(expected, actual)

    def test_classnames_sizes_title_alt_loading(self):
        markup = 'left half http://site.com/images/ninja.png eager 150 150 "Ninja Attack!" "Ninja in attack posture"'
        expected = (
            '<img class="left half" src="http://site.com/images/ninja.png" loading="eager" '
            'width="150" height="150" title="Ninja Attack!" alt="Ninja in attack posture">'
        )
        actual = img(self.preprocessor, self.tag, markup)
        self.assertIn(expected, actual)

    def test_classnames_sizes_title_alt_default_loading(self):
        self.preprocessor.configs.configs["IMG_DEFAULT_LOADING"] = "lazy"
        markup = 'left half http://site.com/images/ninja.png 150 150 "Ninja Attack!" "Ninja in attack posture"'
        # Loading key is not specified but the default settings takes precedence
        expected = (
            '<img class="left half" src="http://site.com/images/ninja.png" '
            'width="150" height="150" title="Ninja Attack!" loading="lazy" alt="Ninja in attack posture">'
        )
        actual = img(self.preprocessor, self.tag, markup)
        self.assertIn(expected, actual)

        markup = 'left half http://site.com/images/ninja.png eager 150 150 "Ninja Attack!" "Ninja in attack posture"'
        expected = (
            '<img class="left half" src="http://site.com/images/ninja.png" loading="eager" '
            'width="150" height="150" title="Ninja Attack!" alt="Ninja in attack posture">'
        )
        actual = img(self.preprocessor, self.tag, markup)
        self.assertIn(expected, actual)


if __name__ == "__main__":
    unittest.main()
