import requests

def sendText(Email, Password,ApiCode,Recipients,Message):
    payload = {'Email': Email, 'Password': Password, 'ApiCode': ApiCode, 'Recipients': [Recipients], 'Message': Message}
    response = requests.post("https://api.itexmo.com/api/broadcast", data = payload)
    print(response.json())


def semaphore(apikey, number, message):
    payload = {'apikey': apikey, 'number': number, 'message': message}
    response = requests.post("https://api.semaphore.co/api/v4/messages", data = payload)
    print(response.json())

semaphore('e309b6a6c4d0a7e2a5d7afd5658f83d8', '09104698404', 'Hello, Im a test from TCC Online')
#sendText('tiritu@teleg.eu', 'P@ssw0rd', 'TR-JAYSM709975_UDGA9', '09104698404', 'Hello Jay!')