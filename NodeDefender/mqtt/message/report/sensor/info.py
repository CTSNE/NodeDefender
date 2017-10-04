import NodeDefender

def qry(topic, payload):
    return NodeDefender.icpe.sensor.\
            sensor_info(topic['mac_address'], topic['node'], **payload)

def sup(topic, payload):
    if type(payload) is not dict:
        return True
    
    types = payload['typelist'].split(',')
    return NodeDefender.icpe.sensor.commandclass.\
            commandclass_types(topic['mac_address'], topic['node'],
                               topic['commandClass'], *types)

def evtsup(topic, payload):
    return True # Add support later
