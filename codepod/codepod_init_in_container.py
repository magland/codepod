#!/usr/bin/env python3
import yaml
import subprocess
import os

def main():
  config=None  
  if os.path.exists('.codepod.yml'):
    config=_parse_yaml('.codepod.yml')
  
  print(':::::::::::::::::::::::config:',config)
  if config:
    if 'tasks' in config:
      for task in config['tasks']:
        if 'command' in task:
          shell_execute(task['command'])
  print('+++extra+',config)
  print(os.environ)
  shell_execute(os.environ['EXTRA_CMD'])

def _parse_yaml(fname):
  try:
    with open(fname) as f:
      obj=yaml.load(f)
    return obj
  except:
    return None

def shell_execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        #yield stdout_line
        print(stdout_line,end='\r')
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

if __name__== "__main__":
  main()
