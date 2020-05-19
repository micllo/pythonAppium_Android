# -*- coding:utf-8 -*-
from Common.com_func import project_path, log, mkdir
from Env import env_config as cfg
import time
from Tools.mongodb import MongoGridFS
from appium import webdriver
from Common.test_func import send_DD_for_FXC


def get_desired_caps(pro_name, current_thread_name_index, connected_android_device_list):
    """
    获取 Appium 服务启动应用所需的能力参数 (指定设备，指定应用)
    :param pro_name
    :param current_thread_name_index: 当前线程名字的索引
    :param connected_android_device_list: 已连接设备信息列表
    [ { "thread_index": 1, "device_name": "小米5S", "platform_version": "7.0", "device_udid": "192.168.31.136:5555" } } ,
      { "thread_index": 2, "device_name": "坚果Pro", "platform_version": "7.1.1", "device_udid": "15a6c95a" } } ]
    :return:

    【 备 注 】通过'当前线程名索引' 获取已连接设备列表中对应的设备信息
    """
    from Config.pro_config import get_app_info
    app_info = get_app_info(pro_name)
    desired_caps = dict()
    desired_caps["platformName"] = "Android"
    desired_caps["appPackage"] = app_info["appPackage"]
    desired_caps["appActivity"] = app_info["appActivity"]
    # 使用哪个自动化引擎
    desired_caps["automationName"] = "UiAutomator2"
    # Appium 等待接收从客户端发送的新命令的超时时长，超时后Appium会终止会话
    desired_caps["newCommandTimeout"] = 30
    # Android 等待设备就绪的超时时长，以秒为单位
    desired_caps["deviceReadyTimeout"] = 30
    # Android 在启动后等待设备就绪的超时时长，以秒为单位
    desired_caps["androidDeviceReadyTimeout"] = 30

    # 唤醒屏幕（效果不理想）
    desired_caps["unlockType"] = "pattern"
    desired_caps["unlockKey"] = "12589"

    device_name = "设备未找到"
    for connected_android_devices_dict in connected_android_device_list:
        if current_thread_name_index == connected_android_devices_dict["thread_index"]:
            desired_caps["platformVersion"] = connected_android_devices_dict["platform_version"]
            desired_caps["deviceName"] = connected_android_devices_dict["device_udid"]
            device_name = connected_android_devices_dict["device_name"]
            break
    return desired_caps, device_name


def get_driver(pro_name, desired_caps, device_name):
    """
    获 取 设 备 驱 动
    :param pro_name:
    :param desired_caps: 启动设备信息(指定设备，指定应用)
    :param device_name: 设备名称
    :return:
    """
    try:
        driver = webdriver.Remote(cfg.APPIUM_SERVER, desired_caps)
    except Exception as e:
        log.error(("显示异常：" + str(e)))
        if "Failed to establish a new connection" in str(e):
            error_msg = "Appium 服务未启动"
        elif "Could not find a connected Android device" in str(e):
            error_msg = "Android 设备(" + device_name + ")未连接"
        elif "Failed to launch Appium Settings app" in str(e):
            error_msg = "Appium Setting 应用启动超时"
        else:
            error_msg = "启动 Appium 服务的其他异常情况"
        send_DD_for_FXC(title=pro_name, text="#### " + error_msg + "")
        raise Exception(error_msg)
    return driver


