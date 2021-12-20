from uuid import uuid4
from initGCP import InitGCP
from Post import Post
from datetime import datetime
import pytz
import operator



# Initialize to GCP
GCP_FIRESTORE = InitGCP.initFirestore()
GCP_STORAGE = InitGCP.initStorage()

POSTS_TABLE_NAME = "<YOUR_DATABASE_TABLE_NAME>" # Your GCP Firestore database table name
BUCKET_NAME = "<YOUR_BUCKET_NAME>" # your GCP Storage bucket name


SG_TIME_ZONE = pytz.timezone("Asia/Singapore")

class Backend:
     # upload media and returns the URL of the media stored in GCP Storage
     def uploadFile(file, contentType):
          fileType = contentType.split("/")[1]

          uuid = uuid4()
          destFileName = "{0}.{1}".format(uuid, fileType) 

          bucket = GCP_STORAGE.bucket(BUCKET_NAME)
          blob = bucket.blob(destFileName)
          
          blob.upload_from_filename(file, content_type=contentType) 

          mediaURL = "https://storage.cloud.google.com/{0}/{1}.{2}?authuser=0".format(BUCKET_NAME, uuid, fileType) 

          return mediaURL

     # download the media from GCP Storage
     def downloadMedia(filePrefix, mediaURL):
          bucket = GCP_STORAGE.bucket(BUCKET_NAME)
          front = "https://storage.cloud.google.com/"
          back = "?authuser=0"

          sourceFileName = mediaURL.replace(front,"").replace(back,"").split("/")[1]
          blob = bucket.blob(sourceFileName)
          destFileName = filePrefix + sourceFileName.split(".")[-1]

          blob.download_to_filename(destFileName)


          return destFileName


     # create post and save it to Firestore database
     def createPost(file, fileType):
          postID = str(uuid4())
          now = datetime.now(SG_TIME_ZONE).strftime("%d/%m/%Y %H:%M:%S")

          mediaURL = Backend.uploadFile(file, fileType)
          newPost = Post(postID=postID, dateTime=now, mediaType= fileType, mediaURL= mediaURL)

          GCP_FIRESTORE.collection(POSTS_TABLE_NAME).document(newPost.postID).set(newPost.to_dict())

      

     # get new posts that is later than given dateTime
     def getNewPosts(dateTime):
          posts = []
          posts_ref = GCP_FIRESTORE.collection(POSTS_TABLE_NAME).where(u'dateTime', u'>', dateTime).get()

          for doc in posts_ref:
               docDict = doc.to_dict()
               post = Post(docDict['postID'], docDict['dateTime'], docDict['mediaURL'], docDict['mediaType'])
               posts.append(post)

          sortedPosts = sorted(posts, key=operator.attrgetter("dateTime"))
          
          return sortedPosts



     

    