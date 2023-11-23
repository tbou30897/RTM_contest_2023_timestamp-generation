#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file timestamp_creation.py
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


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
timestamp_creation_spec = ["implementation_id", "timestamp_creation", 
         "type_name",         "timestamp_creation", 
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
# @class timestamp_creation
# @brief ModuleDescription
# 
# 
# </rtc-template>
class timestamp_creation(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_transition_in = OpenRTM_aist.instantiateDataType(RTC.TimedWString)
        """
        """
        self._transition_inIn = OpenRTM_aist.InPort("transition_in", self._d_transition_in)
        self._d_time_in = OpenRTM_aist.instantiateDataType(RTC.TimedFloat)
        """
        """
        self._time_inIn = OpenRTM_aist.InPort("time_in", self._d_time_in)
        self._d_summarization_in = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        """
        self._summarization_inIn = OpenRTM_aist.InPort("summarization_in", self._d_summarization_in)
        self._d_timestamp_out = OpenRTM_aist.instantiateDataType(RTC.TimedWString)
        """
        """
        self._timestamp_outOut = OpenRTM_aist.OutPort("timestamp_out", self._d_timestamp_out)


		


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
        self.addInPort("transition_in",self._transition_inIn)
        self.addInPort("time_in",self._time_inIn)
        self.addInPort("summarization_in",self._summarization_inIn)
		
        # Set OutPort buffers
        self.addOutPort("timestamp_out",self._timestamp_outOut)
		
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
        self.transition_time = []
        self.time = 0    
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
    def onExecute(self, ec_id):
        #経過時間取得
        if self._time_inIn.isNew(): #新しいデータが来たか確認
            self._d_time_in = self._time_inIn.read() #値を読み込む
            self.time =  self._d_time_in.data

        #画面遷移
        if self._transition_inIn.isNew(): #新しいデータが来たか確認
            if self.time:
                self._d_transition_in = self._transition_inIn.read() #値を読み込む
                transition =  self._d_transition_in.data

                if transition == "true":
                    self.transition_time.append(self.time)
                    print(self.transition_time)

        #要約取得
        if self._summarization_inIn.isNew(): #新しいデータが来たか確認
            self._d_summarization_in = self._summarization_inIn.read() #値を読み込む
            summarization_list = self._d_summarization_in.data

            if len(summarization_list) == 2:
                summarization_text = f"{summarization_list[0]},{summarization_list[1]}" 

                #分数と秒数を計算
                self.time = int(self.transition_time[1])
                print(self.transition_time[1])
                str_minute = str(int(self.time / 60))
                str_second = str(self.time % 60)
                if len(str_second) == 1:
                    str_second = "0" + str_second

                minute_and_second_data = f"{str_minute}:{str_second}"

                print(minute_and_second_data)

                #要約と時間を結合
                timestamp = summarization_text + ":" +  minute_and_second_data

                #タイムスタンプを送信
                self._d_timestamp_out.data = timestamp
                self._timestamp_outOut.write()

                del self.transition_time[0]    
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
	



def timestamp_creationInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=timestamp_creation_spec)
    manager.registerFactory(profile,
                            timestamp_creation,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    timestamp_creationInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("timestamp_creation" + args)

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

