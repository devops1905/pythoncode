#!/usr/bin/env python
# PURPOSE: Deletes tags that match the following:
# - are older than 90 days
# - do not have the tag 'latest'
# - do not have the tag 'release'
# - do not have the tag 'r*'

import datetime
import os
import sys
import re
import requests
import json
baseurl = 'base_url_will be added later'
project_id = os.environ['PROJECT_ID']
token = os.environ['TOKEN']
retention_period_days = int(os.environ['RETENTION_PERIOD_DAYS'])
now = datetime.datetime.now()
today = datetime.date(now.year, now.month, now.day)
pattern_keep = os.environ['PATTERN_KEEP']
pattern_delete = os.environ['PATTERN_DELETE']

headers = {'PRIVATE-TOKEN': f'{token}'}
def getData(url):
    try:
        data = requests.get(url)
        data.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        sys.exit(1)
    return json.loads(data.content)
def delete(url):
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        sys.exit(1)
    return response.status_code
# Get list of repositories (i.e. all microservices)
repos = getData(f"{baseurl}/projects/{project_id}/registry/repositories?per_page=100")
# Loop through each repository in the project (i.e. algoconfig-visualization)
for repository in repos:
    # List the tags for each repository
    repo_id = repository['id']
    tags = getData(f"{baseurl}/projects/{project_id}/registry/repositories/{repo_id}/tags")
    # Loop through each of the tags to get creation date
    for tag in tags:
        # Check if the tag matches the ignore pattern
        if re.match(pattern_keep, tag['name']):
            # Respond that the tag will be ignored since it matches the pattern
            print('Not deleting ' + tag['path'] + ' because it matches the ignore pattern.')
        # If the tag doesn't match the ignore pattern, continue to delete if age is older than the retention period
        else:
            # Check if the tag matches the delete pattern
            if re.match(pattern_delete, tag['name']):
                # Collect the details of the given tag
                tag_name = tag['name']
                tag_details = getData(f"{baseurl}/projects/{project_id}/registry/repositories/{repo_id}/tags/{tag_name}")
                # Calculate age in days from today
                date_time_str = tag_details['created_at']
                date_str = date_time_str[:-19]
                date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                age_days = (today-date_obj.date()).days
                # Delete or do not delete based on age
                if age_days > retention_period_days:
                    print('Deleting ' + tag['path'] + ' for being ' + str(age_days) + ' days old.')
                    delete(f"{baseurl}/projects/{project_id}/registry/repositories/{repo_id}/tags/{tag_name}")
                else:
                    print('Not deleting ' + tag['path'] + ' because it is only ' + str(age_days) + ' day(s) old.')
            else:
                print('Not deleting ' + tag['path'] + ' because it not matches the delete pattern.')
