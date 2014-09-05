ci-metric-push
=======

[![Build Status](https://travis-ci.org/Zemanta/ci-metric-push.svg)](https://travis-ci.org/Zemanta/ci-metric-push)

*Work in progress...*

Push metrics about your code from your CI container to [ librato | statsd | ...] 

**Motivation**

Both Circle CI and Travis CI lack features that would show metrics about coverage, # of tests and tests duration over time. 

With this simple CLI tool you can simply push these metrics to various metrics backends for every build. Currently only librato is supported but adding other backends as statsd can be trivially implemented (*contributers welcome*).

**Usage**

Example for Circle CI

```
...

test:
    override:
        - coverage run manage.py test: # this command also emits JUnit XML files
           
    post:
        - cipush junit "TEST-*.xml" -b librato -c circleci -s frontend
...
```


**Comments**

Tested on python 2.6, 2.7, 3.4 (contributions welcome)

