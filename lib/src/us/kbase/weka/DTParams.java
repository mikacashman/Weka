
package us.kbase.weka;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: DTParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "phenotype_ref",
    "confidenceFactor",
    "minNumObj",
    "numFolds",
    "seed",
    "unpruned",
    "class_values",
    "class_labels"
})
public class DTParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("phenotype_ref")
    private String phenotypeRef;
    @JsonProperty("confidenceFactor")
    private Double confidenceFactor;
    @JsonProperty("minNumObj")
    private Long minNumObj;
    @JsonProperty("numFolds")
    private Long numFolds;
    @JsonProperty("seed")
    private Long seed;
    @JsonProperty("unpruned")
    private Long unpruned;
    @JsonProperty("class_values")
    private String classValues;
    @JsonProperty("class_labels")
    private String classLabels;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public DTParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("phenotype_ref")
    public String getPhenotypeRef() {
        return phenotypeRef;
    }

    @JsonProperty("phenotype_ref")
    public void setPhenotypeRef(String phenotypeRef) {
        this.phenotypeRef = phenotypeRef;
    }

    public DTParams withPhenotypeRef(String phenotypeRef) {
        this.phenotypeRef = phenotypeRef;
        return this;
    }

    @JsonProperty("confidenceFactor")
    public Double getConfidenceFactor() {
        return confidenceFactor;
    }

    @JsonProperty("confidenceFactor")
    public void setConfidenceFactor(Double confidenceFactor) {
        this.confidenceFactor = confidenceFactor;
    }

    public DTParams withConfidenceFactor(Double confidenceFactor) {
        this.confidenceFactor = confidenceFactor;
        return this;
    }

    @JsonProperty("minNumObj")
    public Long getMinNumObj() {
        return minNumObj;
    }

    @JsonProperty("minNumObj")
    public void setMinNumObj(Long minNumObj) {
        this.minNumObj = minNumObj;
    }

    public DTParams withMinNumObj(Long minNumObj) {
        this.minNumObj = minNumObj;
        return this;
    }

    @JsonProperty("numFolds")
    public Long getNumFolds() {
        return numFolds;
    }

    @JsonProperty("numFolds")
    public void setNumFolds(Long numFolds) {
        this.numFolds = numFolds;
    }

    public DTParams withNumFolds(Long numFolds) {
        this.numFolds = numFolds;
        return this;
    }

    @JsonProperty("seed")
    public Long getSeed() {
        return seed;
    }

    @JsonProperty("seed")
    public void setSeed(Long seed) {
        this.seed = seed;
    }

    public DTParams withSeed(Long seed) {
        this.seed = seed;
        return this;
    }

    @JsonProperty("unpruned")
    public Long getUnpruned() {
        return unpruned;
    }

    @JsonProperty("unpruned")
    public void setUnpruned(Long unpruned) {
        this.unpruned = unpruned;
    }

    public DTParams withUnpruned(Long unpruned) {
        this.unpruned = unpruned;
        return this;
    }

    @JsonProperty("class_values")
    public String getClassValues() {
        return classValues;
    }

    @JsonProperty("class_values")
    public void setClassValues(String classValues) {
        this.classValues = classValues;
    }

    public DTParams withClassValues(String classValues) {
        this.classValues = classValues;
        return this;
    }

    @JsonProperty("class_labels")
    public String getClassLabels() {
        return classLabels;
    }

    @JsonProperty("class_labels")
    public void setClassLabels(String classLabels) {
        this.classLabels = classLabels;
    }

    public DTParams withClassLabels(String classLabels) {
        this.classLabels = classLabels;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((((((((((("DTParams"+" [workspaceName=")+ workspaceName)+", phenotypeRef=")+ phenotypeRef)+", confidenceFactor=")+ confidenceFactor)+", minNumObj=")+ minNumObj)+", numFolds=")+ numFolds)+", seed=")+ seed)+", unpruned=")+ unpruned)+", classValues=")+ classValues)+", classLabels=")+ classLabels)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
