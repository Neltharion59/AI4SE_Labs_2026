# Software Requirements Specification

## Document Information

This document was generated from the supplied source corpus by the requirements-refinement network.
- **Consolidator model:** gpt\-5\-mini
- **Extractor model:** gpt\-4o\-mini
- **Review revisions:** 10
- **Reviewer model:** gpt\-6\-luna

> **Validation warning:** Best\-effort output\: the review limit was reached with 4 review issue\(s\) and deterministic validation was evaluated on the final draft and found 7 unresolved issue\(s\) after 10 permitted revision\(s\)\.

## Purpose and Scope

The specification consolidates software capabilities, quality attributes, constraints, documentation needs, and dependencies found in the input documents. Each item retains traceability to its source documents.

## Priority Scale

- **High** — Essential for the intended system outcome or a mandatory constraint; omission would make the solution unacceptable.
- **Medium** — Important and expected, but the solution can still provide core value if delivery is deferred.
- **Low** — Optional enhancement whose deferral has limited effect on core operation.

## Glossary and Terminology

Requirement names and descriptions use the terminology selected during consolidation; the same concept should be named consistently throughout this document.

## Requirements

### Functional Requirements

#### REQ-FUN-001 — Administrative Report Templates

**Priority:** High  
**Sources:** `email_report_features.eml`, `survey_results_2009.txt`  
**Priority rationale:** Merged candidates include ITEM\-00016 \(High\) and ITEM\-00032 \(Medium\); priority set to High because at least one source explicitly marked this as High and administrators' ability to provide templates is a central operational requirement \(email\_report\_features\.eml; survey\_results\_2009\.txt\)\.

System administrators shall be able to create report templates that are made available to staff\. Administrator\-created templates shall be runnable by staff as provided\. Templates may be designated as editable; whether a template is editable and which users or roles may modify it shall be controlled by the system's report\-permissions controls\.

**Verification hint:** Create a template as an administrator, make it available to staff, verify staff can run the template unchanged, and verify that templates designated as editable can be modified only by users/roles granted modification rights via the report\-permissions controls\.

#### REQ-FUN-002 — Anonymized Demographic Statistics

**Priority:** High  
**Sources:** `survey_results_2009.txt`  
**Priority rationale:** Explicitly marked High in the source material \(survey\_results\_2009\.txt\) with privacy considerations noted\.

The system shall provide demographic statistics \(for example, transactions by geographical regions and age ranges\) and shall present such demographic data in an anonymized form to protect patron privacy\.

**Verification hint:** Generate demographic reports and verify identifiable patron data is not exposed and that aggregates match underlying anonymized data\.

#### REQ-FUN-003 — Background Processing for Inactive\-Patrons Report

**Priority:** High  
**Sources:** `conversations/conv_pines024_inactive_patrons.eml`  
**Priority rationale:** Explicitly marked High in the source material \(conversations/conv\_pines024\_inactive\_patrons\.eml\) due to performance concerns with large patron databases\.

The generation of the inactive\-patrons report shall be processed as a background job to avoid blocking interactive sessions and to improve overall system responsiveness for large patron databases\.

**Verification hint:** Request the inactive\-patrons report for a large dataset, confirm the request is queued/executed as a background job, and verify the interactive UI remains responsive while the job runs to completion\.

#### REQ-FUN-004 — Configurable Aggregation Levels for Inactive Patrons Reporting

**Priority:** High  
**Sources:** `conversations/conv_pines024_inactive_patrons.eml`, `early_draft_srs_galecia.txt`  
**Priority rationale:** Explicitly marked High in the source material \(conversations/conv\_pines024\_inactive\_patrons\.eml and early\_draft\_srs\_galecia\.txt\)\.

The system shall allow the inactive\-patrons report to be configured to operate at different aggregation levels \(for example\: system\-wide, home library, county\) as supported by the reporting configuration\.

**Verification hint:** Run the inactive\-patrons report at different aggregation levels and verify counts and membership correspond to the selected configuration\.

