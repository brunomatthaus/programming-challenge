package com.example.sidiatest;

import java.util.HashMap;
import java.util.Map;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
        "AVERAGERATING",
        "NUMVOTES",
        "ORIGINALTITLE",
        "PRIMARYTITLE",
        "STARTYEAR",
        "TCONST"
})
public class Movie {

//movie type definition

    @JsonProperty("AVERAGERATING")
    private Double aVERAGERATING;
    @JsonProperty("NUMVOTES")
    private Integer nUMVOTES;
    @JsonProperty("ORIGINALTITLE")
    private String oRIGINALTITLE;
    @JsonProperty("PRIMARYTITLE")
    private String pRIMARYTITLE;
    @JsonProperty("STARTYEAR")
    private Integer sTARTYEAR;
    @JsonProperty("TCONST")
    private String tCONST;
    @JsonIgnore
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("AVERAGERATING")
    public Double getAVERAGERATING() {
        return aVERAGERATING;
    }

    @JsonProperty("AVERAGERATING")
    public void setAVERAGERATING(Double aVERAGERATING) {
        this.aVERAGERATING = aVERAGERATING;
    }

    @JsonProperty("NUMVOTES")
    public Integer getNUMVOTES() {
        return nUMVOTES;
    }

    @JsonProperty("NUMVOTES")
    public void setNUMVOTES(Integer nUMVOTES) {
        this.nUMVOTES = nUMVOTES;
    }

    @JsonProperty("ORIGINALTITLE")
    public String getORIGINALTITLE() {
        return oRIGINALTITLE;
    }

    @JsonProperty("ORIGINALTITLE")
    public void setORIGINALTITLE(String oRIGINALTITLE) {
        this.oRIGINALTITLE = oRIGINALTITLE;
    }

    @JsonProperty("PRIMARYTITLE")
    public String getPRIMARYTITLE() {
        return pRIMARYTITLE;
    }

    @JsonProperty("PRIMARYTITLE")
    public void setPRIMARYTITLE(String pRIMARYTITLE) {
        this.pRIMARYTITLE = pRIMARYTITLE;
    }

    @JsonProperty("STARTYEAR")
    public Integer getSTARTYEAR() {
        return sTARTYEAR;
    }

    @JsonProperty("STARTYEAR")
    public void setSTARTYEAR(Integer sTARTYEAR) {
        this.sTARTYEAR = sTARTYEAR;
    }

    @JsonProperty("TCONST")
    public String getTCONST() {
        return tCONST;
    }

    @JsonProperty("TCONST")
    public void setTCONST(String tCONST) {
        this.tCONST = tCONST;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperty(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

}