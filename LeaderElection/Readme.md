# Leader Election
A prototype for simulating the bully algorithm for choosing a new leader.

### Installation
The script requires ttab installed and the following packages from Pip:
 - zerorpc
 - gevent
 - sys
 - enum
```sh
$ ./startup.sh 5
```
Which will start 5 nodes from port 9000 -> 9004 on localhost.
Other wise run the manualy:
```sh
$ python bully.sh 127.0.0.1:9000
$ python bully.sh 127.0.0.1:9001
$ python bully.sh 127.0.0.1:9002
$ python bully.sh 127.0.0.1:9003
$ python bully.sh 127.0.0.1:9004
```

In each window
