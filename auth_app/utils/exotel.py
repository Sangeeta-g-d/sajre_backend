import requests
from django.conf import settings

def send_otp_sms(phone_no: str, otp: str) -> bool:
    """
    Sends the OTP to the given number via Exotel 
    (URL uses EXOTEL_SID,   basic auth uses EXOTEL_API_TOKEN : EXOTEL_API_KEY)
    """
    # <-- EXOTEL_SID is used only in the URL
    url = f"https://api.exotel.com/v1/Accounts/{settings.EXOTEL_SID}/Sms/send.json"

    # <-- EXOTEL_API_TOKEN (username), EXOTEL_API_KEY (password) for basic authentication
    auth = (settings.EXOTEL_API_TOKEN, settings.EXOTEL_API_KEY)

    payload = {
        "From": settings.EXOTEL_SENDER_ID,
        "To": phone_no,
        "Body": f"Your OTP for login is {otp} and it is valid for 20 minutes Do not share OTP with anyone  sajre edutech pvt ltd -SAJRE EDUTECH PVT LTD",
        "DltEntityId": settings.EXOTEL_DLT_ENTITY_ID,
        "DltTemplateId": settings.EXOTEL_DLT_TEMPLATE_ID,
    }

    try:
        response = requests.post(url, auth=auth, data=payload)
        response.raise_for_status()
        print("SMS sent successfully:", response.json())
        return True
    except Exception as e:
        print("Exotel error:", e)
        if hasattr(e, 'response') and e.response:
            print("Response content:", e.response.text)
        return False
