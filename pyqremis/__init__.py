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


class ObjectExtension(QremisElement):
    _spec = {}


class LinkingRelationships(QremisElement):
    _spec = {}


class EnvironmentExtension(QremisElement):
    _spec = {}


class EnvironmentRegistry(QremisElement):
    _spec = {}


class EnvironmentDesignation(QremisElement):
    _spec = {}


class EnvironmentFunction(QremisElement):
    _spec = {}


class SignatureInformation(QremisElement):
    _spec = {}


class Storage(QremisElement):
    _spec = {}


class Fixity(QremisElement):
    _spec = {}


class Format(QremisElement):
    _spec = {}


class CreatingApplication(QremisElement):
    _spec = {
        'creatingApplicationName': {'repeatable': False, 'mandatory': False, 'type': str},

    }


class Inhibitors(QremisElement):
    _spec = {
        'inhibitorType': {'repeatable': False, 'mandatory': True, 'type': str},
        'inhinitorTarget': {'repeatable': True, 'mandatory': False, 'type': str},
        'inhibitorKey': {'repeatable': False, 'mandatory': False, 'type': str}
    }


class ObjectCharacteristicsExtension(QremisElement):
    _spec = {}


class ObjectCharacteristics(QremisElement):
    _spec = {
        'compositionLevel': {'repeatable': False, 'mandatory': False, 'type': str},
        'fixity': {'repeatable': True, 'mandatory': False, 'type': Fixity},
        'size': {'repeatable': False, 'mandatory': False, 'type': str},
        'format': {'repeatable': True, 'mandatory': True, 'type': Format},
        'creatingApplication': {'repeatable': True, 'mandatory': False, 'type': CreatingApplication},
        'inhibitors': {'repeatable': True, 'mandatory': False, 'type': Inhibitors},
        'objectCharacteristicsExtension': {'repeatable': True, 'mandatory': False,
                                           'type': ObjectCharacteristicsExtension}
    }


class SignificantPropertiesExtension(QremisElement):
    _spec = {}


class SignificantProperties(QremisElement):
    _spec = {
        'significantPropertiesType': {'repeatable': False, 'mandatory': False, 'type': str},
        'significantPropertiesValue': {'repeatable': False, 'mandatory': False, 'type': str},
        'significantPropertiesExtension': {'repeatable': True, 'mandatory': False,
                                           'type': SignificantPropertiesExtension}
    }


class PreservationLevel(QremisElement):
    _spec = {
        'preservationLevelType': {'repeatable': False, 'mandatory': False, 'type': str},
        'preservationLevelValue': {'repeatable': False, 'mandatory': True, 'type': str},
        'preservationLevelRole': {'repeatable': False, 'mandatory': False, 'type': str},
        'preservationLevelRationale': {'repeatable': True, 'mandatory': False, 'type': str},
        'preservationLevelDateAssigned': {'repeatable': False, 'mandatory': False, 'type': str}
    }


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
        'storage': {'repeatable': True, 'mandatory': False, 'type': Storage},
        'signatureInformation': {'mandatory': False, 'repeatable': True, 'type': SignatureInformation},
        'environmentFunction': {'mandatory': False, 'repeatable': True, 'type': EnvironmentFunction},
        'environmentDesignation': {'mandatory': False, 'repeatable': True, 'type': EnvironmentDesignation},
        'environmentRegistry':  {'mandatory': False, 'repeatable': True, 'type': EnvironmentRegistry},
        'environmentExtension': {'mandatory': False, 'repeatable': True, 'type': EnvironmentExtension},
        'linkingRelationships': {'mandatory': False, 'repeatable': False, 'type': LinkingRelationships},
        'objectExtension': {'mandatory': False, 'repeatable': True, 'type': ObjectExtension}
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
