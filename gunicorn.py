import gevent.monkey
import os
gevent.monkey.patch_all()



if not os.path.exists('log'):
    os.mkdir('log')
debug = False
loglevel = 'debug'
timeout = 600
bind = '0.0.0.0:8089'
pidfile = 'log/gunicorn.pid'
logfile = 'log/debug.log'
errorlog = 'log/error.log'
accesslog = 'log/access.log'

workers = 1  # 预设2个
worker_class = 'gunicorn.workers.ggevent.GeventWorker'

x_forwarded_for_header = 'X-FORWARDED-FOR'
