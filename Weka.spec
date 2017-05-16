/*
A KBase module: Weka
*/

module Weka {
    /*
        Insert your typespec information here.
    */

	typedef structure{
		string workspace_name;
		string phenotype_ref;
	}DTParams;
	typedef structure{
		string report_name;
		string report_ref;
	}DTOutput;

	funcdef DecisionTree(DTParams params) returns (DTOutput) authentication required;

};
