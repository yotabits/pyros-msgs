from __future__ import absolute_import
from __future__ import print_function

"""
Defining Schema for basic ros types

Detailed Ref : http://wiki.ros.org/std_msgs

These Fields and Schema are meant to be used together with ROS message type serialization :
ROSTCP --deserialize in rospy--> std_msgs.msg.* --serialize (dump) in pyros_msgs--> dict
And reversely :
dict --deserialize (load) in pyros_msgs--> std_msgs.msg.* --serialize in rospy--> ROSTCP

This helps pyros deal with data only as dicts without worrying about the underlying ROS implementation.
Also some serialization behavior adjustments have been done :

- optional fields

"""

import marshmallow
try:
    import std_msgs.msg as std_msgs
except ImportError:
    # Because we need to access Ros message types here (from ROS env or from virtualenv, or from somewhere else)
    import pyros_setup
    # We rely on default configuration to point us to the proper distro
    pyros_setup.configurable_import().configure().activate()
    import std_msgs.msg as std_msgs


# To be able to run doctest directly we avoid relative import
from pyros_msgs.schema.decorators import with_explicitly_matched_type


@with_explicitly_matched_type(std_msgs.Empty)
class RosMsgEmpty(marshmallow.Schema):
    """
    RosMsgBool Schema handles serialization from std_msgs.msgs.Bool to python dict
    and deserialization from python dict to std_msgs.msgs.Bool

    >>> schema = RosMsgEmpty()

    >>> rosmsg = std_msgs.Empty()
    >>> marshalled, errors = schema.dump(rosmsg)
    >>> marshmallow.pprint(marshalled) if not errors else print("ERRORS {0}".format(errors))
    {}
    >>> value, errors = schema.load(marshalled)
    >>> type(value) if not errors else print("ERRORS {0}".format(errors))
    <class 'std_msgs.msg._Empty.Empty'>
    >>> print(value) if not errors else print("ERRORS {0}".format(errors))
    <BLANKLINE>

    Load is the inverse of dump (if we ignore possible errors):
    >>> import random
    >>> randomRosEmpty = std_msgs.Empty()
    >>> schema.load(schema.dump(randomRosEmpty).data).data == randomRosEmpty
    True
    """
    pass


