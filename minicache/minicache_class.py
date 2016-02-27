import datetime
from enum import Enum

class MC_BEHAVIOUR(Enum):
    FIFO = 0
    RAISE_ERROR = 1

class MC_EXCEPTION(Exception):
    pass

class minicache:
    __data__ = dict()
    __conf__ = dict()

    # init & general
    def __init__(self, max_size=0, expire_seconds=0, behaviour=MC_BEHAVIOUR.FIFO):
        self.__conf__['expire_seconds']=(expire_seconds if expire_seconds >= 0 else 0)
        self.__conf__['max_size']=(max_size if max_size >= 0 else 0)
        self.__conf__['behaviour']=MC_BEHAVIOUR(behaviour)
        pass

    def getConfig(self):
        return dict(self.__conf__.items())
    # end: init & general

    # set
    def set(self, key, value, expires=None):
        try:
            expires = int(expires)
            if (expires<0): expires=0
        except:
            expires = self.__conf__['expire_seconds']

        if expires == 0: expires=None

        self.__clear__()

        if self.__conf__['max_size']>0 \
                and (len(self.__data__) >= self.__conf__['max_size']) \
                and key not in self.__data__.keys():
            if self.__conf__['behaviour'] == MC_BEHAVIOUR.RAISE_ERROR:
                raise MC_EXCEPTION('max_size exceeded')

            if self.__conf__['behaviour'] == MC_BEHAVIOUR.FIFO:
                del(self.__data__[self.__oldest_item__()])

        now = datetime.datetime.now()
        self.__data__[key] = {
            'created': now,
            'value': value,
            'expires': now + datetime.timedelta(seconds=expires) if expires else None
        }

    def __setattr__(self, key, value):
        self.set(key, value, self.__conf__['expire_seconds'])

    __setitem__ = __setattr__
    # end: set

    # get
    def __getattr__(self, item):
        data = self.__data__.get(item)
        if data:
            return data['value']
        return data

    __getitem__ = __getattr__

    def getExpires(self, item):
        data = self.__data__.get(item)
        if data:
            return data['expires']
        return data

    def getCreated(self, item):
        data = self.__data__.get(item)
        if data:
            return data['created']
        return data
    # end: get

    # represent
    def __repr__(self):
        self.__clear__()
        return dict([(k, v['value']) for k,v in self.__data__.items()]).__repr__()
        #return self.__data__.__repr__()

    # str
    __str__ = __repr__

    # delete
    def __delattr__(self, item):
        try:
            del(self.__data__[item])
        except KeyError:
            pass

    __delitem__ = __delattr__
    # end: delete

    # helpers
    def __clear__(self):
        now = datetime.datetime.now()
        ktd = []
        for k in self.__data__:
            if self.__data__[k]['expires'] \
                and now > self.__data__[k]['expires']:
                ktd.append(k)

        for k in ktd:
            del(self.__data__[k])

    def __oldest_item__(self):
        return min(self.__data__.items(), key=lambda v: v[1]['created'])[0]
    # end: helpers
