import os
import yaml

import cipush

def default_config_file_path():
    current_dir = os.getcwd()
    return os.path.join(current_dir, '.pushci.yml')

def parse_config_file(config_file_path=None):
    file_path = config_file_path or default_config_file_path()
    try:
        with open(file_path, 'r') as f:
            return yaml.load(f)
    except yaml.YAMLError:
        raise cipush.CiPushException('can\'t parse yaml: {0}'.format(file_path))
    except IOError:
        raise cipush.CiPushException('can\'t open file: {0}'.format(file_path))


def validate_keys(keys_dict):
    must_have_config_keys = set(('pwd', 'suite', 'ci', 'backend'))
    assert must_have_config_keys.issubset(keys_dict.keys())

def validate_config(config_list):
    for single_conf_dict in config_list:
        assert len(single_conf_dict) == 1
        assert 'junit' in single_conf_dict or 'coverage' in single_conf_dict
        if 'junit' in single_conf_dict:
            validate_keys(single_conf_dict['junit'])
        else:
            validate_keys(single_conf_dict['coverage'])

def config_from_cli_args(args):
    metrics_type= 'junit' if args['junit'] else 'coverage', 
    suite_slug= args['--suite-name'] or 'main',
    backend_slug = args['--backend'] or 'json', 
    ci_slug= args['--ci'] or 'default',
    path_pattern= args['<path>'],

    return [{
            metrics_type: {
                'pwd': path_pattern,
                'suite': suite_slug,
                'ci': ci_slug,
                'backend': backend_slug
            }
        }]

def get_config_list(args):
    try:
        if args['--config-file']:
            config_list = parse_config_file(args['--config-file'])
            validate_config(config_list)
            return config_list

        if os.path.exists(default_config_file_path()):
            config_list = parse_config_file(default_config_file_path())
            validate_config(config_list)
            return config_list
    except AssertionError:
        raise cipush.CiPushException('unvalid yaml config structure')


    return config_from_cli_args(args)




