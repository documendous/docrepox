## Contributing to Documendous Software Projects

Below are some topics to be aware of if you would like to contribute to development with this project.

---

### Code of Conduct

In the interest of maintaining an open and welcoming environment, we as contributors and maintainers pledge to making participation in Documendous Software Projects a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

---

### Django Debug Toolbar

In the development environment, the Django Debug Toolbar is disabled by default.

To disable it, you have two options:

1. **Modify the .env file:** Set DEBUG to 1 in the .env file used in the development Docker container.

2. **Update settings/debug.py:** Change the show_toolbar function to always return False:

```
def show_toolbar(request):
    return True

DEBUG = env("DEBUG")

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}
```

These changes should take effect without requiring a restart.

### Form Rendering

Use Django forms to define fields that will be used in your form. On the templating side, use django-widget-tweaks to render them unless manual rendering is absolutely necessary.

---

### Javascript

Use libraries like HTMX or Alpine.js to minimize standard Javascript usage where possible. Using vanilla Javascript is ok when needed but must be refactored to the appropriate javascript file.

#### HTMX

For use of AJAX type calls and functions especially from UI elements, consider using HTMX.

---

### Helper scripts

* dev-up.sh : runs the development docker containers
* prod-up.sh : runs the production docker containers
* clear-containers.sh: clears containers and associated volumes. Important: data will be deleted!
* test.sh: runs test scripts

#### test.sh

This runs:

* flake8: a commonly used Python linter to enforce PEP8 guidelines
* mypy: checks for opportunities to add typing where appropriate
* isort: refactors Python imports where appropriate
* coverage: generates coverage and coverage report
* pip-audit: looks for vulnerabilities in the project's dependencies
* Django and Python tests: we only accept 100%

All tests should complete successfully and touch all parts of code as expected from the coverage script.

Important: this does not mean all functionality one can imagine should be tested! And obviously we don't want to test 3rd party (including Django) code.

Currently, coverage settings will look at all code except:

* migrations/\*
* manage.py,config/settings/\_\_init\_\_.py
* apps/\*\*/models.py
* apps/transformations/core.py
* \*\*/\_\_init\_\_.py
* config/settings/\*
* .venv/

If a function or method is not deemed needed for testing or if the work to do it is unnecessarily daunting, we can ignore it by placing the '# pragma: no coverage' comment at the end of the line where missing coverage is indicated.

### Pre-commit

Ensure you are using pre-commit when committing code. How to install pre-commit see: https://pre-commit.com/#installation

In the root of the project is a hidden file: .pre-commit-config.yaml

To use this configuration, in the root of the project run:

```
pre-commit install
```

Whenever you run git commit ... you will see output similar to this:

```
$ git commit -m "Issue #7 - Added pre-commit-config file"
Check for added large files..............................................Passed
runflake8................................................................Passed
- hook id: runflake8
- duration: 0.37s
runtests.................................................................Passed
- hook id: runtests
- duration: 0.76s

Found 0 test(s).
System check identified no issues (0 silenced).

----------------------------------------------------------------------
Ran 0 tests in 0.000s

NO TESTS RAN

coverage.................................................................Passed
- hook id: coverage
- duration: 0.33s

Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
config/__init__.py       0      0   100%
config/settings.py      26      0   100%
config/urls.py           3      0   100%
--------------------------------------------------
TOTAL                   29      0   100%

[Issue-7 dd5b393] Issue #7 - Added pre-commit-config file
 1 file changed, 38 insertions(+)
 create mode 100644 .pre-commit-config.yaml

 pip-audit................................................................Passed
 - hook id: pip-audit
 - duration: 0.98s
 
 No known vulnerabilities found
 Name    Skip Reason
 ------- ----------------------------------------------------------------------
 docrepo Dependency not found on PyPI and could not be audited: docrepo (0.1.0)
 
 documentation............................................................Passed
 - hook id: documentation
 - duration: 0s
 
 Did you add documentation?

```

Note that it will run flake8, mypy, isort, a simple test suite, coverage and pip-audit.

At the end of the pre-commit run, there is also a reminder for contributing to documentation for any changes made. See section below on creating documentation. 

#### Creating Documentation

Documentation for DocrepoX is handled by the ddocs app. At this time, there are essentially 3 major areas where documentation should be considered for any change:

- Using DocrepoX (Using-DocrepoX.md) - for end user documentation
- Customizing DocrepoX (Customizing-DocrepoX.md) - for end users who wish to customize a feature (generally light customizations)
- Developing Documendous Software (Developing-Documendous.md) - general instructions for developers who would like to either extend or perform main development on Documendous products.

It is possible that a change or feature add will require entries in each of these. Currently, markdown is used for documentation. These files can be found in apps/ddocs/markdown/templates.

