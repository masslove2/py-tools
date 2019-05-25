* prepare-mfa.py
The script uses your AWS credentials to get MFA temporary creds (AccessKeyId, SecretAccessKey, Session_Token) and,
then, stores them to another profile in your credentials file

1. Setup:
- open up prepare-mfa.py
- fill in: a) profile name where your creds are, b) profile name where to put temp creds, c) your user arn, d) cred file location

2. Run:
python prepare-mfa.py <token_from_your_mfa_device>

3. Enjoy your recorded temporary creds:
aws s3 ls --profile temp (or whatever you called it)
