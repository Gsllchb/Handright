# 新版本发布流程

在本项目，新版本的发布由且仅能由维护者（maintainer）来完成。维护者在发布新版本前务必遵照以下流程执行。

1. 在与其他维护者讨论后，决定发布新版本，并按照[Semantic Versioning](https://semver.org/)确定新版本号`{NEW_VERSION}`；
2. 更新`handright.__init__.__version__`；
3. 执行所有测试；
4. 若通过以上测试，则继续执行以下步骤；
5. 更新`docs/release_notes.md`（发布日期按照当地日期即可），并视情况将changelog重新整合完善（change不必按照时序排列）以及为新变化撰写摘要；
6. 视情况更新相应文档和创建新文档；
7. 提交更改到master分支上；
8. 在当前master分支的commit上创建标签`v{NEW_VERSION}`;
9. push标签和更改到GitHub；
10. 打包并发布新版本到PyPI：

    ```console
    python setup.py sdist
    python setup.py bdist_wheel
    twine upload ./dist/*{NEW_VERSION}*
    ```
