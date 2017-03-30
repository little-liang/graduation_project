import os, random
from graduation_project import settings
def json_date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.strftime("%Y-%m-%d %T")



def handle_upload_file(request, file_obj):
    random_dir = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba1234567890', 10))
    upload_dir = '%s/%s' % (settings.FileUploadDir, request.user.id)

    upload_dir2 = '%s/%s' % (upload_dir, random_dir)

    #这里的目录必须依次创建1
    if not os.path.isdir(upload_dir):
        os.mkdir(upload_dir)
    # 这里的目录必须依次创建2
    if not os.path.isdir(upload_dir2):
        os.mkdir(upload_dir2)

    #这里没有把同一次上传的文件放到一个目录下，所以前台放了一下upload_files= [];

    with open('%s/%s' % (upload_dir2, file_obj.name), 'wb') as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)

    return "%s/%s" % (random_dir, file_obj.name)