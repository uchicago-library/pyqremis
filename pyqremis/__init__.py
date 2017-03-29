from functools import partial


def lowerFirst(s):
    if not s:
        return s
    return s[0].lower() + s[1:]


class QremisElement:
    def __init__(self, *args, **kwargs):
        # Be sure we can build a valid element
        if len(args) == 0 and len(kwargs) == 0:
            raise ValueError("No empty elements!")
        mandatory_fields = set(x for x in self._spec if self._spec[x]['mandatory'] is True)
        provided_fields = set(lowerFirst(x.__class__.__name__) for x in args)
        provided_fields = provided_fields.union(set([x for x in kwargs]))
        for x in provided_fields:
            if x not in self._spec:
                raise TypeError("Erroneous field! - {}".format(x))
        if not mandatory_fields.issubset(provided_fields):
            raise ValueError(
                "The following are required for init, but were not present: {}".format(
                    ", ".join(mandatory_fields - provided_fields)
                )
            )

        # Dynamically build getters, setters, dellers, adders from spec
        for x in self._spec:
            setattr(self, "get_{}".format(x), partial(self.get_field, x))
            setattr(self, "set_{}".format(x),
                    partial(self.set_field, x, _type=self._spec[x]['type'],
                            repeatable=self._spec[x]['repeatable']))
            setattr(self, "del_{}".format(x), partial(self.del_field, x))
            if self._spec[x]['repeatable']:
                setattr(self, "add_{}".format(x), partial(self.add_to_field, x, _type=self._spec[x]['type']))

            # Set the object properties
            # TODO: Unbreak? Remove?
            # I think this has something to do with attribute search order?
            setattr(self, "{}".format(x), property(fget=getattr(self, "get_{}".format(x)),
                                                   fset=getattr(self, "set_{}".format(x)),
                                                   fdel=getattr(self, "del_{}".format(x))))

        # Build the element with the init args
        self._fields = {}
        for x in args:
            if not isinstance(x, QremisElement):
                raise ValueError("Only QremisElement instance are accepted as args")
            if self._spec[lowerFirst(x.__class__.__name__)]['repeatable']:
                getattr(self, "add_{}".format(lowerFirst(x.__class__.__name__)))(x)
            else:
                getattr(self, "set_{}".format(lowerFirst(x.__class__.__name__)))(x)
        for x in kwargs:
            if self._spec[x]['repeatable']:
                getattr(self, "add_{}".format(x))(kwargs[x])
            else:
                getattr(self, "set_{}".format(x))(kwargs[x])

    def set_field(self, fieldname, fieldvalue, _type=None, repeatable=False):
        if repeatable:
            try:
                self.add_to_field(fieldname, fieldvalue, _type=_type)
            except TypeError:  # Maybe its an iter of values
                for x in fieldvalue:
                    self.add_to_field(fieldname, x, _type=_type)
        else:
            if _type is not None:
                if not isinstance(fieldvalue, _type):
                    raise TypeError()
            self._fields[fieldname] = fieldvalue

    def add_to_field(self, fieldname, fieldvalue, _type=None):
        if _type is not None:
            if not isinstance(fieldvalue, _type):
                raise TypeError()
        if fieldname not in self._fields:
            self._fields[fieldname] = []
        self._fields[fieldname].append(fieldvalue)

    def get_field(self, fieldname):
        return self._fields[fieldname]

    def del_field(self, fieldname, index=None):
        # Dynamically removes empty fields
        if index:
            del self._fields[fieldname][index]
            if len(self._fields[fieldname]) == 0:
                del self._fields[fieldname]
        else:
            del self._fields[fieldname]

    def to_dict(self):
        r = {}
        return r


class PreservationLevel(QremisElement):
    _spec = {}


class ObjectIdentifier(QremisElement):
    _spec = {
        'objectIdentifierType': {'repeatable': False, 'mandatory': True, 'type': str},
        'objectIdentifierValue': {'repeatable': False, 'mandatory': True, 'type': str}
    }


class Object(QremisElement):
    _spec = {
        'objectIdentifier': {'repeatable': True, 'mandatory': True, 'type': ObjectIdentifier},
        'objectCategory': {'repeatable': False, 'mandatory': True, 'type': str},
        'preservationLevel': {'repeatable': True, 'mandatory': False, 'type': PreservationLevel},
        'significantProperties': {'repeatable': True, 'mandatory': False, 'type': SignificantProperties},
        'objectCharacteristics': {'repeatable': True, 'mandatory': True, 'type': ObjectCharacteristics},
        'originalName': {'repeatable': False, 'mandatory': False, 'type': str},
        'storage': {'repeatable': True, 'mandatory':
        'signatureInformation':
        'environmentFunction':
        'environmentDesignation':
        'environmentRegistry':
        'environmentExtension':
        'linkingRelationships':
        'objectExtension':
    }


class Event(QremisElement):
    _spec = {}


class Agent(QremisElement):
    _spec = {}


class Rights(QremisElement):
    _spec = {}


class Relationship(QremisElement):
    _spec = {}


class Qremis(QremisElement):
    _spec = {
        'object': {'repeatable': True, 'mandatory': False, 'type': Object},
        'event': {'repeatable': True, 'mandatory': False, 'type': Event},
        'agent': {'repeatable': True, 'mandatory': False, 'type': Agent},
        'rights': {'repeatable': True, 'mandatory': False, 'type': Rights},
        'relationship': {'repeatable': True, 'mandatory': False, 'type': Relationship}
    }
