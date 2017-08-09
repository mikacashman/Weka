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
		int    seed;
		bool   unpruned;
		string class_values;
		string class_labels;
	}DTParams;
	typedef structure{
		string report_name;
		string report_ref;
	}DTOutput;

	funcdef DecisionTree(DTParams params) returns (DTOutput output) authentication required;

};
