# coding: utf-8
import PIL.Image
import PIL.ImageFont
import pickle
import copy
import pytest

from handright._template import *


def build_template() -> Template:
    return Template(
        background=PIL.Image.new("L", (2, 2), color=1),
        font_size=1,
        font=PIL.ImageFont.load_default(),
    )


def test_eq():
    template1 = build_template()
    template2 = copy.copy(template1)
    assert template1 == template2
    template2.set_font_size(template2.get_font_size() + 1)
    assert template1 != template2
    template1.set_font_size(template1.get_font_size() + 1)
    assert template1 == template2


def test_copy_templates():
    templates = (build_template(),)
    templates_clone = copy_templates(templates)
    assert templates == templates_clone
    for t in templates_clone:
        t.set_font_size(t.get_font_size() + 1)
    assert templates != templates_clone


def test_release_font_resource():
    template = build_template()
    with pytest.raises(TypeError):
        pickle.dumps(template)
    template.release_font_resource()
    pickle.dumps(template)
