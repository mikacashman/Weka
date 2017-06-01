/*
A KBase module: Weka
*/

module Weka {
    /*
        Insert your typespec information here.
    */
	/*A binary boolean*/
	typedef int bool;

	typedef structure{
		string workspace_name;
		string phenotype_ref;
		float  confidenceFactor;
		int    minNumObj;
		int    numFolds;
		bool   reducedErrorPruning;
		int    seed;
		bool   unpruned;
	}DTParams;
	typedef structure{
		string report_name;
		string report_ref;
	}DTOutput;

	funcdef DecisionTree(DTParams params) returns (DTOutput) authentication required;

};
