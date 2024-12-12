import os

def user_avatar_upload_to(instance, filename):
    username = instance.owner.username
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"{username}{file_extension}"
    paths=os.path.join(f'image/{username}/', new_filename)
    print(paths,'看看输出了什么')
    return paths