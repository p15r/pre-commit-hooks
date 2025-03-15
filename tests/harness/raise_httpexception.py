def foobar():
    raise AFKException(
        status_code=500,
        message='Foobar',
    )

async def foobar2():
    raise HTTPException()
