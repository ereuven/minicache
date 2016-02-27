# Minicache
Simple python memory caching solution.

### Dependencies:
- enum34

If pip exists, will try to install when running _setup.py install_.

### Install:
```bash
git clone https://github.com/ereuven/minicache
cd minicache
python setup.py install
```

### Sample usage:
See *test.py*
```python
from minicache import *

# init (max_size, expire_seconds, behaviour are optional)
# defaults:
#       max_size: 0 (unlimited)
#       expire_seconds: 0 (unlimited)
#       behaviour: MC_BEHAVIOUR.FIFO    (will remove oldest item if max_size exceeded)
#               [ MC_BEHAVIOUR.RAISE_ERROR will raise MC_EXCEPTION if max_size exceeded]
mc = minicache(max_size=2, expire_seconds=300, behaviour=MC_BEHAVIOUR.FIFO)

print mc            # {}

# set values
mc.a = [1, 2, 3]
mc['b'] = 'b'
mc.set('c', 3)      # key, value
mc.set('d', 4, 20)  # key, value, custom expiration time (20 seconds)

print mc            # {'c': 3, 'd': 4}

# delete an item
mc.delete('c')
# or
del(mc['c'])

print mc            # {'d': 4}

# get item details
print mc.d          # 4
print mc['d']       # 4
print mc.get('d'
)   # 4
print mc.getCreated('d')    # 2016-02-26 14:44:04.825725
print mc.getExpires('d')    # 2016-02-26 14:44:47.111368

# delete all items
mc.clear()
print mc            # {}

# print configuration
print mc.getConfig()    # {'behaviour': <MC_BEHAVIOUR.FIFO: 0>, 'expire_seconds': 300, 'max_size': 2}

# more methods
mc.a=1
mc.b=['a', 'b', 'c']
mc.c={'aa': 11, 'bb': 22}

print mc            # {'a': 1, 'c': {'aa': 11, 'bb': 22}, 'b': ['a', 'b', 'c']}
print mc.keys()     # ['a', 'c', 'b']
print mc.values()   # [1, {'aa': 11, 'bb': 22}, ['a', 'b', 'c']]
print mc.items()    # [('a', 1), ('c', {'aa': 11, 'bb': 22}), ('b', ['a', 'b', 'c'])]
print mc.dict()     # {'a': 1, 'c': {'aa': 11, 'bb': 22}, 'b': ['a', 'b', 'c']}
```
