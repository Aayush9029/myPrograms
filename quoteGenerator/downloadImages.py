from unsplash.auth import Auth
from unsplash.api import Api
import urllib.request

client_id = "xxxxxxxxxxxxxxx" #add your client key (unsplash)
client_secret = "xxxxxxxxxxxxxx" #add unsplash secret key
redirect_uri = ""
code = ""

auth = Auth(client_id, client_secret, redirect_uri, code=code)
api = Api(auth)

photoId = str(api.search.photos("stars"))
pid = (photoId.split("id"))
imageIds = []

for p in pid:
    imageIds.append(str(p.split('\'')[1]))

count = 1
url = ""
a = ""
limit = 5

for images in imageIds:
    try:
        name = str(count)
        image = api.photo.download(images)
        url = (image['url'])
        a = urllib.request.urlretrieve(url, "images/{}.png".format(name))
        count += 1
        print(f"downloaded {image}")
        if(count > limit):
            print("done.. bye")
            break
    except:
        pass
