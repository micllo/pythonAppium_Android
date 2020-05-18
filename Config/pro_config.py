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


def get_login_accout(thread_name_index):
    """
    通过线程名的索引 获取登录账号
    :param thread_name_index:
    :return:
    """
    if thread_name_index == 1:
        return "user_1", "passwd_1"
    elif thread_name_index == 2:
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


def get_android_device_info():
    """
    获取 Android 设备信息
    :return:
    """
    android_device_info = dict()
    android_device_info["小米5S"] = "192.168.31.136:5555"
    android_device_info["锤子PRO1"] = "15a6c95a"
    return android_device_info


def get_desired_caps(thread_name_index, pro_name):
    """
    通过线程名的索引和项目名称 获取启动设备信息(指定设备，指定应用)
    :param thread_name_index:
    :param pro_name
    :return:
    """
    app_info = get_app_info(pro_name)
    android_device_info = get_android_device_info()
    desired_caps = dict()
    desired_caps["platformName"] = "Android"
    desired_caps["appPackage"] = app_info["appPackage"]
    desired_caps["appActivity"] = app_info["appActivity"]
    # 使用哪个自动化引擎
    desired_caps["automationName"] = "UiAutomator2"
    # Appium 等待接收从客户端发送的新命令的超时时长，超时后Appium会终止会话
    desired_caps["newCommandTimeout"] = 300
    # Android 等待设备就绪的超时时长，以秒为单位
    desired_caps["deviceReadyTimeout"] = 60
    # Android 在启动后等待设备就绪的超时时长，以秒为单位
    desired_caps["androidDeviceReadyTimeout"] = 60

    # 唤醒屏幕
    desired_caps["unlockType"] = "pattern"
    desired_caps["unlockKey"] = "12589"

    if thread_name_index == 1:
        desired_caps["platformVersion"] = "7.0"
        desired_caps["deviceName"] = android_device_info["小米5S"]
        return desired_caps, "小米5S"
    elif thread_name_index == 2:
        desired_caps["platformVersion"] = "7.1.1"
        desired_caps["deviceName"] = android_device_info["锤子PRO1"]
        return desired_caps, "锤子PRO1"
    else:
        return desired_caps, "设备未找到"

