import sys
import chilkat

# This example requires the Chilkat API to have been previously unlocked.
# See Global Unlock Sample for sample code.
glob = chilkat.CkGlobal()
success = glob.UnlockBundle("DFRGTN.CBe0599_TKvwSibG5UPl")
if (success != True):
    print(glob.lastErrorText())
    sys.exit()

status = glob.get_UnlockStatus()
if (status == 2):
    # print("Unlocked using purchased unlock code.")
    # tutto qua dentro -----------------------------------------------------------------------------------------------

    oauth2 = chilkat.CkOAuth2()

    # For Google OAuth2, set the listen port equal to the port used
    # in the Authorized Redirect URL for the Client ID.
    # For example, in this case the Authorized Redirect URL would be http://localhost:55568/
    # Your app should choose a port not likely not used by any other application.
    oauth2.put_ListenPort(55568)

    oauth2.put_AuthorizationEndpoint("https://accounts.google.com/o/oauth2/v2/auth")
    oauth2.put_TokenEndpoint("https://www.googleapis.com/oauth2/v4/token")

    # Replace these with actual values.
    oauth2.put_ClientId("435491809515-ii8m7ehe3ou6s4nl576o9gklge9cjlgn.apps.googleusercontent.com")
    oauth2.put_ClientSecret("7-MLJxw6-8X2Np1xjXa58nJS")

    oauth2.put_CodeChallenge(True)
    oauth2.put_CodeChallengeMethod("S256")

    # See more scopes at https://developers.google.com/identity/protocols/googlescopes
    oauth2.put_Scope("https://www.googleapis.com/auth/drive")

    # Begin the OAuth2 three-legged flow.  This returns a URL that should be loaded in a browser.
    url = oauth2.startAuth()
    if (oauth2.get_LastMethodSuccess() != True):
        print(oauth2.lastErrorText())
        sys.exit()

    # At this point, your application should load the URL in a browser.
    # For example,
    # in C#: System.Diagnostics.Process.Start(url);
    # in Java: Desktop.getDesktop().browse(new URI(url));
    # in VBScript: Set wsh=WScript.CreateObject("WScript.Shell")
    #              wsh.Run url
    # in Xojo: ShowURL(url)  (see http://docs.xojo.com/index.php/ShowURL)
    # in Dataflex: Runprogram Background "c:\Program Files\Internet Explorer\iexplore.exe" sUrl
    # The QuickBooks account owner would interactively accept or deny the authorization request.

    # Add the code to load the url in a web browser here...
    # Add the code to load the url in a web browser here...
    # Add the code to load the url in a web browser here...

    # Now wait for the authorization.
    # We'll wait for a max of 30 seconds.
    numMsWaited = 0
    while (numMsWaited < 30000) and (oauth2.get_AuthFlowState() < 3) :
        oauth2.SleepMs(100)
        numMsWaited = numMsWaited + 100

    # If there was no response from the browser within 30 seconds, then
    # the AuthFlowState will be equal to 1 or 2.
    # 1: Waiting for Redirect. The OAuth2 background thread is waiting to receive the redirect HTTP request from the browser.
    # 2: Waiting for Final Response. The OAuth2 background thread is waiting for the final access token response.
    # In that case, cancel the background task started in the call to StartAuth.
    if (oauth2.get_AuthFlowState() < 3):
        oauth2.Cancel()
        print("No response from the browser!")
        sys.exit()

    # Check the AuthFlowState to see if authorization was granted, denied, or if some error occurred
    # The possible AuthFlowState values are:
    # 3: Completed with Success. The OAuth2 flow has completed, the background thread exited, and the successful JSON response is available in AccessTokenResponse property.
    # 4: Completed with Access Denied. The OAuth2 flow has completed, the background thread exited, and the error JSON is available in AccessTokenResponse property.
    # 5: Failed Prior to Completion. The OAuth2 flow failed to complete, the background thread exited, and the error information is available in the FailureInfo property.
    if (oauth2.get_AuthFlowState() == 5):
        print("OAuth2 failed to complete.")
        print(oauth2.failureInfo())
        sys.exit()

    if (oauth2.get_AuthFlowState() == 4):
        print("OAuth2 authorization was denied.")
        print(oauth2.accessTokenResponse())
        sys.exit()

    if (oauth2.get_AuthFlowState() != 3):
        print("Unexpected AuthFlowState:" + str(oauth2.get_AuthFlowState()))
        sys.exit()

    # Save the full JSON access token response to a file.
    sbJson = chilkat.CkStringBuilder()
    sbJson.Append(oauth2.accessTokenResponse())
    sbJson.WriteFile("qa_data/tokens/googleDrive.json","utf-8",False)

    # The saved JSON response looks like this:

    # 	{
    # 	 "access_token": "ya39.Ci-XA_C5bGgRDC3UaD-h0_NeL-DVIQnI2gHtBBBHkZzrwlARkwX6R3O0PCDEzRlfaQ",
    # 	 "token_type": "Bearer",
    # 	 "expires_in": 3600,
    # 	 "refresh_token": "1/r_2c_7jddspcdfesrrfKqfXtqo08D6Q-gUU0DsdfVMsx0c"
    # 	}
    #
    print("OAuth2 authorization granted!")
    print("Access Token = " + oauth2.accessToken())

else:
    print("Unlocked in trial mode.")