#### REQ-FUN-005 — Deletion Tracking and Audit Logging

**Priority:** High  
**Sources:** `conversations/conv_pines022_deletions.eml`  
**Priority rationale:** Explicitly marked High in the source material \(conversations/conv\_pines022\_deletions\.eml\)\.

The system shall count and track record deletions per location and per system, and shall record for each deletion the record type, timestamp, the user who performed the deletion, and the user location for auditing purposes\.

**Verification hint:** Delete a test record and verify audit log entry contains record type, timestamp, user identity, and user location; verify aggregated deletion counts per location\.

#### REQ-FUN-006 — Error Reporting and Query\-Level Feedback

**Priority:** Medium  
**Sources:** `meeting_minutes/meeting_2009-07-20_minutes.txt`  
**Priority rationale:** Marked Medium in the source material \(meeting\_minutes/meeting\_2009\-07\-20\_minutes\.txt\) to support operational troubleshooting\.

The system shall provide high\-level error reporting for failed reports and shall provide detailed, query\-specific feedback accessible to administrators to facilitate troubleshooting\.

**Verification hint:** Cause a report failure and verify that the system provides a readable high\-level error and a more detailed diagnostic view for administrators\.

#### REQ-FUN-007 — Expand Report Types to Cover Identified Gaps

**Priority:** High  
**Sources:** `evergreen_reference_2009.txt`  
**Priority rationale:** Explicitly marked High in the source material \(evergreen\_reference\_2009\.txt\) which lists missing report types requiring implementation\.

The system shall implement additional report types to address missing reporting capabilities explicitly named in the cited source \(evergreen\_reference\_2009\.txt\)\. Specifically this requirement covers\: \(a\) circulation counts broken down by patron demographics \(for example\: age ranges, ZIP code, county of residence\) and \(b\) counts and reports broken down by item status \(for example\: missing, damaged, in\-transit\)\.

**Verification hint:** Compare the implemented report catalog against the explicit list of report types named in evergreen\_reference\_2009\.txt and verify that the implemented reports provide the specified demographic breakdowns and item\-status reports enumerated in this requirement\.

#### REQ-FUN-008 — Fine\-Grained Report Permissions

**Priority:** High  
**Sources:** `email_report_features.eml`, `survey_results_2009.txt`  
**Priority rationale:** Merged candidates include ITEM\-00017 \(High\) and ITEM\-00033 \(High\); priority set to High as multiple sources explicitly required fine\-grained permissions \(email\_report\_features\.eml; survey\_results\_2009\.txt\)\.

The system shall implement fine\-grained permissions that limit which users may create and clone reports\.

**Verification hint:** Attempt to create and clone reports with users in roles that should/shouldn't have permissions and verify enforced access control\.

#### REQ-FUN-009 — Flagging Inactive Patrons With Outstanding Fines

**Priority:** Medium  
**Sources:** `conversations/conv_pines024_inactive_patrons.eml`  
**Priority rationale:** Marked Medium in the source material \(conversations/conv\_pines024\_inactive\_patrons\.eml\)\.

The system shall identify and allow reporting on inactive patrons who have outstanding fines, so they can be handled separately from other inactive patrons\.

**Verification hint:** Generate an inactive\-patrons report with a filter for outstanding fines and verify flagged patrons have non\-zero fine balances\.

#### REQ-FUN-010 — Inactive Patrons Report

**Priority:** High  
**Sources:** `conversations/conv_pines024_inactive_patrons.eml`, `early_draft_srs_galecia.txt`  
**Priority rationale:** Explicitly marked High in the source material \(conversations/conv\_pines024\_inactive\_patrons\.eml and early\_draft\_srs\_galecia\.txt\)\.

The system shall generate a list of patrons who have had no circulation or electronic activity within a configurable period \(X days, where X is configurable\)\.

**Verification hint:** Set X to a known interval, generate the report, and confirm listed patrons have no recorded activity within X days\.

