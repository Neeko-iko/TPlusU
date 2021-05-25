## Imports
import urllib.request
import json
import re
import os
import zipfile

## Functions

def dump(dta):
    '''dumps data into the T+U JSON file'''
    with open("./TPlusU.json", "w") as f:
            json.dump(dta, f, indent=4)
            f.close()
    
## JSON reading and other init
jsonperm = True
try:
    with open("./TPlusU.json", "r") as f:
        data = json.loads(f.read())
        f.close()  # Reading from JSON


except FileNotFoundError:
    try:
        path =input("Enter the path to your tetrio-desktop resources folder \n enter nothing for windows defualt")
        if path == "":
            path = "%localappdata%/Programs/tetrio-desktop/resources"
        data = {"path":path, "ver":0}
        dump(data)  # Create the JSON after asking TETR.IO install location.


    except PermissionError:   # Do essentially nothing, i have no idea if this works and im not gonna put in the effort to check.
        jsonperm = False
        print("JSON file unable to be created, data kept in ram, will continue to update ig i dunno i kinda added this at the end.")



url = urllib.request.Request("https://gitlab.com/UniQMG/tetrio-plus/-/releases.json")

## Version checking
ver = json.loads(urllib.request.urlopen(url).read())[0]["tag"]
try:
    # tags match
    if ver == data["ver"]:
        input("You're already on the latest version.  Press enter to exit the CMD.")
        exit()
    # tags don't match
    else:
        print("update available" if ver == 0 else "First time running, will assume TETR.IO+ is out of date and proceed with update.")
        data["ver"] = ver
        dump(data)
    # if the version tag doesn't exist, simply create it.
except KeyError:
    print("last version not found, will assume TETR.IO+ is out of date and proceed with update.")
    data["ver"] = ver
    if jsonperm:
        dump(data)
del ver


## URL parsing
url = json.loads(urllib.request.urlopen(url).read())[0]["description"]
url = re.search("\(\/(?:uploads/)(.+?)\)", url).group() # grabs the upload URL from the description, because its stored in that for some reason.
url = url[1:-1] # removes parentheticals from the upload url
filetype = url[-1:] # p = zip  # r = not compressed


## Downloads app.asar
os.chdir(os.path.expandvars(data["path"])) #changes the CWD to the tetrio resources. Can't find any other way to do this.
print("downloading latest TETR.IO+ app.asar")
urllib.request.urlretrieve("https://gitlab.com/UniQMG/tetrio-plus" + url, "app.asar" if filetype == "r" else "app.asar.zip")
print("finished...")


## Extracting app.asar from app.asar.zip (just incase)
if filetype == "p":
    print("app.asar is a zip, extracting...")
    appzip = zipfile.ZipFile("app.asar.zip", 'r')
    zipfile.ZipFile.extract(appzip, "app.asar")
    print("cleaing up....")
    appzip.close()
    os.remove("app.asar.zip")


input("you're now on the latest version, if you weren't already.\n\nPress Enter to close this CMD.")