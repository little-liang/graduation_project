import time
import paramiko
from hosts import models
from django.utils import timezone
def paramiko_ssh(task_id, host_obj, task_content):
    print("will run the", task_id, host_obj, task_content)
    bind_host = host_obj

    print(bind_host.host.ip_addr)
    print(bind_host.host.port)
    print(bind_host.host_user.username)
    print(bind_host.host_user.password)


    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if bind_host.host_user.auth_type == 'ssh_password':
            s.connect(bind_host.host.ip_addr,
                      int(bind_host.host.port),
                      bind_host.host_user.username,
                      bind_host.host_user.password,
                      timeout=5)
        else:  # rsa_key
            pass
            '''
            key = paramiko.RSAKey.from_private_key_file(settings.RSA_PRIVATE_KEY_FILE)
            s.connect(bind_host.host.ip_addr,
                      int(bind_host.host.port),
                      bind_host.host_user.username,
                      pkey=key,
                      timeout=5)
            '''

        stdin, stdout, stderr = s.exec_command("df")


        #这里要求返回值只有一个，返回数据库里只能有一个
        result = stdout.read(), stderr.read()
        print("hhahahh", result)
        #一会看看
        cmd_result = result
        result = 'success'
    except Exception as e:
        print(e)
        cmd_result = e
        result = 'failed'

    #运行结果写入DB
    log_obj = models.TaskLogDetail(
        child_of_task_id=task_id,
        bind_host_id=bind_host.id,
        date=timezone.now(),  ##这里保证存的是本地的时区
        event_log=cmd_result,
        result=result
    )
    log_obj.save()