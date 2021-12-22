class Post(object):
    def __init__(self, postID, dateTime, mediaURL="", mediaType=""):
        self.postID = postID
        self.mediaURL = mediaURL
        self.mediaType = mediaType
        self.dateTime = dateTime
        

    def to_dict(self):
        data = {
            u'postID': self.postID,
            u'mediaURL': self.mediaURL,
            u'mediaType': self.mediaType,
            u'dateTime': self.dateTime
        }
        return data