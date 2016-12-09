import subprocess
import os

p = subprocess.Popen("ps -ef | grep python | grep -v grep | grep -v ApplicationStop |  awk '{print $2}'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
stdout, stderr = p.communicate()
for pid in stdout.split():
        os.system("sudo kill {}".format(pid))