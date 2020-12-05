
import sys
import chilkat
import re

#  This example requires the Chilkat API to have been previously unlocked.
#  See Global Unlock Sample for sample code.
import sys
import chilkat

success = True

http = chilkat.CkHttp()
glob = chilkat.CkGlobal()
success = glob.UnlockBundle("DFRGTN.CBe0599_TKvwSibG5UPl")


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

    # creo la cartella


    #print("Success.")
    nomefolder = "OPP/00001/2020" + "-" + "NANNA"
    replaced = re.sub('[/]', '', nomefolder)
    #creiamo una cartella
    #  See the Online Tool for Generating JSON Creation Code
    json = chilkat.CkJsonObject()
    #json.UpdateString("path", "/Halloween/emojis001")
    json.UpdateString("path", "/" + replaced)
    json.UpdateBool("autorename", False)

    rest.AddHeader("Authorization", "Bearer f1X7SSCjr2AAAAAAAAABAgJAj5mnr62y5enONdcgwOCeIqoCr5BjRZidSyKdyXNg")
    rest.AddHeader("Content-Type", "application/json")

    # resp is a CkHttpResponse

    sbRequestBody = chilkat.CkStringBuilder()
    json.EmitSb(sbRequestBody)
    sbResponseBody = chilkat.CkStringBuilder()
    success = rest.FullRequestSb("POST", "/2/files/create_folder_v2", sbRequestBody, sbResponseBody)
    if (success != True):
        print(rest.lastErrorText())
        sys.exit()

    respStatusCode = rest.get_ResponseStatusCode()
    if (respStatusCode >= 400):
        print("Response Status Code = " + str(respStatusCode))
        print("Response Header:")
        print(rest.responseHeader())
        print("Response Body:")
        print(sbResponseBody.getAsString())
        sys.exit()
    else:
        print("OK CREATA")

    jsonResponse = chilkat.CkJsonObject()
    jsonResponse.LoadSb(sbResponseBody)

    metadataName = jsonResponse.stringOf("metadata.name")
    metadataId = jsonResponse.stringOf("metadata.id")
    metadataPath_lower = jsonResponse.stringOf("metadata.path_lower")
    metadataPath_display = jsonResponse.stringOf("metadata.path_display")
    metadataSharing_infoRead_only = jsonResponse.BoolOf("metadata.sharing_info.read_only")
    metadataSharing_infoParent_shared_folder_id = jsonResponse.stringOf("metadata.sharing_info.parent_shared_folder_id")
    metadataSharing_infoTraverse_only = jsonResponse.BoolOf("metadata.sharing_info.traverse_only")
    metadataSharing_infoNo_access = jsonResponse.BoolOf("metadata.sharing_info.no_access")
    link = jsonResponse.stringOf("link")

    print(metadataPath_display)




else:
    print("Unlocked in trial mode.")
