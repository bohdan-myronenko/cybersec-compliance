# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2020-05-05T00:00:00 (window=90d)

**Risk Level:** CRITICAL


## Key Metrics

- Total login attempts: **6399979**
- Distinct users: **1510016**
- Distinct source IPs: **1251718**

### Authentication
- Successful logins: **2899642**
- Failed logins: **3500337**
- Failure rate: **0.5469**
- Top failing IPs:  

  
  - 23.137.225.33 (63681)
  
  - 158.149.114.95 (21443)
  
  - 10.0.181.232 (14249)
  
  - 10.0.181.221 (14188)
  
  - 10.0.181.231 (11737)
  


### Attack Surface Indicators
- Known attack IP attempts: **0**
- Unique attack IPs: **0**
- Confirmed account takeover events: **0**
- Users impacted by takeovers: **0**

## Notable Exceptions

_No exceptions reported._



## AI-Generated Insights


Across the 90-day window ending 2020-05-05, the organization shows a severe NIS2-aligned control gap: MFA is not enabled for any users (0% coverage), including administrators (0 admins with MFA). Authentication activity also exhibits a persistently high failure rate (~54.7%), with the largest concentration of failures coming from a small set of source IPs (e.g., 23.137.225.33 with 63,681 attempts). While no account takeovers or explicit “attack IP attempts” were detected by the metric set, the combination of zero MFA coverage and elevated authentication failures represents a critical risk of unauthorized access and non-compliance with NIS2 requirements for risk management and access control measures.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

Multi-factor authentication is not enabled for any of the 1,510,016 distinct users in scope. This indicates a complete absence of MFA as a compensating control for password compromise, directly increasing the likelihood and impact of unauthorized access. For NIS2, this is a fundamental access-control measure that should be implemented based on risk, especially for remote access and privileged actions.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0%

- deviation: No improvement; remains at 0% vs baseline periods (e.g., 0.0% on 2020-02-05 and 2019-11-07).




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate technical and organizational measures for risk management and security of network and information systems, including access controls such as MFA, increases exposure to unauthorized access.



**Recommendation:** Implement MFA for all users with a risk-based rollout (start with privileged/admin accounts and remote-access users). Enforce MFA at authentication layer (IdP) and block sign-in for accounts that do not meet MFA policy after a defined deadline. Provide an exception process with time-bound approvals and compensating controls (e.g., device-bound access, step-up authentication).

---


#### CRITICAL: No administrators identified and no MFA for admin population

The metrics report 0 administrators and 0 admins with MFA, with last_review_date marked as 'unknown'. This prevents assurance that privileged accounts are governed and protected. Even if the admin count is a data-mapping issue, the absence of verified privileged-account coverage is a compliance and operational control failure.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0

- baseline_value: 0

- deviation: No change; additionally, last_review_date is 'unknown' indicating missing governance evidence.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of demonstrable privileged access governance and protective controls (e.g., MFA for admins) undermines the organization’s ability to manage risks to information systems.



**Recommendation:** Fix privileged-account inventory and governance: (1) validate admin role mapping in the identity system, (2) produce an authoritative list of privileged accounts, (3) require MFA for all privileged accounts immediately, and (4) set and record a last-review date for privileged access (e.g., quarterly).

---


#### HIGH: High Authentication Failure Rate

Authentication failure rate is 54.7%, which exceeds the 25% critical threshold.


**Evidence:**

- metric: fail_rate

- current_value: 54.7%

- threshold: 25%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): High failure rates may indicate inadequate access control measures.



**Recommendation:** Investigate sources of failed authentications. Consider implementing rate limiting and account lockout policies.

---


#### HIGH: High authentication failure rate (~54.7%) persists vs baseline

Authentication failures are high and remain broadly stable compared to baseline periods. In the current window, total auth failures are 3,500,337 with a fail rate of 0.5469 (54.69%). Baseline on 2020-02-05 shows fail rate 0.5408 (54.08%), indicating no meaningful reduction. Elevated failures can indicate credential stuffing, misconfiguration, or user friction; combined with zero MFA, it increases the probability of successful compromise.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5469 (54.69%)

- baseline_value: 0.5408 (54.08%)

- deviation: Increase of ~0.61 percentage points (~+1.1% relative).




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Persistent high authentication failure rates indicate ongoing risk exposure and insufficient detection/mitigation of unauthorized access attempts.



**Recommendation:** Investigate root causes of failures: (1) correlate failures with user populations and geographies, (2) check for brute-force/credential-stuffing patterns, (3) ensure rate limiting and account lockout/step-up controls are enabled, and (4) tune detection rules and alerting for anomalous login failure spikes. Prioritize remediation before MFA rollout completion to reduce attack success probability.

