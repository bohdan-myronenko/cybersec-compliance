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


Across the 90-day window ending 2020-05-05, the organization shows a severe NIS2 compliance gap in authentication hardening: MFA is effectively not deployed (0% coverage) for 1,510,016 distinct users, including 0 identified admins with MFA. At the same time, authentication activity exhibits a very high failure rate (54.69%) with 3,500,337 total auth failures, indicating either widespread incorrect authentication attempts or potential credential-stuffing/brute-force behavior. While the dataset reports 0 detected account takeovers and 0 “attack IP attempts,” the concentration of failures across specific source IPs (e.g., 23.137.225.33 with 63,681 failures) warrants immediate investigation and compensating controls to meet NIS2 requirements for risk management and access security.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

Multi-factor authentication is not enabled for any of the 1,510,016 distinct users in scope. This represents a direct failure to implement baseline strong authentication controls expected under NIS2 access security and risk management measures. The same condition is reflected historically (0% MFA coverage), indicating a persistent control deficiency rather than a transient reporting issue.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0%

- deviation: No improvement; remains at 0%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of strong authentication undermines measures for securing systems and networks and managing risks related to access control.



**Recommendation:** Implement MFA for all users (start with privileged/admin accounts and high-risk user groups), enforce MFA at authentication entry points, and require phishing-resistant MFA where feasible. Establish a measurable rollout target (e.g., 100% within 30–60 days) and report coverage weekly. Validate that the MFA telemetry pipeline is correctly populating enabled_users and coverage_pct.

---


#### CRITICAL: High authentication failure rate (54.69%) indicating potential credential attacks or misconfiguration

Authentication failures are extremely high: 3,500,337 total failures with a 54.69% fail rate (2,899,642 successes). This level of failure is consistent with credential-stuffing, brute-force attempts, or systemic authentication issues (e.g., incorrect password policies, broken SSO configuration, or clients using stale credentials). Even though the dataset reports 0 account takeovers and 0 attack IP attempts, the failure volume and concentration across top IPs require immediate triage and hardening.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5469 (54.69%)

- baseline_value: 0.5408 (54.08%)

- deviation: +0.61 percentage points (~+1.1% relative)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Persistent high authentication failure rates indicate inadequate access security controls and insufficient detection/response to authentication threats.



**Recommendation:** Immediately investigate the top failure sources and authentication flows: (1) correlate failures by username, application, and auth method; (2) check for password spray/credential stuffing patterns; (3) enable/verify rate limiting, progressive delays, and account lockout policies appropriate to availability; (4) deploy detection rules for anomalous login failure bursts; (5) review SSO/IdP configuration for misrouting or stale token usage. Produce a remediation plan within 72 hours and track reduction in fail_rate and top-IP concentration.

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


#### HIGH: Failure concentration on specific source IPs suggests targeted activity

Auth failures are not uniformly distributed; they are concentrated on a small set of IPs. The top IP 23.137.225.33 generated 63,681 failures, and multiple 10.0.181.x internal addresses also appear among the top sources. This pattern is consistent with automated attempts from known hosts (internal scanners, NAT egress, or compromised systems) and should be investigated for both external and internal threat activity.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: Top IPs: 23.137.225.33=63,681; 158.149.114.95=21,443; 10.0.181.232=14,249; 10.0.181.221=14,188; 10.0.181.231=11,737

- baseline_value: Top IPs in prior period included 158.149.114.95=12,584 and 10.0.181.227=10,967 (others varied)

- deviation: Not directly comparable per-IP, but concentration persists and top external IP activity remains material




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Concentrated authentication failures indicate insufficient monitoring and response to access attempts, increasing risk of unauthorized access.



**Recommendation:** For each top IP: (1) determine whether it is legitimate (corporate egress, monitoring, VPN, NAT) or suspicious; (2) check whether the failures map to a small set of accounts; (3) block or challenge traffic where appropriate (WAF/IdP rules, geo/IP reputation, conditional access); (4) if internal, identify the originating host(s) and validate they are not compromised or misconfigured. Add an alert for top-IP failure spikes and for new IPs exceeding a threshold.

---


#### HIGH: No admins identified and no admin MFA coverage (control visibility gap)

The dataset reports admins.count=0 and with_mfa=0 with last_review_date='unknown'. This prevents validation of privileged access protections and suggests either missing inventory/role mapping or a monitoring/telemetry gap. Under NIS2, privileged access must be managed and protected with appropriate controls.


**Evidence:**

- metric: admins.count

- current_value: 0

- baseline_value: 0

- deviation: No change; persistent lack of privileged access visibility




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Inability to demonstrate MFA and access controls for privileged accounts undermines compliance evidence for access security measures.



**Recommendation:** Fix privileged account inventory: integrate IdP/HR/asset systems to accurately populate admin roles. Then enforce MFA for all privileged accounts and document last review dates. Add a compliance control report that lists admin accounts, MFA status, and last verification timestamp.

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




### Positive Observations

- No detected account takeovers in the dataset (account_takeovers=0; users_with_takeover=0), suggesting either effective prevention/detection or that takeover attempts are not being captured in this telemetry.

- No “attack_ip_attempts” and no “attack_ip_distinct_ips” were flagged (both 0), indicating the current detection logic may not be triggering on this activity or that the activity is not classified as an attack by the current ruleset.




### Trend Analysis


**Degrading:** Authentication failure rate slightly worsened vs prior period: 54.69% (current) vs 54.08% (baseline), a +0.61 percentage point increase.


**Stable:** MFA coverage remains unchanged at 0.0% across current and baseline periods (persistent control gap)., No account takeovers detected (0 in current and baseline periods).





## Compliance Observations
### Access-Control Compliance (Cybersecurity Risk-Management)

- The entity shall implement access control policies as part of human resources security and asset management measures. [NIS2 Art. 21(2)(i)]

- The entity shall use multi-factor authentication or continuous authentication solutions, where appropriate. [NIS2 Art. 21(2)(j)]

- MFA coverage is 0.0% (enabled_users: 0 of total_users: 1510016). [METRICS mfa]

- No administrative accounts are reported (admins.count: 0; admins.with_mfa: 0). [METRICS admins]

- Authentication failures are reported: total 3500337; success_total 2899642; fail_rate 0.5469. [METRICS auth_failures]

- Top source IPs for authentication failures include 23.137.225.33 (63681) and 158.149.114.95 (21443). [METRICS auth_failures.top_ips]

- No account takeovers are reported (account_takeovers: 0; users_with_takeover: 0). [METRICS auth_failures]

- If the entity does not comply with required measures, it shall take corrective measures without undue delay. [NIS2 Art. 21(4)]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures