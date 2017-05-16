# -*- coding: utf-8 -*-
#BEGIN_HEADER
import sys
import traceback
from pprint import pprint, pformat
from biokbase.workspace.client import Workspace as workspaceService
#END_HEADER


class Weka:
    '''
    Module Name:
    Weka

    Module Description:
    A KBase module: Weka
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    workspaceURL = None
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
	self.workspaceURL = config['workspace-url']
	self.scratch = config['scratch']
        #END_CONSTRUCTOR

    def DecisionTree(self, ctx, params):
        """
        :param params: instance of type "DTParams" (Insert your typespec
           information here.) -> structure: parameter "workspace_name" of
           String, parameter "phenotype_ref" of String
        :returns: instance of type "DTOutput" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN DecisionTree
        #runs J48 Deicison trees in weka on phenotype set
 
        ### STEP 1 - Parse input and catch any errors
        if 'workspace_name' not in params:
                raise ValueError('Parameter workspace is not set in input arguments')
        workspace_name = params['workspace_name']
        if 'phenotype_ref' not in params:
        	raise ValueError('Parameter phenotype is not set in input arguments')
        phenotype = params['phenotype_ref']
 
        #STEP 2 - Get the input data
        token = ctx['token']
        wsClient = workspaceService(self.workspaceURL, token=token)
        try:
                pheno = wsClient.get_objects([{'ref': phenotype}])[0]['data']
	except:
        	exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                orig_error = ''.join('   ' + line for line in lines)
                raise ValueError('Error loading original Phenotype object from workspace:\n' + orig_error)
        print('Got Phenotype')
 
        ### STEP 3 - Create Matrix
 
        ### STEP 4 - Print matrix to file
 
        ### STEP 5 - Create ARFF file
 
        ### STEP 6 - Send to WEKA
 
        ### STEP 7 - Print tree result to report
        report = "Success"      
	returnVal = {
		'report_name':'DT_report',
		'report_ref': report}
        #END DecisionTree

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method DecisionTree return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]


    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
