def jwt_response_payload_handler(token, user=None):
    """
    returns payload response for particular token
    """
    return {
        "token": token,
        "user": str(user.username),
        "active": user.is_active
    }
