from image_uploader.commons import constants
from image_uploader.models import DBModel


class Image(DBModel):
    @property
    def table_name(self):
        return constants.IMAGE_TABLE

    @property
    def partition_key(self):
        return "userId"

    def __init__(self, user_id, image_id=None, uploaded_by=None, uploaded_at=None, size=None, tags=None, file_path=None,
                 file_name=None, likes=None, comments=None):
        self.userId = user_id
        self.imageId = image_id
        self.uploadedBy = uploaded_by
        self.uploadedAt = uploaded_at
        self.size = size
        self.tags = tags
        self.filePath = file_path
        self.fileName = file_name
        self.likes = likes
        self.comments = comments

    def __str__(self):
        return f'''userId: {self.userId}, 
         imageId: {self.imageId},
         uploadedBy: {self.uploadedBy},
         uploadedAt: {self.uploadedAt},
         size: {self.size},
         tags: {self.tags},
         filePath: {self.filePath},
         likes: {self.likes},
         comments: {self.comments}
         '''
