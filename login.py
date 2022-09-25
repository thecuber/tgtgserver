import sys
from tgtg import TgtgClient

def get_credentials(mail: str):
    client = TgtgClient(email=mail)
    return client.get_credentials()

if __name__ == "__main__":
    args = sys.argv[1:]
    mail = args[0]
    print("Getting credentials for mail", mail)
    print(get_credentials(mail))


