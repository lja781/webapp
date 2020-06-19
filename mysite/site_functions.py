def generate_meta(request):
    meta = {}
    meta["is_logged_in"] = request.user.is_authenticated
    return meta
