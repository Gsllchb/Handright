# Release Notes
This file records the **main** changes in *PyLf* library.

## in progress version
* **将*font_size*/256作为*template*中3个*sigma*参数的缺省值**
* ***template*添加新的参数*alpha_x*和*alpha_y***
* ***handwrite*的返回值中图片的*mode*将由与*background*保持一致改为均为*RGB***
* **废除*handwrite*的*anti_aliasing*参数**
* **大幅提高性能，大幅减少内存占用**
* **将*line_spacing*的含义改为两临近行间的间隙（即上一行字的下端和下一行字的上端的距离）的大小（以像素为单位），并将(*0.2\*font_size*)
作为其缺省值**
* 完善文档

## v0.5.2 (2017-12-30)
* **将0作为*word_spacing*的缺省值**
* **修复当生成图片数超过*worker*时文字出现大范围重叠的漏洞**

## v0.5.1 (2017-12-14)
* fix #2

## v0.5.0 (2017-12-14)
* **改进算法使得参数*text*可为*iterable***

## v0.4.0 (2017-12-5)
* Add *ValueError* raised by *pylf.handwrite()* to prevent dead loop in some corner cases
* Improve docstring
* **将黑色作为*template*的缺省颜色**
* **字体宽度从由*font_size*决定改为由每个字符自己的信息决定**
* **将(lambda c: False)作为*template*的缺省*is_half_char***
* **将是否在常见非开头字符集中作为*template*的缺省*is_end_char***
