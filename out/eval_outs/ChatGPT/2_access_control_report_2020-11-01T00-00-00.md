# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2020-11-01T00:00:00 (window=90d)

**Risk Level:** CRITICAL


## Key Metrics

- Total login attempts: **9309939**
- Distinct users: **1596182**
- Distinct source IPs: **1237098**

### Authentication
- Successful logins: **2822319**
- Failed logins: **6487620**
- Failure rate: **0.6968**
- Top failing IPs:  

  
  - 10.3.205.197 (443523)
  
  - 10.3.205.196 (257018)
  
  - 10.3.205.195 (236489)
  
  - 10.3.205.194 (177160)
  
  - 10.3.205.193 (152239)
  


### Attack Surface Indicators
- Known attack IP attempts: **0**
- Unique attack IPs: **0**
- Confirmed account takeover events: **0**
- Users impacted by takeovers: **0**

## Notable Exceptions

_No exceptions reported._



## AI-Generated Insights


Across the last 90 days (ending 2020-11-01), the organization shows a severe NIS2 compliance gap in authentication hardening: MFA coverage is 0% for all users and there are zero recorded admins with MFA. In parallel, authentication failure rates are very high and have worsened versus historical baselines (fail rate 69.68% vs ~54–55% previously), indicating either widespread incorrect authentication attempts, misconfiguration, or potential brute-force/credential-stuffing activity (even though automated “attack IP attempts” and “account takeover” detections are currently 0). The combination of no MFA and elevated failure rates represents a critical risk to availability and account security under NIS2 requirements for risk management and access control.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

MFA is not enabled for any of the 1,596,182 users in scope. This is a direct control failure for NIS2-aligned access control and risk management expectations, significantly increasing the likelihood and impact of compromised credentials. The issue is persistent across historical periods (MFA coverage has remained at 0%).


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0%

- deviation: No improvement; remains at 0% across all provided historical baselines




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate technical and organizational measures for risk management and security of network and information systems, including access control protections such as MFA.



**Recommendation:** Implement MFA for all users with a phased rollout (start with privileged/admin accounts and high-risk user groups), enforce MFA at authentication gateways/IdP, and block sign-in for accounts that do not meet MFA policy after a defined deadline. Provide an auditable policy statement and evidence (MFA enrollment rate, enforcement logs).

---


#### CRITICAL: No admins recorded; privileged access not demonstrably protected with MFA

The metrics indicate 0 admins and 0 admins with MFA, with last review date marked as 'unknown'. Even if the 'admins' dataset is incomplete, the absence of recorded privileged accounts and MFA coverage evidence prevents compliance assurance and increases the risk that privileged access is not protected.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0

- baseline_value: 0

- deviation: No evidence of privileged MFA coverage; last_review_date is 'unknown' (control evidence gap)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of demonstrable access control governance and evidence for privileged accounts undermines the organization’s ability to show appropriate security measures.



**Recommendation:** Establish and maintain an authoritative inventory of privileged accounts (admins/roles) and require MFA for all privileged access. Set a measurable review cadence (e.g., quarterly) and record last review dates. Ensure the reporting pipeline correctly captures admin identities and MFA status.

---


#### HIGH: Authentication failure rate is extremely high and worsening

The authentication failure rate is 69.68% (6,487,620 total auth attempts; 2,822,319 successes). This is substantially higher than historical baselines (~54–55%). Such a high failure rate can indicate misconfiguration (e.g., broken auth flows), widespread user errors, or automated credential attacks. While detections for 'attack_ip_attempts' and 'account_takeovers' are 0, the raw failure volume remains a strong operational and security concern.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.6968 (69.68%)

- baseline_value: 0.5548 (55.48%)

- deviation: Increase of ~14.20 percentage points vs 2020-08-03 baseline




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Ineffective authentication security and/or lack of monitoring and response to abnormal authentication behavior increases risk to confidentiality and integrity of systems.



**Recommendation:** Perform an auth-failure root-cause analysis: (1) validate IdP/auth configuration and recent changes, (2) review top failing source patterns and correlate with user populations, (3) check for rate limiting/lockout policies and CAPTCHA/step-up controls, and (4) ensure SIEM alerting for abnormal failure spikes. Produce a remediation plan and track failure-rate reduction targets.

---


#### HIGH: High Authentication Failure Rate

Authentication failure rate is 69.7%, which exceeds the 25% critical threshold.


**Evidence:**

- metric: fail_rate

- current_value: 69.7%

- threshold: 25%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): High failure rates may indicate inadequate access control measures.



**Recommendation:** Investigate sources of failed authentications. Consider implementing rate limiting and account lockout policies.

