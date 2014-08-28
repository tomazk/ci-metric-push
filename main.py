'''
cipush - Push your CI metrics to librato, statsd, ...

Usage:
    main.py (junit|coverage) <path> 
    main.py (junit|coverage) <path> [-b <backend> | --backend <backend>]
    main.py -h | --help
'''
from docopt import docopt
import cipush.push

def main():
    args = docopt(__doc__)
    cipush.push.push(
        metrics_type= 'junit' if args['junit'] else 'coverage', 
        backend_slug= args['<backend>'] or 'json', 
        path_pattern= args['<path>']
        )



if __name__ == '__main__':
    main()