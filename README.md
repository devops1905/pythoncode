> Environment Variables will be setted in our pipeline
> 

PROJECT_ID: Project ID where image repositories will be scanned
TOKEN: Personal access token generated within Gitlab with permission to delete images
RETENTION_PERIOD_DAYS: If the tag is older than this number, it will be deleted
PATTERN: Regex pattern of image tags to ignore (i.e.: r"release|latest|r\d\.\d\.\d*|")
Pipeline schedule can be configured in CICD > Schedules
