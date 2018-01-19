
#
# run with:  py.test tests --junitxml out.xml --cov
#

import pytest
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))


import mongoengine as me
from mongosafe import SafeReferenceField, SafeReferenceListField

me.connect('mydb')

class A(me.Document):
    title = me.StringField()
    protectedBs = SafeReferenceListField(me.ReferenceField('B'))
    unprotectedBs = me.ListField(me.ReferenceField('B'))
    singleBSafe = SafeReferenceField('B', default=None)
    singleBUNSAFE = me.ReferenceField('B', default=None)


class B(me.Document):
    title = me.StringField()


def test_invalid_references():
    b1 = B()
    b2 = B()
    b3 = B()
    b1.save()
    b2.save()
    b3.save()

    a = A()
    a.protectedBs = [b1, b2, b3]
    a.unprotectedBs = [b1, b2, b3]
    a.singleBSafe = b2
    a.singleBUNSAFE = b2
    a.save()

    b2.delete()

    a = A.objects().first()

    print (a.protectedBs)                  # [<B: B object>, <B: B object>]
    assert len(a.protectedBs) == 2

    print (a.unprotectedBs)                # [<B: B object>, DBRef('b', ObjectId('5a61353bfc70143154f58865')), <B: B object>]
    assert len(a.unprotectedBs) == 3

    print (a.singleBSafe)
    assert a.singleBSafe == None

    try:
        print (a.singleBUNSAFE)
        assert False
    except:
        assert True

    b1.delete()
    b3.delete()
    a.delete()


def test_example():
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

    b1.delete()
    b2.delete()
    a.delete()

if __name__ == "__main__":
    test_invalid_references()
    test_example()
