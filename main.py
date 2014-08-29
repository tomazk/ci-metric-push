'''
cipush - Push your CI metrics to librato, statsd, ...

Usage:
    main.py (junit|coverage) <path> [options] 
    main.py -h | --help

Options:
    -c <ci>, --ci <ci>
    -b <backend>, --backend <backend>
    -s <suite_name>, --suite-name <suite_name>
'''
from docopt import docopt
import cipush.push

def main():
    args = docopt(__doc__)
    cipush.push.push(
            metrics_type= 'junit' if args['junit'] else 'coverage', 
            suite_slug= args['--suite-name'] or 'main',
            backend_slug= args['--backend'] or 'json', 
            ci_slug= args['--ci'],
            path_pattern= args['<path>'],
        )

if __name__ == '__main__':
    main()