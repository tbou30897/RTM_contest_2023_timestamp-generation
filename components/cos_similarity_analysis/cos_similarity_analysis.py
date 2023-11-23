#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file cos_similarity_analysis.py
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

import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
cos_similarity_analysis_spec = ["implementation_id", "cos_similarity_analysis", 
         "type_name",         "cos_similarity_analysis", 
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
# @class cos_similarity_analysis
# @brief ModuleDescription
# 
# 
# </rtc-template>
class cos_similarity_analysis(OpenRTM_aist.DataFlowComponentBase):
	
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
        self._d_text_in = OpenRTM_aist.instantiateDataType(RTC.TimedWString)
        """
        """
        self._text_inIn = OpenRTM_aist.InPort("text_in", self._d_text_in)
        self._d_summary_out = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        """
        self._summary_outOut = OpenRTM_aist.OutPort("summary_out", self._d_summary_out)


		


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
        self.addInPort("text_in",self._text_inIn)
		
        # Set OutPort buffers
        self.addOutPort("summary_out",self._summary_outOut)
		
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
    # TF-IDFキーワード抽出関数
    def extract_keywords(self,text, n=2):
        vectorizer = TfidfVectorizer(stop_words=['として', 'こと', 'など', 'で', 'の', 'が', 'を', 'に', 'は', 'も', 'や', 'と', 'おり', 'あり'], max_features=10000)
        tfidf_matrix = vectorizer.fit_transform([text])
        feature_names = np.array(vectorizer.get_feature_names_out())
        sorted_index = np.argsort(tfidf_matrix.toarray()).flatten()[::-1]
        return feature_names[sorted_index][:n]


    # MeCabでの分かち書き関数
    def tokenize_with_mecab(self,text):
        mecab = MeCab.Tagger("-Owakati")
        return mecab.parse(text).strip()

    def compute_cosine_similarity_mecab(self,doc1, doc2, ngram_range=(1, 1)):
        # 日本語の文章をMeCabで単語に分割
        doc1_tokenized = self.tokenize_with_mecab(doc1)
        doc2_tokenized = self.tokenize_with_mecab(doc2)
        
        # n-gramを使用して文章をベクトル化する
        vectorizer = TfidfVectorizer(ngram_range=ngram_range)
        vectorizer.fit([doc1_tokenized, doc2_tokenized])
        
        vectors = vectorizer.transform([doc1_tokenized, doc2_tokenized])
        
        # cos類似度を計算する
        cosine_sim = cosine_similarity(vectors)
        
        # 2つの文章の間のcos類似度を返す
        return cosine_sim[0][1]


    def onActivated(self, ec_id):
        self.integrated_text = ""
        self.prev_sentence = ""    
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
        #画面遷移したらテキストを結合して要約
        if self._text_inIn.isNew(): #新しいデータが来たか確認
            self._d_text_in = self._text_inIn.read() #値を読み込む
            text =  self._d_text_in.data 

            self.integrated_text += text

        if self._transition_inIn.isNew(): #新しいデータが来たか確認(テキスト)
            self._d_transition_in = self._transition_inIn.read() #値を読み込む
            truth =  self._d_transition_in.data 

            if truth == "true" and self.integrated_text.strip() :
                summary_result = self.extract_keywords(self.integrated_text)

                if len(summary_result) >= 2:
                    output_list = [summary_result[0],summary_result[1]]

                    output_text = f"{summary_result[0]},{summary_result[1]}"

                    print(output_list)

                    #前の文章との類似度分析
                    similarity_mecab = self.compute_cosine_similarity_mecab(self.prev_sentence,output_text)
                    if similarity_mecab < 0.1 :
                        self._d_summary_out.data = output_list
                        self._summary_outOut.write()
                        self.text_combined_list = []
                        self.prev_sentence = ""
                        self.integrated_text = ""

                    else:
                        self._d_summary_out.data = ["High similarity to previous sentence"]
                        self._summary_outOut.write()
                        self.text_combined_list = []
                        self.prev_sentence = output_text    
                        self.integrated_text = ""

                else:
                    self._d_summary_out.data = ["The text is too short to be summarized."]
                    self._summary_outOut.write()
                    self.text_combined_list = []
                    self.prev_sentence = output_text    
                    self.integrated_text = ""

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
	



def cos_similarity_analysisInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=cos_similarity_analysis_spec)
    manager.registerFactory(profile,
                            cos_similarity_analysis,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    cos_similarity_analysisInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("cos_similarity_analysis" + args)

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

