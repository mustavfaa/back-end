import httplib2
from ekitaphana.settings import BASE_1C_PATH
# import base64

h = httplib2.Http()
# import base64

# AUTH = base64.b64encode(b'reporter:qxrt5').decode()
AUTH = 'cmVwb3J0ZXI6cXhydDU='
HEADERS = {
    'Authorization': 'Basic ' + AUTH
}

a, b = h.request(
    uri=BASE_1C_PATH+"/eponortfoliohz/hs/otchet/get_otchet/?school=109",
    method="GET",
    headers=HEADERS,
)
from django.http import HttpResponse

HttpResponse(b, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
pass
# peremennaya b soderzhit file
