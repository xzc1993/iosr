for pid in $(ps -ef | grep "python" | grep -v "grep" |  awk '{print $2}'); do sudo kill -9 $pid; done
