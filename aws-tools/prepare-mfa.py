import boto3
import configparser
import sys

prm_profile = 'tef' # profile with your user credentials (they are used to retrieve temp creds)
prm_tempprofile = 'temp' # profile where to record temp credentials to
prm_credfile = 'C:/users/masslove/.aws/credentials' # filename where profile creds are stored
prm_user_arn = 'arn:aws:iam::811293737904:mfa/anatolii.maslov.external' # your user arn
prm_token_code = sys.argv[1] # token_code from your MFA device

# uses credentials to get temporary token info
def get_token(profile_name:str, user_arn:str, token_code:str):
    try:
        session = boto3.session.Session(profile_name=profile_name)
        client = session.client('sts')
        response = client.get_session_token(SerialNumber=user_arn,TokenCode=token_code)

        outp = response['Credentials'] # (AccessKeyId, SecretAccessKey, SessionToken)

        return outp
    except Exception as e:
        print('Error caught')
        print(str(e))

def write_temp_credentials(cred_filename:str, tempprofile_name:str,
                           aws_access_key_id:str, aws_secret_access_key:str, aws_session_token:str):
    config = configparser.ConfigParser()
    config.read(cred_filename)

    if not(tempprofile_name in config.sections()):
        config.add_section(tempprofile_name)

    config[tempprofile_name]['aws_access_key_id'] = aws_access_key_id
    config[tempprofile_name]['aws_secret_access_key'] = aws_secret_access_key
    config[tempprofile_name]['aws_session_token'] = aws_session_token

    with open(cred_filename,'w') as cred_file:
        config.write(cred_file)

def test_credentials(tempprofile_name:str):
    session = boto3.session.Session(profile_name='tef')
    client = session.client('sts')
    response = client.get_caller_identity()
    return response

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please, provide mfa token code as a first argument")
        exit(0)

    creds = get_token(prm_profile, prm_user_arn, prm_token_code)
    write_temp_credentials(prm_credfile,prm_tempprofile
                          ,creds['AccessKeyId'], creds['SecretAccessKey'], creds['SessionToken'])
    print(f"Credentials written successfully into '{prm_tempprofile}' profile.\nTesting..")
    print(test_credentials(prm_tempprofile))
