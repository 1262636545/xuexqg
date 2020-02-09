
# coding: utf-8
#运行学习强国：Allowing start of Intent { act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] cmp=cn.xuexi.android/com.alibaba.android.rimet.biz.SplashActivity } in package cn.xuexi.android
#每日答题：// Allowing start of Intent { act=android.intent.action.VIEW dat=https://qr.dingtalk.com/common_webview.html pkg=cn.xuexi.android cmp=cn.xuexi.android/com.alibaba.lightapp.runtime.activity.CommonWebViewActivity } in package cn.xuexi.android
#在命令提示符中，输入   adb shell monkey --port 62001 -v -v    //adb shell monkey  --port  模拟器商品号 -v -v    加入2个v是为了输出的信息更加详细
from uiautomator import device as driver
import numpy as np
import time
import os
import sys
import win32api

Height=1280
Width=720
all_of_list=[]
if os.path.isfile("jilu.npy"):
    all_of_list = np.load ("jilu.npy", allow_pickle=True).tolist()

def autoJob(tv,sleep_time,sum,click=True):
    count_click=0
    count=0
    drag_str='adb shell input swipe '+str(Width*0.5)+' '+str(Height*0.88)+' '+str(Width*0.5)+' '+str(Height*0.3)
    
    for _ in range(100):
        text_lists=driver(className='android.widget.TextView')
        try:
            for i in range(len(text_lists)):
                txt=text_lists[i].text
                if len(txt)>11 and txt not in all_of_list and count<sum:
                    driver(text=txt,className='android.widget.TextView').click()
                    
                    #分享，收藏，评论
                    if click and count_click<2:
                        #分享
                        time.sleep(5)
                        driver.click(0.94*Width, 0.975*Height)
                        time.sleep(5)
                        driver(text="分享到学习强国").click()
                        time.sleep(5)
                        driver.press.back()
                        #收藏
                        driver.click(0.84*Width, 0.975*Height)
                        time.sleep(5)
                        #评论
                        time.sleep(3)
                        driver(text="欢迎发表你的观点").click()
                        time.sleep(5)
                        os.system("adb shell am broadcast -a ADB_INPUT_TEXT --es msg '中国加油中国加油'")
                        os.system("adb shell input keyevent 66")#不知道为什么输入一个回车，点击发布才有反应
                        time.sleep(2)
                        driver(text="发布").click()
                        
                        count_click=count_click+1
                        time.sleep(2)

                    count=count+1
                    all_of_list.append(txt)
                    print("正在"+tv+"...",txt)
                    time.sleep(sleep_time)
                    driver.press.back()
        except BaseException:
            # print(BaseException)
            print("抛出异常，程序继续执行...")
        if count >=sum:
            break
        os.system(drag_str)
        time.sleep(5)

def watch_local():
    driver(text='重庆').click()
    time.sleep(5)
    driver(text='重庆卫视').click()
    print("观看本地频道...")
    time.sleep(20)
    print("本地频道结束")
    driver.press.back()


#阅读文章,阅读6个文章，每个文章停留240秒
def read_articles():
    time.sleep(10)
    #切换到学习首页面
    # driver(resourceId="cn.xuexi.android:id/home_bottom_tab_button_contact").click()#这里要换，测试后换成新地址
    #切换到要闻界面
    driver(text='要闻').click()
    time.sleep(5)
    autoJob(tv="阅读文章",sleep_time=130,sum=6,click=False)#130
    print("阅读文章结束")

def read_sport():
    time.sleep(10)
    #切换到学习首页面
    # driver(resourceId="cn.xuexi.android:id/home_bottom_tab_button_contact").click()#这里要换，测试后换成新地址
    #切换到要闻界面
    driver(text='体育').click()
    time.sleep(5)
    autoJob(tv="阅读体育新闻2篇并分享收藏评论",sleep_time=20,sum=2)
    print("阅读体育新闻2篇并分享收藏评论结束")


#观看视频,每个视频观看90秒，以及20分钟新闻联盟
def watch_video():
    time.sleep(5)
    #切换到电视台页面
    driver(resourceId="cn.xuexi.android:id/home_bottom_tab_button_contact").click()
    time.sleep(5)
    driver(text="联播频道").click()
    time.sleep(5)
    autoJob(tv="观看视频",sleep_time=20,sum=6,click=False)
    driver(text="联播频道").click()
    time.sleep(5)
    
    news=None
    for v in driver(className='android.widget.TextView'):
        if "《新闻联播》" in v.text:
            news=v.text
            break
    driver(text=news).click()

    
    text_list=None
    #删除最早一天的记录
    if len(all_of_list)>350:
        text_list = np.array (all_of_list[25:])
    else:
        text_list = np.array (all_of_list)
    #存储已看视频和文章
    np.save ('jilu.npy',text_list)
    
    print("正在观看新闻联播...")
    time.sleep(1050)#1050
    driver.press('back')
    print("观看视频结束.")

if __name__ == '__main__':
    print("正在关闭夜神模拟器")
    os.system("taskkill /F /IM Nox.exe")
    time.sleep(5)

    print('正在打开夜神模拟器')
    win32api.ShellExecute(0, 'open', r'"D:\Program Files\Nox\bin\Nox.exe"', '','',1)#安装路径可能不一样，注意修改
    #os.popen( r'"D:\Program Files\Nox\bin\Nox.exe"')
    time.sleep(60)#60
    
    print('正在启动ADB服务项目')
    
    os.system('adb kill-server')
    os.system('adb start-server')
    os.system('adb connect 127.0.0.1:62001')
    time.sleep(5)

    #屏幕高度
    Height=driver.info['displayHeight']
    Width=driver.info['displayWidth']
    time.sleep(5)

    #自动打开学习强国
    os.system('adb shell am start cn.xuexi.android/com.alibaba.android.rimet.biz.SplashActivity')
    time.sleep(40)#30

    watch_local()
    read_articles()
    read_sport()
    watch_video()

    print("正在关闭夜神模拟器")
    os.system("taskkill /F /IM Nox.exe")
    #os.popen (r'"D:\Program Files\Nox\bin\Nox.exe quit"')
    time.sleep(2)
    print("正在关闭ADB服务")
    os.system('adb kill-server')
    print("学习结束！")


