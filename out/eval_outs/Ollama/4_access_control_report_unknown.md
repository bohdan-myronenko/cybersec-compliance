# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** Unknown period

**Risk Level:** HIGH


## Key Metrics

- Total login attempts: **1**
- Distinct users: **0**
- Distinct source IPs: **0**

### Authentication
- Successful logins: **0**
- Failed logins: **0**
- Failure rate: **0.0**
- Top failing IPs:  

  - No failures detected


### Attack Surface Indicators
- Known attack IP attempts: **0**
- Unique attack IPs: **0**
- Confirmed account takeover events: **0**
- Users impacted by takeovers: **0**

## Notable Exceptions

_No exceptions reported._



## AI-Generated Insights


Analysis could not be completed due to an error.


### Security Findings


#### INFO: Analysis Error

Failed to parse JSON: Expecting ',' delimiter: line 14 column 35 (char 693)





**Recommendation:** Retry the analysis or review metrics manually.

---


#### HIGH: Incomplete MFA Coverage

MFA is enabled for 0/0 users (0.0%).


**Evidence:**

- metric: mfa_coverage

- current_value: 0.0%

- target: 100%




**Compliance Impact:**

- **NIS2** (Article 21.2(j)): Multi-factor authentication is explicitly required.



**Recommendation:** Enforce MFA for all user accounts, prioritizing privileged accounts.

---






### Trend Analysis







## Compliance Observations
**Access-Control Compliance Section**

1. **Multi-Factor Authentication**: No data available in the provided evidence to determine compliance with Article 21, paragraph 2(j) ([NIS2-21.2.j]). The metrics JSON does not provide information on MFA usage.
2. **User Access Control**: No data available in the provided evidence to determine compliance with Article 21, paragraph 2(i) ([NIS2-21.2.i]). The metrics JSON does not provide information on user access control policies or asset management.

Note: This section is based solely on the provided legal text and metrics JSON, which do not contain sufficient information to determine compliance for these requirements.

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures