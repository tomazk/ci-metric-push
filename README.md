ci-metric-push
==============

[![Build Status](https://travis-ci.org/Zemanta/ci-metric-push.svg)](https://travis-ci.org/Zemanta/ci-metric-push)

*Work in progress...*

Push metrics about your code from your CI container to [ librato | statsd | ...] 

Motivation
----------

Both [Circle CI](https://travis-ci.org/) and [Travis CI](https://travis-ci.org/) lack features that would show metrics about coverage, # of tests and tests duration over time. 

With this simple CLI tool `pushci` you can simply push these metrics to various metrics backends for every build. Currently only librato is supported but adding other backends (*graphite via statsd for example*) as statsd can be trivially implemented (*contributers welcome*).

With metrics in librato you can then draw graphs that clearly demonstrate trends of code coverage, test suite execution duration, number of tests etc.

Usage
-----

In a nutshell:

- make sure your test suite emits JUnit formatted and cobertura formatted XML files (*made pupular by jenkins both formats are widely supported by test suites for various runtimes*)
- install this python package `pip install git+git://github.com/Zemanta/ci-metric-push.git#cipush`
- run your test suite
- then run `pushci junit "path/to/*.xml"` 



**`circle.yml` example**
```
dependencies:
    override:
        - pip install git+git://github.com/Zemanta/ci-metric-push.git#cipush

test:
    override:
        - coverage run tests.py # this command also emits JUnit XML files
           
    post:
        - coverage xml
        - pushci coverage "coverage.xml" -b librato -c circle -s backend_suite
```

**`.travis.yml` example**
```
install:
  - pip install git+git://github.com/Zemanta/ci-metric-push.git#cipush

script: coverage run tests.py

after_script:
    - coverage xml
    - pushci coverage "coverage.xml" -b librato -c circle -s backend_suite

```

Supported Backends
------------------

Currently `pushci` only supports pushing coverage and test metrics to [**librato**](http://librato.com) backend via their REST API. 

`pushci` uses enviroment variables `LIBRATO_USER` and `LIBRATO_TOKEN` to authenticate with librato api. Just make sure they are set within your container. 

Librato backend also emits an [annotation](http://dev.librato.com/v1/annotations) for every build so you can track down every chnage in your metric to the exact build.

Supported Metrics
-----------------

- **number of unit tests** are extracted from JUnit XML
- **duration of test suite** is also extracted from JUnit XML
- **coverage** is extracted from cobertura formatted XML file


Configuration
-------------

`pushci` can be configured either by cli arguments or in a `.pushci.yml` config file

**Arguments:**

* `<path>` unix style pathname pattern to your JUnit or cobertura XML files
* `<ci>` ci enviroment `circle|travis`
* `<suite_name>` suite name will appear as part of your metric so you're able to distinguish between suites that run in the same container (*e.g. frotend or backend suite*)
* `<config_file>` if not provided pushci will look for `.pushci.yml` in the current directory

**CLI usage**

```

Usage:
    pushci [options] 
    pushci (junit|coverage) <path> [options] 
    pushci -h | --help

Options:
    -c <ci>, --ci <ci>
    -b <backend>, --backend <backend>
    -s <suite_name>, --suite-name <suite_name>
    -f <config_file>, --config-file <config_file> 
    -d, --debug

```

**CLI examples**

* `$ pushci` will read config from `.pushci.yml` and execute
* `$ pushci --config-file ./example/.pushci.yml`
* `$ pushci junit "TEST-*.xml" -b librato -c circle -s frontend`

**`.pushci.yml` format**

```
- [coverage|junit]:
    pwd: <path>
    ci: <ci>
    backend: <backend>
    suite: <suite_name>

```

**`.pushci.yml` example**

```
- coverage:
    pwd: client/coverage/cobertura/C*/cobertura.xml
    ci: circle
    backend: librato
    suite: eins_frontend
- junit:
    pwd: client/test-results.xml
    ci: circle
    backend: librato
    suite: eins_frontend

- coverage:
    pwd: server/coverage.xml
    ci: circle
    backend: librato
    suite: eins_backend
- junit:
    pwd: server/.junit_xml/TEST-*
    ci: circle
    backend: librato
    suite: eins_backend

```


Comments
--------

Tested on python 2.6, 2.7, 3.4 (contributions welcome)

For licence see LICENCE file in this repo.

