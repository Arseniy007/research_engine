import requests

ans = requests.get("https://docs.djangoproject.com/en/4.2/ref/forms/fields/#choicefield")

print(type(ans.status_code))