---


#### HIGH: Concentrated authentication failures from internal IP range

Top source IPs for auth failures are concentrated in the 10.3.205.193–10.3.205.197 range with very large counts (e.g., 443,523; 257,018; 236,489; 177,160; 152,239). This concentration suggests either internal systems/services misconfigured to authenticate repeatedly, a proxy/NAT egress causing aggregation, or internal automated attempts. Even with 'attack_ip_attempts' reported as 0, the concentration warrants investigation.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: Top IP 10.3.205.197 = 443,523 failures; 10.3.205.196 = 257,018; 10.3.205.195 = 236,489

- baseline_value: Different top IPs previously (e.g., 23.137.225.33 = 128,728 in 2020-08-03)

- deviation: Shift in top failure sources; current failures concentrated in 10.3.205.x internal range




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Potential lack of effective detection/response for abnormal authentication behavior and insufficient control over authentication clients/services.



**Recommendation:** Identify what systems correspond to 10.3.205.193–197 (e.g., NAT gateway, reverse proxy, service accounts, integration hosts). Validate their authentication credentials and configurations. Implement/verify rate limiting and step-up authentication for suspicious patterns, and add alerts for concentrated failure sources.

---


#### HIGH: Incomplete MFA Coverage

MFA is enabled for 0/1596182 users (0.0%).


**Evidence:**

- metric: mfa_coverage

- current_value: 0.0%

- target: 100%




**Compliance Impact:**

- **NIS2** (Article 21.2(j)): Multi-factor authentication is explicitly required.



**Recommendation:** Enforce MFA for all user accounts, prioritizing privileged accounts.

---


#### MEDIUM: Distinct source IPs remain high; auth activity scale increased

The dataset shows 1,237,098 distinct source IPs and 9,309,939 total rows in the current window. Compared to 2020-08-03, total rows increased from 6,531,204 to 9,309,939 and distinct users increased from 1,529,697 to 1,596,182. This indicates increased authentication activity and expands the attack surface and operational load, especially given the lack of MFA.


**Evidence:**

- metric: frame.rows / frame.distinct_users / frame.distinct_src_ips

- current_value: rows=9,309,939; distinct_users=1,596,182; distinct_src_ips=1,237,098

- baseline_value: rows=6,531,204; distinct_users=1,529,697; distinct_src_ips=1,234,264

- deviation: Rows +42.5% vs 2020-08-03; distinct_users +4.3%; distinct_src_ips ~stable (+0.2%)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Increased authentication activity without compensating security controls (e.g., MFA) increases risk and undermines risk management effectiveness.



**Recommendation:** Scale security controls proportionally: enforce MFA, ensure robust rate limiting/lockout, and tune monitoring thresholds for auth failures. Validate that logging/telemetry is sufficient to support incident detection and forensic analysis.

---




### Positive Observations

- No account takeover indicators detected in the provided metrics (account_takeovers=0; users_with_takeover=0), suggesting current detection logic may not be flagging successful compromise events.

- No 'attack_ip_attempts' detected (attack_ip_attempts=0; attack_ip_distinct_ips=0), which may indicate either low detected automated attack classification or gaps in detection coverage that should be validated.




### Trend Analysis


**Degrading:** Authentication failure rate increased to 69.68% from 55.48% (2020-08-03 baseline), a deterioration of ~14.20 percentage points., Total authentication event volume increased (frame.rows 6,531,204 -> 9,309,939, +42.5%), increasing exposure given MFA is not enabled.


**Stable:** MFA coverage remained at 0.0% across all provided historical baselines (no progress)., Distinct source IPs are approximately stable vs 2020-08-03 (1,234,264 -> 1,237,098, +0.2%).





## Compliance Observations
### Access-Control Compliance (Article 21)

- The entity shall implement access control policies as part of human resources security and asset management measures. [NIS2 Art. 21(2)(i)]  
- The entity shall use multi-factor authentication or continuous authentication solutions, where appropriate. [NIS2 Art. 21(2)(j)]  
- MFA coverage is 0.0% (enabled_users: 0 of total_users: 1596182). [METRICS mfa]  
- Authentication failures total 6,487,620; success_total 2,822,319; fail_rate 0.6968. [METRICS auth_failures]  
- Top authentication failure IPs include 10.3.205.197 (443,523) and 10.3.205.196 (257,018). [METRICS auth_failures.top_ips]  
- If non-compliance with Article 21(2) measures is identified, corrective measures must be taken without undue delay. [NIS2 Art. 21(4)]  
- No data available in the provided evidence for admin access review status and MFA coverage for administrators. [METRICS admins]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures