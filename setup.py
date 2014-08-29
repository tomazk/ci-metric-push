from setuptools import setup, find_packages

setup(
    name = "ci-metric-push",
    version = "0.1",
    packages = find_packages(),
    scripts = ['pushci'],

    install_requires = [
        'librato-metrics==0.4.11',
        'docopt==0.6.2'
    ],

    author = "Tomaz Kovacic",
    author_email = "tomaz.kovacic@gmail.com",
    description = "Push metrics about your code from your CI container to [ librato | statsd | ...] ",
    license = "MIT",
    keywords = "ci metric push",
    url = "https://github.com/tomazk/ci-metric-push",   # project home page, if any
)