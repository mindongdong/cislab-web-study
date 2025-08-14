def make_response(status: str, data=None, message: str = "", meta: dict | None = None) -> dict:
    return {"status": status, "data": data, "message": message, "meta": meta}
