#!/usr/bin/env python

import configparser
import sys
import json

import requests

config = configparser.ConfigParser()
config.read('config.ini')

postman_api_key = config['postman']['api_key']
base_url = config['postman']['base_url']
headers = {'Content-Type': 'application/json', 'X-Api-Key': postman_api_key}


def print_help():
    print("""usage: supman <action> <args>

    command   description                              args

    view      displays all collection names            n/a
    add       add new collection                       filename
    update    update an existing collection            filename
    delete    delete a collection                      collection name
    export    export a collection into a json file     collection name""")
    sys.exit()


def read_file(filename):
    try:
        with open(filename, 'r') as filehandle:
            return filehandle.read()
    except FileNotFoundError:
        print('File not found.')
        sys.exit()


def get_collections():
    req = requests.get(url=base_url, headers=headers)
    collections = json.loads(req.text)
    return collections


def view():
    print('Getting your collections...\n')
    collections = get_collections()
    [print(collection['name']) for collection in collections['collections']]


def add_collection(filename):
    print('Adding collection...')
    file_content = read_file(filename)
    payload = {'collection': json.loads(file_content)}
    req = requests.post(base_url, headers=headers, json=payload)
    if req.status_code == 200:
        print('success!')
    else:
        print('Something went wrong.')


def main():
    args = sys.argv[1:]
    available_commands = ['view', 'add', 'update', 'delete', 'export']
    if  len(args) == 0 or args[0] not in available_commands:
        print_help()

    elif args[0] == 'view':
        view()

    elif args[0] == 'add':
        add_collection(args[1])

    # elif args[0] == 'update':



if __name__ == '__main__':
    main()
