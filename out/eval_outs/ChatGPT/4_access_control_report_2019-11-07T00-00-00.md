# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2019-11-07T00:00:00 (window=90d)

**Risk Level:** CRITICAL


## Key Metrics

- Total login attempts: **121411**
- Distinct users: **50215**
- Distinct source IPs: **55426**

### Authentication
- Successful logins: **59871**
- Failed logins: **61540**
- Failure rate: **0.5069**
- Top failing IPs:  

  
  - 10.0.181.226 (187)
  
  - 10.0.181.227 (183)
  
  - 10.0.77.228 (108)
  
  - 10.0.77.226 (104)
  
  - 10.0.77.229 (94)
  


### Attack Surface Indicators
- Known attack IP attempts: **0**
- Unique attack IPs: **0**
- Confirmed account takeover events: **0**
- Users impacted by takeovers: **0**

## Notable Exceptions

_No exceptions reported._



## AI-Generated Insights


Across the 90-day window (ending 2019-11-07), the organization shows a severe NIS2 compliance gap in authentication hardening: MFA is not enabled for any users (0% coverage), including zero MFA coverage for admins. In parallel, authentication activity shows a high overall failure rate (fail_rate 0.5069) with repeated attempts concentrated in a small set of internal source IPs, indicating either misconfiguration, credential stuffing, or systemic authentication issues. While no account takeovers or “attack IP” detections are flagged (0), the lack of MFA and missing admin coverage represent the dominant risk to availability and confidentiality under NIS2 requirements.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

MFA coverage is effectively absent: enabled_users is 0 out of 50,215 total users, resulting in 0.0% MFA coverage. This indicates a systemic failure to implement multi-factor authentication for access to information systems, materially increasing the likelihood and impact of credential compromise and unauthorized access.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0% (2021-01-30 and 2020-11-01)

- deviation: No improvement; remains at 0.0% across historical periods




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate access control measures (including MFA where applicable) undermines risk management for network and information systems.



**Recommendation:** Implement MFA for all users as a priority control: (1) enable MFA for all accounts in phases (admins first), (2) enforce MFA at authentication policy level (not per-app exceptions), (3) remove/avoid any MFA disablement paths, and (4) validate via periodic audits that enabled_users equals total_users.

---


#### HIGH: High Authentication Failure Rate

Authentication failure rate is 50.7%, which exceeds the 25% critical threshold.


**Evidence:**

- metric: fail_rate

- current_value: 50.7%

- threshold: 25%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): High failure rates may indicate inadequate access control measures.



**Recommendation:** Investigate sources of failed authentications. Consider implementing rate limiting and account lockout policies.

---


#### CRITICAL: No MFA for administrators (admins count=0 / with_mfa=0 indicates missing governance visibility)

The metrics show admins.count=0 and admins.with_mfa=0 with last_review_date='unknown'. This combination suggests either (a) administrators are not being identified/ingested into the reporting dataset, or (b) there are truly no admin accounts tracked—both are compliance and operational governance concerns. Regardless, the absence of MFA for privileged access paths is a high-risk condition.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0

- baseline_value: 0 (2021-01-30 and 2020-11-01)

- deviation: No improvement; privileged access governance and MFA enforcement cannot be demonstrated




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Inadequate privileged access controls and lack of demonstrable governance/auditability increases risk of unauthorized administrative actions.



**Recommendation:** Fix privileged access governance and reporting: (1) ensure admin/privileged role accounts are correctly classified in telemetry, (2) require MFA for all privileged roles immediately, (3) set and record last_review_date for admin access reviews, and (4) produce evidence artifacts (policy + audit logs) showing MFA enforcement for admin accounts.

---


#### HIGH: Incomplete MFA Coverage

MFA is enabled for 0/50215 users (0.0%).


**Evidence:**

- metric: mfa_coverage

- current_value: 0.0%

- target: 100%




**Compliance Impact:**

- **NIS2** (Article 21.2(j)): Multi-factor authentication is explicitly required.



**Recommendation:** Enforce MFA for all user accounts, prioritizing privileged accounts.

---


#### HIGH: High authentication failure rate (~50.7%) indicates systemic auth issues or attack attempts

Authentication failures are substantial: total auth failures=61,540 with success_total=59,871, producing fail_rate=0.5069 (about half of attempts failing). Even though account takeover detections are 0 and attack_ip_attempts are 0, the failure rate is high enough to warrant investigation for misconfiguration (e.g., incorrect credentials, broken SSO/MFA flows) or credential-stuffing/brute-force attempts that are not being classified as 'attack IPs' by the current detection logic.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5069

- baseline_value: 0.6421 (2021-01-30), 0.6968 (2020-11-01)

