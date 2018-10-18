# Contributing
First of all, every participant should obey [_Contributor Covenant Code of Conduct_](CODE_OF_CONDUCT.md).
In this project, Chinese and English both are welcoming. Besides, before starting
working, I strongly recommend that all of you notify and talk with me (via [Gitter](https://gitter.im/Python-PyLf/PyLf)
or email) first.


## Workflow
1. Fork the PyLf repository;
2. Run `pip install -r requirements.txt` to install the requirements;
3. Do your contribution;
4. Provide tests for any newly added code in `pylf` package;
5. Run [*black*](https://github.com/ambv/black) on the file(s) you have changed or added
with default configuration;
6. Run `tox` in the project's root folder and run `tests/watch_by_eyes.py`;
7. Create a pull request to pull the changes to the master branch.


## Guidelines
* Keep [_The Zen of Python_](https://www.python.org/dev/peps/pep-0020/#the-zen-of-python)
in mind;
* One commit for one change;
* Maximum line length is 88 characters;
* Only can use English in source codes, except in comments;
* Documentations and Examples both are for released versions; 
* Otherwise follow [_Google Python Style Guide_](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#google-python-style-guide);
* Contact me if you have any question.
