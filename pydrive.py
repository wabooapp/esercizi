
from pydrive import GoogleAuth
from pydrive import GoogleDrive

gauth = GoogleAuth()

gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