#### REQ-FUN-011 — Include Mailing Addresses in Outreach Reports

**Priority:** High  
**Sources:** `conversations/conv_pines024_inactive_patrons.eml`  
**Priority rationale:** Explicitly marked High in the source material \(conversations/conv\_pines024\_inactive\_patrons\.eml\)\.

The system shall include current mailing addresses in the inactive\-patrons \(outreach\) report for patrons who have current mailing addresses recorded\.

**Verification hint:** Generate an outreach report and verify mailing address fields are present and populated for patrons with valid address data\.

#### REQ-FUN-012 — Item Record Purging and Batch Decommissioning

**Priority:** High  
**Sources:** `conversations/conv_pines021_item_purging.eml`  
**Priority rationale:** Explicitly marked High in the source material \(conversations/conv\_pines021\_item\_purging\.eml\)\.

The system shall provide utilities and reports to identify item records for purging based on customizable criteria \(including last\-copy detection\), and shall support batch status changes and batch deletion workflows\.

**Verification hint:** Run identification reports with filter criteria, perform a staged batch status conversion, and confirm deletions follow the configured batch deletion workflow\.

#### REQ-FUN-013 — Item Transfer Utility

**Priority:** High  
**Sources:** `conversations/conv_pines018_item_transfer.eml`  
**Priority rationale:** Explicitly marked High in the source material \(conversations/conv\_pines018\_item\_transfer\.eml\)\.

The system shall provide a utility to transfer batches of items between branches that supports querying for candidate items, saving queries, manual selection of titles or items, editing item/holding records prior to transfer, generating pull lists for transfers, and reverting transfers after a set period or based on criteria\.

**Verification hint:** Create a candidate query, save it, select items, perform a batch transfer, verify pull list, then perform revert action after the specified conditions\.

#### REQ-FUN-014 — Material Volume Reporting

**Priority:** High  
**Sources:** `conversations/conv_pines014_material_volume.eml`  
**Priority rationale:** Explicitly marked High in the source material \(conversations/conv\_pines014\_material\_volume\.eml\)\.

The system shall provide reports of the volume of material in a given library at a specified point in time, including counts of new acquisitions, items currently checked in \(on shelf\), and items currently checked out \(in circulation\)\.

**Verification hint:** Generate the report for a known date and verify returned counts match inventory and circulation logs for that date\.

#### REQ-FUN-015 — Missing, Damaged, and Long In\-Transit Items Reporting

**Priority:** High  
**Sources:** `conversations/conv_pines019_020_missing_intransit.eml`  
**Priority rationale:** Explicitly marked High in the source material \(conversations/conv\_pines019\_020\_missing\_intransit\.eml\)\.

The system shall provide reports of missing and damaged items by branch and shall generate lists of items that have been in\-transit for more than a configurable number of days\.

**Verification hint:** Configure threshold X, run in\-transit report, and verify items listed have transit times exceeding X days and that missing/damaged flags are correctly reported per branch\.

#### REQ-FUN-016 — Patron Characteristics Filtering and Grouping

**Priority:** High  
**Sources:** `conversations/conv_pines023_patron_characteristics.eml`  
**Priority rationale:** Explicitly marked High in the source material \(conversations/conv\_pines023\_patron\_characteristics\.eml\)\.

The system shall allow queries and reports to be limited or grouped by patron characteristics including age range, ZIP code, county of residence, home branch, patron type, and preferred language\.

**Verification hint:** Run reports grouped and filtered by each characteristic and verify results match underlying patron attribute values\.

#### REQ-FUN-017 — Report Export Formats \(Inactive Patrons\)

**Priority:** Medium  
**Sources:** `conversations/conv_pines024_inactive_patrons.eml`  
**Priority rationale:** Marked Medium in the source material \(conversations/conv\_pines024\_inactive\_patrons\.eml\)\.

The system shall allow the inactive\-patrons report to be exported in common data formats such as CSV for use in outreach and external processing\.

**Verification hint:** Export the inactive\-patrons report to CSV and verify file contents and encoding match the report data\.

