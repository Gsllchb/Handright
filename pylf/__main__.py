# coding: utf-8
import argparse
import os
import sys
import time

import PIL.Image
import PIL.ImageFont
import yaml

import pylf

ENCODING = "utf-8"

TEXT_FILE = "content.txt"

TEMPLATE_FILE = "template.yml"
FONT_FILE_NAME = "font"
BACKGROUND_FILE_NAME = "background"

OUTPUT_DIRECTORY = "out"
OUTPUT_FORMAT = "png"

FEEDBACK_LINK = "https://github.com/Gsllchb/PyLf/issues"

DESCRIPTION = """
在预先配置好的手写项目上模拟手写

手写项目须含以下文件：
{text_file}\t\t\t待手写内容（{encoding}编码）
{font_file_name}.[ttf|...]\t\t\t用于手写的字体，须为TrueType或OpenType字体文件
{background_file_name}.[png|jpg|...]\t用于手写的背景图片，图片格式须被Pillow库和PyLf库所支持
{template_file}\t\t\t用于手写的其余参数（{encoding}编码）
{output_directory}\t\t\t\t存放生成图片的文件夹（此文件夹可由程序自动创建）

{template_file}示例：
================================================================================
# 页边距（单位：像素）
margin:
  left: 150
  right: 150
  top: 200
  bottom: 200
# 行间距（单位：像素）
line_spacing: 150
# 字体大小（单位：像素）
font_size: 100
# 字间距，缺省值：{default_word_spacing}（单位：像素）
word_spacing: {default_word_spacing}
# 字体颜色，缺省值：{default_color}，详情：https://pillow.readthedocs.io/en/5.2.x/reference/ImageColor.html#color-names
color: {default_color}

# 行间距的高斯分布的σ，缺省值：font_size / 32
line_spacing_sigma: 3.1
# 字体大小的高斯分布的σ，缺省值：font_size / 64
font_size_sigma: 1.6
# 字间距的高斯分布的σ，缺省值：font_size / 32
word_spacing_sigma: 3.1
# 笔画水平位置的高斯分布的σ，缺省值：font_size / 32
perturb_x_sigma: 3.1
# 笔画竖直位置的高斯分布的σ，缺省值：font_size / 32
perturb_y_sigma: 3.1
# 笔画旋转角度的高斯分布的σ，缺省值：{default_perturb_theta_sigma}
perturb_theta_sigma: {default_perturb_theta_sigma}

# 排版时只占据其原宽度一半的字符集，缺省值："{default_half_chars}"
half_chars: "{default_half_chars}"
# 不应出现于行首的字符集，缺省值："{default_end_chars}"
end_chars: "{default_end_chars}"
================================================================================
""".format(
    encoding=ENCODING,
    text_file=TEXT_FILE,
    font_file_name=FONT_FILE_NAME,
    background_file_name=BACKGROUND_FILE_NAME,
    template_file=TEMPLATE_FILE,
    output_directory=OUTPUT_DIRECTORY,
    default_word_spacing=pylf._DEFAULT_WORD_SPACING,
    default_color=pylf._DEFAULT_COLOR,
    default_perturb_theta_sigma=pylf._DEFAULT_PERTURB_THETA_SIGMA,
    default_half_chars="".join(pylf.DEFAULT_HALF_CHARS),
    default_end_chars="".join(pylf.DEFAULT_END_CHARS),
)


def run(*args):
    args = _parse_args(args)
    images = pylf.handwrite(
        _get_text(args.project),
        _get_template(args.project),
        seed=args.seed,
        worker=args.worker,
    )
    _output(args.project, images, args.quiet)


def _parse_args(args) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="pylf",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=DESCRIPTION,
        add_help=False,
        epilog="反馈：{}".format(FEEDBACK_LINK),
    )
    parser.add_argument(
        "project",
        help="手写项目的路径"
    )
    parser.add_argument(
        "-h", "--help",
        action="help",
        help="显示此帮助信息并退出"
    )
    parser.add_argument(
        "-s", "--seed",
        help="设置随机种子"
    )
    parser.add_argument(
        "-w", "--worker",
        type=int,
        help="允许的最大并行处理数，默认为当前系统的CPU数"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="运行时关闭输出"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="PyLf {}".format(pylf.__version__),
        help="显示程序版本号并退出"
    )
    return parser.parse_args(args)


def _get_text(parent: str):
    path = os.path.join(parent, TEXT_FILE)
    with open(path, encoding=ENCODING) as file:
        return file.read()


def _get_template(parent: str):
    with open(os.path.join(parent, TEMPLATE_FILE), encoding=ENCODING) as file:
        template = yaml.safe_load(file)
    if "half_chars" in template:
        half_chars = frozenset(template["half_chars"])
        template["is_half_char_fn"] = lambda c: c in half_chars
        del template["half_chars"]
    if "end_chars" in template:
        end_chars = frozenset(template["end_chars"])
        template["is_end_char_fn"] = lambda c: c in end_chars
        del template["end_chars"]
    template["background"] = PIL.Image.open(os.path.join(parent, _get_file(parent, BACKGROUND_FILE_NAME)))
    template["font"] = PIL.ImageFont.truetype(os.path.join(parent, _get_file(parent, FONT_FILE_NAME)))
    return template


def _get_file(parent: str, name: str) -> str:
    return next((f for f in os.listdir(parent) if f.startswith(name + '.')))


def _output(parent: str, images, quiet: bool):
    path = _get_output_path(parent)
    for index, image in enumerate(images):
        image.save(os.path.join(path, "{}.{}".format(index, OUTPUT_FORMAT)))
    if quiet:
        return
    msg = "成功生成{}张图片！请查看文件夹“{}”。"
    print(msg.format(len(images), path))


def _get_output_path(parent: str) -> str:
    path = os.path.join(
        parent,
        OUTPUT_DIRECTORY,
        "{:.6f}".format(time.time()).replace('.', '')
    )
    os.makedirs(path, exist_ok=True)
    return path


def main():
    run(*sys.argv[1:])


if __name__ == '__main__':
    import multiprocessing

    multiprocessing.freeze_support()
    main()
