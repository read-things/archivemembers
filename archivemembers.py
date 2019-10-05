from __future__ import print_function
import sys
import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Hey dicks. Don't modify my code. Or at least let me know if you do.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.group',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/spreadsheets']

def main():

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    directoryService = build('admin', 'directory_v1', credentials=creds)

    # add a user to the group "users" with the -a or add arguments.
    if sys.argv[1] == 'add' or sys.argv[1] == '-a':
        print('Adding user to the domain')
        groupinfo = {'email': sys.argv[2]}
        results = directoryService.members().insert(groupKey='users@coughlandavismaine.com', body=groupinfo).execute()
        groupmembers = results

        if not groupmembers:
            print('No response from server. Probably you did something wrong.')
        else:
            print('User added:')
            print(groupmembers)
        
    # List the members of the group "users" with the -l or list arguments.
    if sys.argv[1] == 'list' or sys.argv[1] == '-l':
        print('Listing users in the domain... \n')
        results = directoryService.members().list(groupKey='users@coughlandavismaine.com').execute()
        groupmembers = results

        if not groupmembers:
            print('No response from server. Probably you did something wrong.')
        else:
            emails = [member['email'] for member in groupmembers['members']]
            print(*emails, sep = "\n")
            print("\n",len(emails), "total users")

    # Remove a user from the group "users" with the -R or remove arguments.
    if sys.argv[1] == 'remove' or sys.argv[1] == '-R':
        print('removing user from the domain')
        deadmofo = sys.argv[2]
        results = directoryService.members().delete(groupKey='users@coughlandavismaine.com', memberKey=deadmofo).execute()
        groupmembers = results

        if not groupmembers:
            print('No response from server. This is probably fine.')
            print('Verifying the user has been removed...')
            verifyRemoved = directoryService.members().list(groupKey='users@coughlandavismaine.com').execute()
            emails = [member['email'] for member in verifyRemoved['members']]
            if deadmofo in emails:
                print('ERROR', deadmofo, 'still exists in user list')
            else:
                print('Got em.')
        else:
            print('Probably some error text:')
            print(groupmembers)

if __name__ == '__main__':
    main()