---


#### HIGH: Concentrated authentication failures from a small set of IPs

Top source IPs account for large volumes of authentication failures, suggesting automated attempts or a small number of problematic clients. Current top IPs include 23.137.225.33 (63,681 failures), 158.149.114.95 (21,443), and multiple 10.0.181.x internal IPs (e.g., 10.0.181.232 with 14,249). This concentration warrants investigation for both external threat activity and internal misconfiguration (e.g., service accounts, integration clients, or NAT/proxy behavior).


**Evidence:**

- metric: auth_failures.top_ips

- current_value: 23.137.225.33=63,681; 158.149.114.95=21,443; 10.0.181.232=14,249; 10.0.181.221=14,188; 10.0.181.231=11,737

- baseline_value: Top IPs differed on 2020-02-05 (e.g., 158.149.114.95=12,584; 10.0.181.227=10,967; 10.0.181.226=10,254)

- deviation: Concentration persists; specific top IPs changed, indicating evolving sources but continued high-volume failure activity.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Concentrated failure sources indicate potential ongoing unauthorized access attempts or insecure authentication behavior that should be mitigated through monitoring and access control measures.



**Recommendation:** For each top IP: (1) determine whether it is a known NAT/proxy, integration host, or external actor, (2) review associated accounts and authentication flows, (3) apply targeted rate limiting/blocks or step-up authentication for suspicious sources, and (4) ensure service accounts use strong authentication (preferably certificate-based or managed identities) rather than shared credentials.

---


#### HIGH: Incomplete MFA Coverage

MFA is enabled for 0/1510016 users (0.0%).


**Evidence:**

- metric: mfa_coverage

- current_value: 0.0%

- target: 100%




**Compliance Impact:**

- **NIS2** (Article 21.2(j)): Multi-factor authentication is explicitly required.



**Recommendation:** Enforce MFA for all user accounts, prioritizing privileged accounts.

---


#### MEDIUM: No detected account takeovers, but detection may be incomplete

The dataset reports account_takeovers=0 and users_with_takeover=0, and attack_ip_attempts=0. Given the high failure rate and zero MFA coverage, the absence of detected takeovers may reflect limitations in the detection logic/telemetry rather than true absence of compromise attempts.


**Evidence:**

- metric: auth_failures.account_takeovers

- current_value: 0

- baseline_value: 0

- deviation: Stable at 0 across periods; however, this may be a detection coverage gap given other risk indicators.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Insufficient detection/verification of security incidents can undermine risk management effectiveness required by NIS2.



**Recommendation:** Validate and enhance detection: (1) confirm how account takeover is defined and whether it covers MFA-bypass, session hijacking, and password spraying, (2) ensure logs include user-agent, device, geo, and session outcomes, and (3) run tabletop exercises and test detection with controlled simulations (where permitted).

---




### Positive Observations

- No account takeovers detected in the provided metrics (account_takeovers=0; users_with_takeover=0), suggesting either low observed compromise or limited detection—worth validating but not currently indicating confirmed takeovers.

- Authentication failure rate is relatively stable vs baseline (54.69% current vs 54.08% on 2020-02-05), indicating no sudden spike during the analyzed window.




### Trend Analysis


**Degrading:** MFA coverage remains at 0.0% (no improvement across periods), representing an ongoing degradation of security posture relative to best practice.


**Stable:** Auth failure rate is stable around the mid-50% range (0.5469 current vs 0.5408 baseline)., Account takeover indicators remain at 0 across periods (account_takeovers=0).





## Compliance Observations
### Access-Control Compliance (Cybersecurity Risk-Management)

- The entity shall implement access control policies as part of cybersecurity risk-management measures. [NIS2 Art. 21(2)(i)]  
- The entity shall use multi-factor authentication or continuous authentication solutions, where appropriate. [NIS2 Art. 21(2)(j)]  
- MFA coverage is 0.0% (enabled_users: 0 of total_users: 1510016). [METRICS mfa]  
- Administrators count is 0; MFA for administrators is 0. [METRICS admins]  
- Authentication failures total 3500337 with success_total 2899642 (fail_rate 0.5469). [METRICS auth_failures]  
- Top IPs with authentication failures include 23.137.225.33 (63681) and 158.149.114.95 (21443). [METRICS auth_failures.top_ips]  
- If non-compliance with required measures is identified, corrective measures shall be taken without undue delay. [NIS2 Art. 21(4)]  

**No data available in the provided evidence** for: access-control policy existence, administrator review dates, or whether MFA is “appropriate” for the entity. [METRICS admins; NIS2 Art. 21(2)(j)]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures