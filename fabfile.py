from fabric.api import env, run, cd

def common():
    env.host_string = 'nqnwebs.com'
    env.user = 'nqnwebsc'


def production():
    env.python = '/home/nqnwebsc/.virtualenv/lacalma/bin/python'
    env.pip = '/home/nqnwebsc/.virtualenv/lacalma/bin/pip'
    env.app = '/home/nqnwebsc/projects/reservas'
    env.domain = '/home/nqnwebsc/reservas2.lacalma-lasgrutas.com.ar'
    common()


def develop():
    env.python = '/home/nqnwebsc/.virtualenv/reservas_test/bin/python'
    env.pip = '/home/nqnwebsc/.virtualenv/reservas_test/bin/pip'
    env.app = '/home/nqnwebsc/projects/reservas_test'
    env.domain = '/home/nqnwebsc/reservas-test.lacalma-lasgrutas.com.ar'
    common()


def restart():
    run("pkill python")
    run("touch %s/tmp/restart.txt" % env.domain)


def update(branch='master'):
    with cd(env.app):
        #run("git stash")
        run("git fetch && git reset --hard origin/%s" % branch)
        run("%s install -r requirements.txt" % env.pip)
        run("%s manage.py migrate" % env.python)
        run("echo 'yes' | %s manage.py collectstatic" % env.python)
        # run("git stash pop")
        restart()

def django_manage(cmd):
    with cd(env.app):
        run("%s manage.py %s" % (env.python, cmd))
