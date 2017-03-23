#这里为后台批量命令 专门 做了一个 pakages
#这里要有用，必须加入Django的环境变量

#先知道自己的脚本在哪里？,然后找上级的上级 加入环境变量

#当前 文件所在的路径，linux应该是相对路径，
import os, sys
# print(__file__)
#绝对路径这样写
# print(os.path.dirname(os.path.abspath(__file__)))

#win下与liunx不同，win下用了\, 2B win

#这里去掉两层
# BaseDir = os.path.dirname(os.path.abspath(__file__)).split("\\")[:-2]
# BaseDir = "\\".join(BaseDir)

BaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# #这里要有用，必须加入Django的环境变量
sys.path.append(BaseDir)

print(BaseDir)
# #设置了系统级的环境变量

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graduation_project.settings")
os.environ['DJANGO_SETTINGS_MODULE'] = 'graduation_project.settings'
import django
django.setup()  #允许外部的脚本调用 Django db models

from hosts.models import TaskLog
from django.core.exceptions import ObjectDoesNotExist
import multiprocessing
from hosts.backend import paramiko_handle

#导入模块，这以后setting中设置 也要进行设置



def by_paramiko(task_id):
    print("后面的脚本 paramiko 开始了")
    print(type(task_id))
    try:
        #这里只能抓到前一个task——id 不管用，不知道咋回事
        task_obj = TaskLog.objects.get(id=task_id)
        print("你大爷！", task_obj)
        print("zhelima")
        pool = multiprocessing.Pool(processes=5)

        print(task_obj.hosts.select_related())
        for h in task_obj.hosts.select_related():
            p = pool.apply_async(paramiko_handle.paramiko_ssh, args=(task_id, h, task_obj.cmd))
        pool.close()
        pool.join()


    except ObjectDoesNotExist as e:
        print("唉！！！！！！！！！")
        sys.exit(e)



def by_ansible(task_id):
    pass

def by_saltstack(task_id):
    pass





if __name__ == '__main__':
    required_args = ['-task_id', '-run_type']

    for arg in required_args:
        if not arg in sys.argv:
            sys.exit("arg [%s] is required!" % (arg))

    if len(sys.argv) < 5:
        sys.exit("5 arguments expected but %s given" % (len(sys.argv)))

    task_id = sys.argv[sys.argv.index("-task_id") + 1]
    run_type = sys.argv[sys.argv.index("-run_type") + 1]


    #先判断有没有这个方法
    #类中这么来
    # if hasattr(self, '字符串')

    # 这里在一个函数里，这样弄,针对与模块的
    if hasattr(__import__(__name__), run_type):
        func = getattr(__import__(__name__), run_type)
        func(task_id)
    else:
        sys.exit("Invalid run_type, only support [by paramiko, by_ansible, by_saltstack]")