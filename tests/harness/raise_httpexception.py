class HTTPError(Exception):
    ...


class HTTPException(Exception):
    ...


def foobar():
    raise HTTPError(
        status_code=500,
        message='Foobar',
    )


async def foobar2():
    raise HTTPException()
