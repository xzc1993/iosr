export C_FORCE_ROOT=TRUE
cd /home/ubuntu/iosr
sudo celery -A tasks worker --loglevel=info --pool=solo > /home/ubuntu/iosr/launch.log 2>&1 &