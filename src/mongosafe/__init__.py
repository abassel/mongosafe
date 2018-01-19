__version__ = '0.0.1'


import mongoengine as mongo
from bson import DBRef

#
# # https://hack.close.io/posts/mongomallard
class SafeReferenceField(mongo.ReferenceField):
    """
    Like a ReferenceField, but doesn't return non-existing references when
    dereferencing, i.e. no DBRefs are returned. This means that the next time
    an object is saved, the non-existing references are removed and application
    code can rely on having only valid dereferenced objects.

    When the field is referenced, the referenced object is loaded from the
    database.
    """

    def __init__(self, field, **kwargs):
        self.__class__.__name__ = "ReferenceField"
        # Fake as a ListField so form generation works.
        # Removing the line above will cause errors in Jinja complaining
        # that it cannot find fields to render HTML.
        # Check code in: env/lib/python2.7/site-packages/flask_admin/contrib/mongoengine/form.py:57
        # Convert function will remove SafeReferenceListField because it does not know how to convert them.
        # if not isinstance(field, mongo.ReferenceField):
        #     raise ValueError('Field argument must be a ReferenceField instance.')
        super(SafeReferenceField, self).__init__(field, **kwargs)


    def to_python(self, value):
        """Convert a MongoDB-compatible type to a Python type."""
        try:
            # import pdb
            # from pprint import pprint
            # print value
            # pdb.set_trace()
            if (not self.dbref and
                    not isinstance(value, (DBRef, mongo.Document, mongo.EmbeddedDocument))):
                collection = self.document_type._get_collection_name()
                value = DBRef(collection, self.document_type.id.to_python(value))
            return value
        except:
            raise Exception("Blah blah")


    def __get__(self, instance, owner):

        toRet = None

        try:
            toRet = super(SafeReferenceField, self).__get__(instance, owner)
        except:
            pass

        return toRet



# https://hack.close.io/posts/mongomallard
class SafeReferenceListField(mongo.ListField):
    """
    Like a ListField, but doesn't return non-existing references when
    dereferencing, i.e. no DBRefs are returned. This means that the next time
    an object is saved, the non-existing references are removed and application
    code can rely on having only valid dereferenced objects.
    When the field is referenced, all referenced objects are loaded from the
    database.
    Must use ReferenceField as its field class.
    """

    def __init__(self, field, **kwargs):
        self.__class__.__name__ = "ListField"
        # Fake as a ListField so form generation works.
        # Removing the line above will cause errors in Jinja complaining
        # that it cannot find fields to render HTML.
        # Check code in: env/lib/python2.7/site-packages/flask_admin/contrib/mongoengine/form.py:57
        # Convert function will remove SafeReferenceListField because it does not know how to convert them.
        if not isinstance(field, mongo.ReferenceField):
            raise ValueError('Field argument must be a ReferenceField instance.')
        super(SafeReferenceListField, self).__init__(field, **kwargs)

    def to_python(self, value):
        result = super(SafeReferenceListField, self).to_python(value)
        if result:
            # for item in result:
            #     print "before >>>>>", type(item)
            objs = self.field.document_type.objects.in_bulk([obj.id for obj in result])
            # tmp = filter(None, [objs.get(obj.id) for obj in result])
            tmp = [_f for _f in [objs.get(obj.id) for obj in result] if _f]
            # for item in tmp:
            #     print "after >>>>>", type(item), item.name
            # print "Before:", len(result), "  After:", len(tmp)
            return tmp

