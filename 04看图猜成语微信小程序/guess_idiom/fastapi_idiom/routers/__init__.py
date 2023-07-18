




# @router.get('/token')
# def get_token(openid: str):
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"openid": openid}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token}
#
#
# @router.post('/auth_token')
# def check_token(token: str):
#     result = auth_token(token)
#     return {'result': result}
