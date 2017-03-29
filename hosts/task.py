from hosts import models
from django.db import transaction
import subprocess, time, json
from graduation_project import settings
class Task(object):
    def __init__(self, request):
        self.request = request
        self.task_type = self.request.POST.get('task_type')

    def handle(self):
        #如果返回了任务类型（批量命令之类的）
        if self.task_type:
            if hasattr(self, self.task_type):
                #这里func接收到了mutli_cmd的这个,这个mutli_cmd是前台传过来的
                func = getattr(self, self.task_type)
                # print(func)
                #这个func()调用的是mutli_cmd函数
                return func()
            else:
                raise TypeError


    #事务性操作 数据库要支持
    # @transaction.atomic()
    def mutli_cmd(self):

        # print("把 操作 写入 数据库 ！")
        # print(self.request.POST, '11111111111111')
        selected_hosts = self.request.POST.getlist("selected_hosts[]")
        cmd = self.request.POST.getlist("cmd")

        # create task info
        task_obj = models.TaskLog(
            task_type=self.task_type,
            user_id=self.request.user.id,
            # many to many 必须创建完记录再添加
            cmd=cmd,
        )
        task_obj.save()

        # selected_hosts 这个返回的是列表，所以要用 *selected_hosts
        task_obj.hosts.add(*selected_hosts) #添加 many to many 多对多关系
        # task_obj.hosts.add([1,2,3])

        #为所有主机创建相关的任务记录,这里出现了task-id 区分任务的
        for bind_host_id in selected_hosts:
            obj = models.TaskLogDetail(
                child_of_task_id=task_obj.id,
                bind_host_id=bind_host_id,
                event_log="N/A",
            )
            obj.save()

        # print("将要调用 后台脚本执行 ")
        # 调用后台的脚本,这里在setting中配置脚本路径，防止修改,win 与 linux 不同

        p = subprocess.run([
            'python',
            settings.MultiTaskScripts,
            '-task_id', str(task_obj.id),
            '-run_type', settings.MultiTaskRunType,                 ##这里可以在前端定义，用什么调用，我们这里用settings中定义
        ])

        # # print(task_obj)
        return {'task_id': task_obj.id}

    def mutli_file_transfer(self):
        print("going to upload/download")
        selected_hosts = set(self.request.POST.getlist("selected_hosts[]"))
        transfer_type = self.request.POST.get("file_transfer_type")
        remote_path = self.request.POST.get("remote_path")
        upload_files = self.request.POST.getlist("upload_files[]")

        #任务详情
        data_dic = {
            'remote_path': remote_path,
            'upload_files': upload_files,
        }

        task_obj = models.TaskLog(
            task_type=transfer_type,
            user_id=self.request.user.id,
            # many to many 必须创建完记录再添加
            cmd=json.dumps(data_dic)
        )
        task_obj.save()
        task_obj.hosts.add(*selected_hosts)

        for bind_host_id in selected_hosts:
            obj = models.TaskLogDetail(
                child_of_task_id=task_obj.id,
                bind_host_id=bind_host_id,
                event_log="N/A",
            )
            obj.save()

        p = subprocess.run([
            'python',
            settings.MultiTaskScripts,
            '-task_id', str(task_obj.id),
            '-run_type', settings.MultiTaskRunType,                 ##这里可以在前端定义，用什么调用，我们这里用settings中定义
        ])

        # # print(task_obj)
        return {'task_id': task_obj.id}

    def get_task_result(self):
        task_id = self.request.GET.get('task_id')
        if task_id:
            res_list = models.TaskLogDetail.objects.filter(child_of_task=task_id)
            return list(res_list.values('id',
                                        'bind_host__host__hostname',
                                        'bind_host__host__ip_addr',
                                        'bind_host__host_user__username',
                                        'date',
                                        'event_log',
                                        'result',
                                        ))