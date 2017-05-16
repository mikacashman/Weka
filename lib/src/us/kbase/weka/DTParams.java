
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
 * <pre>
 * Insert your typespec information here.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "phenotype_ref"
})
public class DTParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("phenotype_ref")
    private String phenotypeRef;
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
        return ((((((("DTParams"+" [workspaceName=")+ workspaceName)+", phenotypeRef=")+ phenotypeRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
