'''
'''

import os, sys, subprocess, traceback

import datamodel

def get_data_utils_dir():

    return os.path.dirname(os.path.realpath(__file__))

def get_data_model_dir():

    return os.path.dirname(os.path.realpath(datamodel.__file__))

def get_git_info(path): # todo get branch also
    '''
    path is a string giving a path from which a git repository can be found
    returns a dict describing the current state of the repository,
    including the commit it is currently pointed to:

        'commit': the alpha-numeric commit ID
        'date': the date of the commit
        'branch': the branch we are on now
    '''

    repo = {
        'branch': None,
        'commit': None,
        'date': None,
        'query_return_code': None,
        'query_err': None,
        'exception': None,
        }

    repo['query_path'] = path

    # run "git log"
    results = subprocess.run(['git', 'log', '-1'], cwd=path, capture_output=True)

    repo['query_return_code'] = results.returncode
    repo['query_out'] = results.stdout.decode(sys.stdout.encoding)
    repo['query_err'] = results.stderr.decode(sys.stderr.encoding)
    
    keys = ['commit', 'date']
    if repo['query_return_code'] == 0:
        try:
            lines = repo['query_out'].splitlines()
            for line in lines:
                line_lower = line.lower()
                for k in keys:
                    if line_lower.startswith(k):
                        if repo[k] is not None:
                            raise Exception('"{}" appears more than once'.format(k))
                        repo[k] = line[len(k):].lstrip(':').strip()
            for k in keys:
                if repo[k] is None:
                    raise Exception('"{}" does not appear'.format(k))
            #     if line.startswith('commit'):
            #         if repo['commit'] is not None:
            #             raise Exception('"commit" appears more than once')
            #         repo['commit'] = line.split('commit')[1].strip()
            #     if line.startswith('date'):
            #         if repo['date']:
            #             raise Exception('"date" appears more than once')
            #         repo['date'] = line.split('date:')[1].strip()
            # if repo['commit'] is None:
            #     raise Exception('"commit" does not appear')
            # if repo['date'] is None:
            #     raise Exception('"date" does not appear')
        except Exception as e:
            repo['exception'] = traceback.format_exc()

    return repo

def print_git_info_all():

    git_info = get_git_info(get_data_utils_dir())
    #git_info = get_git_info('error_dir')
    if git_info['query_return_code'] != 0 or git_info['exception'] is not None:
        msg = 'get_git_info failed for C3DataUtilities. git_info: {}'.format(git_info)
        print(msg)
        raise Exception(msg)
    else:
        print('C3DataUtilities commit ID: {}'.format(git_info['commit']))
        print('C3DataUtilities commit date: {}'.format(git_info['date']))

    git_info = get_git_info(get_data_model_dir())
    if git_info['query_return_code'] != 0 or git_info['exception'] is not None:
        msg = 'get_git_info failed for Bid-DS-data-model. git_info: {}'.format(git_info)
        print(msg)
        raise Exception(msg)
    else:
        print('Bid-DS-data-model commit ID: {}'.format(git_info['commit']))
        print('Bid-DS-data-model commit date: {}'.format(git_info['date']))

