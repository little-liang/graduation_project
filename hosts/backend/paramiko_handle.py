import time
import paramiko
from hosts import models
from django.utils import timezone
def paramiko_ssh(task_id, host_obj, task_content):
    bind_host = host_obj

    task_content = task_content[2:-2]

    # print(host_obj.host.ip_addr, task_content)
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

        stdin, stdout, stderr = s.exec_command(task_content)


        #这里要求返回值只有一个，返回数据库里只能有一个
        result = stdout.read(), stderr.read()

        #一会看看



        # cmd_result = result[0] if result[0] else result[1]

        if result[0]:
            cmd_result = result[0]
        elif result[1]:
            cmd_result = result[1]


        result = 'success'
        print("运行结果：", bind_host.host.ip_addr, cmd_result)
    except Exception as e:
        print(e)
        cmd_result = e
        result = 'failed'

    # 运行结果写入DB
    # 找到最初的运行结果N/A，并修改它

    log_obj = models.TaskLogDetail.objects.get(child_of_task_id=task_id, bind_host_id=bind_host.id)
    log_obj.event_log = cmd_result
    log_obj.date = timezone.now()
    log_obj.result = result
    log_obj.save()