- deviation: Improved vs baseline by ~13.5 percentage points (0.6421→0.5069) and ~19.6 percentage points (0.6968→0.5069)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Persistent authentication failures can indicate weaknesses in access control and incident risk; controls should include monitoring, detection, and mitigation of unauthorized access attempts.



**Recommendation:** Investigate and remediate root cause: (1) correlate failures with authentication method (SSO/local), user population, and time-of-day, (2) review lockout/rate-limit policies and ensure they are effective, (3) tune detection so repeated failures from internal IPs are classified and investigated, and (4) validate whether failures are due to legitimate user issues (e.g., password resets) vs automated attempts.

---


#### MEDIUM: Concentration of auth failures in a small set of internal source IPs

Top source IPs generating failures are concentrated in internal ranges: 10.0.181.226 (187), 10.0.181.227 (183), 10.0.77.228 (108), 10.0.77.226 (104), 10.0.77.229 (94). This pattern suggests either a small number of hosts/services repeatedly attempting authentication (possibly due to misconfiguration) or internal automation/compromised systems generating repeated failed logins.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: Top IP counts: 187, 183, 108, 104, 94 (total failures=61,540)

- baseline_value: Different top IPs in prior periods; no direct comparable concentration metric provided

- deviation: Not directly comparable, but concentration indicates targeted investigation area




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Anomalous authentication behavior should be detected and addressed as part of access control and security monitoring.



**Recommendation:** Perform host-level triage for the top IPs: (1) identify owning systems/services for 10.0.181.226/227 and 10.0.77.226/228/229, (2) check for recent changes (credential rotation, SSO config, automation scripts), (3) verify whether these IPs correspond to legitimate integration accounts, and (4) apply rate limiting/lockout and block/contain if compromise is suspected.

---


#### LOW: No detected account takeovers or attack IP attempts (0) despite high failure volume

The dataset reports account_takeovers=0 and users_with_takeover=0, and attack_ip_attempts=0 with attack_ip_distinct_ips=0. Given the high fail_rate (0.5069), this may indicate either (a) failures are largely non-malicious (e.g., user errors), or (b) detection logic is insufficiently sensitive to classify attacks/ATO patterns.


**Evidence:**

- metric: auth_failures.account_takeovers

- current_value: 0

- baseline_value: 0 (2021-01-30 and 2020-11-01)

- deviation: Stable at 0; classification coverage may be incomplete




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Effective monitoring and incident detection are required to ensure access control measures can respond to threats.



**Recommendation:** Validate detection coverage: (1) review the logic used to flag account takeovers and attack IP attempts, (2) test with known-good scenarios (e.g., simulated credential stuffing in a safe environment) to confirm alerts trigger, and (3) ensure alerts are generated for anomalous failure patterns even when ATO heuristics are not met.

---




### Positive Observations

- Authentication failure rate has improved versus prior periods: fail_rate 0.5069 vs 0.6421 (2021-01-30) and 0.6968 (2020-11-01).

- No account takeovers detected in the current and historical periods (account_takeovers=0), suggesting either limited successful compromise or detection/classification gaps.




### Trend Analysis

**Improving:** auth_failures.fail_rate decreased to 0.5069 from 0.6421 (2021-01-30) and 0.6968 (2020-11-01).


**Degrading:** No improvement in MFA posture: mfa.coverage_pct remains 0.0% (enabled_users=0) across all compared periods.


**Stable:** account_takeovers and users_with_takeover remain 0 across current and historical periods.





## Compliance Observations
## Access-Control Compliance (Cybersecurity Risk-Management)

- The entity must implement appropriate, proportionate measures to manage risks to network and information systems security. [NIS2 Art. 21(1)]  
- Access control policies must be included within human resources security and asset management measures. [NIS2 Art. 21(2)(i)]  
- Multi-factor authentication (MFA) or continuous authentication solutions must be used where appropriate. [NIS2 Art. 21(2)(j)]  
- MFA coverage is 0.0% (enabled_users: 0 of total_users: 50215). [METRICS mfa]  
- No administrators are recorded (admins.count: 0) and no administrators have MFA (admins.with_mfa: 0). [METRICS admins]  
- Authentication failures total 61540; success_total 59871; fail_rate 0.5069. [METRICS auth_failures]  
- Top authentication failure source IPs include 10.0.181.226 (187) and 10.0.181.227 (183). [METRICS auth_failures.top_ips]  
- If non-compliance with required measures is identified, corrective measures must be taken without undue delay. [NIS2 Art. 21(4)]  
- No data available in the provided evidence for incident handling, business continuity, cryptography use, or access-control effectiveness testing. [NIS2 Art. 21(2)(b),(c),(h),(f)]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures