#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file system_sound_captcha.py
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
import soundcard as sc
import soundfile as sf
import threading
import numpy as np
import speech_recognition as sr


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
system_sound_captcha_spec = ["implementation_id", "system_sound_captcha", 
         "type_name",         "system_sound_captcha", 
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
# @class system_sound_captcha
# @brief ModuleDescription
# 
# 
# </rtc-template>
class system_sound_captcha(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_text_out = OpenRTM_aist.instantiateDataType(RTC.TimedWString)
        """
        """
        self._text_outOut = OpenRTM_aist.OutPort("text_out", self._d_text_out)


		


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
        self.addOutPort("text_out",self._text_outOut)
		
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

        self.output_file_name = "out.wav"    # 出力するファイル名
        self.samplerate = 48000              # サンプリング周波数 [Hz]
        self.record_sec = 5                  # 録音する時間 [秒]
        
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
    def system_sound_cap(self):
        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=self.samplerate) as mic:
            # デフォルトスピーカーから録音
            data = mic.record(numframes=self.samplerate*self.record_sec)
            # データが2次元配列であることを確認（例えば：(サンプル数, チャンネル数)）
            assert len(data.shape) == 2, "録音データは2次元配列でなければなりません。"
            # 録音データをファイルに保存
            sf.write(self.output_file_name, data, self.samplerate)
        return data, self.output_file_name, self.samplerate


    def transcribe_audio(self, audio_file):
        # speech_recognitionのRecognizerインスタンスを作成
        recognizer = sr.Recognizer()
        # 保存したオーディオファイルを読み込む
        with sr.AudioFile(audio_file) as source:
            # ノイズ調整
            recognizer.adjust_for_ambient_noise(source)
            # オーディオデータの読み込み
            audio_data = recognizer.record(source)
                
        try:
            # Google Web Speech APIを使用して音声認識を実行
            text = recognizer.recognize_google(audio_data, language="ja-JP")
            print("Recognized text:", text)
            self._d_text_out.data = text  # 文字起こししたテキストを出力
            self._text_outOut.write()
            
        except sr.RequestError as e:
            # APIが利用できない場合
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except sr.UnknownValueError as e:
            # 認識できない音声の場合
            print(f"Google Speech Recognition could not understand audio; {e}")


    def onExecute(self, ec_id):

        data_array, output_file, sample_rate = self.system_sound_cap()             
        # 文字起こしを別のスレッドで非同期に実行する
        threading.Thread(target=self.transcribe_audio, args=(output_file,)).start()
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
	



def system_sound_captchaInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=system_sound_captcha_spec)
    manager.registerFactory(profile,
                            system_sound_captcha,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    system_sound_captchaInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("system_sound_captcha" + args)

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

