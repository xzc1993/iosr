export C_FORCE_ROOT='true'
cd /home/ubuntu/iosr
celery -A tasks worker --loglevel=info --pool=solo > /home/ubuntu/iosr/launch.log 2>&1 &