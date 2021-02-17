### Contributing to KreusadaCogs

- Contributions are always welcome. Please describe your issue or feature request and I will do my best to satisfy you and evaluate the changes.

I run two checks here, to make sure that everything is merged safely and in style.

### 1. Flake8 Linting

Flake8 is used to ensure the code is correct and contains no NameErrors, IndentationErrors, and so on.
Please check that your code is correct before submitting a pull request.

### 2. Black Style

Black is used to unify styles for each of my cogs so they are more presentable and legible.
You can find out more about its installation and usage below.


_Black_ can be installed by running `pip install black`. It requires Python 3.6.0+ to
run but you can reformat Python 2 code with it, too.

# Usage

To get started right away with sensible defaults:

```sh
black {source_file_or_directory}
```

You can run _Black_ as a package if running it as a script doesn't work:

```sh
python -m black {source_file_or_directory}
```

# Command line options

_Black_ doesn't provide many options. You can list them by running `black --help`:

```text
Usage: black [OPTIONS] [SRC]...

  The uncompromising code formatter.

Options:
  -c, --code TEXT                 Format the code passed in as a string.
  -l, --line-length INTEGER       How many characters per line to allow.
                                  [default: 88]

  -t, --target-version [py27|py33|py34|py35|py36|py37|py38|py39]
                                  Python versions that should be supported by
                                  Black's output. [default: per-file auto-
                                  detection]

  --pyi                           Format all input files like typing stubs
                                  regardless of file extension (useful when
                                  piping source on standard input).

  -S, --skip-string-normalization
                                  Don't normalize string quotes or prefixes.
  -C, --skip-magic-trailing-comma
                                  Don't use trailing commas as a reason to
                                  split lines.

  --check                         Don't write the files back, just return the
                                  status.  Return code 0 means nothing would
                                  change.  Return code 1 means some files
                                  would be reformatted. Return code 123 means
                                  there was an internal error.

  --diff                          Don't write the files back, just output a
                                  diff for each file on stdout.

  --color / --no-color            Show colored diff. Only applies when
                                  `--diff` is given.

  --fast / --safe                 If --fast given, skip temporary sanity
                                  checks. [default: --safe]

  --include TEXT                  A regular expression that matches files and
                                  directories that should be included on
                                  recursive searches.  An empty value means
                                  all files are included regardless of the
                                  name.  Use forward slashes for directories
                                  on all platforms (Windows, too).  Exclusions
                                  are calculated first, inclusions later.
                                  [default: \.pyi?$]

  --exclude TEXT                  A regular expression that matches files and
                                  directories that should be excluded on
                                  recursive searches.  An empty value means no
                                  paths are excluded. Use forward slashes for
                                  directories on all platforms (Windows, too).
                                  Exclusions are calculated first, inclusions
                                  later.  [default: /(\.direnv|\.eggs|\.git|\.
                                  hg|\.mypy_cache|\.nox|\.tox|\.venv|\.svn|_bu
                                  ild|buck-out|build|dist)/]

  --force-exclude TEXT            Like --exclude, but files and directories
                                  matching this regex will be excluded even
                                  when they are passed explicitly as
                                  arguments.

  --stdin-filename TEXT           The name of the file when passing it through
                                  stdin. Useful to make sure Black will
                                  respect --force-exclude option on some
                                  editors that rely on using stdin.

  -q, --quiet                     Don't emit non-error messages to stderr.
                                  Errors are still emitted; silence those with
                                  2>/dev/null.

  -v, --verbose                   Also emit messages to stderr about files
                                  that were not changed or were ignored due to
                                  --exclude=.

  --version                       Show the version and exit.
  --config FILE                   Read configuration from FILE path.
  -h, --help                      Show this message and exit.
```