#### REQ-FUN-018 — Report Scheduling with Acknowledged Limitations

**Priority:** Medium  
**Sources:** `evergreen_reference_2009.txt`  
**Priority rationale:** Marked Medium in the source material \(evergreen\_reference\_2009\.txt\) which documents current scheduling features and their limitations\.

The system shall support scheduling of reports to run at regular intervals \(configurable scheduling frequencies supported by the product\)\. Known scheduling limitations documented in the cited source shall apply; for example, the product does not provide hourly scheduling and does not support automatic email delivery of scheduled reports as described in evergreen\_reference\_2009\.txt\. Where scheduling capabilities are limited, those limitations shall be documented in the reporting\-capabilities overview \(see draft\-req\-019\) and the requirements baseline\.

**Verification hint:** Schedule a report type supported by the system at a supported interval \(e\.g\., daily or coarser\) and verify scheduled execution; verify that unsupported frequencies \(for example hourly\) and unsupported delivery mechanisms \(for example email delivery of scheduled reports\) are either unavailable or explicitly documented as unsupported\. Separately, consult the reporting\-capabilities overview \(draft\-req\-019\) for the documented high\-level statement of supported scheduling capabilities and any known limitations\.

#### REQ-FUN-019 — Report Writer and Query Builder Interface Features

**Priority:** High  
**Sources:** `email_report_features.eml`, `evergreen_reference_2009.txt`  
**Priority rationale:** Merged candidates include ITEM\-00015 \(High\) and ITEM\-00020 \(High\); priority set to High based on explicit priority in source materials \(email\_report\_features\.eml; evergreen\_reference\_2009\.txt\)\.

The system shall provide a web\-based report writer and user\-friendly query interface that enables staff to create custom reports and queries across all record types with features such as drag\-and\-drop field selection, basic filtering and sorting, multiple output formats, and the ability to save and reuse report definitions\.

**Verification hint:** Use the report writer/query interface to create a new report employing drag\-and\-drop, filters, and sorting; save it and produce output in at least two supported formats; create queries across multiple record types and verify results\.

#### REQ-FUN-020 — Role\-Based Access Control for Reporting

**Priority:** High  
**Sources:** `email_staff_login.eml`, `interview_sysadmin_2009-05-10.txt`  
**Priority rationale:** Merged candidates include ITEM\-00018 \(High\) and ITEM\-00025 \(High\); priority set to High because role\-based access control was explicitly required in multiple sources \(email\_staff\_login\.eml; interview\_sysadmin\_2009\-05\-10\.txt\)\.

The system shall manage user rights and privileges for reporting via security groups and/or role definitions, allowing assignment of access at the individual, workgroup, and arbitrary staff\-group level\.

**Verification hint:** Define roles/groups with differing permissions and verify users' access to reporting functions matches assigned roles\.

#### REQ-FUN-021 — Shelf Space Utilization Report

**Priority:** High  
**Sources:** `conversations/conv_pines016_shelf_space.eml`  
**Priority rationale:** Explicitly marked High in the source material \(conversations/conv\_pines016\_shelf\_space\.eml\)\.

The system shall provide, for each genre and material format, a report comparing the percentage of total circulations, the percentage of the collection, and the percentage of total shelf space allocated to that genre/format\.

**Verification hint:** For each reported percentage verify the denominator and formula used\: percent of total circulations = \(circulations for genre/format ÷ total circulations\) × 100; percent of collection = \(items in genre/format ÷ total items in collection\) × 100; percent of total shelf space = \(shelf space allocated to genre/format ÷ total shelf space\) × 100\. Confirm report values match calculations against underlying circulation, item\-count, and shelf\-space source data\.

#### REQ-FUN-022 — Survey Filtering by Name

**Priority:** Medium  
**Sources:** `meeting_tech_subcommittee_2009-06-30.txt`  
**Priority rationale:** Marked Medium in the source material \(meeting\_tech\_subcommittee\_2009\-06\-30\.txt\) to improve usability for report authors\.

