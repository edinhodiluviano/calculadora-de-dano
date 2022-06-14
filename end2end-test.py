import requests


HOST = "https://pshgh2ldvhzu2cw3sr2zpbv2x40cvhzd.lambda-url.us-east-1.on.aws/"


def test_ping_from_app():
    ping_path = "ping2"
    url = HOST + ping_path
    r = requests.get(url, timeout=5)
    assert r.status_code == 200, (r.status_code, r.text)
    assert r.json() == "ok", r.text


def test_ping_from_lambda():
    ping_path = "ping"
    url = HOST + ping_path
    r = requests.get(url, timeout=5)
    assert r.status_code == 200, (r.status_code, r.text)
    assert r.text == "healthy", r.text
