
# MongoSafe



Provides safe reference fields for mongoengine and Flask-admin dashboard.


[Mongoengine](https://github.com/MongoEngine/mongoengine) is an ORM-like layer on top of PyMongo.


> Please note: This may not be the fastest way to manipulate data but it protects you from null references that will break Flask-admin.


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

