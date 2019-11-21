"""
Common MongoDB connection functions.
"""
import pymongo
from mongodb_proxy import MongoProxy
from pymongo import ReadPreference


# pylint: disable=bad-continuation
def connect_to_mongodb(
    db, host,
    port=27017, tz_aware=True, user=None, password=None,
    retry_wait_time=0.1, proxy=True, **kwargs
):
    """
    Returns a MongoDB Database connection, optionally wrapped in a proxy. The proxy
    handles AutoReconnect errors by retrying read operations, since these exceptions
    typically indicate a temporary step-down condition for MongoDB.
    """
    # The MongoReplicaSetClient class is deprecated in Mongo 3.x, in favor of using
    # the MongoClient class for all connections. Update/simplify this code when using
    # PyMongo 3.x.
    if kwargs.get('replicaSet'):
        # Enable reading from secondary nodes in the MongoDB replicaset by using the
        # MongoReplicaSetClient class.
        # The 'replicaSet' parameter in kwargs is required for secondary reads.
        # The read_preference should be set to a proper value, like SECONDARY_PREFERRED.
        mongo_client_class = pymongo.MongoReplicaSetClient
    else:
        # No 'replicaSet' in kwargs - so no secondary reads.
        mongo_client_class = pymongo.MongoClient

    # If read_preference is given as a name of a valid ReadPreference.<NAME> constant
    # such as "SECONDARY_PREFERRED", convert it. Otherwise pass it through unchanged.
    if 'read_preference' in kwargs:
        read_preference = getattr(ReadPreference, kwargs['read_preference'], None)
        if read_preference is not None:
            kwargs = kwargs.copy()
            kwargs['read_preference'] = read_preference

    mongo_conn = pymongo.database.Database(
        mongo_client_class(
            host=host,
            port=port,
            tz_aware=tz_aware,
            document_class=dict,
            **kwargs
        ),
        db
    )

    if proxy:
        mongo_conn = MongoProxy(
            mongo_conn,
            wait_time=retry_wait_time
        )

    # If credentials were provided, authenticate the user.
    if user is not None and password is not None:
        mongo_conn.authenticate(user, password)

    return mongo_conn
