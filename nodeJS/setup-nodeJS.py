from Naked.toolshed.shell import muterun

# function for installing js library
def download_Tiktok_signature():
    try:
        e = muterun("npm i tiktok-signature")       # install tiktok-signature
        if e.exitcode == 1:
            print("Not able to install tiktok-signature. Please make sure Node.js is installed properly and restart your script running environment.")
        rewrite_browserJS()
    except():
        print("Not able to install tiktok-signature. Please make sure Node.js is installed properly and restart your script running environment.")

# function for modifying file in installed js library
def rewrite_browserJS():
    try:
        # rewrite browser.js -- adding correct User agent
        with open("node_modules\\tiktok-signature\\browser.js", "r+") as file:
            content = file.readlines()
            content[6] = '        const signer = new Signer("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")\n'
            file.seek(0)
            file.truncate()
            file.writelines(content)
        print("Crawler is ready to use!")
    except FileNotFoundError:
        print("Not able to find browser.js, is Node.js installed properly and did you restart your script running environment?")

download_Tiktok_signature()