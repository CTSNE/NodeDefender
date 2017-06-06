from ... import BaseModel, PayloadSplitter, DataDescriptor
from .. import ClassInfo

mtype = {'1' : 'AirTemperature', '0x01' : 'AirTemperature',
         '01' : 'AirTemperature'}

class MsensorModel:
    unit = DataDescriptor('unit')
    type = DataDescriptor('type')
    precision = DataDescriptor('precision')
    size = DataDescriptor('sizeize')
    data32 = DataDescriptor('data32')
    data = DataDescriptor('data')

    def __init__(self):
        self.unit = None
        self.type = None
        self.precision = None
        self.size = None
        self.data32 = None
        self.data = None
        super().__init__()

def Info(classtype = None):
    if classtype:
        try:
            return eval(mtype[classtype] + '.Info')()
        except KeyError:
            return False
    classinfo = ClassInfo()
    classinfo.number = '31'
    classinfo.name = 'msensor'
    classinfo.types = True
    return classinfo

def Icon(value):
    return False

def Load(classtypes):
    return {'meter' : 0}

def Fields():
    return False

@PayloadSplitter(model=MsensorModel)
def Event(payload):
    try:
        return eval(mtype[payload.type] + '.Event')(payload)
    except KeyError as e:
        print(str(e))

from . import AirTemperature