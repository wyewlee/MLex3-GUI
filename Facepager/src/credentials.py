#
# Facepager needs some secret keys to connect to Facebook, YouTube and Twitter
# Fill out the following values and rename this file to credentials.py
#

credentials = {}

# Create an app under https://developers.facebook.com/apps 
# to get a Facebook Client Id
#
# Settings of the Facebook App (see "Settings" and "Facebook Login"):
#
#    Native or desktop app = yes
#    app secret embedded = no
#    client oauth login = yes
#    Embedded browser OAuth Login = yes
#    App Secret Proof for Server API calls = no
#    Require 2-factor reauthorization = no
#    Valid OAuth redirect URIs = empty
#
#    The termsurl is a webppage that will open before login (show Facepager usage terms)

credentials['facebook'] = {}
credentials['facebook']['client_id'] = '708287943187981'
credentials['facebook']['termsurl'] = '' # Facepager prelogin page for preregistered apps, can be blank.

# Create an app under https://dev.twitter.com
# to get consumer_key and consumer_secret
#
#  Settings of the Twitter App:
#
#    Callback URL = arbitrary URL of a page hosted by you
#    Sign-ign with Twitter = No
#    Access level = Read-only
#    Sign in with Twitter = No
#    App-only authentication = https://api.twitter.com/oauth2/token
#    Request token URL = https://api.twitter.com/oauth/request_token
#    Authorize URL = https://api.twitter.com/oauth/authorize
#    Access token URL = https://api.twitter.com/oauth/access_token
#
#    NOTE: You must specify a callback/redirect-URL in the Twitter-App Settings,
#    otherwise Twitter assumes a Pin-based oAuth which isn't suitable for the Facepager.
#    The URL could be any URL (it will never be exposed to the end-user)
#

credentials['twitter'] = {}
credentials['twitter']['client_id'] = 'AAAAAAAAAAAAAAAAAA' #consumer_key
credentials['twitter']['client_secret'] = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' #consumer_secret
credentials['twitter']['termsurl'] = '' #Facepager prelogin page for preregistered apps, can be blank.

credentials['twitter_streaming'] = {}
credentials['twitter_streaming']['client_id'] = 'AAAAAAAAAAAAAAAAAA' #consumer_key
credentials['twitter_streaming']['client_secret'] = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' #consumer_secret
credentials['twitter_streaming']['termsurl'] = '' #Facepager prelogin page for preregistered apps, can be blank.

# Create a project under https://console.developers.google.com
# and add Youtube API to the project, then get client_id and client_secret
#
# See https://developers.google.com/youtube/v3/guides/auth/installed-apps for authorization details
#
# Settings of the Project:
#
#    Application type: other
#
# Download the json file Google provides to see the details of allowed uris and stuff

credentials['youtube'] = {}
credentials['youtube']['client_id'] = '0000000000000000000000000000000000000000000.googleusercontent.com'
credentials['youtube']['client_secret'] = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaa'
credentials['youtube']['termsurl'] = '' #Facepager prelogin page for preregistered apps, can be blank.

#
# Set proxies
#

proxies = {}


# In order to comply with the Facebook terms, Facepager needs to keep a list of users.
# Nevertheless, we try to extremely minimize the data stored and transferred. The user 
# list only contains anonymized tokens that are encrypted using strong state of the art
# methods (salted sha256). Deriving any personal information from the token in practice
# should be impossible. 

# When you log into Facebook with the Facebook module, your Facebook User ID is encrypted using a salt. 
# The resulting anonymized token is transferred to an online Facepager service.
# If not already present, expired or blacklisted, the token is added to our user list along with a timestamp.
# Finally, the user list is searched for your token and if present you get permission to use the
# Facebook module of Facepager.

# The Facepager service is hosted at Amazon Web Services (Frankfurt data center, Germany).
# Thus, when using Facepager we ask you permission to transfer the anonymized token to this service.
# For Facepager developers, steps to setup the service:

# 1. Create bucket "facepager-users" 
#   - Create at https://s3.console.aws.amazon.com/s3/home?region=eu-central-1#
#   - block public access, server encryption is useless here because metadata is not encrypted
#
# 2. Create a lambda function "facepagerAuthorize" using Node.js 12.x.
#   - https://eu-central-1.console.aws.amazon.com/lambda/home?region=eu-central-1#/
#   - see Facepager code in src/aws/authorize.js
#   - create new role "facepagerAuthorize". You will need to configure the role in the next step. 
#     For now, add S3 read access.
#
#  3. Configure role facepagerAuthorize
#     - https://console.aws.amazon.com/iam/home?#/roles/facepagerAuthorize?section=permissions
#     - Add permissions (lookout for add policy button or whatsover): AmazonS3FullAccess ( and possibly AWSLambdaFullAccess, CloudWatchFullAccess)
#
#  4. Create API "facepager"
#     - https://eu-central-1.console.aws.amazon.com/apigateway/main/apis?region=eu-central-1
#     - REST API, regional
#     - Create ressource "login" (action menu)
#     - Create method "GET", lamda function with proxy integration, type into the field and select facepagerAuthorize
#     - API bereitstellen (action menu), Stufe prod erzeugen, die Aufruf-URL notieren
#     - API drosseln (5 requests per sec, burst = 5)

#
# Facepager AWS
#

credentials['facepager'] = {}
credentials['facepager']['salt'] = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
credentials['facepager']['url'] = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
