# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests

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

        print("starting test...")
	test_dir = os.path.dirname(os.path.realpath(__file__))
	#pheno_path = test_dir + "/data/Jmmol.pheno.json"
	#genome_path = test_dir + "/data/BThetaGenome.json"
	#with open(genome_path) as f:
	#	object_data = json.load(f)
	#file_name = "TestGeno"
	#self.getWsClient().save_objects({'workspace': self.getWsName(),'objects': [{'type': 'KBaseGenomes.Genome-7.0','name': file_name,'data': object_data}]})
	
	#with open(pheno_path) as f:
	#	object_data = json.load(f)
	#file_name = "TestPheno"
	#self.getWsClient().save_objects({'workspace': self.getWsName(),'objects': [{'type': 'KBasePhenotypes.PhenotypeSet-3.0','name': file_name,'data': object_data}]})
	
	#hardcoded
	ret = self.getImpl().DecisionTree(self.getContext(),{'workspace_name':'mikaelacashman:narrative_1496165061369','phenotype_ref':'4965/10/1'})
	
	#test narrative
	#ret = self.getImpl().DecisionTree(self.getContext(), {"phenotype_ref": self.getWsName() + "/" + file_path})[0]
		
	print("Running zero asserts...")
	#expected_output_file = test_dir + "/data/weka.out"
	#expected_output = open(expected_output_file)
	#self.assertEqual(ret[0]['report_ref'],expected_output)

    def test_DTAdvancedUnPruned(self):
	print("starting advanced test...")
	ret = self.getImpl().DecisionTree(self.getContext(),{'workspace_name':'mikaelacashman:narrative_1496165061369','phenotype_ref':'4965/10/1','unpruned':'true'})

    def test_DTAdvancedReducedPrune(self):
	print("starting advanced test...")
	ret = self.getImpl().DecisionTree(self.getContext(),{'workspace_name':'mikaelacashman:narrative_1496165061369','phenotype_ref':'4965/10/1','reducedErrorPruning':'true','numFolds':'11','seed':'142'})

    def test_DTAdvancedMinObj(self):
	print("starting advanced test...")
	ret = self.getImpl().DecisionTree(self.getContext(),{'workspace_name':'mikaelacashman:narrative_1496165061369','phenotype_ref':'4965/10/1','minNumObj':'10'})
