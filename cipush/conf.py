import os
import yaml

def default_config_file_path():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_dir, '.pushci.yml')

def parse_config_file(config_file_path=None):
    file_path = config_file_path or default_config_file_path()
    with open(file_path, 'r') as f:
        return yaml.load(f)

def validate_keys(keys_dict):
    keys = set(keys_dict.keys())
    valid_config_keys = set(('pwd', 'suite', 'ci', 'backend'))
    must_have_config_keys = set(('pwd',))

    assert len(keys.difference(valid_config_keys)) == 0
    assert must_have_config_keys.issubset(keys)

def is_config_file_valid(config_list):
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



