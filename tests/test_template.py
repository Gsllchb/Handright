# coding: utf-8
import pickle

import PIL.Image
import PIL.ImageFont

from handright._template import *
from tests.util import *


def build_template() -> Template:
    return Template(
        background=PIL.Image.new("L", (2, 2), color=1),
        font=get_default_font(8),
    )


def test_eq():
    template1 = build_template()
    template2 = copy.copy(template1)
    assert template1 == template2


def test_copy_templates():
    templates = (build_template(),)
    templates_clone = copy_templates(templates)
    assert templates == templates_clone


def test_release_font_resource():
    template = build_template()
    template.release_font_resource()
    pickle.dumps(template)
