from json import dumps
from httplib2 import Http
def gchatMessage(message):
    """Google Chat incoming webhook quickstart."""
    url = "https://chat.googleapis.com/v1/spaces/AAAAY9hmt_M/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=cLXMYuhb-Of-8IwguR29vcdNDiHG79Pk2L9uEnx2p-g"
    app_message = {
        'text': message}
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(app_message),
    )