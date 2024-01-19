#!/usr/bin/env python3

from requests import request

CLIENT_ID = "663879890665-n3qt04m3q2tppesb1ufdee9rpkqq9m4a.apps.googleusercontent.com"
CLIENT_SECRET = "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"

# step 2: get a temporary access code manually
# https://accounts.google.com/o/oauth2/auth?access_type=offline&approval_prompt=auto&client_id=663879890665-n3qt04m3q2tppesb1ufdee9rpkqq9m4a.apps.googleusercontent.com&response_type=code&scope=https://www.googleapis.com/auth/spreadsheets&redirect_uri=http://localhost

ACCESS_CODE = "4/0AfJohXm6ZIumRQPhcm86n4Jcmh1jTPAlnPHG2yB2LrRDsEJdVURVeZyiS862YBKY7KolIw"

def main():
    url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "grant_type": "authorization_code",
        "code": ACCESS_CODE,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "https://www.googleapis.com/auth/spreadsheets",
        "redirect_uri": "http://localhost"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }

    r = request("POST", url, data=data, headers=headers)
    print(r.text)

if __name__ == "__main__":
    main()
