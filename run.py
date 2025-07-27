import os
from app import create_app
from pyngrok import ngrok
from dotenv import load_dotenv

load_dotenv()  #
authtoken = os.getenv('NGROK_TOKEN')
ngrok_domain = os.getenv('NGROK_DOMAIN')


app = create_app()

if __name__ == "__main__":
    if ngrok_domain:
        ngrok.set_auth_token(authtoken)
        ngrok_url = ngrok.connect(addr=9999, domain=ngrok_domain)
        print(f"Ngrok tunnel: {ngrok_url}")
    else:
        print("Running locally on http://localhost:9999")

    app.run(port=9999)
