'''
cipush - Push your CI metrics to librato, statsd, ...

Usage:
    main.py (junit|coverage) <path> [-b <backend>] [-c <ci>]
    main.py -h | --help
'''
from docopt import docopt
import cipush.push

def main():
    args = docopt(__doc__)
    cipush.push.push(
        metrics_type= 'junit' if args['junit'] else 'coverage', 
        backend_slug= args['<backend>'] or 'json', 
        ci_slug= args['ci'] or 'default',
        path_pattern= args['<path>'],
        )



if __name__ == '__main__':
    main()