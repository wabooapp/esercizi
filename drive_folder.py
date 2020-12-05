import sys
import chilkat

success = True

glob = chilkat.CkGlobal()
success = glob.UnlockBundle("DFRGTN.CBe0599_TKvwSibG5UPl")
if (success != True):
    print(glob.lastErrorText())
    sys.exit()

status = glob.get_UnlockStatus()
if (status == 2):
    # print("Unlocked using purchased unlock code.")
    # tutto qua dentro -----------------------------------------------------------------------------------------------

    # First load the JSON key into a string.
    fac = chilkat.CkFileAccess()
    jsonKey = fac.readEntireTextFile("qa_data/adelmo-465e9d93e2fa.json","utf-8")
    if (fac.get_LastMethodSuccess() != True):
        print(fac.lastErrorText())
        sys.exit()

    gAuth = chilkat.CkAuthGoogle()
    gAuth.put_JsonKey(jsonKey)

    # Choose a scope.
    gAuth.put_Scope("https://www.googleapis.com/auth/drive")

    # Request an access token that is valid for this many seconds.
    gAuth.put_ExpireNumSeconds(5000)

    # If the application is requesting delegated access:
    # The email address of the user for which the application is requesting delegated access,
    # then set the email address here. (Otherwise leave it empty.)
    gAuth.put_SubEmailAddress("")

    # Connect to www.googleapis.com using TLS (TLS 1.2 is the default.)
    # The Chilkat socket object is used so that the connection can be established
    # through proxies or an SSH tunnel if desired.
    tlsSock = chilkat.CkSocket()
    success = tlsSock.Connect("www.googleapis.com",443,True,5000)
    if (success != True):
        print(tlsSock.lastErrorText())
        sys.exit()

    # Send the request to obtain the access token.
    success = gAuth.ObtainAccessToken(tlsSock)
    if (success != True):
        print(gAuth.lastErrorText())
        sys.exit()

    # Examine the access token:
    print("Access Token: " + gAuth.accessToken())

    # accesso DRIVE
    gAuth.put_AccessToken(gAuth.accessToken())

    rest = chilkat.CkRest()

    #  Connect using TLS.
    bAutoReconnect = True
    success = rest.Connect("www.googleapis.com", 443, True, bAutoReconnect)

    #  Provide the authentication credentials (i.e. the access token)
    rest.SetAuthGoogle(gAuth)

    #  A multipart upload to Google Drive needs a multipart/related Content-Type
    rest.AddHeader("Content-Type", "multipart/related")

    #  Specify each part of the request.

    #  The 1st part is JSON with information about the folder.
    rest.put_PartSelector("1")
    rest.AddHeader("Content-Type", "application/json; charset=UTF-8")

    json = chilkat.CkJsonObject()
    json.AppendString("name", "testFolderPIPPO")
    json.AppendString("description", "A folder to contain test files.")
    json.AppendString("mimeType", "application/vnd.google-apps.folder")
    json.AppendString("type", "user")
    json.AppendString("role", "writer")
    json.AppendString("emailAddress", "api.i9056.cloud@gmail.com")
    rest.SetMultipartBodyString(json.emit())

    #  The 2nd part would be the file content.
    #  Since this is a folder, skip the 2nd part entirely and go straight to the upload..

    jsonResponse = rest.fullRequestMultipart("POST", "/upload/drive/v3/files?uploadType=multipart")
    if (rest.get_LastMethodSuccess() != True):
        print(rest.lastErrorText())
        sys.exit()

    #  A successful response will have a status code equal to 200.
    if (rest.get_ResponseStatusCode() != 200):
        print("response status code = " + str(rest.get_ResponseStatusCode()))
        print("response status text = " + rest.responseStatusText())
        print("response header: " + rest.responseHeader())
        print("response JSON: " + jsonResponse)
        sys.exit()

    #  Show the JSON response.
    json.Load(jsonResponse)

    #  Show the full JSON response.
    json.put_EmitCompact(False)
    print(json.emit())

    #  A successful response looks like this:
    #  {
    #   "kind": "drive#file",
    #    "id": "0B53Q6OSTWYolY2tPU1BnYW02T2c",
    #    "name": "testFolder",
    #    "mimeType": "application/vnd.google-apps.folder"
    #  }

    #  Get the fileId:
    print("fileId: " + json.stringOf("id"))




else:
    print("Unlocked in trial mode.")

# The LastErrorText can be examined in the success case to see if it was unlocked in
# trial more, or with a purchased unlock code.
#print(glob.lastErrorText())