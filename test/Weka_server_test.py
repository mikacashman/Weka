# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests
import re
import difflib

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from Weka.WekaImpl import Weka
from Weka.WekaServer import MethodContext
from Weka.authclient import KBaseAuth as _KBaseAuth


class WekaTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('Weka'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'Weka',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = Weka(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_Weka_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx
   
    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_DecisionTree(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods

	print
        print("starting test...")
	ret = self.getImpl().DecisionTree(self.getContext(),{'workspace_name':'mikaelacashman:narrative_1496165061369','phenotype_ref':'4965/10/1'})
	report = self.wsClient.get_objects([{'ref': ret[0]['report_ref']}])[0]['data']
	oracle_path = self.cfg['scratch'] + "/test_oracle/BTLabCLI.out"
	
	self.assertTrue(self.compare_by_lines(oracle_path,report))


#    def test_DTAdvancedUnPruned(self):
#	print
#	print("starting advanced test -U...")
#	ret = self.getImpl().DecisionTree(self.getContext(),{'workspace_name':'mikaelacashman:narrative_1496165061369','phenotype_ref':'4965/10/1','unpruned':1})
#	report = self.wsClient.get_objects([{'ref': ret[0]['report_ref']}])[0]['data']
#	oracle_path = self.cfg['scratch']+"/test_oracle/BTLabCLI-U.out"
	
#	self.assertTrue(self.compare_by_lines(oracle_path,report))


    def test_DTAdvancedReducedPrune(self):
	print
	print("starting advanced test -R...")
	ret = self.getImpl().DecisionTree(self.getContext(),{'workspace_name':'mikaelacashman:narrative_1496165061369','phenotype_ref':'4965/10/1','reducedErrorPruning':1})
	report = self.wsClient.get_objects([{'ref': ret[0]['report_ref']}])[0]['data']
	oracle_path = self.cfg['scratch']+"/test_oracle/BTLabCLI-R.out"
	
	self.assertTrue(self.compare_by_lines(oracle_path,report))

    def test_DTAdvancedMinObj(self):
	print
	print("starting advanced test -M...")
	ret = self.getImpl().DecisionTree(self.getContext(),{'workspace_name':'mikaelacashman:narrative_1496165061369','phenotype_ref':'4965/10/1','minNumObj':'10'})
	report = self.wsClient.get_objects([{'ref': ret[0]['report_ref']}])[0]['data']
	oracle_path = self.cfg['scratch']+"/test_oracle/BTLabCLI-M.out"

	self.assertTrue(self.compare_by_lines(oracle_path,report))

#    def test_DTcustomClasses(self):
#	print
#	print("starting custom classes test...")
#	ret = self.getImpl().DecisionTree(self.getContext(),{'workspace_name':'mikaelacashman:narrative_1496165061369','phenotype_ref':'4965/13/1','class_values':"1,2,3",'class_labels':"LOW,MED,HIGH"})
#	report = self.wsClient.get_objects([{'ref': ret[0]['report_ref']}])[0]['data']
#	oracle_path = self.cfg['scratch']+"/test_oracle/BTKBaseCLI-custclass.out"
#
#	self.assertTrue(self.compare_by_lines(oracle_path,report))

    def test_DTAdvnacedConf(self):
	print
	print("starting advanced test -C...")
	ret = self.getImpl().DecisionTree(self.getContext(),{'workspace_name':'mikaelacashman:narrative_1496165061369','phenotype_ref':'4965/10/1','confidenceFactor':.1})
	report = self.wsClient.get_objects([{'ref': ret[0]['report_ref']}])[0]['data']
	oracle_path = self.cfg['scratch']+"/test_oracle/BTLabCLI-C.out"

	self.assertTrue(self.compare_by_lines(oracle_path,report))
    
    def test_Fail(self):
	print
	print("starting advanced test -C Fail...")
	ret = self.getImpl().DecisionTree(self.getContext(),{'workspace_name':'mikaelacashman:narrative_1496165061369','phenotype_ref':'4965/10/1','confidenceFactor':0.1})
	report = self.wsClient.get_objects([{'ref': ret[0]['report_ref']}])[0]['data']
	oracle_path = self.cfg['scratch']+"/test_oracle/BTLabCLI-C.fail.out"

	self.assertFalse(self.compare_by_lines(oracle_path,report))

    def compare_by_lines(self,oracle_path,test_report):
	#get strings
	oracleFile = open(oracle_path,"r").read()
	result = test_report['text_message']
	#remove variable time element
	oracleFileReplaced = re.sub("[0-9]+\.[0-9]+ seconds","seconds",oracleFile)
	resultReplaced = re.sub("[0-9]+\.[0-9]+ seconds","seconds",result)
	#split into lists for easy compare
	oracleFileSplit = oracleFileReplaced.splitlines()
	resultSplit = resultReplaced.splitlines()
	#compare line by line until cross-validation
	#ignore cross-validation as it can be variable
	for x in range(0,len(oracleFileSplit)):
		if oracleFileSplit[x] == "=== Stratified cross-validation ===" and resultSplit[x] == "=== Stratified cross-validation ===":
			isSame = True
		elif oracleFileSplit[x] == resultSplit[x]:
			isSame = True
		else:
			print(oracleFileSplit[x]+'\n'+resultSplit[x]+'\n')
			isSame = False
			break
	print("test val is: " + str(isSame))
	return isSame 

