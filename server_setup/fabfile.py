
# https://gist.github.com/eshandas/41683b920e116e29648de5f58f828778
# Fabfile to:
#    - update the remote system(s)
#    - download and install an application


"""
Steps to perform:
    cd to code directory
    Activate Virtual environment
    Pull latest code branch: Master
    Install Packages.
    Run Migrations
    InstallTasks for Cron
    Restart Supervisor.
"""


from fabric import Connection
from fabric import task

git = 'https://github.com/neerajgupta2407/telegram_bot_service.git'
# Path for code directory
path = '/home/ubuntu/codes/telegram_bot/telegram_bot_service'

# Virtual env path on server.
venv_path = '/home/ubuntu/codes/telegram_bot/tele_venv'



prod_servers = [
    # 'x.x.x.x', # admin
]
pem_file = "/Users/neeraj/.ssh/dsacademy.pem"

STAGES = {
    'prod':  {
        'hosts': prod_servers,
        'pem_file': pem_file,
        'code_dir': path,
        'code_branch': 'master',
        'virtual_env': venv_path,
        'user': 'ubuntu',
        'env_file': 'env_files/prod_env',
    },
}

def print_banner(messages):
    """
    Prints useful information while running a task
    """
    print('\n\n')
    print('...........................................')
    if type(messages) == list:
        for message in messages:
            print(message)
    else:
        print(messages)
    print('...........................................')
    print('\n\n')


@task(help={
    'stage-name': 'Name of the server which needs to be updated',
    'pem-file': 'The pem_file to use while connecting. If nothing provided, the default pem file will be used'})
def deploy(arg, stage_name, pem_file=None):
    """
    Pull updated code from repository and then restart all the services.

    Example:

        fab deploy -p some.pem -s dev
        or
        fab deploy -pem-file=some.pem -stage-name=dev
    """
    stage = STAGES[stage_name]

    if pem_file is None:
        pem_file = stage['pem_file']

    messages = [
        'Deploying %s' % stage_name,
        'Host: %s' % stage['hosts'],
        'Using pem: %s' % stage['pem_file']]
    print_banner(messages)

    for host in stage['hosts']:
        # Connect for each host (can be used Fabric groups here)
        with Connection(host=host, user='ubuntu', connect_kwargs={'key_filename': pem_file}) as c:
            # Change to the code directory
            with c.cd(stage['code_dir']):
                with c.prefix(f"source {venv_path}/bin/activate "):
                    c.run('git checkout {0} && git pull origin {0}'.format(stage['code_branch']))

                    print_banner("Installing packages..")
                    c.run('pip install -r installed_packages')

                    print_banner("Applying Migrations")
                    c.run('python manage.py migrate')

                    print_banner("Install Cron tasks")
                    c.run('python manage.py installtasks')

                    print_banner("Restarting Supervisor.")
                    c.run('sudo supervisorctl restart all')

###
