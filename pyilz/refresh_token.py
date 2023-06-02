import requests
import os


def refresh_token(ref_token=None):
    REFRESH_TOKEN = os.getenv(
        'REFRESH_TOKEN') if ref_token is None else ref_token
    if REFRESH_TOKEN is None:
        raise Exception(
            'No refresh token found. Please provide a refresh token.')

    response = requests.post('https://cognito-idp.us-east-1.amazonaws.com/', headers={
        'authority': 'cognito-idp.us-east-1.amazonaws.com',
        'content-type': 'application/x-amz-json-1.1',
        'x-amz-target': 'AWSCognitoIdentityProviderService.InitiateAuth'
    },
        json={
        'ClientId': 'kutk35sfb1haiut4s7vmda4e8',
        'AuthFlow': 'REFRESH_TOKEN_AUTH',
        'AuthParameters': {
            'REFRESH_TOKEN': REFRESH_TOKEN,
        }
    }, timeout=5)

    if response.status_code != 200:
        raise Exception(
            f'Failed to refresh token. {response.status_code} {response.text}')

    authentication_result = response.json()['AuthenticationResult']
    #access_token = authentication_result['AccessToken']
    #expires_in = authentication_result['ExpiresIn']
    id_token = authentication_result['IdToken']
    #token_type = authentication_result['TokenType']

    return id_token
