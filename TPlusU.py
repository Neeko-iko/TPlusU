import urllib.request
import json
import re
import os
import zipfile
## imports

try:
    with open("./updateT+.json", "r") as f:
        data = json.loads(f.read())
        f.close()  ## Read from JSON


except FileNotFoundError:
    try:
        path =input("Enter the path to your tetrio-desktop resources folder \n enter nothing for windows defualt")
        if path == "":
            path = "%localappdata%/Programs/tetrio-desktop/resources"
        data = {"path":path}
        with open("./updateT+.json", "w") as f:
            json.dump(data, f, indent=4)
            f.close()  ## Create the JSON after asking TETR.IO install location.


    except PermissionError:   ## Do essentially nothing, i have no idea if this works and im not gonna put in the effort to check.
        print("JSON file unable to be created, data kept in ram, will continue to update ig i dunno i kinda added this at the end.")



url = urllib.request.Request("https://gitlab.com/UniQMG/tetrio-plus/-/releases.json")
url = json.loads(urllib.request.urlopen(url).read())[0]["description"]
## Does some awful parsing to grab specifically the description of the first item in the gitlab for T+.


url = re.search("\(\/(?:uploads/)(.+?)\)", url).group() # grabs the upload URL from the description, because its stored in that for some reason.
url = url[1:-1] # removes parentheticals from the upload url
filetype = url[-1:] # p = zip  # r = not compressed
## URL parsing and filetyping


os.chdir(os.path.expandvars(data["path"])) #changes the CWD to the tetrio resources. Can't find any other way to do this.
print("downloading latest TETR.IO+ app.asar")
urllib.request.urlretrieve("https://gitlab.com/UniQMG/tetrio-plus" + url, "app.asar" if filetype == "r" else "app.asar.zip")
print("finished...")
## Actually downloading the app.asar


if filetype == "p":
    print("app.asar is a zip, extracting...")
    appzip = zipfile.ZipFile("app.asar.zip", 'r')
    zipfile.ZipFile.extract(appzip, "app.asar")
    print("cleaing up....")
    appzip.close()
    os.remove("app.asar.zip")
    ## extracting the app.asar incase its compressed in a .zip.


input("you're now on the latest version, if you weren't already.\n\nPress Enter to close this CMD.")
