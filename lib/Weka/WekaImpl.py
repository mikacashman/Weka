# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
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
	#currently assumed the base media is the same for all phenotypes,
	#this should be updated later to allow more flexibility.
	phenos = []
	compounds = []
	growth = []
 	
 	for i in range(0,len(pheno['phenotypes'])):
		temp = []
		#zero out list first (no compounds present)
		for j in range(0,len(compounds)):
			temp.append(0)
		for j in range(0,len(pheno['phenotypes'][i]['additionalcompound_refs'])):
			if pheno['phenotypes'][i]['additionalcompound_refs'][j] in compounds:
				#find it in the list and make it a 1
				temp[compounds.index(pheno['phenotypes'][i]['additionalcompound_refs'][j])]=1
			else:
				#add 0 to all exisiting phenos and add 1 to this one
				compounds.append(pheno['phenotypes'][i]['additionalcompound_refs'][j])
				for k in range(0,len(phenos)):
					phenos[k].append(0)
				temp.append(1)
		phenos.append(temp)
		growth.append(pheno['phenotypes'][i]['normalizedGrowth'])
	print(compounds)
	#print(phenos)
	print(growth)

        ### STEP temp - Print matrix to file
 	matfilename = self.scratch + "/matrix.txt"
	matrixfile = open(matfilename,"w+")
	for i in range(0,len(compounds)):
		matrixfile.write(compounds[i] + " ")
	matrixfile.write("\n")	
	for i in range(0,len(phenos)):
		for j in range(0,len(phenos[i])):
			matrixfile.write(str(phenos[i][j]))
		matrixfile.write(" --> " + str(growth[i]))
		matrixfile.write("\n")
	matrixfile.close()	

        ### STEP 4 - Create ARFF file
 	wekafile = self.scratch + "/weka.arff"
	arff = open(wekafile,"w+")
	arff.write("@RELATION J48DT_Phenotype\n\n")
	for i in range(0,len(compounds)):
		arff.write("@ATTRIBUTE " + compounds[i] + " {ON,OFF}\n")
	arff.write("@ATTRIBUTE class {GROWTH,NO_GROWTH}")
	arff.write("\n@data\n")
	for i in range(0,len(phenos)):
		for j in range(0,len(phenos[i])):
			if phenos[i][j] == 1:
				arff.write("ON,")
			elif phenos[i][j] == 0:
				arff.write("OFF,")
			else:
				raise ValueError('Error: Invalid compound in phenos associated with phenotype.  Must be a 1 (for ON) or 0 (for OFF).  Please report bug.')
		
		if growth[i] == 0:
			arff.write("GROWTH" + '\n')
		elif growth[i] == 1:
			arff.write("NO_GROWTH" + '\n')
		else:
			raise ValueError('Error: Invalid growth class associated with phenotype.  Must be a 1 (for growth) or 0 (for no_growth).  Please check your phenotype data set.')
	arff.close()
		
        ### STEP 5 - Send to WEKA
	#Call weka with a different protocol?  os.system not recomeneded - what is?
	outfilename = self.scratch + "/weka.out"
	os.system("java weka.classifiers.trees.J48 -t " + wekafile + " -T " + wekafile + " -i > " + outfilename) 

        ### STEP 6 - Print tree result to report
        report = outfilename      
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
