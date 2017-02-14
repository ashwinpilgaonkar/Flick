__author__ = 'priyanshubhatnagar'

import speech_recognition as sr

def Googlelisten():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{"type": "service_account",
          "project_id": "iris-virtual-assistant-158706",
          "private_key_id": "311dd1d628459aac5e2c7bc0357371daa6ea1f0f",
          "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQClJPbA04XGCbbM\nTGWfAw7iE9A5r8+g81//6cngDppA+VTEaHwkQ7NhiBeci72r5ETelLDdYFusPnA6\nV8vk2yGEONlBoC0jzPWIwR+/iwfIV1IK7nDsM2RW3B19Ox0uw6zvBB/n6moag/7T\n2y2ySQjGCJ7IwMjU+Kmgu3TRqOtRFciHHB0ivnfyTwDDLO9oTUWH1FOtNS9T2gi6\nT0tnh8hGnnYGpw+H0OPL6Yt9gwqlPn0giWo4VdqxTbeeYLLI0laJA7GO5V+g5G1h\n82vQ9kb8ymyHhbiBAyZuUiMJze0ChU+vYH4KyJw+ZZ4hLoVngET3E9JMpaWgfIMb\nUJxMjgqHAgMBAAECggEBAJ0fqC4akoKzp1qFrYI3FKgBFfJs1e1a4ZHJTCuDeTws\nfXxJtSODzl4Tb/Of+RxcmTH04rod/drJpVm9Qt9Bpof41qxby9buIQa2SJCjpQn2\nGrcP2hzBYMxLrTsDTWa7AgR/NiQfokgMIh5LwRSJ7HEOrpRu6CXJWQr2j9UTFKEV\nw15/QfmruIzhyXY9LQU16G+IYVNE2l6IPRgNh8z/rIpaKeAvmDv0hNn/CZ9zJ4+6\n4m0sHIE1ESs9iCAkdNFk/b977W47KFXTCoPlYHCpSdfQyp/rErNIAIoaOhEO6542\n/cRmK6rDzcb58zYyoV1VAzfDd/lw3XmPBB3G/QWb+nECgYEA0Qez2U+6TiswVwCf\nDpd0kyUNF/WlnPbPUf7/a+fQSQcr6bcSa95nqyG5K46CqRR0kYe1P76avGznYWhQ\nFSkgAZQVMMcqYCRccqhztEQXXsX+9Gi2FmUPPdUDQbzhRO5SP8r+QCtIDSFRxDej\nzpFtAUXvKxt4nae3OompFbkDP3MCgYEAykDFEvB2enVZ+JhtoLFvVRe7oJneU5/U\nQCUFKxa/SHzEAqHux6lTaL05EmsFHWSJb++1hesDnxU7WpS0YCW2Sw1YRpY/WgkL\nIII0itDLc+Xrlu0A1x5+z0ZwD46X6hV8cgr6AB8Cd0X4aJ87NyC86+17/QDf0VD/\nbZ1Tf1TlG50CgYA4wdGoyQg6X2nBxe5qZN+HcMEMZ2vvoeiLSCUMpKYeni7jSA1d\ncsdNZVvFIu4BgQdh2KpzQ4r6bMuq3EsaY89H/nB+jSXJczYTAABiyzZZSoO+04vV\nqt0nmeZHfETilZ+JqNG+lMH8prZwA/ebiEtD1DxrxQrMLBUJdQWPW2wxVwKBgQC+\nN55hyqBTWe1NXea1HEvOJu0DBdPQqGBSF789oD406Yrbwvq0866LsnNrvBVqaHTO\nPw9lLPwR8UEKVxMx3iYNfjaI5KQehKTfZTYPXIIMtbAWGT8SEw9G2ENqjjyYHq8U\n/vfTh1alYLxZgXCKz5J+/bL/54OY9GnW6QFvnyN/DQKBgHDAKF26t9C8KjoTSPHq\naVZb2KOtieyb2f2CPz5TKSiEhOHaQR7LzmnnISMH5RMrVh+Ah9IqB+WESy+Ik4fg\nls6jToGuOYQEcAcrxs0rRde5AIh/dDHOD5vtM+ZmSD9uDAdzb4MQGAEApb0LTdV0\nx022M2yrRdjy5ONpQ/DjanZT\n-----END PRIVATE KEY-----\n",
          "client_email": "755183626981-compute@developer.gserviceaccount.com",
          "client_id": "108269919291065152528",
          "auth_uri": "https://accounts.google.com/o/oauth2/auth",
          "token_uri": "https://accounts.google.com/o/oauth2/token",
          "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
          "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/755183626981-compute%40developer.gserviceaccount.com"
        }
        """
    try:
        text  = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        print("Google Cloud Speech thinks you said " + text)
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))

    return text