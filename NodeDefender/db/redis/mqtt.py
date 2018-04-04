from NodeDefender.db.redis import redisconn
from datetime import datetime
import NodeDefender

@redisconn
def load(mqtt, conn):
    if mqtt is None:
        return None
    i = {
        'host' : mqtt.host,
        'port' : mqtt.port,
        'online' : False,
        'date_created' : mqtt.date_created,
        'date_loaded' : datetime.now().timestamp()
     }
    for icpe in mqtt.icpes:
        load_icpe(mqtt, icpe)
    return conn.hmset(mqtt.host + str(mqtt.port), i)

@redisconn
def get(host, port, conn):
    return conn.hgetall(host + str(port))

@redisconn
def save(host, port, conn, **kwargs):
    field  = conn.hgetall(host + str(port))
    for key, value in kwargs.items():
        field[key] = str(value)
    field['date_updated'] = datetime.now().timestamp()
    return conn.hmset(host + str(port), field)

@redisconn
def get_icpe(host, port, mac_address, conn):
    return conn.hgetall(host + str(port) + mac_address)

@redisconn
def list_icpes(host, port, conn):
    return conn.smembers(host + str(port) + ":icpes")

@redisconn
def load_icpe(mqtt, icpe, conn):
    conn.sadd(mqtt.host + str(mqtt.port) + ":icpes", icpe.mac_address)
    return conn.hmset(mqtt.host + str(mqtt.port) + icpe.mac_address, {
        'sent' : 0,
        'recieved' : 0,
        'date_loaded' : datetime.now().timestamp()
    })

@redisconn
def message_sent(host, port, mac_address, conn):
    sent = conn.hget(host + str(port) + mac_address, "sent")
    if sent is None:
        sent = 0
    conn.hset(host + str(port) + mac_address, "sent", (int(sent) + 1))
    conn.hset(host + str(port) + mac_address, "last_send",
              datetime.now().timestamp())
    sent = conn.srandmember(host + str(port) + mac_address + ':sent')
    if sent and NodeDefender.db.icpe.online(mac_address):
        if (datetime.now().timestamp() - float(sent)) > 10:
            NodeDefender.db.icpe.mark_offline(mac_address)
    conn.sadd(host + str(port) + mac_address + ':sent', datetime.now().timestamp())
    return True

@redisconn
def message_recieved(host, port, mac_address, conn):
    recieved = conn.hget(host + str(port) + mac_address, "recieved")
    if recieved is None:
        recieved = 0
    conn.hset(host + str(port) + mac_address, "recieved", int(recieved) + 1)
    conn.hset(host + str(port) + mac_address, "last_recieved",
              datetime.now().timestamp())
    conn.srem(host + str(port) + mac_address + ':sent',\
              conn.smembers(host + str(port) + mac_address + ':sent'))
    if not NodeDefender.db.icpe.online(mac_address):
        NodeDefender.db.icpe.mark_online(mac_address)
    return True

@redisconn
def updated(host, port, conn):
    return conn.hmset(host + str(port), {'date_updated' : datetime.now().timestamp()})

@redisconn
def flush(host, port, conn):
    if conn.hkeys(host + str(port)):
        return conn.hdel(host + str(port), *conn.hkeys(host + str(port)))
    else:
        return True
