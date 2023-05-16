def serialization(data, include=[], exclude=[]):
    serialized_data = {}
    
    if include:
        serialized_data = data.copy()
        for key in include:
            serialized_data[key] = None
    
    if exclude:
        serialized_data = dict((k, v) for k, v in data.items() if k not in exclude)

    return serialized_data

def check_jwt_exists(auth_info):
    if "status" not in auth_info.keys():
        return False
    return auth_info["status"]

# from sqlalchemy import insert, update
# def create_update_data(table, data, method):
#     if method == 'create':  
#         insert(table), {}
#         pass
#     elif method == 'update':
#         pass
#     else:
#         return "No Method"

