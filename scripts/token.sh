#!/bin/bash

curl --location --request POST 'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid' --header 'Content-Type: application/x-www-form-urlencoded' --header 'Authorization: Basic al9tR25keEsyV0xLRVVLYkdya1g3bjF1eEFFYTpCcnN6SDhvRjlRc0hSamlPQUMxRDlaZTBJbG9h'