The system shall allow survey\-related queries and filters to use survey names \(human\-readable\) rather than only survey IDs, resolving names internally to the appropriate IDs\.

**Verification hint:** Run survey queries using survey name strings and verify results match the expected survey ID\-backed data\.

#### REQ-FUN-023 — System Capacity Interface

**Priority:** High  
**Sources:** `conversations/conv_pines015_capacity_interface.eml`  
**Priority rationale:** Explicitly marked High in the source material \(conversations/conv\_pines015\_capacity\_interface\.eml\)\.

The system shall provide a capacity interface that shows capacity metrics for all branches, including a high\-level overview, the ability to drill down to individual branches, sorting and filtering of results, display of trend data, and export of displayed data to CSV\. The navigational and data\-presentation capabilities named above shall be provided for whatever capacity measures are specified for the project\.

**Verification hint:** Open the interface, verify overview, drill\-down, sort/filter actions, view trend charts, and export resulting dataset to CSV\. Verify that the interface presents the capacity measures and units as specified for the project\.

### Non-functional Requirements

#### REQ-NFR-001 — Accessibility Compliance \(Section 508\)

**Priority:** High  
**Sources:** `interview_sysadmin_2009-05-10.txt`  
**Priority rationale:** Explicitly marked High in the source material \(interview\_sysadmin\_2009\-05\-10\.txt\)\.

The reporting system shall comply with Section 508 accessibility requirements and be compatible with assistive technologies such as screen readers and magnification software\.

**Verification hint:** Perform accessibility testing \(e\.g\., screen reader walkthrough and a11y checklists\) and confirm compliance with Section 508 checkpoints\.

### Constraints

#### REQ-CON-001 — Development and Training Environments with Migration

**Priority:** High  
**Sources:** `interview_sysadmin_2009-05-10.txt`  
**Priority rationale:** Explicitly marked High in the source material \(interview\_sysadmin\_2009\-05\-10\.txt\) to support safe development and training practices\.

The system shall provide separate development and training environments and shall support configuration migration paths to production so changes can be tested without affecting live operations\.

**Verification hint:** Demonstrate configuration changes in development, migrate them to the training environment, and then migrate to production following the documented migration steps\.

#### REQ-CON-002 — Server Environment Compatibility

**Priority:** High  
**Sources:** `interview_sysadmin_2009-05-10.txt`  
**Priority rationale:** Explicitly marked High in the source material \(interview\_sysadmin\_2009\-05\-10\.txt\) reflecting current deployment constraints\.

The reporting system shall be deployable on both Linux and Solaris server environments to ensure compatibility with the organization's existing infrastructure\.

**Verification hint:** Install and run the system on representative Linux and Solaris test servers and verify full functionality\.

#### REQ-CON-003 — Transaction History Retention Policy

**Priority:** High  
**Sources:** `survey_results_2009.txt`  
**Priority rationale:** Explicitly marked High in the source material \(survey\_results\_2009\.txt\) and is a core operational constraint for reporting and historical analysis\.

The system shall retain transaction history for a configurable number of days for detailed transactional queries, and shall retain monthly and annual aggregates indefinitely for long\-term reporting\.

**Verification hint:** Verify that transaction\-history retention settings are honored \(raw transaction access subject to configured retention limits\) and that monthly and annual aggregates remain available for long\-term reporting\.

### Documentation Requirements

#### REQ-DOC-001 — Complete Data Specifications and Process Descriptions

**Priority:** Medium  
**Sources:** `meeting_minutes/meeting_2009-07-20_minutes.txt`  
**Priority rationale:** Marked Medium in the source material \(meeting\_minutes/meeting\_2009\-07\-20\_minutes\.txt\); documentation is required but prioritized behind core functional features\.

The software developer shall provide data specifications and a high\-level description of major reporting processes sufficient to enable staff to understand report data structures and reporting workflows\.

