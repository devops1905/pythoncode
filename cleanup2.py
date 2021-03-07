#!/usr/bin/env python
import datetime
import os
import re
import requests
import gitlab
# Configs
baseurl = 'https://gitlab. baseurl will be added here later'
group_id = os.environ['GROUP_ID']
token = os.environ['TOKEN']
pattern = os.environ['PATTERN']
retention_period_days = int(os.environ['RETENTION_PERIOD_DAYS'])
now = datetime.datetime.now()
today = datetime.date(now.year, now.month, now.day)
# Authenticate to Gitlab
gl = gitlab.Gitlab(baseurl, private_token=token)
# Get group details
group = gl.groups.get(group_id)
# Get list of projects in the group
projects = group.projects.list(all=True)
# Loop through each project in the group
for project in projects:
    # Get list of repositories in each project
    project = gl.projects.get(project.attributes['id'])
    repositories = project.repositories.list(all=True)
    # Loop through each repository in the project
    for repository in repositories:
        # List the tags for each repository
        tags = repository.tags.list(all=True)
        # Loop through each of the tags to get creation date
        for tag in tags:
            # Check if the tag matches the ignore pattern
            if re.match(pattern, tag.attributes['name']):
                # Respond that the tag will be ignored since it matches the pattern
                print('Not deleting ' + tag.attributes['path'] + ' because it matches the ignore pattern.')
            # If the tag doesn't match the ignore pattern, continue to delete if age is older than the retention period
            else:
                # Collect the details of the given tag
                tag_details = repository.tags.get(id=tag.attributes['name'])
                # Calculate age in days from today
                date_time_str = tag_details.attributes['created_at']
                date_str = date_time_str[:-19]
                date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                age_days = (today-date_obj.date()).days
                # Delete or do not delete based on age
                if age_days > retention_period_days:
                    print('Deleting ' + tag.attributes['path'] + ' for being ' + str(age_days) + ' days old.')
                    repository.tags.delete(id=tag['name'])
                else:
                    print('Not deleting ' + tag.attributes['path'] + ' because it is only ' + str(age_days) + ' days old.')
