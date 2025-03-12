import os

def update_token():
    token = input("Enter your Discord Bot Token: ")
    with open('.env', 'w') as env_file:
        env_file.write(f"DISCORD_BOT_TOKEN={token}\n")
    print("Token updated successfully.")

if __name__ == "__main__":
    update_token()
