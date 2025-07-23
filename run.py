import os
from app import create_app
from pyngrok import ngrok
from dotenv import load_dotenv

load_dotenv()  #

authtoken = os.getenv('NGROK_TOKEN')
ngrok.set_auth_token(authtoken)

app = create_app()

if __name__ == "__main__":
    ngrok_url = ngrok.connect(addr=9999, domain="evident-kingfish-actual.ngrok-free.app")
    print(ngrok_url)
    app.run(port=9999)
