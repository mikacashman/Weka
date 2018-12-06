# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import re

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3
    import io

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
        #cls.phenotype_ref = '4965/10/1'
        cls.phenotype_ref = '79/21/1'

        # test_workspace = 'mikaelacashman:narrative_1497284550796'
        # file_to_save = cls.scratch+"/test_data/BTPhenoLab.tsv"
        # print(file_to_save)
        # param = {'id':'testSaveBTLab.pheno',
        #        'type':'KBasePhenotypes.PhenotypeSet',
        #        'data':file_to_save,
        #        'workspace':test_workspace
        #       }
        # cls.wsClient.save_object(param)

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
        print
        print("starting test...")
        print(self.cfg['scratch'])
        self.getImpl().DecisionTree(self.getContext(),
                                    {'workspace_name': self.getWsName(),
                                     #'mikaelacashman:narrative_1497284550796',
                                     'phenotype_ref': self.phenotype_ref})
        oracle_path = os.path.join("test_oracle", "BTLab.out")
        report_path = self.cfg['scratch'] + "/weka.out"
        self.assertTrue(self.compare_by_lines(oracle_path, report_path))

    def test_DTAdvancedUnPruned(self):
        print
        print("starting advanced test -U...")
        self.getImpl().DecisionTree(self.getContext(),
                                    {'workspace_name': self.getWsName(),
                                    #'mikaelacashman:narrative_1497284550796',
                                     'phenotype_ref': self.phenotype_ref, 'unpruned': 1})
        oracle_path = os.path.join("test_oracle", "BTLab-U.out")
        report_path = self.cfg['scratch'] + "/weka.out"
        self.assertTrue(self.compare_by_lines(oracle_path, report_path))

    def test_DTAdvancedMinObj(self):
        print
        print("starting advanced test -M...")
        self.getImpl().DecisionTree(self.getContext(),
                                    {'workspace_name': self.getWsName(),
                                    #'mikaelacashman:narrative_1497284550796',
                                     'phenotype_ref': self.phenotype_ref, 'minNumObj': '10'})
        oracle_path = os.path.join("test_oracle", "BTLab-M.out")
        report_path = self.cfg['scratch'] + "/weka.out"
        self.assertTrue(self.compare_by_lines(oracle_path, report_path))

    def test_DTcustomClasses(self):
        print
        print("starting custom classes test...")
        self.getImpl().DecisionTree(self.getContext(),
                                    {'workspace_name': self.getWsName(),
                                    #'mikaelacashman:narrative_1497284550796',
                                     #'phenotype_ref': '4965/13/1',
                                     'phenotype_ref': self.phenotype_ref,
                                     'class_values': "0,1", 'class_labels': "MED,HIGH"})
        oracle_path = os.path.join("test_oracle", "BTLab-custclass.out")
        report_path = self.cfg['scratch'] + "/weka.out"
        self.assertTrue(self.compare_by_lines(oracle_path, report_path))

    def test_DTAdvnacedConf(self):
        print
        print("starting advanced test -C...")
        self.getImpl().DecisionTree(self.getContext(),
                                    {'workspace_name': self.getWsName(),
                                    #'mikaelacashman:narrative_1497284550796',
                                     'phenotype_ref': self.phenotype_ref, 'confidenceFactor': .1})
        oracle_path = os.path.join("test_oracle", "BTLab-C.out")
        report_path = self.cfg['scratch'] + "/weka.out"
        self.assertTrue(self.compare_by_lines(oracle_path, report_path))

    def test_Fail(self):
        print
        print("starting advanced test -C Fail...")
        self.getImpl().DecisionTree(self.getContext(),
                                    {'workspace_name': self.getWsName(),
                                    #'mikaelacashman:narrative_1497284550796',
                                     'phenotype_ref': self.phenotype_ref, 'confidenceFactor': 0.1})
        oracle_path = os.path.join("test_oracle", "BTLab-C.fail.out")
        report_path = self.cfg['scratch'] + "/weka.out"
        self.assertTrue(self.compare_by_lines(oracle_path, report_path))

    def test_SeedPass(self):
        print
        print("starting seed test Pass...")
        report_path = self.cfg['scratch'] + "/weka.out"

        self.getImpl().DecisionTree(self.getContext(),
                                    {'workspace_name': self.getWsName(),
                                    #'mikaelacashman:narrative_1497284550796',
                                     'phenotype_ref': self.phenotype_ref, 'seed': 100})
        reportFile = open(report_path, "r").read()

        self.getImpl().DecisionTree(self.getContext(),
                                    {'workspace_name': self.getWsName(),
                                    #'mikaelacashman:narrative_1497284550796',
                                     'phenotype_ref': self.phenotype_ref, 'seed': 100})
        reportFile2 = open(report_path, "r").read()

        resultReplaced = re.sub("[0-9]+\.?[0-9]* seconds", "seconds", reportFile)
        result2Replaced = re.sub("[0-9]+\.?[0-9]* seconds", "seconds", reportFile2)

        self.assertTrue(resultReplaced == result2Replaced)

    def notWorkingTest_SeedFail(self):
        print
        print("starting seed test Fail...")
        report_path = self.cfg['scratch'] + "/weka.out"

        self.getImpl().DecisionTree(self.getContext(),
                                    {'workspace_name': self.getWsName(),
                                    #'mikaelacashman:narrative_1497284550796',
                                     'phenotype_ref': self.phenotype_ref})  # default seed is 1
        reportFile = open(report_path, "r").read()

        self.getImpl().DecisionTree(self.getContext(),
                                    {'workspace_name': self.getWsName(),
                                    #'mikaelacashman:narrative_1497284550796',
                                     'phenotype_ref': self.phenotype_ref, 'seed': 42})
        reportFile2 = open(report_path, "r").read()

        resultReplaced = re.sub("[0-9]+\.?[0-9]* seconds", "seconds", reportFile)
        result2Replaced = re.sub("[0-9]+\.?[0-9]* seconds", "seconds", reportFile2)

        self.assertFalse(resultReplaced == result2Replaced)

    def compare_by_lines(self, oracle_path, result_path):
        # get strings
        oracleFile = open(oracle_path, "r").read()
        resultFile = open(result_path, "r").read()
        # remove variable time element
        oracleFileReplaced = re.sub("[0-9]+\.?[0-9]+ seconds", "seconds", oracleFile)
        resultReplaced = re.sub("[0-9]+\.?[0-9]+ seconds", "seconds", resultFile)
        # split into lists for easy compare
        oracleFileSplit = oracleFileReplaced.splitlines()
        resultSplit = resultReplaced.splitlines()
        # compare line by line until cross-validation
        # ignore cross-validation as it can be variable
        isSame = True
        for x in range(0, len(oracleFileSplit)):
                if (oracleFileSplit[x] == "=== Stratified cross-validation ==="
                        and resultSplit[x] == "=== Stratified cross-validation ==="):
                    isSame = True
                    break
                elif oracleFileSplit[x] == resultSplit[x]:
                        isSame = True
                else:
                        if "Time taken" in oracleFileSplit[x]:
                            isSame = True
                            continue 
                        print("The line is",x,'\n')
                        print("MISMATCH\n" + oracleFileSplit[x] + '--\n' + resultSplit[x] + '--\n')
                        isSame = False
                        break
        print("test val is: " + str(isSame))
        return isSame
