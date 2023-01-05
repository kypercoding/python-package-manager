import redis

from user import User


def create_redis_object(host="127.0.0.1", port="6379", db=0):
    """
    Returns a Redis connection.
    """
    return redis.Redis(host, port, db)


def set_user_tokens(user: User, params: dict):
    """
    Sets JWT tokens in Redis.
    """

    # create connection
    r = create_redis_object(params["host"], params["port"], params["db"])

    # get user info
    username = user.get_id()
    access_token = user.get_access_token()
    refresh_token = user.get_refresh_token()

    # set user tokens
    r.hset("users:{}".format(username), "access_token", access_token)
    r.hset("users:{}".format(username), "refresh_token", refresh_token)

    # close connection
    r.close()


def unset_user_tokens(user: User, params: dict):
    """
    Unset JWT tokens in Redis.
    """

    # create connection
    r = create_redis_object(params["host"], params["port"], params["db"])

    # get user info
    username = user.get_id()

    # unset user tokens
    r.delete("users:{}".format(username))

    # close connection
    r.close()


def get_access_token(id: str, params: dict):
    # create connection
    r = create_redis_object(params["host"], params["port"], params["db"])

    # get access token
    token = r.hget("users:{}".format(id), "access_token")

    # close connection
    r.close()

    return token


def get_refresh_token(id: str, params: dict):
    # create connection
    r = create_redis_object(params["host"], params["port"], params["db"])

    # get access token
    token = r.hget("users:{}".format(id), "refresh_token")

    # close connection
    r.close()

    return token
