
# MongoSafe



Provides safe reference fields for mongoengine and Flask-admin dashboard.


[Mongoengine](https://github.com/MongoEngine/mongoengine) is an ORM-like layer on top of PyMongo.


> Please note: This may not be the fastest way to manipulate data but it protects you from null references that will break Flask-admin.


## Example

Some simple examples of what MongoEngine code looks like:

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

Tests
=====
To run the test suite, ensure you are running a local instance of MongoDB on
the standard port and have ``nose`` installed. Then, run ``python setup.py nosetests``.
