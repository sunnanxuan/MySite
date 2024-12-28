import os

def user_avatar_upload_to(instance, filename):
    username = instance.owner.username
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"{username}{file_extension}"
    path=os.path.join(f'image/{username}/', new_filename)
    return path