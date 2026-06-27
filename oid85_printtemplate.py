import time
import os
import shutil
import config


def deploy():
    # остановка и удаление службы
    cmd = f'sc stop {config.printtemplate_service_name}'
    print(cmd)
    res = os.system(cmd)
    print(res)

    cmd = f'sc delete {config.printtemplate_service_name}'
    print(cmd)
    res = os.system(cmd)
    print(res)

    # формируем директории
    if not os.path.exists(config.deploy_path):
        os.makedirs(config.deploy_path)

    if not os.path.exists(os.path.join(config.deploy_path, config.printtemplate_deploy_directory)):
        os.makedirs(os.path.join(config.deploy_path, config.printtemplate_deploy_directory))

    current_time = time.time()
    current_deploy_version = f"{current_time}"

    dest_path = os.path.join(config.deploy_path, config.printtemplate_deploy_directory, current_deploy_version)

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    # build
    cmd = f'cd {config.printtemplate_source_path} && dotnet build --configuration Release --output {dest_path}'
    print(cmd)
    res = os.system(cmd)
    print(res)

    # копируем appsettings.json
    shutil.copy(config.printtemplate_appsettings_file, dest_path)

    exe_file_path = os.path.join(dest_path, config.printtemplate_exe_file_name)

    # установка и запуск службы
    cmd = f'sc create {config.printtemplate_service_name} binPath={exe_file_path}'
    print(cmd)
    res = os.system(cmd)
    print(res)

    cmd = f'sc start {config.printtemplate_service_name}'
    print(cmd)
    res = os.system(cmd)
    print(res)
