import http.client as httplib
import httplib2
import os
import random
import sys
import time
import argparse

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

httplib2.RETRIES = 1

MAX_RETRIES = 10

RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
                        httplib.IncompleteRead, httplib.ImproperConnectionState,
                        httplib.CannotSendRequest, httplib.CannotSendHeader,
                        httplib.ResponseNotReady, httplib.BadStatusLine)

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

CLIENT_SECRETS_FILE = "client_secret_813278049069-ct94j40333ch9h687c12bhk312javef3.apps.googleusercontent.com.json"

YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

def get_authenticated_service(args):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                   scope=YOUTUBE_UPLOAD_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                 http=credentials.authorize(httplib2.Http()))

def initialize_upload(youtube, options):
    tags = None
    if options.keywords:
        tags = options.keywords.split(",")

    body = dict(
        snippet=dict(
            title=options.title,
            description=options.description,
            tags=tags,
            categoryId=options.category
        ),
        status=dict(
            privacyStatus=options.privacyStatus
        )
    )

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
    )

    return resumable_upload(insert_request)

def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            # print("Uploading file...")
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    # print("Video id '%s' was successfully uploaded." % response['id'])
                    url = 'https://www.youtube.com/watch?v=' + response['id']
                    return url
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
        except  HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                     e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = "A retriable error occurred: %s" % e

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print("Sleeping %f seconds and then retrying..." % sleep_seconds)
            time.sleep(sleep_seconds)

def start_upload(file,title): #檔名 標題 回傳yt url
    parser = argparse.ArgumentParser()
    parser.add_argument('--file')
    parser.add_argument('--title')
    parser.add_argument('--keywords')
    parser.add_argument('--description')
    parser.add_argument('--category')
    parser.add_argument('--privacyStatus')
    args = parser.parse_args(args=['--file', file, '--title', title, '--keywords', '', '--description', 'Test', '--category', '22', "--privacyStatus",VALID_PRIVACY_STATUSES[0]])
    youtube = get_authenticated_service(args)
    try:
        youtube_url = initialize_upload(youtube, args)
        return youtube_url
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
    # arg = Namespace(auth_host_name='localhost', auth_host_port=[8080, 8090], category='22', description='Test Description', file='598408072_1.mp4', keywords='', logging_level='ERROR', noauth_local_webserver=False, privacyStatus='public', title='598408072_2')

# url = start_upload('598408072_1.mp4','598408072_3')
# print(url)