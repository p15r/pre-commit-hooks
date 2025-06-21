class HTTPError(Exception):
    ...


class HTTP422Error(Exception):
    ...


class HTTPException(Exception):
    ...


class WebSocketException(Exception):
    ...


def foobar():
    return HTTPError(
        status_code=500,
        message='Foobar',
    )


async def foobar2():
    return HTTPException()


async def foobar3():
    resp = HTTPException()
    return resp


def foobar4():
    return HTTP422Error(
        status_code=500,
        message='Foobar',
    )


async def foobar5():
    resp = WebSocketException()
    return resp
