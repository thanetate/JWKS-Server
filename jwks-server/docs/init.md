1. Init 

we run the server using:
python3 run.py

then we can curl the endpoints to make sure they are working. 

curl http://127.0.0.1:8080/jwks
{
  "keys": []
}
curl -X POST http://127.0.0.1:8080/auth
{
  "token": "valid_token_placeholder"
}