**Verification hint:** Review delivered documentation and confirm presence of a data\-specifications deliverable that provides a high\-level description of major reporting processes sufficient for staff to understand report data structures and workflows\.

#### REQ-DOC-002 — Reporting Capabilities Overview and Gap Analysis \(documentation deliverable\)

**Priority:** High  
**Sources:** `evergreen_reference_2009.txt`  
**Priority rationale:** Explicitly marked High in the source material \(evergreen\_reference\_2009\.txt\) as a necessary step before enhancement planning\.

Deliver a documented overview of existing reporting capabilities in the system together with an identification of gaps and limitations that have driven the need for enhanced reporting\. The delivered document shall describe existing capabilities, known limitations, and the primary gaps identified in the reviewed reporting sources\.

**Conflict resolution:** Source\-level coverage dispositions \(explicit\)\: \- email\_financial\_reports\.eml — disposition\: out of scope for this reporting\-requirements set\. Reason\: content pertains to financial reporting practices rather than management\-process/reporting feature requirements addressed in these drafts\. \- interview\_cataloging\_2009\-05\-08\.txt — disposition\: out of scope for this reporting\-requirements set\. Reason\: source content pertains to cataloging workflows and does not introduce additional in\-scope management\-reporting requirements\. \- meeting\_minutes/meeting\_2009\-03\-15\_minutes\.txt — disposition\: out of scope for this reporting\-requirements set\. Reason\: meeting contents do not introduce additional in\-scope reporting requirements related to the management\-process/reporting features documented here\.

**Verification hint:** Review the delivered overview and gap\-list document and confirm it maps existing features to identified enhancement needs and describes known limitations and primary gaps identified in the reviewed reporting sources\.

### Dependencies and Assumptions

_No requirements in this category._

## Blacklist

_No identified requirements were discarded._

## Traceability Matrix

| ID | Type | Sources | Extracted Item IDs |
|---|---|---|---|
| REQ-FUN-001 | Requirement | `email_report_features.eml`, `survey_results_2009.txt` | `ITEM-00016`, `ITEM-00032` |
| REQ-FUN-002 | Requirement | `survey_results_2009.txt` | `ITEM-00031` |
| REQ-FUN-003 | Requirement | `conversations/conv_pines024_inactive_patrons.eml` | `ITEM-00012` |
| REQ-FUN-004 | Requirement | `conversations/conv_pines024_inactive_patrons.eml`, `early_draft_srs_galecia.txt` | `ITEM-00010` |
| REQ-FUN-005 | Requirement | `conversations/conv_pines022_deletions.eml` | `ITEM-00007` |
| REQ-FUN-006 | Requirement | `meeting_minutes/meeting_2009-07-20_minutes.txt` | `ITEM-00028` |
| REQ-FUN-007 | Requirement | `evergreen_reference_2009.txt` | `ITEM-00022` |
| REQ-FUN-008 | Requirement | `email_report_features.eml`, `survey_results_2009.txt` | `ITEM-00017`, `ITEM-00033` |
| REQ-FUN-009 | Requirement | `conversations/conv_pines024_inactive_patrons.eml` | `ITEM-00014` |
| REQ-FUN-010 | Requirement | `conversations/conv_pines024_inactive_patrons.eml`, `early_draft_srs_galecia.txt` | `ITEM-00009` |
| REQ-FUN-011 | Requirement | `conversations/conv_pines024_inactive_patrons.eml` | `ITEM-00013` |
| REQ-FUN-012 | Requirement | `conversations/conv_pines021_item_purging.eml` | `ITEM-00006` |
| REQ-FUN-013 | Requirement | `conversations/conv_pines018_item_transfer.eml` | `ITEM-00004` |
| REQ-FUN-014 | Requirement | `conversations/conv_pines014_material_volume.eml` | `ITEM-00001` |
| REQ-FUN-015 | Requirement | `conversations/conv_pines019_020_missing_intransit.eml` | `ITEM-00005` |
| REQ-FUN-016 | Requirement | `conversations/conv_pines023_patron_characteristics.eml` | `ITEM-00008` |
| REQ-FUN-017 | Requirement | `conversations/conv_pines024_inactive_patrons.eml` | `ITEM-00011` |
| REQ-FUN-018 | Requirement | `evergreen_reference_2009.txt` | `ITEM-00021` |
| REQ-FUN-019 | Requirement | `email_report_features.eml`, `evergreen_reference_2009.txt` | `ITEM-00015`, `ITEM-00020` |
| REQ-FUN-020 | Requirement | `email_staff_login.eml`, `interview_sysadmin_2009-05-10.txt` | `ITEM-00018`, `ITEM-00025` |
| REQ-FUN-021 | Requirement | `conversations/conv_pines016_shelf_space.eml` | `ITEM-00003` |
| REQ-FUN-022 | Requirement | `meeting_tech_subcommittee_2009-06-30.txt` | `ITEM-00029` |
| REQ-FUN-023 | Requirement | `conversations/conv_pines015_capacity_interface.eml` | `ITEM-00002` |
| REQ-NFR-001 | Requirement | `interview_sysadmin_2009-05-10.txt` | `ITEM-00023` |
| REQ-CON-001 | Requirement | `interview_sysadmin_2009-05-10.txt` | `ITEM-00026` |
| REQ-CON-002 | Requirement | `interview_sysadmin_2009-05-10.txt` | `ITEM-00024` |
| REQ-CON-003 | Requirement | `survey_results_2009.txt` | `ITEM-00030` |
| REQ-DOC-001 | Requirement | `meeting_minutes/meeting_2009-07-20_minutes.txt` | `ITEM-00027` |
| REQ-DOC-002 | Requirement | `evergreen_reference_2009.txt` | `ITEM-00019` |

