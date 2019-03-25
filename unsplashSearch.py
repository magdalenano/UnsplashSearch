#! python3
# unsplashSearch.py - Opens  first images for searching word and saves them

import sys,webbrowser,requests,os,ctypes,random,json,math,threading
fileNames=[]

os.makedirs('wallpapers', exist_ok=True)
query=input("What kind of images would you like?")
request_url="https://unsplash.com/napi/search/photos"
params={
    'query':query,
    'xp':'',
    'per_page':20,
    'page':1
}
jsonObj=requests.get(request_url,params=params).json()
max=50
print("There are %s '%s' images."%(jsonObj['total'],query))
while True:
    numb = int(input("How many do you want to save?"))
    if numb>max:
        print("You can save up to 50 images")
    else:
        break
pages=list(range(1,math.ceil(numb/20)+1))


count = 1
for page in pages:
            params={'query':query,
            'xp':'',
            'per_page':20,
            'page':page}
            jsonObj=requests.get(request_url,params=params).json()
            for result in jsonObj['results']:
                img_url=result['urls']['raw']
                webbrowser.open(img_url)

                valid_ans=False
                while valid_ans ==False:
                    ans=input( "Do you want to save it? (y/n)")
                    if ans.lower()=="y":
                        name=input("How to name it?")
                        fileName=name+".jpg"
                        fileNames.append(fileName)
                        print ("Saving " + fileName + " to the hard drive")
                        with open(os.path.join("wallpapers",fileName),"wb") as f:
                            response=requests.get(img_url,stream=True)
                            if not response.ok:
                                print(response)
                            for chunk in response.iter_content(100000):
                                f.write(chunk)
                        valid_ans=True
                        count+=1
                    elif ans.lower()=="n":
                        valid_ans=True
                        pass
                    else:
                        print("Invalid response")
                if count>numb:
                    print("Reached a desired number of images.")
                    break
print("Changing your desktop wallpaper..")
wall=random.choice(fileNames)
pathToWall=os.path.join(r"C:\Users\User\PycharmProjects\untitled\wallpapers",wall)
SPI_SETDESKWALLPAPER=20
ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER,0,pathToWall,0)
