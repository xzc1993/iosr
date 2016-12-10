import os
import shutil

if 'IOSR_TARGET_WORKER' in os.environ:
    shutil.rmtree('codeDeploy_script')
    os.rename('codeDeploy_worker_scripts', 'codeDeploy_script')