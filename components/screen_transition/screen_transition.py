#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file screen_transition.py
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
import numpy
import numpy as np

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
screen_transition_spec = ["implementation_id", "screen_transition", 
         "type_name",         "screen_transition", 
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
# @class screen_transition
# @brief ModuleDescription
# 
# 
# </rtc-template>
class screen_transition(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_screen_in = OpenRTM_aist.instantiateDataType(RTC.CameraImage)
        """
        """
        self._screen_inIn = OpenRTM_aist.InPort("screen_in", self._d_screen_in)
        self._d_transition_out = OpenRTM_aist.instantiateDataType(RTC.TimedWString)
        """
        """
        self._transition_outOut = OpenRTM_aist.OutPort("transition_out", self._d_transition_out)


		


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
        self.addInPort("screen_in",self._screen_inIn)
		
        # Set OutPort buffers
        self.addOutPort("transition_out",self._transition_outOut)
		
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
    def onActivated(self, ec_id):
        #最初に黒背景の画像を読み込ませる
        self.previous_screen_img = cv2.imread("Black.jpg")
        self.first_image_acquisition = True
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

    def get_average_color(self,image, x, y, w, h):

        region = image[y:y+h, x:x+w]
        mean_color = cv2.mean(region)[:3]
        return mean_color


    def detect_screen_transition(self,previous_screen_img,new_screen_pimg, threshold=55, num_divisions=10):
        
        # 画像の大きさを取得
        height, width, _ = previous_screen_img.shape

        # 分割する領域の幅と高さを計算
        div_width = width // num_divisions
        div_height = height // num_divisions

        # 各領域の平均色を計算比較
        for i in range(num_divisions):
            for j in range(num_divisions):
                x = i * div_width
                y = j * div_height

                prev_avg_color = self.get_average_color(previous_screen_img, x, y, div_width, div_height)
                new_avg_color = self.get_average_color(new_screen_pimg, x, y, div_width, div_height)
                
                # 2つの平均色の差を計算
                color_diff = np.sqrt(sum([(prev_avg_color[k] - new_avg_color[k])**2 for k in range(3)]))
                
                # 色の差が閾値以上であれば、画面遷移があったと判断
                if color_diff > threshold:
                    return True

        return False


    def onExecute(self, ec_id):

        if self._screen_inIn.isNew(): #新しいデータが来たか確認
            self._d_screen_in = self._screen_inIn.read()
            #最初一回の取得の際にtrueを出力してしまうことを防ぐ変数
            self.first_image_acquisition = False

            frame = numpy.frombuffer(bytes(self._d_screen_in.pixels), dtype=numpy.uint8)
            frame = frame.reshape(self._d_screen_in.height, self._d_screen_in.width, self._d_screen_in.bpp//8)    
            frame = cv2.cvtColor(
                frame, cv2.COLOR_BGRA2BGR)

            #画面遷移を検出
            self.new_screen_img = frame
            transition_detected = self.detect_screen_transition(self.previous_screen_img, self.new_screen_img)
            self.previous_screen_img = self.new_screen_img

            #画面遷移が検出されたら1,されなかったら0を送信
            if transition_detected == True and self.first_image_acquisition == False:
                self._d_transition_out.data = 1
                self._transition_outOut.write()
                result = "true"

            else:
                self._d_transition_out.data = 0
                self._transition_outOut.write()    
                result = "false"     

            print(result)
            self._d_transition_out.data = result
            self._transition_outOut.write()       
        
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
	



def screen_transitionInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=screen_transition_spec)
    manager.registerFactory(profile,
                            screen_transition,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    screen_transitionInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("screen_transition" + args)

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

