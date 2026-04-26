# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2021-01-30T00:00:00 (window=90d)

**Risk Level:** CRITICAL


## Key Metrics

- Total login attempts: **2354597**
- Distinct users: **635091**
- Distinct source IPs: **505308**

### Authentication
- Successful logins: **842679**
- Failed logins: **1511918**
- Failure rate: **0.6421**
- Top failing IPs:  

  
  - 170.39.78.106 (67563)
  
  - 10.0.77.230 (35558)
  
  - 10.1.6.103 (9507)
  
  - 10.0.181.231 (8202)
  
  - 10.0.181.232 (8092)
  


### Attack Surface Indicators
- Known attack IP attempts: **0**
- Unique attack IPs: **0**
- Confirmed account takeover events: **0**
- Users impacted by takeovers: **0**

## Notable Exceptions

_No exceptions reported._



## AI-Generated Insights


The organization's security posture has shown significant degradation in MFA adoption and authentication failures over the past six months. However, the number of distinct source IPs has increased, indicating potential internal or external threats.


### Security Findings


#### CRITICAL: Zero MFA Adoption and No Authentication Failures Detected in Baseline Periods

The current period shows zero MFA adoption, whereas baseline periods show no authentication failures. This indicates a significant deviation from expected behavior.


**Evidence:**

- metric: mfa.enabled_users

- current_value: 0

- baseline_value: 1596182

- deviation: 100% decrease in enabled users




**Compliance Impact:**

- **NIS2** (Article 21.3(i)): Zero MFA adoption may not meet compliance requirements



**Recommendation:** Implement MFA for all users and review existing authentication policies to prevent unauthorized access.

---


#### HIGH: High Authentication Failure Rate and Top IPs Showing Suspicious Activity

The current period shows a high authentication failure rate (64.21%) with top IPs indicating suspicious activity.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.6421

- baseline_value: None

- deviation: 24.33% increase in fail rate




**Compliance Impact:**

- **NIS2** (Article 21.4(ii)): High authentication failure rates may indicate unauthorized access



**Recommendation:** Implement additional security measures to prevent unauthorized access, such as IP blocking or account lockout policies.

---


#### HIGH: High Authentication Failure Rate

Authentication failure rate is 64.2%, which exceeds the 25% critical threshold.


**Evidence:**

- metric: fail_rate

- current_value: 64.2%

- threshold: 25%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): High failure rates may indicate inadequate access control measures.



**Recommendation:** Investigate sources of failed authentications. Consider implementing rate limiting and account lockout policies.

---


#### HIGH: Incomplete MFA Coverage

MFA is enabled for 0/635091 users (0.0%).


**Evidence:**

- metric: mfa_coverage

- current_value: 0.0%

- target: 100%




**Compliance Impact:**

- **NIS2** (Article 21.2(j)): Multi-factor authentication is explicitly required.



**Recommendation:** Enforce MFA for all user accounts, prioritizing privileged accounts.

---


#### MEDIUM: Admins' Last Review Date Unknown

The current period shows that admins' last review date is unknown, indicating potential non-compliance with access control policies.


**Evidence:**

- metric: admins.last_review_date

- current_value: unknown

- baseline_value: unknown

- deviation: no change




**Compliance Impact:**

- **NIS2** (Article 21.5(iii)): Unknown last review dates may not meet compliance requirements



**Recommendation:** Review and update access control policies to ensure all admins' accounts are reviewed regularly.

---


#### LOW: Admins Without MFA

The current period shows that no admins have MFA enabled, indicating potential non-compliance with access control policies.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0

- baseline_value: None

- deviation: no change




**Compliance Impact:**

- **NIS2** (Article 21.5(iv)): No MFA adoption for admins may not meet compliance requirements



**Recommendation:** Enable MFA for all admin accounts to enhance access control.

---




### Positive Observations

- Increased distinct source IPs (505,308) indicate a potentially diverse user base or increased legitimate traffic.




### Trend Analysis

**Improving:** distinct source IPs


**Degrading:** MFA adoption, authentication failure rate


**Stable:** admin accounts





## Compliance Observations
**Access-Control Compliance Section**

The organization has failed to meet certain access-control requirements.

• **Multi-Factor Authentication**: No MFA is enabled for any users ([NIS2-21.2.j]). Total users: 635,091; Enabled users: 0; Coverage percentage: 0.0% ([metrics.json]).

• **Admins with Multi-Factor Authentication**: There are no admins with MFA enabled ([metrics.json]).

• **Regular Review of Admin Access Control**: No data available in the provided evidence to determine if admin access control is regularly reviewed.

Note: The provided metrics and legal texts do not provide sufficient information to assess other aspects of access-control compliance, such as basic cyber hygiene practices or cybersecurity training.

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures