import redis
import time
if __name__ == '__main__':
    time.sleep(20)
    conn = redis.Redis(host='redis')
    conn.set('abcd','blabla')
    print('OK!')