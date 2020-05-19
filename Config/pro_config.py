from Project.pro_demo_1.test_case.demo_test import YybTest


def get_test_class_list(pro_name):
    """
    通过'项目名'获取'测试类'列表
    :param pro_name:
    :return:
    """
    if pro_name == "pro_demo_1":
        test_class_list = [YybTest]
    else:
        test_class_list = None
    return test_class_list


def pro_exist(pro_name):
    """
    判断项目名称是否存在
    :param pro_name:
    :return:
    """
    pro_name_list = ["pro_demo_1", "pro_demo_2"]
    if pro_name in pro_name_list:
        return True
    else:
        return False


def get_login_accout(current_thread_name_index):
    """
    通过线程名的索引 获取登录账号
    :param current_thread_name_index:
    :return:
    """
    if current_thread_name_index == 1:
        return "user_1", "passwd_1"
    elif current_thread_name_index == 2:
        return "user_2", "passwd_2"
    else:
        return "user_3", "passwd_3"


def get_app_info(pro_name):
    """
    通过项目名称 获取APP信息 （ appPackage、 appActivity ）
    :param pro_name:
    :return:
    """
    app_info = {}
    if pro_name == "pro_demo_1":  # 应用宝
        app_info["appPackage"] = 'com.tencent.android.qqdownloader'
        app_info["appActivity"] = 'com.tencent.pangu.link.SplashActivity'
    else:
        app_info["appPackage"] = None
        app_info["appActivity"] = None
    return app_info


def config_android_device_info_list():
    """
    配置 Android 设备信息列表
    [ { "device_name": "小米5S", "platform_version": "7.0", "device_udid": "192.168.31.136:5555" } } ,
      { "device_name": "坚果Pro", "platform_version": "7.1.1", "device_udid": "15a6c95a" } } ]
    :return:
    """
    android_device_info_list = []

    xiao_mi_5s = dict()
    xiao_mi_5s["device_name"] = "小米5S"
    xiao_mi_5s["platform_version"] = "7.0"
    xiao_mi_5s["device_udid"] = "192.168.31.136:5555"
    android_device_info_list.append(xiao_mi_5s)

    smartisan_pro = dict()
    smartisan_pro["device_name"] = "坚果Pro"
    smartisan_pro["platform_version"] = "7.1.1"
    smartisan_pro["device_udid"] = "15a6c95a"
    android_device_info_list.append(smartisan_pro)

    return android_device_info_list


# def get_desired_caps(pro_name, current_thread_name_index, connected_android_device_list):
#     """
#     获取 Appium 服务启动应用所需的能力参数 (指定设备，指定应用)
#     :param pro_name
#     :param current_thread_name_index: 当前线程名字的索引
#     :param connected_android_device_list: 已连接设备信息列表
#     [ { "thread_index": 1, "device_name": "小米5S", "platform_version": "7.0", "device_udid": "192.168.31.136:5555" } } ,
#       { "thread_index": 2, "device_name": "坚果Pro", "platform_version": "7.1.1", "device_udid": "15a6c95a" } } ]
#     :return:
#
#     【 备 注 】通过'当前线程名索引' 获取已连接设备列表中对应的设备信息
#     """
#     app_info = get_app_info(pro_name)
#     desired_caps = dict()
#     desired_caps["platformName"] = "Android"
#     desired_caps["appPackage"] = app_info["appPackage"]
#     desired_caps["appActivity"] = app_info["appActivity"]
#     # 使用哪个自动化引擎
#     desired_caps["automationName"] = "UiAutomator2"
#     # Appium 等待接收从客户端发送的新命令的超时时长，超时后Appium会终止会话
#     desired_caps["newCommandTimeout"] = 30
#     # Android 等待设备就绪的超时时长，以秒为单位
#     desired_caps["deviceReadyTimeout"] = 30
#     # Android 在启动后等待设备就绪的超时时长，以秒为单位
#     desired_caps["androidDeviceReadyTimeout"] = 30
#
#     # 唤醒屏幕（效果不理想）
#     desired_caps["unlockType"] = "pattern"
#     desired_caps["unlockKey"] = "12589"
#
#     device_name = "设备未找到"
#     for connected_android_devices_dict in connected_android_device_list:
#         if current_thread_name_index == connected_android_devices_dict["thread_index"]:
#             desired_caps["platformVersion"] = connected_android_devices_dict["platform_version"]
#             desired_caps["deviceName"] = connected_android_devices_dict["device_udid"]
#             device_name = connected_android_devices_dict["device_name"]
#             break
#     return desired_caps, device_name
