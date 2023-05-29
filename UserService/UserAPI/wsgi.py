from app import APP
import app

# @JWT.token_in_blocklist_loader # Callback function to check if a JWT exists in the database blocklist
# def check_if_token_revoked(jwt_header, jwt_payload):
#     """
#     Will run for every request and check if token is revoked
#     """
    
#     from service import Service
#     from config import ORM
#     from sqlalchemy import select
    
#     service = Service(model_config=ORM)
#     with service.query_model("Token_Blocklist") as (conn, Blocklist):
#         res = conn.execute(
#             select(Blocklist).where(Blocklist.jti == jwt_payload["jti"])
#         ).mappings().fetchone()

#         print("BLOCKLIST RESULT: ", res, flush=True)

#         return False if res is None else True


if __name__=="__main__":
    APP.run(host="0.0.0.0", port=5000)


