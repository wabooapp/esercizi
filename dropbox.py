




import sys
import chilkat

#  This example requires the Chilkat API to have been previously unlocked.
#  See Global Unlock Sample for sample code.
import sys
import chilkat

success = True

glob = chilkat.CkGlobal()
success = glob.UnlockBundle("DFRGTN.CBe0599_TKvwSibG5UPl")

ACCESS_TOKEN = "f1X7SSCjr2AAAAAAAAABAgJAj5mnr62y5enONdcgwOCeIqoCr5BjRZidSyKdyXNg"

if (success != True):
    print(glob.lastErrorText())
    sys.exit()

status = glob.get_UnlockStatus()
if (status == 2):
    # print("Unlocked using purchased unlock code.")
    # tutto qua dentro -----------------------------------------------------------------------------------------------

    rest = chilkat.CkRest()

    #  Connect to the www.dropbox.com endpoint.
    bTls = True
    port = 443
    bAutoReconnect = True
    success = rest.Connect("api.dropboxapi.com",port,bTls,bAutoReconnect)
    if (success != True):
        print(rest.lastErrorText())
        sys.exit()

    rest.AddHeader("Content-Type","application/json")
    rest.AddHeader("Authorization","Bearer f1X7SSCjr2AAAAAAAAABAgJAj5mnr62y5enONdcgwOCeIqoCr5BjRZidSyKdyXNg")

    json = chilkat.CkJsonObject()
    #  The root folder should be an empty string, not "/"
    json.AppendString("path","")
    json.AppendBool("recursive",False)
    json.AppendBool("include_media_info",False)
    json.AppendBool("include_deleted",False)
    json.AppendBool("include_has_explicit_shared_members",False)

    responseStr = rest.fullRequestString("POST","/2/files/list_folder",json.emit())
    if (rest.get_LastMethodSuccess() != True):
        print(rest.lastErrorText())
        sys.exit()

    #  Success is indicated by a 200 response status code.
    if (rest.get_ResponseStatusCode() != 200):
        #  Examine the request/response to see what happened.
        print("response status code = " + str(rest.get_ResponseStatusCode()))
        print("response status text = " + rest.responseStatusText())
        print("response header: " + rest.responseHeader())
        print("response body (if any): " + responseStr)
        print("---")
        print("LastRequestStartLine: " + rest.lastRequestStartLine())
        print("LastRequestHeader: " + rest.lastRequestHeader())
        sys.exit()

    jsonResponse = chilkat.CkJsonObject()
    jsonResponse.Load(responseStr)

    jsonResponse.put_EmitCompact(False)
    print(jsonResponse.emit())

    #  A sample JSON response is shown at the end of this example.
    #  The following code iterates over the entries.
    numEntries = jsonResponse.SizeOfArray("entries")
    i = 0
    while i < numEntries :
        jsonResponse.put_I(i)
        print("----")
        print("name: " + jsonResponse.stringOf("entries[i].name"))
        print("path_lower: " + jsonResponse.stringOf("entries[i].path_lower"))
        print("path_display: " + jsonResponse.stringOf("entries[i].path_display"))
        if (jsonResponse.HasMember("entries[i].sharing_info") == True):
            print("has sharing_info...")
            print("read_only: " + jsonResponse.stringOf("entries[i].sharing_info.read_only"))
            print("shared_folder_id: " + jsonResponse.stringOf("entries[i].sharing_info.shared_folder_id"))

        if (jsonResponse.HasMember("entries[i].client_modified") == True):
            #  Demonstrate how to parse a date/time:
            ckdt = chilkat.CkDateTime()
            success = ckdt.SetFromTimestamp(jsonResponse.stringOf("entries[i].client_modified"))
            #  The date/time can now be converted to many other formats, or the individual parts
            #  can be accessed.
            bLocalDateTime = True
            # dt is a CkDtObj
            dt = ckdt.GetDtObj(bLocalDateTime)
            print(str(dt.get_Year()) + "-" + str(dt.get_Month()) + "-" + str(dt.get_Day()))

        i = i + 1

    print("Success.")

    #creiamo una cartella




else:
    print("Unlocked in trial mode.")