class Base(object):

    def __init__(self, driver):
        self.driver = driver
        self.log = log

    def find_ele(self, *args):
        try:
            self.log.info("通过" + args[0] + "定位，元素是 " + args[1])
            return self.driver.find_element(*args)
        except Exception:
            raise Exception(args[1] + " 元素定位失败！")

    def find_ele_by_text(self, content):
        """
        通过text找到元素（唯一）
        :param content:
        :return:
        """
        try:
            return self.driver.find_element_by_android_uiautomator('new UiSelector().text("' + content + '")')
        except Exception:
            raise Exception("text = \"" + content + "\" 的元素未找到")

    def find_eles_by_text(self, content):
        """
        通过text找到元素（多个）
        :param content:
        :return:
        """
        try:
            return self.driver.find_elements_by_android_uiautomator('new UiSelector().text("' + content + '")')
        except Exception:
            raise Exception("text = \"" + content + "\" 的元素未找到")

    def click(self, *args):
        self.find_ele(*args).click()

    def send_key(self, *args, value):
        self.find_ele(*args).send_keys(value)

    def js(self, str):
        self.driver.execute_script(str)

    def url(self):
        return self.driver.current_url

    def back(self):
        self.driver.back()

    def forward(self):
        self.driver.forward()

    def quit(self):
        self.driver.quit()

    # 判断页面内容是否存在
    def content_is_exist(self, content, time_out):
        time_init = 1   # 初始化时间
        polling_interval = 1  # 轮询间隔时间
        while content not in self.driver.page_source:
            time.sleep(polling_interval)
            time_init = time_init + 1
            if time_init >= time_out:
                return False
        return True

    def screenshot(self, image_name, case_instance):
        """
         截 图、保 存 mongo、记录图片ID
        :param image_name: 图片名称
        :param case_instance: 测试类实例对象
        :return:
        """
        # ../类名/方法名/
        current_test_path = cfg.SCREENSHOTS_DIR + case_instance.pro_name + "/" + case_instance.class_method_path
        mkdir(current_test_path)
        self.driver.get_screenshot_as_file(current_test_path + image_name)
        mgf = MongoGridFS()
        files_id = mgf.upload_file(img_file_full=current_test_path + image_name)
        case_instance.screen_shot_id_list.append(files_id)

    def assert_content_and_screenshot(self, image_name, case_instance, content, time_out, error_msg):
        """
        断言内容是否存在、同时截屏
        :param image_name: 图片名称
        :param case_instance: 测试类实例对象
        :param content: 需要轮询的内容
        :param time_out: 轮询内容的超时时间
        :param error_msg: 断言失败后的 错误提示
        :return:
        """
        is_exist = True
        time_init = 1   # 初始化时间
        polling_interval = 1  # 轮询间隔时间
        while content not in self.driver.page_source:
            time.sleep(polling_interval)
            time_init = time_init + 1
            if time_init >= time_out:
                is_exist = False
                break
        self.screenshot(image_name, case_instance)
        case_instance.assertTrue(is_exist, error_msg)

    def touch_click(self, x, y):
        """
        触摸点击
        :param x: 横坐标（从左上角开始）
        :param y: 从坐标（从左上角开始）
        :return:
        """
        self.driver.tap([(x, y)])

    # 获得机器屏幕大小x,y
    def get_size(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        # log.info(x, y)
        return x, y

    # 屏幕向上滑动（效果：屏幕往'下'翻动）
    def swipe_up(self, t=1000):
        l = self.get_size()
        x = int(l[0] * 0.5)  # 固定 x 坐标
        y1 = int(l[1] * 0.75)  # 起始 y 坐标
        y2 = int(l[1] * 0.25)  # 终点 y 坐标
        self.driver.swipe(x, y1, x, y2, t)

    # 屏幕向下滑动（效果：屏幕往'上'翻动）
    def swipe_down(self, t=1000):
        l = self.get_size()
        x = int(l[0] * 0.5)  # 固定 x 坐标
        y1 = int(l[1] * 0.25)  # 起始 y 坐标
        y2 = int(l[1] * 0.75)  # 终点 y 坐标
        self.driver.swipe(x, y1, x, y2, t)

    # 屏幕向左滑动（效果：屏幕往'右'翻动）
    def swip_left(self, t=1000):
        l = self.get_size()
        y = int(l[1] * 0.5)  # 固定 y 坐标
        x1 = int(l[0] * 0.75)  # 起始 x 坐标
        x2 = int(l[0] * 0.05)  # 终点 x 坐标
        self.driver.swipe(x1, y, x2, y, t)

    # 屏幕向右滑动（效果：屏幕往'左'翻动）
    def swip_right(self, t=1000):
        l = self.get_size()
        y = int(l[1] * 0.5)  # 固定 y 坐标
        x1 = int(l[0] * 0.05)  # 起始 x 坐标
        x2 = int(l[0] * 0.75)  # 终点 x 坐标
        self.driver.swipe(x1, y, x2, y, t)


if __name__ == "__main__":
    print(project_path())

