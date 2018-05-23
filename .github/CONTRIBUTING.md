# Contributing
First of all, every participant should obey [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). In this project,
Chinese and English both are welcoming. Besides, before starting working, I strongly recommend that all of you notify
and talk with me (via [Gitter](https://gitter.im/Python-PyLf/PyLf) or email) first.


## Workflow
1. Fork the PyLf repository;
2. Run `pip install -r requirements.txt` to install the requirements;
3. Improve documents and examples, improve tests, optimize algorithm, etc;
4. Provide tests for any newly added code in `pylf` package;
5. Run `tox` in the project's root folder and run `tests/watch_by_eyes.py`;
6. Update `docs/release_notes.md` for non-transparent changes;
7. Create a pull request to pull the changes to the master branch.


## Guidelines
* One commit for one change;
* Maximum line length is 120 characters;
* Only can use English in source codes, except in comments;
* Maintain consistency with the whole (e.g. code style, algorithm, expressions, etc);
* Documentations and Examples both are for released versions; 
* Otherwise follow [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#Line_length);
* Contact me if you have any question.
