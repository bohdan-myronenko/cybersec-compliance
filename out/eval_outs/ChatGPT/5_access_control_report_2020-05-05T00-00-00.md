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


Across the 90-day window ending 2020-05-05, the organization shows a severe NIS2 compliance gap in authentication hardening: MFA coverage is 0% for 1,510,016 users and there are 0 recorded admins (and 0 with MFA), indicating either missing telemetry or a systemic lack of required controls. Authentication failures are extremely high (fail rate 54.69% with 3,500,337 total failures vs 2,899,642 successes), and the top offending source IPs include both public and private ranges (e.g., 23.137.225.33 with 63,681 attempts). While no account takeovers or “attack IP attempts” are flagged (0), the combination of zero MFA and elevated failure rates represents a critical risk of credential compromise and non-compliance with NIS2 requirements for risk management and access control.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

Multi-factor authentication is not enabled for any of the 1,510,016 distinct users in scope. This is a direct control failure for access security and significantly increases the likelihood and impact of credential theft, replay, and brute-force attempts. The same condition existed in prior periods (baseline also shows 0% coverage), indicating the issue is persistent rather than transient.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0%

- deviation: No improvement; remains at 0%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate measures to secure network and information systems (including access controls such as MFA) increases the risk of incidents and undermines required risk-management practices.



**Recommendation:** Implement MFA for all users as a mandatory policy (start with privileged/admin accounts and then all users). Enforce via identity provider conditional access (or equivalent), require phishing-resistant MFA where feasible, and block sign-in without MFA. Validate coverage by producing a daily report of enabled_users vs total_users and require remediation SLAs for any exceptions.

---


#### CRITICAL: Very high authentication failure rate (possible brute-force/credential stuffing)

Authentication failures are high: 3,500,337 total failures with a fail rate of 54.69% (vs 2,899,642 successes). This indicates a large volume of unsuccessful authentication attempts. Although the dataset reports 0 flagged “attack_ip_attempts” and 0 account takeovers, the failure rate itself is consistent with automated attempts and increases the probability of eventual compromise, especially in the absence of MFA.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5469 (54.69%)

- baseline_value: 0.5408 (54.08%)

- deviation: +0.61 percentage points (~+1.1% relative)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Inadequate access security and insufficient detection/response to repeated authentication failures can lead to security incidents, conflicting with NIS2 expectations for risk reduction and incident prevention.



**Recommendation:** Enable and tune protective controls: (1) rate limiting and progressive backoff on authentication endpoints, (2) account lockout or step-up verification after repeated failures, (3) bot/credential-stuffing detection, and (4) IP reputation and geo-velocity checks. Create an alert for sustained high fail rates per tenant/application and for top source IPs. Perform a targeted investigation of the top IPs (e.g., 23.137.225.33 with 63,681 failures; 158.149.114.95 with 21,443) to determine whether they are legitimate services, misconfigured clients, or hostile traffic.

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


#### HIGH: Top source IP concentration suggests automated attempts

The highest-volume authentication failure sources are concentrated in a small set of IPs, including both public and internal/private ranges (e.g., 23.137.225.33 and 158.149.114.95, plus 10.0.181.232/221/231). This pattern is typical of automated login attempts (credential stuffing/brute force) or misconfigured integrations. The presence of internal-range IPs may also indicate internal systems generating repeated failures (e.g., stale credentials in services).


**Evidence:**

- metric: auth_failures.top_ips

- current_value: Top IP counts: 23.137.225.33=63,681; 158.149.114.95=21,443; 10.0.181.232=14,249; 10.0.181.221=14,188; 10.0.181.231=11,737

- baseline_value: Baseline top IPs included 158.149.114.95=12,584 and 10.0.181.227=10,967 (others varied)

- deviation: Public IP 23.137.225.33 appears as a top offender in current period; 158.149.114.95 increased from 12,584 to 21,443 (~+70%)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of effective access monitoring and response to suspicious authentication patterns increases the likelihood of incidents and indicates insufficient risk management.



**Recommendation:** Classify the top source IPs: (a) identify whether they belong to known NAT gateways, corporate egress, monitoring systems, or partner services; (b) if unknown, block or challenge them at the edge (WAF/IdP) and add them to an allow/block list with review. For internal-range IPs (10.0.181.*), audit service accounts and scheduled jobs for stale credentials and rotate secrets. Add logging enrichment (user agent, application, endpoint, and correlation IDs) to distinguish legitimate automation from hostile traffic.

---


#### HIGH: Privileged access telemetry missing (admins count = 0, last_review_date unknown)

The metrics report 0 admins and 0 admins with MFA, with last_review_date set to 'unknown'. This is either a data quality/collection issue or indicates that privileged accounts are not being tracked and protected. Under NIS2, privileged access should be explicitly managed, reviewed, and protected with strong authentication.


**Evidence:**

- metric: admins.count / admins.last_review_date

- current_value: admins.count=0; with_mfa=0; last_review_date='unknown'

- baseline_value: Same in prior periods (admins.count=0; with_mfa=0; last_review_date='unknown')

- deviation: No change; persistent absence of privileged access visibility




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Insufficient visibility and management of privileged access undermines access control measures required for risk reduction.



**Recommendation:** Fix privileged account inventory and reporting: ensure the identity system exports admin/role membership to the compliance metrics pipeline. Establish a recurring privileged access review process (e.g., monthly) and record last_review_date. Require MFA for all privileged roles and verify via role-based reporting (not only user-level MFA coverage).

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

- No account takeovers were detected in the dataset (account_takeovers=0; users_with_takeover=0), suggesting either effective prevention/detection for takeover events or limited visibility into takeover signals.

- No 'attack_ip_attempts' or 'attack_ip_distinct_ips' were flagged (both 0), which may indicate that the current failure activity is not being classified as a specific attack type by the detection logic (or that detection thresholds are high).




### Trend Analysis


**Degrading:** Authentication failure rate slightly worsened vs baseline: 54.69% (current) vs 54.08% (baseline), +0.61 percentage points., Public IP 158.149.114.95 increased substantially in top-failure volume: 21,443 (current) vs 12,584 (baseline), ~+70%.


**Stable:** MFA coverage remains unchanged at 0.0% across periods (persistent control gap)., No account takeovers detected (0 in current and baseline).





## Compliance Observations
### Access-control compliance (Article 21)

- The entity shall implement access control policies as part of human resources security and asset management measures. [NIS2 Art. 21(2)(i)]

- The entity shall use multi-factor authentication or continuous authentication solutions, where appropriate. [NIS2 Art. 21(2)(j)]

- MFA coverage is 0.0% (enabled_users: 0 of total_users: 1510016). [METRICS mfa]

- No MFA-enabled administrators are reported (admins count: 0; with_mfa: 0). [METRICS admins]

- Authentication failures total 3500337 with success_total 2899642 (fail_rate 0.5469). [METRICS auth_failures]

- Top authentication failure IPs include 23.137.225.33 (63681) and 158.149.114.95 (21443). [METRICS auth_failures.top_ips]

- No account takeovers are reported (account_takeovers: 0; users_with_takeover: 0). [METRICS auth_failures]

- No data available in the provided evidence for access-control effectiveness assessment procedures. [NIS2 Art. 21(2)(f)]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures