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





**Comments**

Tested on python 2.6, 2.7, 3.4 (contributions welcome)

