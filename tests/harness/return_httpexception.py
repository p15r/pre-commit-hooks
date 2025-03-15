def foobar():
    return AFKException(
        status_code=500,
        message='Foobar',
    )

async def foobar2():
    return HTTPException()

async def foobar3():
    resp = HTTPException()
    return resp