## Source Coverage

The input manifest contains **20** source document(s).

| Source document | Derived requirement or blacklist IDs |
|---|---|
| `conversations/conv_pines014_material_volume.eml` | REQ-FUN-014 |
| `conversations/conv_pines015_capacity_interface.eml` | REQ-FUN-023 |
| `conversations/conv_pines016_shelf_space.eml` | REQ-FUN-021 |
| `conversations/conv_pines018_item_transfer.eml` | REQ-FUN-013 |
| `conversations/conv_pines019_020_missing_intransit.eml` | REQ-FUN-015 |
| `conversations/conv_pines021_item_purging.eml` | REQ-FUN-012 |
| `conversations/conv_pines022_deletions.eml` | REQ-FUN-005 |
| `conversations/conv_pines023_patron_characteristics.eml` | REQ-FUN-016 |
| `conversations/conv_pines024_inactive_patrons.eml` | REQ-FUN-003, REQ-FUN-004, REQ-FUN-009, REQ-FUN-010, REQ-FUN-011, REQ-FUN-017 |
| `early_draft_srs_galecia.txt` | REQ-FUN-004, REQ-FUN-010 |
| `email_financial_reports.eml` | _No derived item_ |
| `email_report_features.eml` | REQ-FUN-001, REQ-FUN-008, REQ-FUN-019 |
| `email_staff_login.eml` | REQ-FUN-020 |
| `evergreen_reference_2009.txt` | REQ-DOC-002, REQ-FUN-007, REQ-FUN-018, REQ-FUN-019 |
| `interview_cataloging_2009-05-08.txt` | _No derived item_ |
| `interview_sysadmin_2009-05-10.txt` | REQ-CON-001, REQ-CON-002, REQ-FUN-020, REQ-NFR-001 |
| `meeting_minutes/meeting_2009-03-15_minutes.txt` | _No derived item_ |
| `meeting_minutes/meeting_2009-07-20_minutes.txt` | REQ-DOC-001, REQ-FUN-006 |
| `meeting_tech_subcommittee_2009-06-30.txt` | REQ-FUN-022 |
| `survey_results_2009.txt` | REQ-CON-003, REQ-FUN-001, REQ-FUN-002, REQ-FUN-008 |
