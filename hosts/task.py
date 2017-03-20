
class Task(object):
    def __init__(self, request):
        self.request = request
        self.task_type = self.request.POST.get('task_type')

    def handle(self):
        #如果返回了任务类型（批量命令之类的）
        if self.task_type:

            #这里func接收到了mutli_cmd的这个,
            func = getattr(self, self.task_type)
            print(func)
            #这个func（） 调用的是mutli_cmd函数
            return func()

    def mutli_cmd(self):
        print("run cmd ")
