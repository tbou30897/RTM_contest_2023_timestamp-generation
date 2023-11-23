#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file window_captcha.py
 @brief ModuleDescription
 @date $Date$


"""
# </rtc-template>

import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

#other-import
import cv2
import pygetwindow as gw
import pyautogui
import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
window_captcha_spec = ["implementation_id", "window_captcha", 
         "type_name",         "window_captcha", 
         "description",       "ModuleDescription", 
         "version",           "1.0.0", 
         "vendor",            "VenderName", 
         "category",          "Category", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class window_captcha
# @brief ModuleDescription
# 
# 
# </rtc-template>
class window_captcha(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_image_out = OpenRTM_aist.instantiateDataType(RTC.CameraImage)
        """
        """
        self._image_outOut = OpenRTM_aist.OutPort("image_out", self._d_image_out)
        self._d_time_out = OpenRTM_aist.instantiateDataType(RTC.TimedFloat)
        """
        """
        self._time_outOut = OpenRTM_aist.OutPort("time_out", self._d_time_out)


		


        # initialize of configuration-data.
        # <rtc-template block="init_conf_param">
		
        # </rtc-template>


		 
    ##
    #
    # The initialize action (on CREATED->ALIVE transition)
    # 
    # @return RTC::ReturnCode_t
    # 
    #
    def onInitialize(self):
        # Bind variables and configuration variable
		
        # Set InPort buffers
		
        # Set OutPort buffers
        self.addOutPort("image_out",self._image_outOut)
        self.addOutPort("time_out",self._time_outOut)
		
        # Set service provider to Ports
		
        # Set service consumers to Ports
		
        # Set CORBA Service Ports
		
        return RTC.RTC_OK
	
    ###
    ## 
    ## The finalize action (on ALIVE->END transition)
    ## 
    ## @return RTC::ReturnCode_t
    #
    ## 
    #def onFinalize(self):
    #

    #    return RTC.RTC_OK
	
    ###
    ##
    ## The startup action when ExecutionContext startup
    ## 
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onStartup(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The shutdown action when ExecutionContext stop
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onShutdown(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ##
    #
    # The activated action (Active state entry action)
    #
    # @param ec_id target ExecutionContext Id
    # 
    # @return RTC::ReturnCode_t
    #
    #
    # 開かれているウィンドウ名を出す
    def show_window_list(self):
        print("現在開かれているウィンドウの一覧：")
        windows = gw.getWindowsWithTitle("")
        for i, window in enumerate(windows):
            print(f"{i+1}. {window.title}")

        return windows
    

    #キャプチャするウィンドウを選択するUI
    def select_window_gui(self):
        root = tk.Tk()
        root.withdraw()  # 主ウィンドウを隠す

        window_titles = [window.title for window in self.windows]
        answer = simpledialog.askstring("ウィンドウの選択",
                                        "キャプチャするウィンドウの番号を選択してください：\n" + "\n".join([f"{i+1}. {title}" for i, title in enumerate(window_titles)]),
                                        parent=root)
        return int(answer)



    def onActivated(self, ec_id):
        self.start_time = None  #タイムスタンプ保存変数

        self.windows = self.show_window_list()  # 現在開かれているウィンドウの一覧を表示

        # GUIでウィンドウを選択する
        self.window_num = self.select_window_gui()

        self.window = self.windows[self.window_num - 1]


    
        return RTC.RTC_OK
	
    ##
    #
    # The deactivated action (Active state exit action)
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    def onDeactivated(self, ec_id):
    
        return RTC.RTC_OK
	
    ##
    #
    # The execution action that is invoked periodically
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #

    # 画面キャプチャ関数
    def capture_window(self,window):

        # ウィンドウの位置とサイズを取得
        window_location = gw.getWindowsWithTitle(window.title)[0]._rect

        # ウィンドウの範囲をスクリーンショットでキャプチャ
        screenshot = pyautogui.screenshot(region=(window_location.left, window_location.top, window_location.width, window_location.height))
            
        # スクリーンショットをNumPy配列に変換
        frame = np.array(screenshot)
        #RGBをBGRに
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        #画像をリターン
        return frame


    def onExecute(self, ec_id):
        # 指定されたウィンドウを一度キャプチャ 
        frame = self.capture_window(self.window)  
        
        # キャプチャ開始時のタイムスタンプがない場合は保存
        if self.start_time is None:
            self.start_time = time.time()

        # 経過時間を計算して送信
        elapsed_time = time.time() - self.start_time
        print(elapsed_time)
        self._d_time_out.data = elapsed_time
        self._time_outOut.write()
          
        # 一度キャプチャされたら0.25待つ
        time.sleep(0.25)  

        #画像データ送信
        self._d_image_out.height = frame.shape[0]
        self._d_image_out.width = frame.shape[1]
        if(len(frame.shape)>2):
            self._d_image_out.bpp = 8*frame.shape[2]
        else:
            self._d_image_out.bpp = 8
        self._d_image_out.pixels = frame.flatten().tobytes()
        self._image_outOut.write() 

        time.sleep(10)
     
        
           
        return RTC.RTC_OK

    ###
    ##
    ## The aborting action when main logic error occurred.
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onAborting(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The error action in ERROR state
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onError(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The reset action that is invoked resetting
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onReset(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The state update action that is invoked after onExecute() action
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##

    ##
    #def onStateUpdate(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The action that is invoked when execution context's rate is changed
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onRateChanged(self, ec_id):
    #
    #    return RTC.RTC_OK
	



def window_captchaInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=window_captcha_spec)
    manager.registerFactory(profile,
                            window_captcha,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    window_captchaInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("window_captcha" + args)

def main():
    # remove --instance_name= option
    argv = [i for i in sys.argv if not "--instance_name=" in i]
    # Initialize manager
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager()

if __name__ == "__main__":
    main()

