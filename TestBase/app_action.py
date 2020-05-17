# -*- coding:utf-8 -*-
from Common.com_func import project_path, log, mkdir
from Env import env_config as cfg
from selenium.common.exceptions import TimeoutException
from Config import global_var as gv
import time
from Tools.mongodb import MongoGridFS
from appium import webdriver
from Common.test_func import send_DD_for_FXC


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

