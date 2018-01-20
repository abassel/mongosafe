
# MongoSafe

[![Build Status](https://travis-ci.org/abassel/mongosafe.svg?branch=master)](https://travis-ci.org/abassel/mongosafe)
[![Coverage Status](https://coveralls.io/repos/github/abassel/mongosafe/badge.svg?branch=master)](https://coveralls.io/github/abassel/mongosafe?branch=master)
[![PyPI version](https://badge.fury.io/py/mongosafe.svg)](https://badge.fury.io/py/mongosafe)
[![PyPI](https://img.shields.io/pypi/wheel/Django.svg)](https://pypi.python.org/pypi/mongosafe)
[![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)](https://pypi.python.org/pypi/mongosafe)
[![PyPI](https://img.shields.io/pypi/l/Django.svg)](https://pypi.python.org/pypi/mongosafe)


Provides safe reference fields for Mongoengine and Flask-admin dashboard without the need to migrate to MongoMallard!
It is heavily based(stolen) on [MongoMallard](https://hack.close.io/posts/mongomallard)


[Mongoengine](https://github.com/MongoEngine/mongoengine) is an ORM-like layer on top of PyMongo.
[Flask-admin](https://github.com/flask-admin/flask-admin) is a simple and extensible administrative interface framework for Flask.
[MongoMallard](https://hack.close.io/posts/mongomallard) is a fast ORM based on MongoEngine

> Please note: This may not be the fastest way to manipulate data but it protects you from null references that will break Flask-admin.

## Install

```bash
pip install mongosafe
```

## Example

In the example bellow, mongosafe handles missing references automatically:

```python

import mongoengine as me
from mongosafe import SafeReferenceField, SafeReferenceListField

class A(me.Document):
    protectedBs = SafeReferenceListField(me.ReferenceField('B'))
    unprotectedBs = me.ListField(me.ReferenceField('B'))

class B(me.Document):
    title = me.StringField()

b1 = B()
b2 = B()
b1.save()
b2.save()
a = A()
a.protectedBs = [b1, b2]
a.unprotectedBs = [b1, b2]
a.save()

b2.delete()

a = A.objects().first()

print (a.protectedBs)                  # [<B: B object>]
print (a.unprotectedBs)                # [<B: B object>, DBRef('b', ObjectId('5a62438cfc701444a2e2107f'))]

```

## References :notebook:
- [MongoMallard](https://hack.close.io/posts/mongomallard)
- [Mongoengine](https://github.com/MongoEngine/mongoengine)
- [Flask-admin](https://github.com/flask-admin/flask-admin)