# History


## 1 (2017-01-28)

* First release on PyPI.

## 1.0.1 (2017-01-29)

* Rename package due to conflict in PyPI.

## 1.0.2 (2017-01-29)

* Fix broken docs.

## 1.0.3 (2017-01-29)

* Fix bug with the template not beign include in the package.

## 1.1.0 (2017-06-25)

* Improment of documantation
* Custom templates feature
* Minor internal changes

## 1.1.1 (2017-07-16)

* Fix print func bug inseted on 1.1.0
* Fix loading default template in py27 inserted on 1.1.0
* Fix time elapsed output in console.
* Fix template overwrite when runned in the same minute.


## 1.1.2 (2018-01-27)

* Minor fix


## 1.2 (2019-03-15)

* Fixed Template wording
* Add support for combining reports into single report.
* Add support for test cases with underscores in name.
* Add optional timestamp of filenames.
* Add optional automatic opening of generated reports in browser tab/
* Add support for optional user variables to be passed to template.
* Add tracebacks to reports.
* Add stdout to reports.
* Add print relative paths to generated reports
* Made default output directory the current working directory so there are now no required args
* Update and adjusted readme
* Changed use of deprecated _TextTestResult -> TextTestResult
* Changed format of template slightly
expanded test case names to include full path to classes (should avoid clashes from * duplicate names)
* Simply test method names
* Update docstrings and deleted unused method
* Add check for template_args to be dict-like
* Add optional report naming
* Add support for subtests
* Add support for skipped tests skip reasons
* Change template to support subtests in sub-tables
* Fixed bug where non-combined tests had summaries with details from all tests
* Tweaked format of HTML has that info buttons line up better
