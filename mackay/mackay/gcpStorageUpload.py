from storages.backends.gcloud import GoogleCloudStorage
storage = GoogleCloudStorage()

def gcp_upload_image(file, filePath):
    try:
        storage.save(filePath, file)
        return filePath
    except Exception as e:
        # print("Failed to upload!")