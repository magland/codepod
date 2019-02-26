import subprocess
import os
import shutil
import tempfile
import random
import string
import yaml

src_dir=os.path.dirname(os.path.realpath(__file__))

def codepod(*,repository='',image=None,volumes=[],mount_tmp=True,host_working_directory=None,docker_opts=None,git_smart=False,no_pull=False,command=False):
    if not docker_opts:
        docker_opts=''
    if docker_opts.startswith('"'):
        docker_opts=docker_opts[1:-1]
    if host_working_directory is None:
        if not repository:
            raise Exception('You must either specify a repository or a host working directory.')
        host_working_directory=_get_random_directory()
    host_working_directory=os.path.abspath(host_working_directory)
    if repository:
        if os.path.exists(host_working_directory):
            raise Exception('Host working directory already exists: '+host_working_directory)
        _git_clone_into_directory(repository,host_working_directory)

    config={}
    if os.path.exists(host_working_directory+'/.codepod.yml'):
        config=_parse_yaml(host_working_directory+'/.codepod.yml')

    print(':::::::::::::::::::::::config:',config)
    if image is None:
        if 'image' in config:
            image=config['image']
        
    if image is None:
        image='magland/codepod:latest'

    print('Using image: '+image)

    opts=[
        '-it',
        '--mount type=bind,source={src_dir}/codepod_init_in_container.py,destination=/codepod_init,readonly',
        '--mount type=bind,source={host_working_directory},destination=/home/project',
        '--network host',
        '--privileged',
        '-e DISPLAY=unix{}'.format(os.environ.get('DISPLAY','')),
        '--mount type=bind,source=/tmp/.X11-unix,destination=/tmp/.X11-unix'
    ]

    if command is not None:
        del opts[0]
        opts.append('--entrypoint="' + command + '"')

    # git configuration
#if [ -f "$HOME/.gitconfig" ]; then
#  OPTS="$OPTS -v $HOME/.gitconfig:/home/theiapod/.gitconfig"
#fi
#if [ -d "$HOME/.git-credential-cache" ]; then
#  OPTS="$OPTS -v $HOME/.git-credential-cache:/home/theiapod/.git-credential-cache"
#fi

    path0=os.environ.get('HOME','')+'/.gitconfig'
    if os.path.exists(path0):
        print('Mounting '+path0)
        opts.append('--mount type=bind,source={},destination={}'.format(path0,'/home/user/.gitconfig'))
    path0=os.environ.get('HOME','')+'/.git-credential-cache'
    if os.path.exists(path0):
        print('Mounting '+path0)
        opts.append('--mount type=bind,source={},destination={}'.format(path0,'/home/user/.git-credential-cache'))

    if mount_tmp:
        opts.append('--mount type=bind,source=/tmp,destination=/tmp')

    for vv in volumes:
        if type(vv)==tuple:
            opts.append('--mount type=bind,source={},destination={}'.format(os.path.abspath(vv[0]),os.path.abspath(vv[1])))
        else:
            raise Exception('volumes must be tuples.')

    if no_pull:
        print('Not pulling docker image because no_pull was specified')
    else:
        try:
            _run_command_and_print_output('docker pull {image}'.format(image=image))
        except:
            print('WARNING: failed to pull docker image: {image}... proceeding without pulling...'.format(image=image))

    cmd='docker run {opts} {docker_opts} {image} /home/project {user} {uid}'
    #cmd='docker run {opts} {image}'
    cmd=cmd.replace('{opts}',' '.join(opts))
    cmd=cmd.replace('{docker_opts}',docker_opts)
    cmd=cmd.replace('{src_dir}',src_dir)
    cmd=cmd.replace('{image}',image)
    # cmd=cmd.replace('{repository}',repository)
    cmd=cmd.replace('{host_working_directory}',host_working_directory)
    cmd=cmd.replace('{user}',os.environ['USER'])
    cmd=cmd.replace('{uid}',str(os.getuid()))

    print('RUNNING: '+cmd)
    os.system(cmd)
    #_run_command_and_print_output(cmd)

#def _write_text_file(fname,txt):
#    with open(fname,'w') as f:
#        f.write(txt)

def _parse_yaml(fname):
  try:
    with open(fname) as f:
      obj=yaml.load(f)
    return obj
  except:
    return None

def _get_random_directory():
    return tempfile.gettempdir()+'/codepod_workspace_'+_get_random_string(10)

def _get_random_string(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

def _git_clone_into_directory(repo,path):
    cmd='git clone {} {}'.format(repo,path)
    _run_command_and_print_output(cmd)

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        #yield stdout_line
        print(stdout_line,end='\r')
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def _run_command_and_print_output(cmd):
    print('RUNNING: '+cmd);
    execute(cmd.split())
