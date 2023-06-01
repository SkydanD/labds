import time
import hazelcast
import threading

client = hazelcast.HazelcastClient( cluster_members=["172.20.0.199:5701","172.20.0.199:5702","172.20.0.199:5703"])
lock = client.get_map('my-distributed-ma').blocking()

lock.set(1,0)
time.sleep(1)
def thread_function2(name):
    for i in range(10000):
         while True:
             oldValue = lock.get( 1 ) ;
             if lock.replace_if_same( 1, oldValue, oldValue+1 ):
                break
    print( f'Thread {name} done')
t = time.time()
threads = []
for index in range(10):
 x = threading.Thread(target=thread_function2, args=(index,))
 threads.append(x)
 x.start()
for thread in threads:
 thread.join()
print(time.time() - t)
print( lock.get(1))