Once written, you can manually create the documention html templates for them. Each one of these will have a corresponding template. These are described in apps/ddocs/utils/chart/ddocs.py:

```python
chart = {
  "markdown_dir": "markdown/templates",
  "templates_dir": "templates",
  "styles_file": "staticfiles/styles.html",
  "items": [
      {
          "markdown": "Using-DocrepoX.md",
          "template": "ddocs/partials/_using_docrepox.html",
      },
      {
          "markdown": "Customizing-DocrepoX.md",
          "template": "ddocs/partials/_customizing_docrepox.html",
      },
      {
          "markdown": "Developing-Documendous.md",
          "template": "ddocs/partials/_contributing_documendous.html",
      },
  ],
}
```

To make use of this chart, you can run at the command line in the apps/ddocs directory:

```
# python utils/md2html.py
```

Be aware that pre-commit will run the md2html script.

This will create the corresponding html template in the ddocs templates directory.

#### CSS

Tailwind is used for CSS styling. For Tailwind Docs: see https://tailwindcss.com/docs/installation

Any ui style modifications or adds should be consistent with the rest of the project. You will need to have tailwind running when you make css changes so that the styles.css gets updated. To work with tailwind, you will need to ensure you have the latest nodejs runtime installed along with npm.

* To run tailwind, go to the tailwind/ directory in the root of the project. 

* You will need to install the node packages needed first:

```
> npm install
```

* After that, you run the tailwind compiler in either of these fashions:

```
> npm run tw-doc:watch  # to continuously run and update
```

or

```
> npm run tw-doc:build  # for single builds
```

#### UI Template Organization

In an html page, the best practice is to set a page like this:

```
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ page_title }}</title>
</head>
<body>
  <header>
    DocrepoX!
    <nav>
      <ul>
        <li><a href="">Nav Link 1</a></li>
        <li><a href="">Nave Link 2</a></li>
        ...
      </ul>
    </nav>
  </header>
  <main>
    <h1>Page Header!</h1>
    <section>
      This is section 1 ...
    </section>
    <section>
      This is section 2 ...
    </section>
    ...
  </main>
  <footer>
    My footer
  </footer>
</body>
</html>
```

Ideally, each of the top level tags: head, body, header, nav, main, section, footer should have their own template page.

Templates, ideally should be organized like this:

```
.
└── ui
    ├── base
    │   ├── _base.html
    │   ├── _footer.html
    │   ├── _header.html
    │   └── _head.html
    ├── css
    │   └── _css_links.html
    ├── index.html
    └── js
        └── _js_sources.html
```

#### Views

Class-based views (CBVs) are generally preferred.

However, functional views can be used for simple GET operations that do not require the additional functionality typically associated with CBVs.

##### Messaging

For operations where user notifications in the UI are useful, we recommend using Django's messaging system. Here is an example:

```python
messages.add_message(
    request,
    messages.INFO,
    f'Project "{project.name}" was successfully created.',
)

return HttpResponseRedirect(redirect_url)
```

When this code is placed in a view before a redirect, it will display the message as a notification to the user in the UI.

#### Unit Tests

Unit tests are run with test.sh script in the docrepo project folder.

To run:

```
./test.sh

Found 2 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..
----------------------------------------------------------------------
Ran 2 tests in 0.030s

OK
Destroying test database for alias 'default'...
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
apps/__init__.py            0      0   100%
apps/core/__init__.py       0      0   100%
apps/core/admin.py          0      0   100%
apps/core/apps.py           4      0   100%
apps/core/models.py         0      0   100%
apps/core/tests.py          9      0   100%
apps/core/urls.py           4      0   100%
apps/core/views.py          6      0   100%
apps/ui/__init__.py         0      0   100%
apps/ui/admin.py            0      0   100%
apps/ui/apps.py             4      0   100%
apps/ui/models.py           0      0   100%
apps/ui/tests.py            3      0   100%
apps/ui/urls.py             4      0   100%
apps/ui/views.py            6      0   100%
config/__init__.py          0      0   100%
config/settings.py         29      0   100%
config/urls.py              3      0   100%
-----------------------------------------------------
TOTAL                      72      0   100%
```

The core app has a set of generic tests in core/tests.py.

Each View should inherit the GenericViewTest from this module and put in your app's tests.py file:

```
from apps.core.tests import ViewTest


class IndexViewTest(ViewTest):
    url_name = "repo:index"

```

#### Refactoring

Views should be thin. Make use of functions and methods.

Ideally, one module (a Python file) or a template should:

- Contain one view for views modules.
- Be viewable without needing to scroll but if your class or set of functions exceed the page view of your editor, then keep it around 100 lines.
- Broken into other logical templates once larger than a page view.
- Contain one model for major models.
- Or ... group smaller models into one logical module.

Make good use of `__init__.py` files.

