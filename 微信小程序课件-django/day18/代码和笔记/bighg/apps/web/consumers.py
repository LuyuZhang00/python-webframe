import json
import traceback
import threading
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from apps.web import models
from django.db import transaction
import os
from utils.repository import GitRepository
from django.conf import settings
import shutil
import subprocess
from utils.ssh import SSHProxy


class DeployConsumer(WebsocketConsumer):

    # 自定义
    def send_message_to_user(self, code, data):
        """
        给用户端发送消息
        :param code: 类型：init / log / error
        :param data: 数据
        :return:
        """
        self.send(json.dumps({'code': code, 'data': data}))

    def send_message_to_group(self, group_id, code, data):
        async_to_sync(self.channel_layer.group_send)(group_id, {'type': 'xxx.ooo',
                                                                'message': {'code': code,
                                                                            'data': data}})

    def is_valid_type(self, message):
        deploy_type = json.loads(message['text']).get('type')
        if deploy_type in ['deploy', 'retry_deploy']:
            return True

    def is_deploy(self, message):
        deploy_type = json.loads(message['text']).get('type')
        return deploy_type == "deploy"

    def init_diagram_record(self, task_object, task_id):
        try:
            diagram_object_list = []
            with transaction.atomic():

                start_object = models.Diagram.objects.create(task=task_object, text='开始')
                diagram_object_list.append(start_object)

                if task_object.before_download_script:
                    start_object = before_download_object = models.Diagram.objects.create(task=task_object, text='下载前',
                                                                                          parent=start_object)
                    diagram_object_list.append(before_download_object)

                download_object = models.Diagram.objects.create(task=task_object, text='下载', parent=start_object)
                diagram_object_list.append(download_object)

                if task_object.after_download_script:
                    download_object = after_download_object = models.Diagram.objects.create(task=task_object,
                                                                                            text='下载后',
                                                                                            parent=download_object)
                    diagram_object_list.append(after_download_object)

                zip_object = models.Diagram.objects.create(task=task_object, text='打包', parent=download_object)
                diagram_object_list.append(zip_object)

                deploy_server_list = models.DeployServer.objects.filter(deploy=task_object)
                for row in deploy_server_list:
                    row.status = 2
                    row.save()
                    server_object = models.Diagram.objects.create(
                        task=task_object,
                        text=row.server.hostname,
                        parent=zip_object,
                        deploy_record=row
                    )
                    diagram_object_list.append(server_object)

                    if task_object.before_deploy_script:
                        server_object = before_deploy_object = models.Diagram.objects.create(
                            task=task_object,
                            text="发布前",
                            parent=server_object,
                            deploy_record=row
                        )
                        diagram_object_list.append(before_deploy_object)

                    publish_object = models.Diagram.objects.create(
                        task=task_object,
                        text="发布",
                        parent=server_object,
                        deploy_record=row
                    )
                    diagram_object_list.append(publish_object)

                    if task_object.after_deploy_script:
                        after_deploy_object = models.Diagram.objects.create(
                            task=task_object,
                            text="发布后",
                            parent=publish_object,
                            deploy_record=row
                        )
                        diagram_object_list.append(after_deploy_object)

            diagram_data_list = []
            for item in diagram_object_list:
                temp = {
                    "key": str(item.id),
                    "text": item.text,
                    "color": item.status,
                }
                if item.parent:
                    temp['parent'] = str(item.parent_id)
                diagram_data_list.append(temp)
            # 创建成功，将 任务节点 发送给所有人，以便显示节点
            self.send_message_to_group(task_id, 'init', diagram_data_list)
            self.send_message_to_group(task_id, 'log', '【初始化图表】成功')
            return True
        except Exception as e:
            msg = "【初始化图表】失败。\n具体原因：%s" % traceback.format_exc()
            # 创建错误，将 错误信息日志 发送给所有人，展示实时错误
            self.send_message_to_group(task_id, 'log', msg)

    def retry_init_diagram_record(self, task_object, task_id):
        exists = models.Diagram.objects.filter(task=task_object).exists()
        if not exists:
            return self.init_diagram_record(task_object, task_id)
        return True

    def change_status_to_fail(self, task_object):
        # 发布任务更新为失败
        models.DeployTask.objects.filter(id=task_object.id).update(status=4)
        # 关联服务器发布状态更新为失败
        models.DeployServer.objects.filter(deploy=task_object).update(status=4)

    # 步骤状态更新
    def step_success(self, diagram_object, log, task_id):
        color = "green"
        models.Diagram.objects.filter(id=diagram_object.id).update(status=color, log=log)

        self.send_message_to_group(task_id, 'update', {'key': str(diagram_object.id), 'color': color})
        self.send_message_to_group(task_id, 'log', log)

    def step_error(self, diagram_object, log, task_id):
        color = "red"
        models.Diagram.objects.filter(id=diagram_object.id).update(status=color, log=log)

        self.send_message_to_group(task_id, 'update', {'key': str(diagram_object.id), 'color': color})
        self.send_message_to_group(task_id, 'log', log)

    def step_server_error(self, diagram_object, log, task_id, deploy_server):
        color = "red"
        models.Diagram.objects.filter(id=diagram_object.id).update(status=color, log=log)
        models.DeployServer.objects.filter(id=deploy_server.id).update(status=4)

        self.send_message_to_group(task_id, 'update', {'key': str(diagram_object.id), 'color': color})
        self.send_message_to_group(task_id, 'log', log)

    # 发布任务
    def deploy_start(self, task_object, task_id, retry=False):
        process_start_object = models.Diagram.objects.filter(task=task_object, text='开始').first()
        # 已成功，则不再执行此任务。
        if retry and process_start_object.status == 'green':
            return True
        # 执行开始任务
        try:
            self.step_success(process_start_object, "【开始发布】成功", task_id)
            return True
        except Exception as e:
            log = "【开始发布】失败。\n具体原因：%s" % traceback.format_exc()
            self.step_error(process_start_object, log, task_id)

    def deploy_before_download(self, task_object, task_id, retry=False):

        deploy_before_object = models.Diagram.objects.filter(task=task_object, text='下载前').first()

        try:
            if not deploy_before_object:
                return True

            if retry and deploy_before_object.status == 'green':
                return True

            script_folder_path = os.path.join(
                settings.HG_DEPLOY_BASE_PATH, task_object.env.project.title, task_object.env.env, task_object.uid,
                'script'
            )

            if not os.path.exists(script_folder_path):
                os.makedirs(script_folder_path)

            # .py   /   .sh
            # python a.py    /   sh  a.sh(linux命令)
            with open(os.path.join(script_folder_path, 'before_download.sh'), mode='w',
                      encoding='utf-8') as file_object:
                file_object.write(task_object.before_download_script)

            result = subprocess.check_output('sh before_download.sh', cwd=script_folder_path, shell=True)

            message = "【下载前钩子】成功。执行日志：{}".format(result.decode('utf-8'))
            self.step_success(deploy_before_object, message, task_id)
            return True
        except Exception as e:
            log = "【下载前钩子】失败。\n具体原因：%s" % traceback.format_exc()
            self.step_error(deploy_before_object, log, task_id)

    def deploy_download(self, task_object, task_id, retry=False):
        process_download_object = models.Diagram.objects.filter(task=task_object, text='下载').first()
        if retry and process_download_object.status == 'green':
            return True

        try:
            local_project_path = os.path.join(settings.HG_DEPLOY_BASE_PATH,
                                              task_object.env.project.title,
                                              task_object.env.env,
                                              task_object.env.project.title,
                                              )

            repo_object = GitRepository(local_project_path, task_object.env.project.repo)

            if task_object.tag:
                # 基于tag发布
                repo_object.change_to_tag(task_object.tag)
            else:
                # 基于分支和commit发布
                repo_object.change_to_commit(task_object.branch, task_object.commit)

            self.step_success(process_download_object, "【下载代码】成功", task_id)
            return True
        except Exception as e:
            log = "【下载代码】失败。\n具体原因：%s" % traceback.format_exc()
            self.step_error(process_download_object, log, task_id)

    def deploy_after_download(self, task_object, task_id, retry=False):

        deploy_after_object = models.Diagram.objects.filter(task=task_object, text='下载后').first()

        try:
            if not deploy_after_object:
                return True

            if retry and deploy_after_object.status == 'green':
                return True

            script_folder_path = os.path.join(
                settings.HG_DEPLOY_BASE_PATH, task_object.env.project.title, task_object.env.env, task_object.uid,
                'script'
            )

            if not os.path.exists(script_folder_path):
                os.makedirs(script_folder_path)

            with open(os.path.join(script_folder_path, 'after_download.sh'), mode='w', encoding='utf-8') as file_object:
                file_object.write(task_object.before_download_script)

            result = subprocess.check_output('sh after_download.sh', cwd=script_folder_path, shell=True)

            message = "【下载后钩子】成功。执行日志：{}".format(result.decode('utf-8'))
            self.step_success(deploy_after_object, message, task_id)
            return True
        except Exception as e:
            log = "【下载后钩子】失败。\n具体原因：%s" % traceback.format_exc()
            self.step_error(deploy_after_object, log, task_id)

    def deploy_zip(self, task_object, task_id, retry=False):
        zip_object = models.Diagram.objects.filter(task=task_object, text='打包').first()
        if retry and zip_object.status == 'green':
            return os.path.join(settings.HG_ZIP_BASE_PATH,
                                task_object.env.project.title,
                                task_object.env.env,
                                task_object.uid + '.zip')
        try:

            # 提前把远程脚本写入script目录
            script_folder_path = os.path.join(
                settings.HG_DEPLOY_BASE_PATH, task_object.env.project.title, task_object.env.env, task_object.uid,
                'script'
            )
            if not os.path.exists(script_folder_path):
                os.makedirs(script_folder_path)

            if task_object.before_deploy_script:
                with open(os.path.join(script_folder_path, 'before_deploy.sh', ), mode='w',
                          encoding='utf-8') as file_object:
                    file_object.write(task_object.before_deploy_script)

            if task_object.after_deploy_script:
                with open(os.path.join(script_folder_path, 'after_deploy.sh'), mode='w',
                          encoding='utf-8') as file_object:
                    file_object.write(task_object.after_deploy_script)

            zip_file_path = shutil.make_archive(
                # base_name="code/www",  # 压缩包文件路劲
                base_name=os.path.join(settings.HG_ZIP_BASE_PATH,
                                       task_object.env.project.title,
                                       task_object.env.env,
                                       task_object.uid),
                # 压缩包文件路劲
                format='zip',  # “zip”, “tar”
                root_dir=os.path.join(settings.HG_DEPLOY_BASE_PATH,
                                      task_object.env.project.title,
                                      task_object.env.env,
                                      task_object.uid)  # 被压缩的文件件
            )
            self.step_success(zip_object, "【打包】成功", task_id)
            return zip_file_path
        except Exception as e:
            log = "【打包】失败。\n具体原因：%s" % traceback.format_exc()
            self.step_error(zip_object, log, task_id)

    def deploy_upload(self, zip_file_path, task_object, task_id, retry):
        rsa_object = models.Rsa.objects.filter(status=1).first()
        deploy_server_list = models.DeployServer.objects.filter(deploy=task_object)
        has_error = False
        for deploy_server in deploy_server_list:
            with SSHProxy(deploy_server.server.hostname, 22, rsa_object.user, rsa_object.private_key) as proxy:
                project_name = task_object.env.project.title
                upload_file_folder = "/data/codes/{}/{}/".format(project_name, task_object.env.env)
                upload_script_folder = os.path.join(upload_file_folder, task_object.uid, 'script')
                upload_code_path = os.path.join(upload_file_folder, task_object.uid, project_name)

                # 1. 上传代码 & 解压 /data/history/项目
                status = self.deploy_upload_code(task_object, task_id, proxy, deploy_server, zip_file_path,
                                                 upload_file_folder, retry)
                if not status:
                    has_error = True
                    continue

                # 2. 执行 发布前钩子
                status = self.deploy_upload_before_hook(task_object, task_id, proxy, upload_script_folder,
                                                        deploy_server, retry)
                if not status:
                    has_error = True
                    continue

                # 3. 执行 发布（备份/软连接）
                status = self.deploy_upload_publish(task_object, task_id, proxy, upload_code_path, deploy_server, retry)
                if not status:
                    has_error = True
                    continue

                # 4. 执行发布后钩子
                status = self.deploy_upload_after_hook(task_object, task_id, proxy, upload_script_folder,
                                                       deploy_server, retry)
                if not status:
                    has_error = True
                    continue

                deploy_server.status = 4
                deploy_server.save()

        return has_error

    # 服务器发布操作
    def deploy_upload_code(self, task_object, task_id, proxy, deploy_server, zip_file_path, upload_file_folder, retry):
        diagram_object = models.Diagram.objects.filter(task=task_object, text=deploy_server.server.hostname,
                                                       deploy_record=deploy_server).first()
        if retry and diagram_object.status == 'green':
            return True
        try:
            upload_file_path = os.path.join(upload_file_folder, task_object.uid + '.zip')
            unzip_file_folder = os.path.join(upload_file_folder, task_object.uid)
            # 检查上传目录
            proxy.command("mkdir -p %s" % upload_file_folder)
            proxy.upload(zip_file_path, upload_file_path)
            proxy.command("unzip {0} -d {1}".format(upload_file_path, unzip_file_folder))
            self.step_success(diagram_object, "【{} 上传代码】成功".format(deploy_server.server.hostname), task_id)
            return True
        except Exception as e:
            log = "【上传代码】失败。\n具体原因：%s" % traceback.format_exc()
            self.step_server_error(diagram_object, log, task_id, deploy_server)

    def deploy_upload_before_hook(self, task_object, task_id, proxy, script_folder, deploy_server, retry):
        diagram_object = models.Diagram.objects.filter(task=task_object, text='发布前',
                                                       deploy_record=deploy_server).first()
        if not diagram_object:
            return True

        if retry and diagram_object.status == 'green':
            return True
        try:
            cmd = "sh {0} {1}".format(os.path.join(script_folder, 'before_deploy.sh'), task_object.env.path)
            result = proxy.command(cmd)
            msg = "【{} 发布后钩子】成功。\n详细信息如下：{}".format(deploy_server.server.hostname, result.decode('utf-8'))
            self.step_success(diagram_object, msg, task_id)
            return True
        except Exception as e:
            log = "【{} 发布前钩子】失败。\n具体原因：{}".format(deploy_server.server.hostname, traceback.format_exc())
            self.step_server_error(diagram_object, log, task_id, deploy_server)

    def deploy_upload_publish(self, task_object, task_id, proxy, upload_code_path, deploy_server, retry):
        diagram_object = models.Diagram.objects.filter(task=task_object, text='发布', deploy_record=deploy_server).first()
        if retry and diagram_object.status == 'green':
            return True
        try:
            # 删除软连接
            proxy.command("rm -rf {}".format(task_object.env.path))

            # 创建线上目录
            proxy.command("mkdir -p {}".format(task_object.env.path))

            # 新建软连接 ln –s  /var/www/test   /var/test
            #   新上传代码路径 upload_code_path;  线上代码路径 task_object.env.path
            target = os.path.join(task_object.env.path, task_object.env.project.title)
            proxy.command("ln -s {} {}".format(upload_code_path, target))

            self.step_success(diagram_object, "【{} 发布】成功".format(deploy_server.server.hostname), task_id)
            return True
        except Exception as e:
            log = "【{} 发布】失败。\n具体原因：{}".format(deploy_server.server.hostname, traceback.format_exc())
            self.step_server_error(diagram_object, log, task_id, deploy_server)

    def deploy_upload_after_hook(self, task_object, task_id, proxy, script_folder, deploy_server, retry):
        diagram_object = models.Diagram.objects.filter(task=task_object, text='发布后',
                                                       deploy_record=deploy_server).first()
        if not diagram_object:
            return True

        if retry and diagram_object.status == 'green':
            return True
        try:
            cmd = "sh {0} {1}".format(os.path.join(script_folder, 'after_deploy.sh'), task_object.env.path)
            result = proxy.command(cmd)
            msg = "【{} 发布后钩子】成功。\n详细信息如下：{}".format(deploy_server.server.hostname, result.decode('utf-8'))
            self.step_success(diagram_object, msg, task_id)
            return True
        except Exception as e:
            log = "【{} 发布后钩子】失败。\n具体原因：{}".format(deploy_server.server.hostname, traceback.format_exc())
            self.step_server_error(diagram_object, log, task_id, deploy_server)

    # websocket
    def websocket_connect(self, message):

        # 获取发布任务ID和发布任务对象，不存则断开连接
        task_id = self.scope['url_route']['kwargs'].get('task_id')
        task_object = models.DeployTask.objects.filter(id=task_id).first()
        if not task_object:
            self.close()
            raise StopConsumer()

        # 接受前端发来的websocket请求
        self.accept()

        # 去数据库中获取当前任务的所有节点记录，用来生成页面上的流程图标。
        # 去数据库中获取当前任务的每个节点的日志，并在日志部分输出。
        diagram_object_list = models.Diagram.objects.filter(task=task_object)
        diagram_data_list = []
        for item in diagram_object_list:
            temp = {
                "key": str(item.id),
                "text": item.text,
                "color": item.status,
            }
            if item.parent:
                temp['parent'] = str(item.parent_id)
            diagram_data_list.append(temp)

            if not item.log:
                continue
            # 将每个节点日志 发送给 当前用户 的前端
            self.send_message_to_user('log', item.log)

        # 将任务的节点将数据返 当前用户 的前端
        self.send_message_to_user('init', diagram_data_list)

        # 判断发布任务的状态，如果 已成功，则断开 websocket 链接，因为不需要再进行实时交互了。
        # 待发布，需要去发布；发布中，需要实时动态显示效果；失败，需要执行重发布。
        if task_object.status == 3:
            self.close()  # 告诉客户端，我要和你断开连接。
            raise StopConsumer()  # 我先自杀

        # 把自己加到 task_id 群里，以接受之后发来的消息。
        async_to_sync(self.channel_layer.group_add)(task_id, self.channel_name)

    def websocket_receive(self, message):

        # 1. 点击按钮类型是否合法：发布 /  重新发布
        if not self.is_valid_type(message):
            self.send_message_to_user('error', '发布类型错误')
            return

        # 2. 检查任务ID是否合法
        task_id = self.scope['url_route']['kwargs'].get('task_id')

        # 3. 状态&锁 处理，保证任务不会重复发布。
        with transaction.atomic():
            task_object = models.DeployTask.objects.filter(id=task_id).select_for_update().first()
            # 任务不存在
            if not task_object:
                self.send_message_to_user('error', '任务ID不存在')
                return
            # 正在发布中，提示无需重复操作。
            if task_object.status == 2:
                self.send_message_to_user('error', '正在发布中，无需重复操作。')
                return
            # 已发布成功，提示已成功
            if task_object.status == 3:
                self.send_message_to_user('error', '已发布成功，无需重复操作。')
                return

            # 未发布，点击发布按钮 -> 变更为发布中，进行发布。
            # 发布失败，点击重新发布 -> 变更为发布中，进行重新发布。
            task_object.status = 2
            task_object.save()

        # 4. 点击发布按钮，生成图表节点记录
        if self.is_deploy(message):
            success = self.init_diagram_record(task_object, task_id)
            if not success:
                # 失败，更新状态为 失败
                self.change_status_to_fail(task_object)
                return
        # 5. 点击重新发布按钮，未生成图标，则立即生成图表节点记录
        else:
            success = self.retry_init_diagram_record(task_object, task_id)
            if not success:
                # 失败，更新状态为 失败
                self.change_status_to_fail(task_object)
                return

        # 6. 去发布
        def task(retry):
            # 6.1 处理开始
            is_success = self.deploy_start(task_object, task_id, retry)
            if not is_success:
                self.change_status_to_fail(task_object)
                return

            # 6.2 下载前钩子，创建脚本并本地执行
            is_success = self.deploy_before_download(task_object, task_id, retry)
            if not is_success:
                self.change_status_to_fail(task_object)
                return

            # 6.3 处理下载
            is_success = self.deploy_download(task_object, task_id, retry)
            if not is_success:
                self.change_status_to_fail(task_object)
                return

            # 6.4 下载后钩子，创建脚本并本地执行
            is_success = self.deploy_after_download(task_object, task_id, retry)
            if not is_success:
                self.change_status_to_fail(task_object)
                return

            # 6.5 打包代码（本地&远程脚本）
            zip_file_path = self.deploy_zip(task_object, task_id, retry)
            if not zip_file_path:
                self.change_status_to_fail(task_object)
                return

            # 6.6 上传代码 并 远程执行脚本
            has_error = self.deploy_upload(zip_file_path, task_object, task_id, retry)
            if has_error:
                task_object.status = 4
            else:
                task_object.status = 3
            task_object.save()

        retry = not self.is_deploy(message)
        deploy_thread = threading.Thread(target=task, args=(retry,))
        deploy_thread.start()

    def xxx_ooo(self, event):
        message = event['message']
        if message.get('close'):
            self.close()
        else:
            self.send(json.dumps(message))

    def websocket_disconnect(self, message):
        """
        用户主动断开连接，在 task 群组中移除此用户
        :param message:
        :return:
        """
        task_id = self.scope['url_route']['kwargs'].get('task_id')
        async_to_sync(self.channel_layer.group_discard)(task_id, self.channel_name)
        raise StopConsumer()
