from Naked.toolshed.shell import muterun

def download_Tiktok_signature():
    try:
        muterun("npm i tiktok-signature")       # install tiktok-signature
        rewrite_browserJS()
    except():
        print("Could not install tiktok-signature")

def rewrite_browserJS():
    try:
        # rewrite browser.js -- adding correct User agent
        with open("node_modules\\tiktok-signature\\browser.js", "r+") as file:
            content = file.readlines()
            content[6] = '        const signer = new Signer("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36")\n'
            file.seek(0)
            file.truncate()
            file.writelines(content)
        print("Crawler is ready to use!")
    except():
        print("Could not rewrite browser.js")

download_Tiktok_signature()