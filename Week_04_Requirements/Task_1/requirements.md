# Software Requirements Specification (generated)

Generated from 20 input documents by the requirements-refinement agentic network.

## 1. Priority scale

| Priority | Meaning |
|---|---|
| **Must** | Release-blocking. The system cannot go live or fails its core purpose without it: a legal, regulatory or accessibility obligation, security or data integrity, a function the stakeholders call critical or essential, or a prerequisite of another Must. |
| **Should** | High value, but the release is still usable without it: a manual or ad-hoc workaround exists, even if painful. Planned for the first release unless time is critically short. |
| **Could** | Nice to have. Small benefit or convenience; most users would not notice its absence. Include only if capacity allows. |
| **Won't** | Explicitly deferred or excluded by the stakeholders for this release, or dependent on a question they left undecided. Kept for future planning. |

## 2. Source documents

| ID | File |
|---|---|
| D01 | conversations\conv_pines014_material_volume.eml |
| D02 | conversations\conv_pines015_capacity_interface.eml |
| D03 | conversations\conv_pines016_shelf_space.eml |
| D04 | conversations\conv_pines018_item_transfer.eml |
| D05 | conversations\conv_pines019_020_missing_intransit.eml |
| D06 | conversations\conv_pines021_item_purging.eml |
| D07 | conversations\conv_pines022_deletions.eml |
| D08 | conversations\conv_pines023_patron_characteristics.eml |
| D09 | conversations\conv_pines024_inactive_patrons.eml |
| D10 | early_draft_srs_galecia.txt |
| D11 | email_financial_reports.eml |
| D12 | email_report_features.eml |
| D13 | email_staff_login.eml |
| D14 | evergreen_reference_2009.txt |
| D15 | interview_cataloging_2009-05-08.txt |
| D16 | interview_sysadmin_2009-05-10.txt |
| D17 | meeting_minutes\meeting_2009-03-15_minutes.txt |
| D18 | meeting_minutes\meeting_2009-07-20_minutes.txt |
| D19 | meeting_tech_subcommittee_2009-06-30.txt |
| D20 | survey_results_2009.txt |

## 3. Glossary (canonical vocabulary)

| Term | Definition |
|---|---|
| branch | An individual library location within the consortium; use this term for location-level reporting scope. |
| consortium | The entire participating library system and its branches; use this term for system-wide organizational scope. |
| staff user | A person authorized to use staff or administrative functions of the system. |
| patron | A library borrower or account holder, including a person whose records are used in reporting. |
| item | A copy-level library material record; it is distinct from a bibliographic record describing a work. |
| bibliographic record | A catalog record describing a work or title to which one or more item records may be associated. |
| report | A defined query or presentation of system data, including its selection criteria and results. |
| hold | A patron request for an item or title; hold counts are reported separately from inventory-state totals. |
| location | A field describing where an item is or is assigned to be; use branch when referring to the organizational unit itself. |
| staff role | A named set of permissions assigned to staff users to control access to system functions. |

## 4. Requirements summary

| ID | Name | Priority | Sources |
|---|---|---|---|
| REQ-006 | Holds reporting with placement/origin and workflow status | Must | D01, D10, D20 |
| REQ-014 | Support large branch counts | Must | D02 |
| REQ-019 | Aggregate queries from central database | Must | D02 |
| REQ-020 | Shelf Space Report (genre & format) | Must | D03 |
| REQ-021 | Report scope selection (per branch or consortium) | Must | D03 |
| REQ-022 | Date range filtering (including quarters) | Must | D03 |
| REQ-024 | Compute item counts by genre/format | Must | D03 |
| REQ-025 | Compute checkouts by genre/format | Must | D03 |
| REQ-027 | Provide system-average alongside branch metrics | Must | D03 |
| REQ-028 | Query builder for candidates | Must | D04 |
| REQ-029 | Save and share queries | Must | D04 |
| REQ-030 | Manual selection from results | Must | D04 |
| REQ-031 | Batch administrative item operations (transfer/move/delete) with safety and performance | Must | D04, D10, D20 |
| REQ-032 | Store original location metadata | Must | D04 |
| REQ-033 | Pull list generation | Must | D04 |
| REQ-034 | Printable transit labels | Must | D04 |
| REQ-035 | Auto-revert by time period | Must | D04 |
| REQ-039 | Immediate undo function | Must | D04 |
| REQ-040 | Security groups/roles administration and enforcement | Must | D04, D10, D13, D16 |
| REQ-041 | Transfer history and audit logging | Must | D04 |
| REQ-043 | Preview and confirmation dialog | Must | D04 |
| REQ-044 | Transfer delay and issue alerts | Must | D04 |
| REQ-047 | Temporary transfer by event scheduling | Must | D04 |
| REQ-050 | Customizable purging criteria builder | Must | D06 |
| REQ-054 | Separate confirmation step for deletions | Must | D06 |
| REQ-055 | Deletion/audit trails with immutable logging and evidence reporting | Must | D06, D07, D10, D15, D20 |
| REQ-056 | Last-copy identification report with scope | Must | D06 |
| REQ-061 | Log denied deletion attempts | Must | D07 |
| REQ-062 | Report interface to query audits | Must | D07 |
| REQ-064 | Deletion volume reports | Must | D07 |
| REQ-066 | Trace deletion by record ID | Must | D07 |
| REQ-072 | Include null/blank field values in results | Must | D08, D10, D14, D19, D20 |
| REQ-075 | Source demographic fields from patron table | Must | D08 |
| REQ-078 | Aggregate events across sources | Must | D09 |
| REQ-080 | Include current mailing addresses | Must | D09 |
| REQ-084 | Asynchronous/background processing for long/concurrent reports | Must | D09, D10, D14, D16 |
| REQ-085 | Performance scalability for large datasets | Must | D09 |
| REQ-086 | Support consortium scale | Must | D10, D18 |
| REQ-089 | Client access modes (web browser and Windows client) | Must | D10, D18 |
| REQ-091 | Accessibility compliance for UI and help | Must | D10, D14, D18, D19 |
| REQ-092 | Relational backend and PostgreSQL support | Must | D10, D16, D18, D19 |
| REQ-094 | Development and training environment | Must | D10 |
| REQ-099 | Online hierarchical cross-linked HTML help | Must | D10, D14, D16, D18, D19 |
| REQ-100 | Admin/user error reporting with query diagnostics | Must | D10, D18, D19 |
| REQ-101 | Centralized multi-location management/reporting | Must | D10, D18, D19 |
| REQ-102 | Interface with vendor websites and data formats | Must | D10 |
| REQ-105 | Report template creation, distribution, and field locking | Must | D10, D12, D14, D17, D20 |
| REQ-106 | Report creation and cloning permissions | Must | D10 |
| REQ-108 | Predefined executive reports | Must | D10 |
| REQ-109 | Transaction archive privacy protections | Must | D10, D12 |
| REQ-110 | Periodic management reports | Must | D10 |
| REQ-116 | Anonymized demographic/statistical data | Must | D10, D12, D20 |
| REQ-120 | Uncataloged item tracking and usage statistics | Must | D10, D15 |
| REQ-133 | Transaction totals by organizational scope | Must | D10, D20 |
| REQ-135 | Accounting, auditing, and retention compliance | Must | D10, D11 |
| REQ-138 | Patron payments ledger with charge mapping | Must | D10, D11 |
| REQ-163 | Real-time and historical reporting support | Must | D10, D14, D19, D20 |
| REQ-170 | Transaction report grouping and filtering | Must | D10, D20 |
| REQ-171 | Value-of-items report | Must | D11 |
| REQ-172 | Join patron and item financial data | Must | D11 |
| REQ-173 | Patron account balances report | Must | D11 |
| REQ-175 | Fines and charges accrual reports | Must | D11 |
| REQ-176 | Fines waived reporting by branch and period | Must | D11 |
| REQ-177 | Payments reporting with method, channel, and branch breakdowns | Must | D11 |
| REQ-180 | Immediate update of financial information | Must | D11 |
| REQ-181 | Include ecommerce transactions in financial records | Must | D11 |
| REQ-193 | Transaction retention per State law | Must | D12 |
| REQ-196 | Pre-defined board reports and metrics | Must | D12 |
| REQ-199 | Multiple authentication methods | Must | D13 |
| REQ-201 | Badge-swipe login authenticates the staff user | Must | D13 |
| REQ-202 | Staff session audit logging | Must | D13 |
| REQ-204 | Permissions determined by role on login | Must | D13 |
| REQ-227 | Use reporting replica/reads to protect production | Must | D14, D16 |
| REQ-266 | Item transfer utility | Must | D15 |
| REQ-275 | Data quality exception reports | Must | D15 |
| REQ-277 | Deploy on RHEL5 and Solaris10 | Must | D16 |
| REQ-282 | Preserve OPAC/circulation responsiveness; no patron-facing functionality in management reporting | Must | D16, D17, D18, D19 |
| REQ-284 | Section 508 Accessibility Compliance | Must | D16 |
| REQ-285 | Support Assistive Technologies | Must | D16 |
| REQ-286 | Role-based access control with defined user classes | Must | D16, D17, D18, D19 |
| REQ-291 | Support Secondary Site/Disaster Recovery | Must | D16 |
| REQ-293 | Management Reports and Analysis Tools | Must | D17 |
| REQ-294 | Executive Reports Interface | Must | D17 |
| REQ-298 | Local Configuration by Administrators | Must | D17 |
| REQ-299 | Consortium-level Aggregated Reporting | Must | D17 |
| REQ-300 | Collection Use Analysis Reports | Must | D17 |
| REQ-301 | Branch Capacity and Distribution Analysis | Must | D17 |
| REQ-302 | Patron demographic and interest reporting | Must | D17, D20 |
| REQ-303 | Staff Productivity and Workflow Reports | Must | D17 |
| REQ-304 | Financial Transaction Tracking Reports | Must | D17 |
| REQ-305 | Integration with ILS Modules | Must | D17 |
| REQ-307 | Report Testing and Staging Workflow | Must | D17 |
| REQ-311 | Non-disruptive report processing | Must | D18 |
| REQ-317 | Complete data specifications | Must | D18 |
| REQ-320 | Enterprise system integration | Must | D18 |
| REQ-322 | Integration with acquisitions and cataloging | Must | D18 |
| REQ-323 | Vendor interfaces and standard formats | Must | D18 |
| REQ-329 | Missing and damaged item reports by branch | Must | D18 |
| REQ-334 | Inventory and capacity reports | Must | D18 |
| REQ-335 | Financial reporting for directors | Must | D18 |
| REQ-336 | PostgreSQL compatibility | Must | D19 |
| REQ-341 | Predefined user roles | Must | D19 |
| REQ-343 | Data dictionaries and specifications | Must | D19 |
| REQ-349 | Timely data currency | Must | D19 |
| REQ-350 | Read-only ILS reporting integration | Must | D19 |
| REQ-351 | Vendor data format support | Must | D19 |
| REQ-359 | Circulation reports | Must | D20 |
| REQ-360 | Item inventory reports | Must | D20 |
| REQ-362 | Financial transaction reports | Must | D20 |
| REQ-364 | Custom and on‑demand reports | Must | D20 |
| REQ-371 | Patron behavior statistics | Must | D20 |
| REQ-375 | Save and reuse queries | Must | D20 |
| REQ-379 | Performance under peak load | Must | D20 |
| REQ-380 | Export deduplication option | Must | D20 |
| REQ-382 | Select and consolidate MARC fields | Must | D20 |
| REQ-384 | Move items between locations | Must | D20 |
| REQ-385 | Revert item location changes | Must | D20 |
| REQ-388 | Snapshot bills history | Must | D20 |
| REQ-389 | Last circulation date on items | Must | D20 |
| REQ-390 | Exclude renewals from checkin time | Must | D20 |
| REQ-001 | Material volume reports with as-of point-in-time and category breakdowns | Should | D01, D10, D15 |
| REQ-002 | Separate acquisition, check-in, and check-out counts | Should | D01 |
| REQ-003 | Breakdown by predefined categories | Should | D01 |
| REQ-004 | Customizable category definitions | Should | D01 |
| REQ-005 | Group by classification and format | Should | D01 |
| REQ-007 | Filter by branch | Should | D01 |
| REQ-008 | Acquisition date filtering and recent additions | Should | D01 |
| REQ-010 | System-wide capacity overview | Should | D02 |
| REQ-012 | Sorting and filtering controls | Should | D02, D14 |
| REQ-015 | Export to CSV | Should | D02 |
| REQ-018 | Branch capacity interface with color status | Should | D02, D10 |
| REQ-023 | Comparison view across libraries (side-by-side) | Should | D03 |
| REQ-026 | Estimate shelf space per genre/format with fallback | Should | D03 |
| REQ-036 | Auto-revert transfer rules (event/status criteria) | Should | D04 |
| REQ-038 | Scheduled report runs and automated background jobs | Should | D04, D06, D10, D20 |
| REQ-046 | Integration with existing query tools | Should | D04 |
| REQ-048 | Missing and damaged items reports by branch with detail + summary + filtering | Should | D05, D10, D15 |
| REQ-049 | In-transit items aging report with configurable X and merged directions | Should | D05, D10, D15, D18 |
| REQ-051 | Combinable logical criteria | Should | D06 |
| REQ-052 | Bulk status conversion for item records | Should | D06, D15 |
| REQ-057 | Bulk deletion of volumes and orphan biblios | Should | D06, D15 |
| REQ-063 | Filtering and aggregation options | Should | D07 |
| REQ-069 | Age/inactivity filtering using derived age and configurable age ranges with exclusions | Should | D08, D09 |
| REQ-071 | Combine filters with AND/OR logic | Should | D08 |
| REQ-079 | Configurable scope and grouping levels | Should | D09 |
| REQ-081 | Flag or separate patrons with fines | Should | D09 |
| REQ-083 | CSV export for outreach systems | Should | D09 |
| REQ-088 | Server OS compatibility (Linux and Solaris) | Should | D10, D18 |
| REQ-090 | Browser compatibility (IE6+ and Firefox2+) | Should | D10, D16, D18 |
| REQ-093 | Standards-compliant HTML output | Should | D10, D18, D19 |
| REQ-097 | Record data specifications provided | Should | D10 |
| REQ-098 | High-level process documentation | Should | D10, D18, D19 |
| REQ-103 | OPAC interaction reflected in management reports | Should | D10, D18 |
| REQ-104 | Staff login options | Should | D10 |
| REQ-107 | Graphical query builder with field/regex/boolean controls | Should | D10, D12, D14 |
| REQ-111 | Display selection criteria with results | Should | D10, D12, D14 |
| REQ-112 | Report queue visibility to submitters | Should | D10, D12, D14, D18, D20 |
| REQ-119 | Shelf space comparative report | Should | D10 |
| REQ-126 | Patron characteristic filtering and grouping | Should | D10 |
| REQ-127 | Inactive patrons listing | Should | D10 |
| REQ-130 | Count check-ins by type | Should | D10, D20 |
| REQ-131 | Count check-outs and renewals by type | Should | D10, D20 |
| REQ-137 | Financial reporting suite | Should | D10 |
| REQ-139 | Three reporting interfaces | Should | D10 |
| REQ-146 | Multiple export formats for report results (CSV/HTML/Excel-compatible) | Should | D10, D14, D20 |
| REQ-147 | Cancel scheduled or running report jobs | Should | D10, D14, D19, D20 |
| REQ-150 | Batch status conversion assistance report | Should | D10 |
| REQ-154 | Report prioritization and queue preemption | Should | D10, D12, D14 |
| REQ-156 | Retrieve total circulation with breakdown | Should | D10 |
| REQ-157 | Upload file filter input | Should | D10, D14 |
| REQ-158 | Pre-overdue/overdue/hold notices reporting | Should | D10 |
| REQ-164 | Historical reporting via point-in-time snapshots / warehouse | Should | D10, D14, D20 |
| REQ-184 | Fine-grained RBAC for report/query access and actions | Should | D12, D14, D20 |
| REQ-190 | Shared report folders with scoped access controls | Should | D12, D20 |
| REQ-197 | Cross-tabulation reporting dimensions | Should | D12 |
| REQ-200 | Streamlined login optional and configurable | Should | D13 |
| REQ-207 | Support for defined staff roles | Should | D13 |
| REQ-208 | Web-based report writer | Should | D14 |
| REQ-211 | Save and reuse report definitions | Should | D14 |
| REQ-212 | Complex query construction | Should | D14 |
| REQ-222 | Email report delivery with selectable recipients via address book | Should | D10, D14, D20 |
| REQ-229 | Development and training separation | Should | D14 |
| REQ-230 | Configuration migration between environments | Should | D14 |
| REQ-234 | Separate last-circulation date and last-edit timestamp | Should | D14, D15 |
| REQ-235 | Separate checkin and renewal timestamps | Should | D14 |
| REQ-260 | Staff password change audit | Should | D14 |
| REQ-262 | Unfilled holds report | Should | D14 |
| REQ-263 | Stale holds report | Should | D14 |
| REQ-268 | Weeding reports with configurable criteria | Should | D15, D18 |
| REQ-270 | Last-copy identification report | Should | D15 |
| REQ-289 | Separate dev, training, and production environments | Should | D16, D19 |
| REQ-297 | Staff Report Authoring | Should | D17 |
| REQ-308 | Prototype Deployment for User Review | Should | D17 |
| REQ-309 | Display-ready Reports for Public Screens | Should | D17 |
| REQ-310 | Documentation for Both Audiences | Should | D17 |
| REQ-315 | Dev and training environment migration | Should | D18 |
| REQ-325 | Pre-defined executive report templates | Should | D18 |
| REQ-326 | Data quality reporting | Should | D18 |
| REQ-327 | Staff badge-swipe login | Should | D18 |
| REQ-331 | Shelf space utilization reports | Should | D18 |
| REQ-332 | Demographic analysis reports | Should | D18 |
| REQ-333 | Cross-branch comparison reports | Should | D18 |
| REQ-346 | Low-level query-specific error feedback | Should | D19 |
| REQ-347 | Enterprise operating assumptions | Should | D19 |
| REQ-352 | Graceful handling of optional vendor data | Should | D19 |
| REQ-353 | Read-only OPAC queries | Should | D19 |
| REQ-354 | Support Excel, CSV, HTML exports | Should | D19 |
| REQ-394 | Staff account expiration reporting | Should | D10 |
| REQ-009 | Historical comparison / time-series output | Could | D01 |
| REQ-011 | Drill-down branch details | Could | D02 |
| REQ-013 | Grouping by region or system | Could | D02 |
| REQ-016 | Trend data and charts | Could | D02 |
| REQ-017 | Configurable capacity metrics | Could | D02 |
| REQ-053 | Read-only candidate reports | Could | D06 |
| REQ-068 | Filter and group by demographics | Could | D08 |
| REQ-073 | Aggregate circulation/checkout counts | Could | D08 |
| REQ-115 | Patron behavior / use analytics | Could | D10 |
| REQ-124 | Item record purging and conversion utilities | Could | D10 |
| REQ-128 | Configurable transaction history retention | Could | D10 |
| REQ-129 | Backroom transaction statistics grouping | Could | D10 |
| REQ-134 | Value of items reporting | Could | D10 |
| REQ-140 | Pre-written canned report templates | Could | D10 |
| REQ-141 | On-demand maintenance/collection reports | Could | D10 |
| REQ-143 | Quick-access report UI pop-up descriptions | Could | D10 |
| REQ-144 | Quick-access check-off selection | Could | D10 |
| REQ-149 | Multi-period comparative columns | Could | D10 |
| REQ-151 | Editable canned report definitions/display with permissions | Could | D10, D14 |
| REQ-153 | Last-copy deletion list for WorldCat updates | Could | D10 |
| REQ-155 | Total use count and date-range breakdown | Could | D10 |
| REQ-159 | Pivot table output | Could | D10, D14, D20 |
| REQ-166 | Report metadata showing date selection and name | Could | D10 |
| REQ-167 | Survey name selection by name | Could | D10 |
| REQ-168 | Reports on deleted items that were last copy | Could | D10 |
| REQ-169 | Flatten MARC fields into single row | Could | D10 |
| REQ-174 | Query accounts by balance threshold | Could | D11 |
| REQ-187 | Clone report/template capability | Could | D12 |
| REQ-189 | Role-based automatic permission updates | Could | D12 |
| REQ-209 | Drag-and-drop field selection | Could | D14 |
| REQ-213 | Boolean operators in filters | Could | D14 |
| REQ-226 | Quick access UI with descriptions | Could | D14 |
| REQ-236 | Snapshot bills historical report | Could | D14 |
| REQ-237 | Last copy report enhancements | Could | D14 |
| REQ-238 | Items Edited Count report | Could | D14 |
| REQ-239 | Circulation by circ modifier report | Could | D14 |
| REQ-240 | Circulation by Dewey report | Could | D14 |
| REQ-241 | Circulation by MARC fields report | Could | D14 |
| REQ-242 | Circulation by location and patron county | Could | D14 |
| REQ-243 | Circulation by age demographic report | Could | D14 |
| REQ-244 | List items by fines stopped reason | Could | D14 |
| REQ-245 | Items overdue with patron contact | Could | D14 |
| REQ-246 | Items by total use count | Could | D14 |
| REQ-247 | Items by creation date range | Could | D14 |
| REQ-248 | Claims returned report | Could | D14 |
| REQ-249 | Weeding report with last circulation date | Could | D14 |
| REQ-250 | Age of collection by call number | Could | D14 |
| REQ-251 | Price value by call number | Could | D14 |
| REQ-252 | Bib records edited count | Could | D14 |
| REQ-253 | Bib records added by user/library | Could | D14 |
| REQ-254 | Bib records missing MARC fields | Could | D14 |
| REQ-255 | Patron count by age demographic | Could | D14 |
| REQ-256 | Patron count by county | Could | D14 |
| REQ-257 | Patron count by county/city/zip | Could | D14 |
| REQ-258 | Voter survey responses report | Could | D14 |
| REQ-259 | List of inactive patrons | Could | D14 |
| REQ-261 | Holds purchase alert report | Could | D14 |
| REQ-264 | Aged debt detailed report | Could | D14 |
| REQ-273 | Shelf space comparison report | Could | D15 |
| REQ-358 | Filter by survey name resolution | Could | D19 |
| REQ-392 | Sort in-transit items by due date | Could | D05 |

## 5. Requirements

### REQ-001 — Material volume reports with as-of point-in-time and category breakdowns

- **Priority:** Should — High value: requested by multiple sources for material volume reporting with detailed breakdowns.
- **Derived from:** D01 (conversations\conv_pines014_material_volume.eml), D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt)

The system shall provide Material Volume reporting that returns item counts for a specified library/location as-of a user-selected date/time (not only current state), reflecting item states such as acquired/checked in/checked out as of that point. The reporting must support breakdowns by selectable categories (including at least total items, holds, adult fiction, board books and other selectable categories) and allow selecting filters/breakdown categories so returned counts are consistent with the chosen as-of date.

### REQ-002 — Separate acquisition, check-in, and check-out counts

- **Priority:** Should — High value: clearly requested for separate acquisition and item state counts.
- **Derived from:** D01 (conversations\conv_pines014_material_volume.eml)

The system shall present separate counts for new acquisitions (items recently added), items checked in, and items checked out, plus a total item count for the selected branch and date. The acquisition count is a separate metric and shall not be added to checked-in or checked-out counts when it overlaps with those inventory states. The total shall aggregate mutually exclusive item states, including checked-in, checked-out, and any other included inventory states. Acceptance hints: output includes distinct acquisition, checked-in, checked-out, and total values, and the total equals the defined aggregation of mutually exclusive item states for the selected date.

### REQ-003 — Breakdown by predefined categories

- **Priority:** Should — High value: necessary for reporting specifics by category, as indicated by stakeholders.
- **Derived from:** D01 (conversations\conv_pines014_material_volume.eml)

The system shall break down volume counts by categorical groupings such as adult fiction, board books, total items, and other predefined categories (for example fiction/non-fiction and format). Library staff need category-level detail to report on specific parts of the collection. Acceptance hints: report displays category names and counts for each category for the selected library/date.

### REQ-004 — Customizable category definitions

- **Priority:** Should — High value: allows libraries to customize reporting categories for better relevance.
- **Derived from:** D01 (conversations\conv_pines014_material_volume.eml)

The system shall allow library staff to define and customize which categories or category groupings are used in the Material Volume report (for example adding or removing categories like 'juvenile non-fiction' or 'large print'). Different libraries must be able to configure their own category sets so each branch can produce the breakdowns it requires. Acceptance hints: staff can create, edit and select a category set; the report reflects the chosen/custom category definitions.

### REQ-005 — Group by classification and format

- **Priority:** Should — High value: flexible grouping is requested to analyze collection attributes.
- **Derived from:** D01 (conversations\conv_pines014_material_volume.eml)

The system shall support grouping volume counts by classification types (e.g., fiction vs. non-fiction) and by item format (e.g., book, DVD, board book) and allow staff to choose which grouping(s) to apply in the report. Staff need flexible grouping to analyze collection composition by different attributes. Acceptance hints: report options include at least 'classification' and 'format' groupings and the output shows counts per group.

### REQ-006 — Holds reporting with placement/origin and workflow status

- **Priority:** Must — Core function: holds reporting is essential for workflow management in libraries.
- **Derived from:** D01 (conversations\conv_pines014_material_volume.eml), D10 (early_draft_srs_galecia.txt), D20 (survey_results_2009.txt)

The system shall count holds and provide holds reports that analyze how each hold was placed (staff desk, public computer inside library, remotely; placement_method attribute) and support workflow management via hold status. Reports must include holds placed and filled, stale holds, counts broken down by placement/origin, and include placement and fill dates, and be filterable/exportable. Additionally, in the Material Volume report the system must show an overall holds count for the selected library/date and, when category grouping is applied, a holds count broken down by category with holds count columns per category.

### REQ-007 — Filter by branch

- **Priority:** Should — High value: essential for branch-specific reporting needs of staff.
- **Derived from:** D01 (conversations\conv_pines014_material_volume.eml)

The system shall restrict counts to items whose location field equals the selected branch. Staff users need branch-scoped reports so each branch can produce its own monthly or quarterly reports. Acceptance hints: selecting a branch returns counts only for items with location = that branch.

### REQ-008 — Acquisition date filtering and recent additions

- **Priority:** Should — High value: requested for measuring collection growth with specific date filters.
- **Derived from:** D01 (conversations\conv_pines014_material_volume.eml)

The system shall use item acquisition date to support filters and counts of recently added volume, including the ability to report how much volume was added in a recent period such as the last 30, 60 or 90 days (and allow custom date ranges). Staff need to measure collection growth over standard windows for assessments. Acceptance hints: report can be run with preset windows (30/60/90 days) or a custom acquisition-date range and returns the count of items acquired in that period for the selected library.

### REQ-009 — Historical comparison / time-series output

- **Priority:** Could — Nice to have: historical comparisons are useful but not critical for initial release.
- **Derived from:** D01 (conversations\conv_pines014_material_volume.eml)

The system shall provide the ability to compare material volume across multiple points in time (a time series) so staff can see changes in volume (deltas) over time for a library and categories. Staff need historical comparisons for trend analysis and board reporting. Acceptance hints: user can request the report for multiple dates or a date range and receive a sequence of counts (or per-period deltas) suitable for charting or tabular comparison.

### REQ-010 — System-wide capacity overview

- **Priority:** Should — High value: overview of branch capacity is needed for resource allocation.
- **Derived from:** D02 (conversations\conv_pines015_capacity_interface.eml)

The system shall provide a high-level overview interface that displays the capacity status of all branches at once so branch managers and directors can see the big picture when deciding where to move items or allocate resources. Acceptance hints: the overview presents each branch as a row or tile with its key capacity metrics and current status; the view is accessible to staff users with appropriate permissions and is discoverable from the reporting/dashboard area.

### REQ-011 — Drill-down branch details

- **Priority:** Could — Nice to have: drill-down details provide deeper insights but are not essential initially.
- **Derived from:** D02 (conversations\conv_pines015_capacity_interface.eml)

The system shall allow users to drill down from the high-level overview into an individual branch's detailed capacity information so a manager can inspect underlying metrics and recent activity for a specific branch. Acceptance hints: clicking a branch in the overview opens a detail page or panel showing the branch's capacity metric(s), recent trend charts, and any configured limits or notes.

### REQ-012 — Sorting and filtering controls

- **Priority:** Should — High value: sorting and filtering will enhance the capacity interface usability significantly.
- **Derived from:** D02 (conversations\conv_pines015_capacity_interface.eml), D14 (evergreen_reference_2009.txt)

The system shall provide sorting and filtering capabilities for the capacity interface so users can limit or order branches by attributes such as region, library type, or current load to find suitable destinations or focus on a subset of branches. Acceptance hints: UI includes filters for region and library type and an option to sort by current load; filters can be combined and persist while exporting or drilling down.

### REQ-013 — Grouping by region or system

- **Priority:** Could — Nice to have: grouping by region helps organize data but is not critical.
- **Derived from:** D02 (conversations\conv_pines015_capacity_interface.eml)

The system shall support grouping or aggregating branches by system/region (or similar hierarchical groupings) so that users can reduce visual clutter and analyze capacity at a group level before inspecting individual branches. Acceptance hints: users can toggle group-by-region to see per-region aggregates (counts, averages) and expand groups to view member branches.

### REQ-014 — Support large branch counts

- **Priority:** Must — Release-blocking: must support large branch counts to ensure usability across many locations.
- **Derived from:** D02 (conversations\conv_pines015_capacity_interface.eml)

The system shall be able to present and work with a large number of locations (e.g., on the order of 286 branches) without rendering the overview unusable, so staff can manage system-wide capacity even for large networks. Acceptance hints: the interface remains usable with hundreds of branches by leveraging grouping, filtering, virtual scrolling, pagination or other strategies; administrative users can view or export full lists when needed.

### REQ-015 — Export to CSV

- **Priority:** Should — High value: CSV export functionality is useful for offline analysis.
- **Derived from:** D02 (conversations\conv_pines015_capacity_interface.eml)

The system shall allow users to export capacity data (the overview and any filtered/subset results) to CSV so directors and other stakeholders can perform offline analysis in spreadsheets. Acceptance hints: exported CSV includes one row per branch (or per grouped aggregate when grouping is active) and contains the displayed key metrics and any status labels; export respects current filters and sorts.

### REQ-016 — Trend data and charts

- **Priority:** Could — Nice to have: visualizations for trends would enhance understanding but are not essential.
- **Derived from:** D02 (conversations\conv_pines015_capacity_interface.eml)

The system shall provide trend data (historical time-series) and visualizations indicating whether a branch is growing or shrinking so planners can use capacity trends for long-term decisions. Acceptance hints: branch detail pages include a time-series chart of the selected capacity metric over configurable time ranges and a summary indicator of recent trend (increasing/decreasing/stable).

### REQ-017 — Configurable capacity metrics

- **Priority:** Could — Nice to have: configurable metrics provide flexibility but are not needed for initial rollout.
- **Derived from:** D02 (conversations\conv_pines015_capacity_interface.eml)

The system shall support multiple capacity metric definitions and allow configuration/selection of which metric(s) to use (examples raised include number of items vs. shelf space, number of physical items vs. a configured limit, and circulation volume vs. processing capacity) so stakeholders can define 'capacity' in the way that matches their operational needs. Acceptance hints: administrators can configure available metrics and select a primary metric for the overview; the UI can display multiple metrics side-by-side if configured.

### REQ-018 — Branch capacity interface with color status

- **Priority:** Should — High value: color coding for status indicators aids in quick capacity assessments.
- **Derived from:** D02 (conversations\conv_pines015_capacity_interface.eml), D10 (early_draft_srs_galecia.txt)

Provide an interface showing the capacity of all branches with per-branch and system metrics, including current occupancy/utilization values, and a color-coded status indicator (e.g., green/yellow/red for under-capacity/warning/at-or-over-capacity). Threshold values driving colors must be visible and configurable by an administrator, and color application must be consistent across overview tiles/rows and trend charts. Acceptance requires display of capacity metrics and correct color/status behavior.

### REQ-019 — Aggregate queries from central database

- **Priority:** Must — Core function: querying the centralized database for accurate reporting is essential.
- **Derived from:** D02 (conversations\conv_pines015_capacity_interface.eml)

The system shall obtain branch capacity data by querying the centralized database and performing necessary aggregations across branches so reports reflect the authoritative system data. Acceptance hints: the reporting component executes aggregate queries against the central database (or a replicated reporting store) to produce the overview, grouping, filtering and trend data; data freshness and source should be documented.

### REQ-020 — Shelf Space Report (genre & format)

- **Priority:** Must — Core function: generating accurate shelf space reports is essential for branch management.
- **Derived from:** D03 (conversations\conv_pines016_shelf_space.eml)

The system must generate a Shelf Space Report that, for each combination of genre and format of material, presents three metrics: (a) the percentage of total circulations attributable to that genre/format, (b) the percentage of the collection (item count) represented by that genre/format, and (c) the percentage of total shelf space occupied by that genre/format. Branch managers, catalogers and directors need this report to evaluate whether shelf allocation matches usage. Acceptance hints: the report lists one row per genre/format, includes the three percentage columns, and each percentage column sums to 100% across all rows for the selected scope.

### REQ-021 — Report scope selection (per branch or consortium)

- **Priority:** Must — Core function: allowing report scope selection is vital for accurate reporting.
- **Derived from:** D03 (conversations\conv_pines016_shelf_space.eml)

The system must allow the user to select the report scope as either a single branch or the entire consortium; all metrics and totals in the Shelf Space Report must be computed within the chosen scope. Branch managers need branch-level views and system administrators/directors need consortium-level overviews. Acceptance hints: when a single branch is selected, totals and percentages are computed only from that branch's data; when the consortium is selected, totals and percentages are computed across all branches.

### REQ-022 — Date range filtering (including quarters)

- **Priority:** Must — Core function: date range filtering is essential for relevant circulation data analysis.
- **Derived from:** D03 (conversations\conv_pines016_shelf_space.eml)

The system must allow the user to filter the Shelf Space Report by an arbitrary date range for circulation data (start and end dates) and provide convenience options for common reporting periods such as quarters (e.g., Q1, Q2). Directors and managers use time filtering to compare seasonal or quarterly utilization. Acceptance hints: circulation-derived percentages change according to the selected date range; preset quarter options produce the equivalent start/end dates.

### REQ-023 — Comparison view across libraries (side-by-side)

- **Priority:** Should — High value: side-by-side comparisons are useful for managers to visually assess allocations.
- **Derived from:** D03 (conversations\conv_pines016_shelf_space.eml)

The system must provide a comparison view that displays each library's genre/format breakdown side-by-side so users can compare libraries at a glance. Directors and managers need this to spot branches with unusually high or low allocation or usage. Acceptance hints: for a system-level run, the comparison view shows a column or pane per library with the same set of genre/format metrics, allowing visual comparison across libraries (e.g., each library's percentage-of-circulations and percentage-of-collection for a selected genre).

### REQ-024 — Compute item counts by genre/format

- **Priority:** Must — Core function: computing item counts is essential for accurate collection metrics.
- **Derived from:** D03 (conversations\conv_pines016_shelf_space.eml)

The system must compute and expose the number of items (item count) for each genre and format combination within the selected scope and date-independent context (i.e., collection size). Catalogers and report consumers need item counts to derive the 'percentage of collection' metric. Acceptance hints: item counts used in the report must match database inventory counts for the selected library or system scope and be included in the report or available for drill-down.

### REQ-025 — Compute checkouts by genre/format

- **Priority:** Must — Core function: computing total checkouts is critical for understanding circulation metrics.
- **Derived from:** D03 (conversations\conv_pines016_shelf_space.eml)

The system must compute and expose the total number of checkouts (sum of circulations) for each genre and format combination within the selected scope and date range. Report users require this to derive the 'percentage of total circulations' metric. Acceptance hints: checkout totals must be calculated from circulation transaction records and must reflect the selected date range; the report must show the raw checkout counts in addition to the derived percentages.

### REQ-026 — Estimate shelf space per genre/format with fallback

- **Priority:** Should — Workaround exists: staff can estimate shelf space manually based on item data.
- **Derived from:** D03 (conversations\conv_pines016_shelf_space.eml)

Because explicit shelf-space measurements are not tracked, the system must estimate shelf space used by each genre/format using available item data: when item dimensions (e.g., width/height/depth or linear length) are present, compute a dimensions-based shelf-space estimate; when dimensions are unavailable, provide an item-count-based proxy estimate. Report consumers need an estimate of percentage of shelf space for planning reallocations. Acceptance hints: the report must include the shelf-space estimate value per genre/format and indicate which estimation method (dimensions or count proxy) was used for each calculation; documented methodology must be included or accessible.

### REQ-027 — Provide system-average alongside branch metrics

- **Priority:** Must — Stakeholders call it critical: branch managers need system-level averages for comparison.
- **Derived from:** D03 (conversations\conv_pines016_shelf_space.eml)

When viewing a branch's Shelf Space Report, the system must present the corresponding system-level average (or system aggregate percentages) for the same metrics so branch managers can directly compare local values to the system norm. Branch managers and directors need this comparison to identify outliers and justify reallocation. Acceptance hints: the branch report displays both the branch metric and the system-level metric side-by-side (or in an adjacent column) for each genre/format and metric.

### REQ-028 — Query builder for candidates

- **Priority:** Must — Stakeholders call it critical: cataloging staff need query builder for selecting transfer materials.
- **Derived from:** D04 (conversations\conv_pines018_item_transfer.eml)

The system must provide a query builder for selecting candidate materials to transfer. Cataloging and circulation staff will use this to locate items by criteria (e.g., genre, circulation age) so they can assemble transfer sets; acceptance can be demonstrated by building queries that return expected result sets (for example: all items in genre X not circulated in 6 months).

### REQ-029 — Save and share queries

- **Priority:** Must — Stakeholders call it critical: staff require saving and sharing query definitions for efficiency.
- **Derived from:** D04 (conversations\conv_pines018_item_transfer.eml)

The system must allow users to save query definitions for repeated use and to share saved query templates with other staff. Staff who regularly run monthly or event-based transfers must be able to reuse a saved query (e.g., monthly move of items in genre X not circulated in 6 months) or run a colleague's shared template; acceptance is shown by saving a query, re-running it later, and granting another user access to that saved template.

### REQ-030 — Manual selection from results

- **Priority:** Must — Stakeholders call it critical: manual selection of query results is essential for transfer accuracy.
- **Derived from:** D04 (conversations\conv_pines018_item_transfer.eml)

After running a query the system must allow manual selection of any subset of returned items (e.g., check boxes to pick 25 of 100 results). Staff users need this to refine candidate sets before transfer; acceptance is shown by selecting particular items from a query result set and proceeding with only the selected items.

### REQ-031 — Batch administrative item operations (transfer/move/delete) with safety and performance

- **Priority:** Must — Stakeholders call it critical: batch operations are vital for administrative efficiency.
- **Derived from:** D04 (conversations\conv_pines018_item_transfer.eml), D10 (early_draft_srs_galecia.txt), D20 (survey_results_2009.txt)

The system shall support administrative batch operations for items/volumes, including batch item transfer/moving and targeted administrative selection. It must provide a batch transfer utility enabling candidate querying, saving queries, manual selection from query results, changing the location field, generating pull lists, and configured automated revert to original location after a set period; it must also support batch updates to the item location field with transaction safety (all-or-nothing rollback on failure). Administrators/authorized staff must be able to manually select records from query results for batch operations (e.g., move location/delete) with multi-select, batch invocation, and confirmation. For large-scale transfer operations (up to 9.6M items), operations must be processed in smaller batches to avoid long DB locks and unacceptable service impact. Additionally, the system must attach fines/charges/waivers/e-commerce transactions to patron/item records and allow staff queries for patron accounts with balances greater than a configurable threshold X (per-library tracking) as part of administrative financial-related workflows tied to record operations.

### REQ-032 — Store original location metadata

- **Priority:** Must — Stakeholders call it critical: original location metadata is needed for reliable item reversion.
- **Derived from:** D04 (conversations\conv_pines018_item_transfer.eml)

When items are transferred, the system must record and retain each item's original location (and related transfer metadata) so items can be reverted to that original location later. Transfer coordinators need preserved original-location data for reliable reversion; acceptance is verified by inspecting an item's transfer record to see the stored original location after a transfer.

### REQ-033 — Pull list generation

- **Priority:** Must — Stakeholders call it critical: printable pull lists are required for staff to gather items.
- **Derived from:** D04 (conversations\conv_pines018_item_transfer.eml)

The system must be able to generate printable pull lists of items to be moved (a human-readable list of titles/barcodes/locations). Circulation and shelving staff require pull lists to physically gather items; acceptance is generation of a printable list containing the expected items and fields shown in examples.

### REQ-034 — Printable transit labels

- **Priority:** Must — Stakeholders call it critical: transit labels are necessary for packaging and scanning items.
- **Derived from:** D04 (conversations\conv_pines018_item_transfer.eml)

The system must be able to produce printable transit labels (including barcodes) for items included in a transfer. Staff handling physical movement need labels for packaging and scanning; acceptance is printable labels for transferred items that include a scannable barcode and required identifying text.

### REQ-035 — Auto-revert by time period

- **Priority:** Must — Stakeholders call it critical: auto-reverting items supports efficient inventory management.
- **Derived from:** D04 (conversations\conv_pines018_item_transfer.eml)

The system must support auto-reverting transferred items to their original location after a configurable time period (for example, 30 days or X days). Transfer coordinators and program organizers need temporary transfers to expire automatically; acceptance is configuration of a per-transfer expiry and observed automatic reversion of items when the period elapses.

### REQ-036 — Auto-revert transfer rules (event/status criteria)

- **Priority:** Should — Workaround exists: items can be reverted manually based on statuses.
- **Derived from:** D04 (conversations\conv_pines018_item_transfer.eml)

The system shall support auto-revert behavior based on configurable event/status criteria for transfers, allowing automatic reversion when specific item status/event is detected (e.g., revert on status change to 'sold' or 'returned'). Additionally, configuration must support suppressing reversion for exceptions—for example, do not revert items checked out at the destination (items checked out at destination remain there). Acceptance requires creation of rules keyed to item status/event and demonstration that suppressed reversion exceptions prevent revert when checkout at destination occurs.

### REQ-038 — Scheduled report runs and automated background jobs

- **Priority:** Should — Workaround exists: reports can be run manually without scheduling.
- **Derived from:** D04 (conversations\conv_pines018_item_transfer.eml), D06 (conversations\conv_pines021_item_purging.eml), D10 (early_draft_srs_galecia.txt), D20 (survey_results_2009.txt)

The system shall support scheduling for both reports and related automated background tasks. For reports, users can run recurring schedules such as Run ASAP, Hourly, Daily, Weekly, Monthly, and Yearly, and define delivery options so periodic data is delivered automatically. Separately, the system must allow scheduled purging/candidate report runs with recurrence settings and criteria sets, returning results/notifications on completion while still enforcing a separate confirmation step for destructive deletion unless explicitly configured. For transfers, the system must include a scheduled background task to periodically evaluate transferred items and apply auto-revert rules (time-based or event-based) as a configurable scheduled job with evaluation criteria and action logging.

### REQ-039 — Immediate undo function

- **Priority:** Must — Stakeholders call it critical: undo functionality is essential for recovering from errors.
- **Derived from:** D04 (conversations\conv_pines018_item_transfer.eml)

The system must provide an immediate undo capability to reverse a recent transfer operation (a user-initiated rollback) so accidental moves can be undone without waiting for auto-revert. Staff need to recover from mistaken operations quickly; acceptance is performing an undo action that restores items to their prior recorded locations and records the undo in the audit log.

### REQ-040 — Security groups/roles administration and enforcement

- **Priority:** Must — Stakeholders call it critical: access control is essential for system security.
- **Derived from:** D04 (conversations\conv_pines018_item_transfer.eml), D10 (early_draft_srs_galecia.txt), D13 (email_staff_login.eml), D16 (interview_sysadmin_2009-05-10.txt)

The system shall control access through security groups and/or roles assignable to individuals, workgroups (predefined operational groups), and arbitrary staff groups, with administrative UI to create/modify/delete roles/groups, assign/revoke role/group permissions to users and groups, and enforce permissions during operation. Acceptance includes defining roles with permissions, assigning users and groups to roles, immediate permission changes, and denying access to restricted utilities (e.g., transfer utility functions) for users lacking designated roles.

### REQ-041 — Transfer history and audit logging

- **Priority:** Must — Stakeholders call it critical: transfer history is essential for auditing purposes.
- **Derived from:** D04 (conversations\conv_pines018_item_transfer.eml)

The system must provide transfer history and auditability for items: it must log all transfer actions and maintain per-item persistent history entries (timestamp, user, source, destination), and it must support reporting/queries or an item view that lists past transfers with a summary count (e.g., number of transfers in the past year) and returns the item’s transfer events for historical reporting and auditability.

### REQ-043 — Preview and confirmation dialog

- **Priority:** Must — Stakeholders call it critical: confirmation dialog is necessary to prevent accidental changes.
- **Derived from:** D04 (conversations\conv_pines018_item_transfer.eml)

Before making any bulk changes, the system must present a preview showing details (e.g., number of items, source branch, destination branch, and example titles) and require explicit confirmation to proceed. Staff need to verify actions before applying potentially large updates; acceptance is that a preview is displayed and the system performs no updates until the user confirms.

### REQ-044 — Transfer delay and issue alerts

- **Priority:** Must — Stakeholders call it critical: alerts for delays are essential for timely problem resolution.
- **Derived from:** D04 (conversations\conv_pines018_item_transfer.eml)

The system must provide alerts or notifications when a transfer is delayed or encounters issues (for example, transfer processing errors or items not found). Transfer coordinators need prompt notification to address problems; acceptance is generation of a user-visible notification or configurable alert when a transfer job reports delays or failures.

### REQ-046 — Integration with existing query tools

- **Priority:** Should — Workaround exists: existing tools can be used in place of integration.
- **Derived from:** D04 (conversations\conv_pines018_item_transfer.eml)

The transfer utility's query capability must integrate with or reuse the existing report/query tool functionality so users have equivalent query power and avoid duplicating query-defining work. Reporting and cataloging staff need a consistent query experience; acceptance is the ability to create transfer queries using the same features/criteria available in the existing report query tool or import saved report queries into the transfer utility.

### REQ-047 — Temporary transfer by event scheduling

- **Priority:** Must — Stakeholders call it critical: transferring based on events is essential for program management.
- **Derived from:** D04 (conversations\conv_pines018_item_transfer.eml)

The system must allow creation of transfers tied to a specific event or program period (for example, transfer items to a community center for a genealogy workshop and revert after the event). Program staff need to schedule location changes with explicit start and end dates; acceptance is scheduling a transfer with event start/end dates and observing automatic reversion at the configured end date.

### REQ-048 — Missing and damaged items reports by branch with detail + summary + filtering

- **Priority:** Should — Workaround exists: staff can manage missing/damaged items manually.
- **Derived from:** D05 (conversations\conv_pines019_020_missing_intransit.eml), D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt)

The system shall provide Missing and Damaged Items reporting at the branch level so branch inventory/audit/collection staff can identify and manage missing and damaged items. The report must include item-level details (e.g., title, barcode, branch, status such as missing/lost, reported date, and condition notes like water damage or vandalism), summary counts (total missing, total damaged), and support grouping/aggregation (e.g., counts by title and by branch) with filtering by item status (including at minimum missing and lost) and by date range (e.g., last 30 days/last quarter). Acceptance includes running for a single branch with both detailed list and summary counts, supporting selected date ranges, and grouping/sorting to show frequently lost titles.

### REQ-049 — In-transit items aging report with configurable X and merged directions

- **Priority:** Should — Workaround exists: staff can identify delayed transfers via manual checks.
- **Derived from:** D05 (conversations\conv_pines019_020_missing_intransit.eml), D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt), D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

The system shall provide in-transit item reports that identify items that have been in-transit longer than a configurable threshold X days, with results available both per branch and across the entire system. The reports must merge transit-to and transit-from directions into a single easy-to-read list/view so staff can chase delayed transfers without running separate reports. Acceptance includes making X configurable (default suggested 7 days where stated), returning items currently in transit exceeding X days using the transit record logic (e.g., arrival_date IS NULL and departure_date <= today - X days), presenting transit-to and transit-from entries together (including routing/destination/origin fields and expected delivery status where applicable), and supporting sorting by due/date.

### REQ-050 — Customizable purging criteria builder

- **Priority:** Must — Stakeholders call it critical: purging criteria are essential for inventory management.
- **Derived from:** D06 (conversations\conv_pines021_item_purging.eml)

The system must provide a configurable filter/builder that identifies item records that are candidates for purging based on user-defined criteria. Staff users (cataloging/collection management) will use this to locate items to remove during weeding; criteria must include status values (e.g., 'missing', 'discard/weed', 'damaged'), time-in-status thresholds (e.g., in status for X months/years), and activity/usage thresholds (e.g., last circulated more than X days/months/years). Acceptance hints: users can create, save and reuse criteria sets, specify numeric durations (days/months/years), and run the filter to return a result set of candidate item records.

### REQ-051 — Combinable logical criteria

- **Priority:** Should — Workaround exists: staff can manually combine criteria without logical operators.
- **Derived from:** D06 (conversations\conv_pines021_item_purging.eml)

The system must allow users to combine multiple purging criteria using logical operators so compound conditions can be expressed (for example: status = 'missing' for >6 months AND last circulation >2 years, or damaged AND last circulation >2 years). Cataloging and collection staff need this to express real-world weeding rules. Acceptance hints: the builder must support AND/OR grouping with parentheses and produce deterministic results matching the composed condition.

### REQ-052 — Bulk status conversion for item records

- **Priority:** Should — Workaround exists: status can be changed individually without bulk operations.
- **Derived from:** D06 (conversations\conv_pines021_item_purging.eml), D15 (interview_cataloging_2009-05-08.txt)

The system shall support bulk operations to change the status of many item records at once (including examples like converting 100 items from 'missing' to 'discard/weed'), where selection can come from a report/query or an upload/list. Acceptance requires selecting items, previewing candidates/items to be changed, specifying the target status, applying the change to all selected items as one operation, scaling to hundreds, and producing a summary of affected records.

### REQ-053 — Read-only candidate reports

- **Priority:** Could — Nice to have: read-only reports improve safety, but are not critical.
- **Derived from:** D06 (conversations\conv_pines021_item_purging.eml)

Reports that list candidates for purging must be read-only by default so staff can safely review results before any destructive action. Collection managers and catalogers need a safe way to inspect candidates. Acceptance hints: running a purging criteria returns a non-editable report view that supports sorting, filtering and exporting but does not perform deletions or status changes directly from the view.

### REQ-054 — Separate confirmation step for deletions

- **Priority:** Must — Critical functionality: Prevents accidental mass deletion, ensuring data integrity.
- **Derived from:** D06 (conversations\conv_pines021_item_purging.eml)

The system must require an explicit, separate confirmation step before performing any destructive operation (deleting items, deleting volumes, or deleting records), distinct from generating candidate reports. Cataloging staff need the extra confirmation to avoid accidental mass deletion. Acceptance hints: after initiating a delete, the system displays a list of items/records to be deleted, requires the user to confirm (e.g., a Confirm button and an acknowledgement), and only then executes the deletion.

### REQ-055 — Deletion/audit trails with immutable logging and evidence reporting

- **Priority:** Must — Regulatory obligation: Provides essential audit trail for deletions for compliance purposes.
- **Derived from:** D06 (conversations\conv_pines021_item_purging.eml), D07 (conversations\conv_pines022_deletions.eml), D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt), D20 (survey_results_2009.txt)

The system shall provide immutable auditing for deletions and purge/bulk operations, including persistent audit table entries recorded via a trigger/equivalent mechanism with required fields. Deletion audit entries must include record_type (item/patron/bib/other), record_id, deleted_by (user id/name), deleted_at (timestamp), location (branch/origin of acting user), and prior_status or deletion_reason when available; audit trails must also be queryable and exportable and support before/after state for status changes or deletion events. The system must also track and report deletion counts/lists by location/branch and across the system with required reasons/categories, support compliance-oriented proof reporting producing dated statements/counts filtered by record type/location, and preserve audit row persistence/queryability after source record removal with correct field/value recording.

### REQ-056 — Last-copy identification report with scope

- **Priority:** Must — Essential for avoiding loss: Necessary for catalogers to ensure no sole copy is deleted.
- **Derived from:** D06 (conversations\conv_pines021_item_purging.eml)

The system must provide a 'last copy' report that determines, for each item record, whether it is the only copy within a selectable scope (per library branch or per entire system/consortium) and flags such items. Catalogers need this to avoid deleting the sole copy and to update WorldCat holdings. Acceptance hints: the report must allow users to choose scope (single library or entire system), list flagged items, and include sufficient identifying information (bibliographic and holding identifiers and library/branch) so catalogers can act on WorldCat entries.

### REQ-057 — Bulk deletion of volumes and orphan biblios

- **Priority:** Should — High value: A workaround exists but a manual process is needed to conduct bulk deletions.
- **Derived from:** D06 (conversations\conv_pines021_item_purging.eml), D15 (interview_cataloging_2009-05-08.txt)

Provide a fast bulk-delete utility to delete volume entries together with their associated copy/item entries and to identify and delete bibliographic records with no items (orphans). Acceptance requires the utility allow selection of volumes/records for deletion, show dependent copies/items that will be removed (including listing zero-associated-item bibliographic records), support bulk execution with required confirmation, and include audit logging.

### REQ-061 — Log denied deletion attempts

- **Priority:** Must — Security monitoring: Captures and logs denied attempts for compliance and security needs.
- **Derived from:** D07 (conversations\conv_pines022_deletions.eml)

The system must log attempted deletions that are denied (permission failure or system policy) into an audit/attempt table recording: attempted target (record_type and record_id), attempted_by, attempted_at (timestamp), location, and reason for denial. This enables compliance and security monitoring to detect improper deletion attempts. Acceptance hints: when a user attempts a deletion and the system denies it, an audit entry is created containing the target, user, timestamp, location, and denial reason.

### REQ-062 — Report interface to query audits

- **Priority:** Must — Critical for troubleshooting: Enables staff to query and verify deletion audit data.
- **Derived from:** D07 (conversations\conv_pines022_deletions.eml)

The system must provide a report/query interface that allows staff/administrators to query the deletion audit data (both successful deletions and denied attempts). The interface should allow viewing of audit rows and retrieving details (all audit fields) for inspection and troubleshooting. Acceptance hints: an administrative user can run a query in the interface and see the audit rows with record_id, record_type, deleted_by/attempted_by, deleted_at/attempted_at, location, and prior_status/reason.

### REQ-063 — Filtering and aggregation options

- **Priority:** Should — High value: Filtering and aggregation improve usability but manual queries can be used.
- **Derived from:** D07 (conversations\conv_pines022_deletions.eml)

The reporting interface must support filtering and aggregation of deletion audit data by date range, user, record type, location (branch), and system-wide scope so staff can produce counts and summaries per location or for the entire system. This supports auditing and process analysis (e.g., find deletions by a particular user or branch). Acceptance hints: the report UI or query returns results restricted to selected filters and can aggregate (counts) grouped by the chosen dimensions.

### REQ-064 — Deletion volume reports

- **Priority:** Must — Required reporting: Tracks deletions and identifies top deleting users for auditing.
- **Derived from:** D07 (conversations\conv_pines022_deletions.eml)

The system must provide deletion (successful delete) reporting for administrators, including (1) a ranked “Top deleting users” report sorted by deletion count over a selectable time period and scope (branch or system-wide), and (2) deletion totals for standard reporting periods (monthly, quarterly, yearly) where a user can request deletion totals for a specified month/quarter/year and the system returns the correct count(s) filtered by record type and/or location as requested (e.g., “all patron records deleted in Q1” or monthly deletion tallies).

### REQ-066 — Trace deletion by record ID

- **Priority:** Must — Essential functionality: Allows tracking of deletion events for accountability.
- **Derived from:** D07 (conversations\conv_pines022_deletions.eml)

The system must allow staff to locate the deletion audit entry for a specific record (searchable by record_id) so they can answer 'why did this patron's record disappear?'. The trace view should show the audit fields (who, when, where, prior_status/reason). Acceptance hints: searching the audit table by a record's id returns the exact deletion event(s) for that record with complete details.

### REQ-068 — Filter and group by demographics

- **Priority:** Could — Nice to have: Enhances report targeting but is not critical to functionality.
- **Derived from:** D08 (conversations\conv_pines023_patron_characteristics.eml)

The system shall allow a staff user to limit (filter) reports and to GROUP BY (aggregate) using the following patron characteristics: age range, zip code, county of residence, home branch, patron type, and preferred language. This is needed so staff can run targeted program-planning and reporting (for example, counts of patrons or circulation grouped by home branch or language). Acceptance hints: a report builder or query interface must permit selecting any of these fields as a filter and/or grouping key and return matching records or aggregated results accordingly.

### REQ-069 — Age/inactivity filtering using derived age and configurable age ranges with exclusions

- **Priority:** Should — High value: Useful for reporting but can be worked around without strict age filtering.
- **Derived from:** D08 (conversations\conv_pines023_patron_characteristics.eml), D09 (conversations\conv_pines024_inactive_patrons.eml)

The system shall compute patron age at query time from birth_date and assign patrons into configurable age brackets/intervals defined per report (with age-range configuration exposed in the report definition). Inactivity/targeting logic shall consider electronic activity in addition to physical circulation, counting OPAC/patron-account logins, online hold placements, online renewals, and logged digital-collection accesses, treating those electronic events equivalently to circulation events when computing a last-activity timestamp; inactivity reports then list patrons whose most-recent activity (circulation or electronic) is older than a configurable X-day window (with preset examples like 30/90/180/365) or who have no activity, and must include last-activity date. The system shall support filtering patrons based on activity/inactivity time windows combined with other demographic filters, and allow configurable exclusion filters to omit exempt patrons based on patron-record attributes/flags (e.g., do-not-disturb, VIP status, staff accounts, opt-out communications) so excluded patrons do not appear in generated lists/exports when selected.

### REQ-071 — Combine filters with AND/OR logic

- **Priority:** Should — Enhances reporting: Allows complex queries to be expressed but not essential.
- **Derived from:** D08 (conversations\conv_pines023_patron_characteristics.eml)

The system shall allow staff users to combine multiple filters across demographic and other fields using AND and OR logical operators. This is needed so complex queries can be expressed (for example, juvenile patrons in zip code 30505 who also meet an activity condition). Acceptance hints: the query builder must permit combining two or more filter clauses with selectable AND/OR semantics and return records that match the combined expression.

### REQ-072 — Include null/blank field values in results

- **Priority:** Must — Data integrity: Ensures no data is omitted in reports, crucial for accuracy.
- **Derived from:** D08 (conversations\conv_pines023_patron_characteristics.eml), D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt), D20 (survey_results_2009.txt)

The reporting system must include null and blank field values in report outputs when requested (and/or by default), rather than omitting them, so exports preserve missing data for analysis. This includes including empty/null cells in visible results and exports, providing explicit null/blank markers or categories (e.g., an explicit “null” or visible blank) for optional demographic fields (such as when a chosen field is missing), and ensuring downstream processing sees those empty values consistently across filtering and display selections.

### REQ-073 — Aggregate circulation/checkout counts

- **Priority:** Could — Convenient: Analysis of borrowing behavior is helpful but not essential.
- **Derived from:** D08 (conversations\conv_pines023_patron_characteristics.eml)

The system shall be able to compute and present aggregate circulation metrics (for example checkout counts) and group those aggregates by one or more demographic fields (for example checkout counts grouped by age range). This is needed so staff can analyze borrowing behavior across demographic segments for program planning and collection development. Acceptance hints: reports must provide aggregate functions (counts/sums) over circulation transactions and permit GROUP BY on selected demographic fields.

### REQ-075 — Source demographic fields from patron table

- **Priority:** Must — Data sourcing: Ensures reports use authoritative data for accurate reporting.
- **Derived from:** D08 (conversations\conv_pines023_patron_characteristics.eml)

The system shall source the named demographic fields (birth_date for age computation, zip code, county, home branch, patron type, preferred language) from the patron table as the canonical data source for these reports. This is needed because the referenced fields exist in the patron table and reports must reflect the authoritative values. Acceptance hints: report metadata or implementation documentation should indicate the patron table columns used for each reported demographic field.

### REQ-078 — Aggregate events across sources

- **Priority:** Must — Critical functionality: Essential for accurate reporting across multiple data sources.
- **Derived from:** D09 (conversations\conv_pines024_inactive_patrons.eml)

The system must aggregate activity records stored in multiple tables and/or systems to compute a single per-patron most-recent-activity timestamp. This is required because electronic activity and circulation events may be stored in separate tables. Acceptance hints: the report logic must query all relevant event tables (e.g., circulation transactions, OPAC login events, online holds/renewals, digital-access logs) and use the latest timestamp among them as the patron's last activity.

### REQ-079 — Configurable scope and grouping levels

- **Priority:** Should — Valuable for administrative tasks: Configurable reports improve analysis but not critical.
- **Derived from:** D09 (conversations\conv_pines024_inactive_patrons.eml)

The report must be configurable by scope level so staff users can run it at consortium, home branch, county, or other administrative levels. This lets system administrators identify branches with the most inactive patrons and branch staff focus on their home-branch lists. Acceptance hints: the UI or report parameters allow selecting scope level and the report supports GROUP BY or equivalent aggregation; when run at consortium level the report includes counts of inactive patrons per home branch.

### REQ-080 — Include current mailing addresses

- **Priority:** Must — Required for outreach: Current mailing addresses are necessary for effective communication.
- **Derived from:** D09 (conversations\conv_pines024_inactive_patrons.eml)

Because the list is used for outreach (postcard mailings), the report must include each patron's current mailing address. This is required for outreach staff to prepare and mail notifications. Acceptance hints: the export and on-screen report include the patron's current mailing address fields (street, city, state, postal code) as stored in the patron record, and the system uses the most-recent address on file.

### REQ-081 — Flag or separate patrons with fines

- **Priority:** Should — High value: Identifies patrons with financial obligations but a manual check can be performed.
- **Derived from:** D09 (conversations\conv_pines024_inactive_patrons.eml)

The report must identify patrons who are inactive but have outstanding fines or balances and allow them to be handled separately. This supports different workflows for accounts with monetary obligations. Acceptance hints: the report shows a fine-balance field or a clear 'outstanding fines' flag for each patron and can filter or produce a separate list containing only patrons with non-zero balances.

### REQ-083 — CSV export for outreach systems

- **Priority:** Should — Useful capability: Enables integration with outreach systems but can be handled manually.
- **Derived from:** D09 (conversations\conv_pines024_inactive_patrons.eml)

The report must be exportable in CSV format so libraries can upload the list to outreach or mailing systems. The exported CSV must include at least the report's key fields required for outreach: patron name, current mailing address, last-activity date, home branch, and an indicator of outstanding fines or exclusion flags. Acceptance hints: staff users can download the CSV from the report UI or schedule exports, and the CSV column set is documented and consistent to allow automated uploads.

### REQ-084 — Asynchronous/background processing for long/concurrent reports

- **Priority:** Must — Operational necessity: Enables background processing of reports without disrupting services.
- **Derived from:** D09 (conversations\conv_pines024_inactive_patrons.eml), D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D16 (interview_sysadmin_2009-05-10.txt)

The system shall support running long-running reports asynchronously as background jobs and must also process searches/reports during open hours without disrupting other system functions, using acceptable performance. For asynchronous jobs, acceptance requires immediate return of job status/ID, job lifecycle management (IDs, completion/failure notifications), caching of results with job status/cached result metadata (e.g., last-run timestamp), polling/notification mechanisms, and cancellation/completion handling without blocking interactive operations. For open hours, acceptance requires representative report workloads while OPAC/circulation continues within stakeholder-defined acceptable response-time thresholds.

### REQ-085 — Performance scalability for large datasets

- **Priority:** Must — Performance requirement: Necessary to handle large datasets effectively.
- **Derived from:** D09 (conversations\conv_pines024_inactive_patrons.eml)

The inactive-patrons report must be designed to perform acceptably at scale (example scale noted: ~3.5 million patrons). This includes query optimization and consideration of indexing, materialized views, or pre-aggregated data to make report runs feasible. Acceptance hints: typical scheduled runs complete within operationally acceptable windows (per-site SLA), background execution does not unduly impact transactional operations, and architects have options (caching, incremental updates) to reduce full-table scans.

### REQ-086 — Support consortium scale

- **Priority:** Must — Scalability: Essential to support consortium size and workload without performance issues.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

The system must support a large library consortium scale as described (example: 286 locations, 17 million annual circulations, and purchasing/processing over 900,000 items per year). Library administrators and IT staff need this to ensure the system handles expected data volumes and workloads; acceptance can be tested by demonstrating equivalent data loads and sustained operations at that scale without data loss.

### REQ-088 — Server OS compatibility (Linux and Solaris)

- **Priority:** Should — Compatibility: Important for deployment but can use alternative setups if necessary.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

The system shall operate on Linux or Solaris server environments. Acceptance requires installation and operation verified on at least one Linux distribution and on Solaris, with installation packages and successful deployment on both platforms.

### REQ-089 — Client access modes (web browser and Windows client)

- **Priority:** Must — Critical access: Required for users to function effectively across different platforms.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

The system must be accessible via a web browser and/or a Windows-compatible client application so staff/managers can use supported workstations, including feature parity documentation/known differences across modes. Acceptance requires demonstrating full functionality using a supported browser and a Windows client, and ensuring both access modes provide fully functional workflows with documented parity/differences.

### REQ-090 — Browser compatibility (IE6+ and Firefox2+)

- **Priority:** Should — Workaround exists: browser-specific issues can be manually addressed.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D16 (interview_sysadmin_2009-05-10.txt), D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

If web-browser based, the system must support Microsoft Internet Explorer 6.0+ and Mozilla Firefox 2.0+ for user workflows. Acceptance requires UI/workflows (e.g., login, running reports, viewing/downloading results, configuring templates) to function correctly in IE6 and Firefox 2.0 on representative workstations, with documented browser-specific workarounds as needed.

### REQ-091 — Accessibility compliance for UI and help

- **Priority:** Must — Accessibility obligation: compliance with WCAG is essential.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D18 (meeting_minutes\meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

The reporting interface (including the web UI and help system) shall comply with recognized accessibility standards (e.g., WCAG) so staff with disabilities can use report creation, scheduling, and viewing. Accessibility must include keyboard navigation, screen-reader compatibility/assistive-technology support, and sufficient color contrast, with acceptance demonstrating pass/follow accessibility checks (including common screen-reader tests and verified contrast) for both UI elements and help pages.

### REQ-092 — Relational backend and PostgreSQL support

- **Priority:** Must — Essential function: supporting a relational backend is critical for operations.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D16 (interview_sysadmin_2009-05-10.txt), D18 (meeting_minutes\meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

The reporting system must support the existing normalized relational database schema and complex joins, and must use a fully relational backend with relational integrity and ACID-compliant operations. Current-state reports shall query that schema or a relational read replica; they shall not require a denormalized reporting schema or ETL copy. Historical reports may use snapshots, a historical warehouse, or an equivalent mechanism to preserve past states. The system must be compatible with PostgreSQL as used by PINES, including the ability to connect to PostgreSQL 8.3, execute complex read queries, and return correct results without requiring schema changes.

### REQ-093 — Standards-compliant HTML output

- **Priority:** Should — Workaround exists: can produce reports with non-compliant HTML but may face rendering issues.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D18 (meeting_minutes\meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

Web-based components must produce standards-compliant HTML output so browser rendering and accessibility are reliable. Acceptance: validate representative pages against HTML standards (e.g., W3C) and show results.

### REQ-094 — Development and training environment

- **Priority:** Must — Essential function: required to ensure safe environment for changes.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

The system must provide a development and training environment with the ability to migrate configurations to a production environment so administrators can test changes safely; acceptance: demonstrate export/import of configuration and successful promotion from training to production.

### REQ-097 — Record data specifications provided

- **Priority:** Should — Workaround exists: documentation can be provided manually, though it's not ideal.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Developer must provide complete data specifications for authority records, bibliographic records, order records, item records, hold/request records, and other records accessed by Management Processes so system integrators and reporting tools can map fields correctly; acceptance: deliver a data dictionary covering all record types and fields.

### REQ-098 — High-level process documentation

- **Priority:** Should — Workaround exists: basic process information can be provided without detailed documentation.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D18 (meeting_minutes\meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

Developer must provide a thorough high-level description of major processes (including bibliographic import/export, validation against authority sources, and standard reports) to support configuration and training; acceptance: provide process flow documents and examples of import/export operations and validation behavior.

### REQ-099 — Online hierarchical cross-linked HTML help

- **Priority:** Must — Essential function: a help system is critical for user support.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D16 (interview_sysadmin_2009-05-10.txt), D18 (meeting_minutes\meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

The system must provide an online, hierarchical, cross-linked HTML help system integrated into the application, with contextual/help links available in relevant UI screens and documentation for major functions and report-building workflows. Help content must be searchable where specified, and support users/admins finding instructions for running/configuring reports without contacting IT; acceptance includes verifying HTML hierarchical/cross-linked pages, in-application links, navigation, coverage, and (for the searchable variant) full-text search returning relevant help topics.

### REQ-100 — Admin/user error reporting with query diagnostics

- **Priority:** Must — Essential function: thorough error reporting is critical for troubleshooting.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D18 (meeting_minutes\meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

The system shall provide thorough error reporting and user-facing feedback with understandable, actionable messages for both Local and Global System Administrators, including low-level query-specific diagnostics for troubleshooting. Acceptance requires error messages that include actionable details plus admin-accessible logs/drilldowns for query errors, front-end interfaces to view error details, and administrative query logs demonstrating detailed query diagnostics; user-level error reports should include context and suggested next steps for common failure cases.

### REQ-101 — Centralized multi-location management/reporting

- **Priority:** Must — Essential function: centralized reporting is critical for library management.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D18 (meeting_minutes\meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

Management processes and reporting shall be consolidated at a central location and accept input from, and provide services to, multiple library locations/branches across the consortium as a single source of truth. Acceptance requires centralized services/data aggregation and the ability to operate via remote access from multiple branch endpoints, including simulated branches to demonstrate system-wide management/reporting across locations.

### REQ-102 — Interface with vendor websites and data formats

- **Priority:** Must — Essential function: interfacing with vendor data is necessary for acquisitions.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

The system must interface with a variety of vendor websites via published APIs and/or automated transfer of standard-format data files (e.g., USMARC21, EDIFACT) to support acquisitions and vendor integrations; acceptance: implement sample import/export using at least one vendor API and one standard-format file transfer.

### REQ-103 — OPAC interaction reflected in management reports

- **Priority:** Should — Workaround exists: reporting can function based on non-OPAC data but isn’t optimal.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

Management/reporting must interact with the OPAC/patron interface so patron-initiated transactions and holds are reflected in management reporting. Reports that query patron-derived data (e.g., holds and circulation) must produce expected results for activity initiated in the OPAC, and the interface/data integration points used to access those patron-created data must be documented.

### REQ-104 — Staff login options

- **Priority:** Should — Workaround exists: staff can log in using alternative methods if card-based login is not available.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

The system should support streamlined staff login methods including card-swipe (e.g., RFID badge) and username/password, and must not require card-based login so staff can use fallback credentials; acceptance: demonstrate staff login using a badge and using username/password and ability to configure allowed methods.

### REQ-105 — Report template creation, distribution, and field locking

- **Priority:** Must — Essential function: standardized report templates are critical for consistent reporting.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml), D14 (evergreen_reference_2009.txt), D17 (meeting_minutes\meeting_2009-03-15_minutes.txt), D20 (survey_results_2009.txt)

Administrators shall be able to create, store, and distribute standardized report templates to libraries/branches so libraries can consistently produce required reports; templates must be runnable as-is or clonable/modified within administrator-defined limits, and staff can run or instantiate reports from them. Templates support integrity controls by locking specific filters and display fields so non-admins can only change allowed parameters (e.g., allow editing certain filters like call-number-range or changing allowed display columns while preventing changes such as showing deleted items). Central management includes pushing/applying templates to one or more libraries, with acceptance covering template creation/publishing, staff execution using defaults unless permitted parameters are changed, and enforcement that locked elements cannot be altered.

### REQ-106 — Report creation and cloning permissions

- **Priority:** Must — Essential function: distinct permission levels are critical for security and management.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

The system must provide distinct, fine-grained permission levels that limit who can create and clone reports and be easy to administer; administrators must be able to create shared folders to control who can run specific reports or run ad hoc reports on specific data sets; acceptance: configure roles and shared folders and verify enforced permissions for create/clone/run operations.

### REQ-107 — Graphical query builder with field/regex/boolean controls

- **Priority:** Should — Workaround exists: complex queries can be constructed manually, though it's cumbersome.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml), D14 (evergreen_reference_2009.txt)

The system shall provide a user-friendly query design/build interface for creating queries across all record types (e.g., bibliographic, item, patron, transaction/financial) that allows selecting record type(s), choosing fields to include, selecting values from picklists, applying a full Boolean operator set (e.g., AND/OR/NOT), and using regular-expression matching via a dropdown of predefined regex patterns. Administrators must be able to control staff access to tables and fields so prohibited tables/fields are hidden. Acceptance includes constructing representative queries using picklists/regex/Boolean operators and verifying that access controls hide prohibited tables/fields.

### REQ-108 — Predefined executive reports

- **Priority:** Must — Essential function: predefined reports are critical for compliance with state reporting.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

The system must provide predefined Board/Executive reports (including basic statistics such as those required by Georgia Annual Report and Application for State Aid) showing activity (check-outs, check-ins, holds placed, holds filled) and supporting cross-tabulation by terminal, branch, system, hour, patron age range, patron type, and patron location; acceptance: produce these predefined reports and demonstrate requested cross-tabulations.

### REQ-109 — Transaction archive privacy protections

- **Priority:** Must — Legal obligation: privacy protections are required by state law.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml)

The system must archive transaction data in a privacy-preserving form required by applicable State Law: archived datasets must remove or anonymize personally identifiable information (e.g., names, addresses, exact identifiers) while still retaining the transaction data necessary for reporting and useful demographic/statistical aggregates. The acceptance includes demonstrating archived schemas with identifying fields excluded or masked and providing tools/verification showing absence of prohibited PII, including that privacy officers and managers can use anonymized archives for analysis.

### REQ-110 — Periodic management reports

- **Priority:** Must — Essential function: generating periodic reports is critical for operational oversight.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

The system must generate periodic reports such as bibliographic records with holds; items not checked out in X days; item-level holds; items with invalid item type; in-transit items with outstanding hold; items in-transit > X days; items that are the last copy; items with long call numbers; missing items; bibliographic records with no item records; patrons with invalid home library — with X and similar parameters configurable; acceptance: produce each example report for sample data and allow configuration of X where applicable.

### REQ-111 — Display selection criteria with results

- **Priority:** Should — Workaround exists: results can be manually matched to criteria, but it's less efficient.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml), D14 (evergreen_reference_2009.txt)

For every report run/result, the system shall display the selection criteria used to generate the results. This includes showing the full selection criteria (filters, date ranges, and field selections) alongside the results and ensuring the criteria are also included when exporting or saving the report, using a human-readable representation of criteria/template parameter values. Additionally, selection criteria definitions must be clearly defined (naming/semantics) with definitional metadata for every selection field used. Acceptance requires visibility of criteria with results and in exported/saved outputs, plus definitional metadata per selection field.

### REQ-112 — Report queue visibility to submitters

- **Priority:** Should — Workaround exists: submitters can track reports by checking in manually without visibility.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml), D14 (evergreen_reference_2009.txt), D18 (meeting_minutes\meeting_2009-07-20_minutes.txt), D20 (survey_results_2009.txt)

The system shall provide visibility into a report’s position in the execution queue for both staff and report submitters. A report queue UI/job detail page must show at least: position in queue (how many reports are ahead), submission timestamp, and current status with defined values including waiting, running, completed, and failed.

### REQ-115 — Patron behavior / use analytics

- **Priority:** Could — Nice to have: analytics would enhance reporting but are not critical.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

The system should produce patron behavior and use statistics (e.g., average return time for a title, renewal likelihood, percent renewals at a branch) to enable collection and service planning; acceptance: provide analytic reports that compute average return intervals, renewal rates, and branch-level renewal percentages for given material sets.

### REQ-116 — Anonymized demographic/statistical data

- **Priority:** Must — Legal obligation: preserving privacy while generating demographic data is critical.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml), D20 (survey_results_2009.txt)

The system shall produce demographic statistics and preserve archived demographic/transaction attributes needed for aggregated statistics while protecting privacy by removing PII/identifiers. Requirements include: archived transaction archive records preserve demographic attributes needed for aggregated counts/cross-tabulations while removing PII; demographic statistics used in reports/exports/on-screen aggregates do not include names, addresses, or identifiers unless explicit PII permission is granted and a privacy audit log exists; and demographic statistics are generated from anonymized datasets with verifying that identifiers are deleted. Acceptance covers anonymized aggregate generation, identifier removal verification, and that privacy/audit constraints are met for any PII-including outputs.

### REQ-119 — Shelf space comparative report

- **Priority:** Should — Workaround exists: comparisons can be manually conducted, though it's tedious.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

For each genre and format, the system must compare percentage of total circulations, percentage of the collection, and percentage of total shelf space, with the ability to run per library and per system; acceptance: produce reports showing the three percentages across genre/format for a branch and for the system.

### REQ-120 — Uncataloged item tracking and usage statistics

- **Priority:** Must — Essential function: tracking uncataloged items is critical for inventory management.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt)

The system must support tracking and inventorying uncataloged items (e.g., paperback and board books) that do not have individual catalog records, including quick cataloging/inventory-only recording with minimal per-item labor, inclusion of these items in circulation transaction counts and circulation statistics, and producing usage/checkout metrics for inventory-only items. Acceptance includes batch inventory additions, circulation transactions against inventory items being counted in circulation statistics/reports, and availability of usage/checkout summaries for inventory-only items.

### REQ-124 — Item record purging and conversion utilities

- **Priority:** Could — Convenience: Provides utilities for item record management but not essential for operation.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Provide utilities and reports to identify item records to purge based on customizable criteria (e.g., status 'missing' > X months, status 'discard/weed'), assist batch conversion of item statuses, produce a last-copy report to identify system last copies, and support deletion of volume entries and records with no items attached; acceptance: demonstrate identification of purge candidates, batch status conversion, last-copy listing, and deletion of volumes with associated copy entries.

### REQ-126 — Patron characteristic filtering and grouping

- **Priority:** Should — High value: Allows for better patron analysis, yet a workaround exists.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Queries and reports must be limitable or groupable by patron characteristics including age range, zip code, county of residence, home branch, patron type, and preferred language so managers can analyze patron segments; acceptance: generate reports grouped and filtered by each listed patron characteristic.

### REQ-127 — Inactive patrons listing

- **Priority:** Should — High value: Inactive patrons could be managed manually if needed.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Generate configurable lists of patrons with no circulation or electronic activity in the last X days (X configurable), with ability to scope to System, Home Library, County, etc.; acceptance: produce inactive patron lists for multiple X settings and scoping options.

### REQ-128 — Configurable transaction history retention

- **Priority:** Could — Convenience: Retention management adds value, but system could function without it.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Maintain transaction history for a configurable number of days (X configurable) while keeping monthly and annual aggregate information indefinitely so transaction detail and long-term aggregates are preserved; acceptance: configure retention X and demonstrate purge of detailed transactions older than X while aggregates remain accessible.

### REQ-129 — Backroom transaction statistics grouping

- **Priority:** Could — Convenience: Enhances reporting but not critical for the system's core integrity.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Provide transaction grouping and statistics by hour, terminal, branch, and system for transaction types (check-ins, check-outs, fines collected, patron registrations, etc.) and allow queries by all transactions or by transaction type; acceptance: generate grouped statistics by each grouping axis and by transaction type.

### REQ-130 — Count check-ins by type

- **Priority:** Should — High value: Reporting check-ins by type is useful, but could be done manually.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D20 (survey_results_2009.txt)

The system shall count and report check-ins broken down by method/type (e.g., book drop, staff terminal, self-service; also by terminal and by user/self-service) and provide cumulative totals. Acceptance requires separate counts for each check-in method/type and cumulative totals.

### REQ-131 — Count check-outs and renewals by type

- **Priority:** Should — High value: Useful for operational insights, but workarounds exist.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D20 (survey_results_2009.txt)

The system shall count and report check-outs and renewals broken down by type (staff checkout, self checkout, staff renewal, self checkout renewal, online renewal, OPAC renewal) and provide cumulative totals. Acceptance requires separate columns/categories for each listed type and cumulative totals.

### REQ-133 — Transaction totals by organizational scope

- **Priority:** Must — Critical reporting: Needed for transaction data management.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D20 (survey_results_2009.txt)

The system must generate transaction-related reports aggregated across organizational scopes for comparison and analysis. This includes producing transaction reports (e.g., holds placed, holds filled, check-outs) scoped to patron, library, selected groups of libraries, system, and county, showing per-patron counts (including check-out counts) and holds subtotals by type (active, frozen, frozen-until), as well as providing total transactions reports aggregated per patron, per library, per specified group of libraries, per system, and per county with a scope selector that outputs totals and per-entity rows for the chosen scope.

### REQ-134 — Value of items reporting

- **Priority:** Could — Convenience: Provides useful financial assessment data but not essential.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Generate reports of the monetary value of items (based on data in item records) for the entire collection or a portion (e.g., longoverdue items, DVDs in children's collection) to support financial assessment; acceptance: produce value-of-items reports filtered by status, format, or collection segment.

### REQ-135 — Accounting, auditing, and retention compliance

- **Priority:** Must — Compliance obligation: Must meet accounting and auditing requirements.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D11 (email_financial_reports.eml)

Reports and data archiving/retention must comply with standard accounting practices and applicable state/county/municipal auditing requirements to support fiscal audits. The system must support configurable enforcement of retention periods (example given: retaining some data for 7 years), prevent deletion contrary to policy, and allow retrieval/query/export of archived records for audit purposes; acceptance requires documentation of compliance mechanisms, audit-trail availability for financial reports, and demonstrating that archived records are accessible for auditor review.

### REQ-137 — Financial reporting suite

- **Priority:** Should — High value: Helps with financial tracking; a manual record keeping can substitute.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Provide financial reports including patron account balances by patron/home library/system; fines and charges accrued per time period and per charge type (overdue, damaged, lost); fines waived per time period and per branch; payments made per time period and per payment method (staff desk, self-check station, OPAC); acceptance: produce each financial report type for sample data.

### REQ-138 — Patron payments ledger with charge mapping

- **Priority:** Must — Critical function: Required for financial traceability and auditing.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D11 (email_financial_reports.eml)

The system must maintain a financial audit trail/ledger of patron payment transactions that explicitly links each payment to the specific charge(s) it was applied to, enabling auditors and finance to trace every payment back to exact charges for reconciliation. Ledger entries must include a payment identifier, date/time, amount, and applied-charge identifiers, and the system must provide a report or drill-down demonstrating the mapping from a payment to its applied charges.

### REQ-139 — Three reporting interfaces

- **Priority:** Should — High value: Increases report generation efficiency, but basic reporting can exist without it.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Provide three reporting interfaces: canned reports (predefined templates runnable ASAP or recurring), non-canned/on-demand reports (preset but editable selection criteria), and open-template reporting (full attribute selection for filtering and display across circulation, items, patrons, bills, and bibs) so users of different skill levels can generate reports; acceptance: show all three interfaces and workflows with representative reports.

### REQ-140 — Pre-written canned report templates

- **Priority:** Could — Convenience: Pre-written templates are helpful but not essential.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Deliver a set of pre-written canned report templates shipped with the product, with the ability to run them for fixed periods (yesterday, last week, last month, last year), check multiple canned reports to run together, and view results in one document; acceptance: provide sample canned templates and run combined scheduled runs into a single output.

### REQ-141 — On-demand maintenance/collection reports

- **Priority:** Could — Convenience: On-demand features enhance user experience, but not critical.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Provide on-demand reports for pre-selected maintenance and collections-development criteria that can be run interactively by staff for ad-hoc needs; acceptance: run representative maintenance reports on demand using editable criteria.

### REQ-143 — Quick-access report UI pop-up descriptions

- **Priority:** Could — Convenience: Pop-up descriptions aid usability, but are not essential.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

The quick-access interface must show a pop-up description when hovering over each canned report/template title to help users identify report purpose; acceptance: verify hover pop-ups display descriptive text for canned templates.

### REQ-144 — Quick-access check-off selection

- **Priority:** Could — Convenience: Selection UI improves user experience but isn't critical.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Users must be able to check off any part of the data they want (i.e., select multiple canned reports or data sections) in a quick-access UI; acceptance: select multiple report parts and run combined outputs.

### REQ-146 — Multiple export formats for report results (CSV/HTML/Excel-compatible)

- **Priority:** Should — Highly valuable: Multiple export formats enhance usability, with manual export as a workaround.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D20 (survey_results_2009.txt)

The system shall export report results in multiple output formats, including at minimum CSV and HTML, and provide Excel-compatible output (e.g., XLSX where feasible). Acceptance includes downloading the same report as CSV and viewing in HTML, and exporting in Excel-compatible form that preserves rows and columns; also includes producing valid XLSX, CSV, and HTML files representing report rows/columns.

### REQ-147 — Cancel scheduled or running report jobs

- **Priority:** Should — High value: Cancellation of jobs is important for user control; manual tracking could work.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt), D20 (survey_results_2009.txt)

The system shall allow authorized users to cancel a report/job that is either scheduled to run or currently running. When a cancellation is issued, the system shall promptly stop further processing of that report within a bounded timeframe and update the report job status to indicate it was cancelled. This capability must work consistently for scheduled/batch report execution, ensuring processing halts and status reflects cancellation.

### REQ-149 — Multi-period comparative columns

- **Priority:** Could — Convenience: Comparative columns enhance reports but are not essential.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Reports must be able to present comparative columns (e.g., last month's circs, previous month's circs, percent difference, previous year's month, percent difference from last month to last year's month) so trend comparisons are visible in a single result set; acceptance: produce a sample report with the specified comparative columns populated from historical data.

### REQ-150 — Batch status conversion assistance report

- **Priority:** Should — High value: Valuable for status management, though staff can do it manually without the tool.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Provide a report to assist batch conversion of item statuses (e.g., to convert items from one status to another) so catalogers and operations staff can prepare status changes safely; acceptance: generate a candidate list and perform a batch conversion using the tool with a preview step.

### REQ-151 — Editable canned report definitions/display with permissions

- **Priority:** Could — Convenience: Allows customization of reports but not essential for core functions.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

Users with appropriate permissions shall be able to add new canned reports and edit canned report display options (e.g., visible columns/column order/sorting and additional display fields such as shelving location) without changing the underlying certified canned logic/locked filters. The system shall also enforce permissions so only authorized roles can add or edit canned reports, and acceptance requires verifying that availability/behavior matches permissions (new canned reports appear for permitted users; display edits affect only presentation while logic remains intact).

### REQ-153 — Last-copy deletion list for WorldCat updates

- **Priority:** Could — Convenience: Last-copy updates are helpful but not critical to operations.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Provide the ability to get a list of items deleted that were the last copy owned by the library system to assist catalogers in updating WorldCat; acceptance: generate a list of deleted items flagged as last-copy with necessary identifiers for WorldCat updates.

### REQ-154 — Report prioritization and queue preemption

- **Priority:** Should — High value: Report prioritization improves efficiency, but can be done manually.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml), D14 (evergreen_reference_2009.txt)

The reporting subsystem shall support administrators assigning priority to report runs (or report types/templates) so higher-priority jobs execute ahead of lower-priority ones, including reordering/preemption in the report queue (e.g., a director’s board report processed before routine ad-hoc queries). Priority changes must be reflected in scheduler execution order and audited/logged; acceptance requires an admin/authorized user to mark a run high-priority, verify it preempts lower-priority queued reports, and ensure audit/log shows priority changes.

### REQ-155 — Total use count and date-range breakdown

- **Priority:** Could — Convenience: Usage counts provide helpful data but aren't critical for system operation.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Provide total use counts for items and use counts broken down by usage-date ranges (e.g., FY use count, monthly use count) for collection analysis; acceptance: produce total and date-range use counts for items in sample datasets.

### REQ-156 — Retrieve total circulation with breakdown

- **Priority:** Should — High value: requested to generate total-circulation reports with breakdowns.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Ability to retrieve total circulation (including checkouts, renewals, non-cataloged uses) with breakdowns displaying those circulation types so aggregate and component views are available; acceptance: generate total-circulation reports showing component counts and verify totals match sum of components.

### REQ-157 — Upload file filter input

- **Priority:** Should — High value: allows bulk selection criteria without manual entry, but staff can handle manual inputs.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

The report writer must allow staff to upload text files (e.g., lists of barcodes, TCNs) and use their contents as filter input for reports, enabling bulk selection criteria without manual entry. Acceptance includes that a user uploads a text file of barcodes and runs a report filtered to only include matching items (i.e., external lists are matched against holdings or transactions).

### REQ-158 — Pre-overdue/overdue/hold notices reporting

- **Priority:** Should — High value: supports auditing workflows via reports, workarounds possible.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Support running reports for pre-overdue, overdue, and holds notices sent so notification workflows can be audited; acceptance: generate lists of notices sent and corresponding patron/item records for a given period.

### REQ-159 — Pivot table output

- **Priority:** Could — Nice to have: small benefit for users wanting dynamic report output.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D20 (survey_results_2009.txt)

Provide pivot-table style output so users can dynamically cross-tabulate and summarize report results (pivoting by attributes such as branch, age, format); acceptance: export report results to a pivot-capable format or provide in-UI pivoting and demonstrate pivot operations.

### REQ-163 — Real-time and historical reporting support

- **Priority:** Must — Core function: real-time reporting is essential for immediate transaction reflection.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt), D20 (survey_results_2009.txt)

The system shall support both real-time reporting (current-state queries) and historical reporting (point-in-time or longitudinal queries). Real-time reporting must allow running reports immediately after transactions with inclusion of new transactions in results, while historical reporting must match archived snapshots/warehouse data for specified historical dates (and may rely on a reporting warehouse or equivalent mechanism). The system should also support near-real-time reporting for busy periods with agreed short latency (e.g., minutes) under load so staff can monitor live activity.

### REQ-164 — Historical reporting via point-in-time snapshots / warehouse

- **Priority:** Should — High value: historical reporting improves data insights, but workarounds exist.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D20 (survey_results_2009.txt)

The system shall provide historical reporting capabilities that generate records as they existed on a specified past date (including time-sensitive state such as prior shelving locations and bill states) using either a historical reporting warehouse/snapshot store or equivalent mechanism. The report builder must accept a historical date parameter or past date range and return results independent of later changes, producing consistent outcomes with archived snapshots and without impacting production.

### REQ-166 — Report metadata showing date selection and name

- **Priority:** Could — Nice to have: enhances clarity of report results without impacting core functionality.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Report results must include the date selection criteria and the name of the report (displayed at top or bottom) to quickly show the date range and report identity used to generate the result; acceptance: generated reports include report name and date-range criteria in header or footer.

### REQ-167 — Survey name selection by name

- **Priority:** Could — Nice to have: convenience for users when filtering.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Allow selecting survey filters by survey name so users do not have to enter survey IDs when filtering reports; acceptance: present a survey-name picklist and filter results using the selected survey name.

### REQ-168 — Reports on deleted items that were last copy

- **Priority:** Could — Nice to have: aids in reconciliation but not critical.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Ability to run a report on deleted items that were the last copy in the facility to aid catalog and discovery reconciliation (repeat of last-copy requirement specific to deleted items); acceptance: generate a list of deleted last-copy items including deletion timestamps and identifiers.

### REQ-169 — Flatten MARC fields into single row

- **Priority:** Could — Nice to have: simplifies export process, not critical.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

Ability to pull MARC record fields so that they appear on a single row of data in the report output to simplify record-level exports; acceptance: export bibliographic records with selected MARC fields flattened into columns on one row per bib record.

### REQ-170 — Transaction report grouping and filtering

- **Priority:** Must — Core function: transaction reporting with specified grouping and filtering is essential.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D20 (survey_results_2009.txt)

The system must support transaction reporting with both grouping and detailed filtering: it must allow transaction reports to be grouped by hour, terminal, branch, and system (with selectors in the report builder and output matching the selected granularity), and it must allow running reports filtered by exact date/time ranges, workstation identifiers, and specific staff user IDs to support investigations and audits.

### REQ-171 — Value-of-items report

- **Priority:** Must — Core function: calculating total item value is essential for financial oversight.
- **Derived from:** D11 (email_financial_reports.eml)

The system must generate a report that calculates the total value of items using the purchase price field from item records. Staff users from finance or collection management must be able to run this report for the entire collection or for a selected portion by applying filters on item-record fields (examples given: status = "longoverdue", format/collection = "DVDs in children's collection"). Acceptance hints: the report returns the count of items and the summed purchase-price total for the selected filter set; filters may include status, collection/childrens flag, format, and other item-record fields.

### REQ-172 — Join patron and item financial data

- **Priority:** Must — Core function: joining financial data from different records is essential for accuracy.
- **Derived from:** D11 (email_financial_reports.eml)

The system must support queries and reports that join financial data attached to patron records and financial data attached to item records. Staff users producing financial reports must be able to include data from both sources in a single report (for example, linking a payment or fine on a patron account to the related item). Acceptance hints: reports can reference fields from both patron and item tables and produce combined results for the same transaction set.

### REQ-173 — Patron account balances report

- **Priority:** Must — Core function: patron account balances report is essential for financial management.
- **Derived from:** D11 (email_financial_reports.eml)

The system must provide a report of patron account balances that can be viewed at multiple aggregation levels: by individual patron, by patron home branch, and for the entire consortium. Finance and branch staff will use this to assess outstanding receivables. Acceptance hints: the report can be run for a list of patrons or the whole consortium and supports grouping or sorting by patron, home branch, or consortium-level totals.

### REQ-174 — Query accounts by balance threshold

- **Priority:** Could — Nice to have: assists staff but does not block core functions.
- **Derived from:** D11 (email_financial_reports.eml)

A staff user must be able to query and list patron accounts whose current balance is greater than a specified threshold X (user-supplied). This is used by staff to identify accounts needing attention. Acceptance hints: the UI or report interface accepts a numeric threshold and returns all patrons with balances > X, with links to account details.

### REQ-175 — Fines and charges accrual reports

- **Priority:** Must — Core function: reporting fines accrued is essential for financial analysis.
- **Derived from:** D11 (email_financial_reports.eml)

The system must produce reports of fines and charges accrued over selectable time periods and by charge type. Time-period options must include (at minimum) last 12 months, year-to-date (YTD), and last month; charge-type breakdowns must include categories such as overdue fines, damaged-item charges, lost-item charges, etc. Finance staff will use these reports for trend analysis and reconciliation. Acceptance hints: report supports the predefined time ranges, arbitrary date ranges, and grouping by charge type with amounts and counts.

### REQ-176 — Fines waived reporting by branch and period

- **Priority:** Must — Core function: tracking and reporting waived fines is essential for budget management.
- **Derived from:** D11 (email_financial_reports.eml)

The system must track and report fines waived, with the ability to filter or group results by branch and time period. Each branch's finance staff must be able to see waived amounts that affect their local budget. Acceptance hints: the report lists waived transactions with date, amount, reason, and originating branch and can aggregate totals per branch and per selected time period.

### REQ-177 — Payments reporting with method, channel, and branch breakdowns

- **Priority:** Must — Core function: payments reporting is essential for financial oversight.
- **Derived from:** D11 (email_financial_reports.eml)

The system must provide payments reports that can be broken down by time period, payment method (examples: cash, credit card, check, ecommerce), and payment channel or collection point (examples: staff desk, self-check station, OPAC). Reports must also support filtering or grouping by branch and common time ranges (last month, YTD, last 12 months). Branch and finance staff will use these to perform daily and month-end reconciliation. Acceptance hints: the report shows counts and amounts per payment method and payment channel for the selected period and branch.

### REQ-180 — Immediate update of financial information

- **Priority:** Must — Core function: immediate updates of financial information are essential for accuracy.
- **Derived from:** D11 (email_financial_reports.eml)

When a patron makes a payment (for example at the front desk), the system must update the patron's financial information immediately so that account balances and relevant reports reflect the payment in near real time. Front-line staff and finance need up-to-date balances for accurate transactions and reconciliation. Acceptance hints: a payment entered via the staff interface updates the patron account balance and appears in reports and ledgers without manual refresh delays.

### REQ-181 — Include ecommerce transactions in financial records

- **Priority:** Must — Core function: recording ecommerce transactions is essential for comprehensive financial records.
- **Derived from:** D11 (email_financial_reports.eml)

The system must record ecommerce (online) transactions and attach them to the appropriate patron and item records so they are included in financial reports, ledgers, and reconciliations. Finance staff must be able to see ecommerce payments alongside in-person payment methods. Acceptance hints: ecommerce transactions appear with payment method = ecommerce (or equivalent), include transaction identifiers, and are selectable in payments and account-balance reports.

### REQ-184 — Fine-grained RBAC for report/query access and actions

- **Priority:** Should — High value: fine-grained permissions enhance security, workarounds exist.
- **Derived from:** D12 (email_report_features.eml), D14 (evergreen_reference_2009.txt), D20 (survey_results_2009.txt)

The system shall implement fine-grained permissions that let admins control which users/roles can access the query tool and which query features (e.g., regex, advanced boolean, specific record types) they may use, and also control who can create/edit/clone/publish/delete/run reports and templates/queries with separately assignable rights per capability. Enforcement must occur in both the UI and APIs via an admin permission matrix, preventing unauthorized actions. Acceptance requires admin UI/controls to enable/disable tool/features per role and tested permission enforcement that blocks disallowed actions.

### REQ-187 — Clone report/template capability

- **Priority:** Could — Nice to have: improves user experience but not critical.
- **Derived from:** D12 (email_report_features.eml)

The system shall provide a 'clone' operation that creates a new report or template based on an existing one without modifying the original template. This lets staff or admins create variants while preserving the canonical template. Acceptance hints: 'Clone' produces a separate editable object with its own metadata; original template remains unchanged.

### REQ-189 — Role-based automatic permission updates

- **Priority:** Could — Nice to have: convenience for permission management, not critical.
- **Derived from:** D12 (email_report_features.eml)

The system shall support role-based administration so that when a user's role changes (for example from 'Staff' to 'Manager') their report-related permissions update automatically according to the role-to-permission mapping. This reduces manual permission management. Acceptance hints: changing a user's role immediately changes their effective permissions without manual per-user edits.

### REQ-190 — Shared report folders with scoped access controls

- **Priority:** Should — High value: shared folders improve collaboration, though not essential.
- **Derived from:** D12 (email_report_features.eml), D20 (survey_results_2009.txt)

The system shall support shared report folders with configurable, folder-level access controls (ACLs) so administrators can allow/disallow staff from seeing or running reports in those folders. Acceptance includes per-folder permissions enforced in the UI for list/run/edit rights, and the ability to scope ad-hoc report execution to predefined data subsets as configured by admins.

### REQ-193 — Transaction retention per State law

- **Priority:** Must — Legal obligation: compliance with State law necessitates retention of transaction records.
- **Derived from:** D12 (email_report_features.eml)

The system shall retain detailed transaction records for the period required by State Law (the specified “X years” for the jurisdiction). This satisfies legal compliance for retained transaction records. Acceptance hints: archive configuration stores detailed transaction data for the legally required retention period and enforces the retention policy after expiry. Long-term monthly and annual aggregates may be retained indefinitely as specified in REQ-128.

### REQ-196 — Pre-defined board reports and metrics

- **Priority:** Must — Statutory reporting needs: Required for compliance with Georgia Annual Report requirements.
- **Derived from:** D12 (email_report_features.eml)

The system shall provide pre-defined board reports that satisfy basic/statutory reporting needs (e.g., Georgia Annual Report requirements). These reports must include activity metrics such as checkouts, check-ins, holds placed, and holds filled. Acceptance hints: packaged board report templates exist and produce the listed activity counts consistent with operational data.

### REQ-197 — Cross-tabulation reporting dimensions

- **Priority:** Should — Workaround exists: Users can manually create ad-hoc queries without cross-tabulation.
- **Derived from:** D12 (email_report_features.eml)

Board and activity reports (and ad-hoc cross-tab reports) shall support cross-tabulation by the dimensions requested: terminal, branch, system, hour (time-of-day), age range, patron type, and patron location. Users (or templates) must be able to group and cross-tabulate results by any combination of these dimensions. Acceptance hints: report UI or query builder supports selecting these dimensions as row/column/group keys and produces multi-dimensional counts.

### REQ-199 — Multiple authentication methods

- **Priority:** Must — Critical functionality: Multiple authentication methods are essential for system accessibility across branches.
- **Derived from:** D13 (email_staff_login.eml)

The system shall support more than one staff authentication method: streamlined methods (for example, badge-swipe login using an employee ID badge) and traditional individual username/password login. Staff users must be able to authenticate using either method so branches with and without badge-reader hardware can operate. Acceptance hints: a staff user can successfully log in using a badge swipe and can also log in using a username and password.

### REQ-200 — Streamlined login optional and configurable

- **Priority:** Should — Workaround exists: Users can use username/password login in absence of badge-swipe authentication.
- **Derived from:** D13 (email_staff_login.eml)

The system shall not require streamlined login methods; badge-swipe authentication must be supported but configurable and optional so branches without badge-reader infrastructure can continue using username/password. Administrators or site configuration must be able to enable or disable badge-swipe login at branches or globally as appropriate. Acceptance hints: a branch can be configured to accept badge swipes or to operate without them; disabling badge-swipe login does not prevent username/password logins.

### REQ-201 — Badge-swipe login authenticates the staff user

- **Priority:** Must — Critical functionality: Badge-swipe must authenticate staff to ensure proper identity association.
- **Derived from:** D13 (email_staff_login.eml)

When badge-swipe login is used, the system shall authenticate and associate the session with the specific staff user account; the badge swipe is a means of identifying the individual and must not bypass individual authentication or identity association. Acceptance hints: badge-swipe login results in the same staff identity and permissions as if that staff user had entered a username and password, and actions are attributed to that staff account.

### REQ-202 — Staff session audit logging

- **Priority:** Must — Audit logging necessity: Required for tracing actions for accountability and audits.
- **Derived from:** D13 (email_staff_login.eml)

The system shall record audit information that identifies which staff user is logged in (and when) so that actions can be traced for audit purposes. Audit logging must capture at minimum the staff user identity and the occurrence of login sessions so administrators can determine who was using a terminal. Acceptance hints: audit entries exist showing staff user identities and session start events; records can be reviewed by administrators for auditing.

### REQ-204 — Permissions determined by role on login

- **Priority:** Must — Access control: Permissions determine system access, critical for security compliance.
- **Derived from:** D13 (email_staff_login.eml)

When a staff user logs in by any method, the system shall determine and apply that user's effective permissions from their assigned security group(s) or role(s) for the session. This ensures consistent enforcement of access control regardless of authentication method. Acceptance hints: after login, a staff user's available actions match the permissions defined for their assigned role(s) without needing per-session manual adjustments.

### REQ-207 — Support for defined staff roles

- **Priority:** Should — Workaround exists: Staff can manage roles manually if creation/assignment is complex.
- **Derived from:** D13 (email_staff_login.eml)

The system shall support creation and assignment of common staff roles (examples mentioned: front desk staff, department heads, system administrators) so that different classes of staff can be granted appropriate abilities such as running basic reports, creating/modifying templates, or full system administration. Acceptance hints: the system can represent and assign roles corresponding to the referenced examples and enforce distinct permission sets per role.

### REQ-208 — Web-based report writer

- **Priority:** Should — Workaround exists: Users can manually create reports without a web-based interface.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide a web-based report writer interface that allows staff users to build reports in the browser; it must support visual field selection and report construction so librarians and administrators can create ad-hoc reports without writing SQL. Acceptance: a staff user can create a new report in the UI, add fields via the interface, save it, and run it to produce output.

### REQ-209 — Drag-and-drop field selection

- **Priority:** Could — Nice to have: Drag-and-drop feature would improve user experience but isn't critical.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The report writer shall allow staff users to select report fields using drag-and-drop operations from a field palette into the report layout so that report creation is quick and discoverable. Acceptance: a user can drag a field from the palette into the report and the field appears in the result layout when the report is run.

### REQ-211 — Save and reuse report definitions

- **Priority:** Should — Workaround exists: Users can recreate report definitions manually if not saved.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall allow staff users to save report definitions (field selections, filters, sorts, formatting) and later reuse or modify them so commonly used reports can be run without rebuilding. Acceptance: a saved report definition is available to the creator for re-run and editing, and runs produce consistent results.

### REQ-212 — Complex query construction

- **Priority:** Should — Workaround exists: Users can create simpler reports without complex query construction.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The reporting system shall support construction of complex queries (multi-table joins, nested criteria) so advanced staff users and report authors can express non-trivial report logic that current simple filters cannot represent. Acceptance: a staff user can create a query combining fields from related record types (e.g., item joined to action_circulation and patron) and obtain expected results.

### REQ-213 — Boolean operators in filters

- **Priority:** Could — Nice to have: Boolean operators enhance report functionality but aren't essential.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The report writer shall support Boolean logic (AND, OR, grouping/parentheses) in filter expressions so staff can express combined conditions in a single report definition. Acceptance: a report with combined AND/OR conditions returns results that match the composed logical expression.

### REQ-222 — Email report delivery with selectable recipients via address book

- **Priority:** Should — Workaround exists: Reports can be delivered manually without email automation.
- **Derived from:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D20 (survey_results_2009.txt)

The system shall deliver report results by email to one or more specified recipients, supporting both ad-hoc (Run ASAP) and scheduled/recurring report runs. Users must be able to enter multiple recipient email addresses and/or select recipients from a centrally managed address book of delivery targets (including email addresses and distribution lists) when scheduling or running a report, with recipients specifiable at run time or saved with the recurring schedule; acceptance requires email delivery to the selected entries and support for canned/on-demand/recurring report definitions.

### REQ-226 — Quick access UI with descriptions

- **Priority:** Could — Nice to have: Quick access UI would enhance discoverability but isn't critical.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The reporting UI shall provide a quick access area (favorites, recent, or pinned reports) with pop-up descriptions and hover tooltips for report titles so users can discover report purposes without opening them. Acceptance: hovering over a report title shows a brief description and a quick access list allows pinning a report.

### REQ-227 — Use reporting replica/reads to protect production

- **Priority:** Must — Performance enhancement: Protects production data integrity by offloading reporting.
- **Derived from:** D14 (evergreen_reference_2009.txt), D16 (interview_sysadmin_2009-05-10.txt)

The reporting architecture shall offload heavy reporting queries from the production write master by using a separate reporting database and/or a read-only replica/connection. Acceptance requires reports execute against the replica by default (or be configurable to target it) and that production write transactions are unaffected, with identical report output when comparing replica vs production for the same query.

### REQ-229 — Development and training separation

- **Priority:** Should — Workaround exists: Users can develop reports in production under careful management.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The reporting platform shall support separate development/training environments distinct from production so staff can develop and test reports and training exercises without impacting live data and services. Acceptance: a non-production environment containing representative (anonymized or scrubbed) data is available for report development and training tasks.

### REQ-230 — Configuration migration between environments

- **Priority:** Should — Workaround exists: Changes can be made across environments without migration tools, albeit manually.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide tools or processes to migrate report definitions, templates, and configuration between environments (development, staging, production) so changes can be promoted reliably. Acceptance: a saved report or template can be exported from one environment and imported into another preserving definitions and permissions.

### REQ-234 — Separate last-circulation date and last-edit timestamp

- **Priority:** Should — Workaround exists: Reports can still be created with combined date fields if separate fields aren't available.
- **Derived from:** D14 (evergreen_reference_2009.txt), D15 (interview_cataloging_2009-05-08.txt)

The system shall expose separate fields for reporting: a distinct last circulation date reflecting the latest checkout/return activity independent of other timestamps, and a separate last-edit timestamp reflecting the last time the bibliographic or item record was edited (not updated by circulation events). Acceptance requires reports can include last_circulation_date and last-edit values with correct update behavior.

### REQ-235 — Separate checkin and renewal timestamps

- **Priority:** Should — Workaround exists: Users can aggregate data without separate timestamps; it's less convenient.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The data model and reporting shall provide separate timestamp fields for checkin and renewal events (not stored together) so reports can differentiate check-ins from renewals. Acceptance: a report can query checkin_timestamp and renewal_timestamp separately and return distinct values consistent with transaction history.

### REQ-236 — Snapshot bills historical report

- **Priority:** Could — Nice to have: Historical bills report enhances analysis but isn't mandatory.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall support a snapshot-style bills report that can report bills and related financial state as of historical dates so aged-debt and time-based financial analysis is possible. Acceptance: a user requests bills as of a past date and the report returns bill states consistent with stored snapshots or warehouse data for that date.

### REQ-237 — Last copy report enhancements

- **Priority:** Could — Nice to have: Enhanced Last Copy report would aid collection management but isn't essential.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The reporting system shall provide an enhanced Last Copy report that identifies the last copy of a bibliographic record and its status and metadata so collection management can identify unique holdings. Acceptance: report lists bib records with only one active copy and includes item id, barcode, location, and last circulation date.

### REQ-238 — Items Edited Count report

- **Priority:** Could — Nice to have: Items Edited Count report would improve monitoring but isn't critical.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide a report that counts items edited within a specified date range so staff can monitor item-edit activity. Acceptance: the report accepts a date range and returns a count of item records edited per user and per library in that range.

### REQ-239 — Circulation by circ modifier report

- **Priority:** Could — Nice to have: Circulation by circ modifier report enhances analysis but isn't essential.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide a Circulation Count by Circ Modifier report that aggregates circulation transactions grouped by circ_modifier so circulation patterns by modifier can be analyzed. Acceptance: report accepts date range and returns counts grouped by circ_modifier and optionally by library.

### REQ-240 — Circulation by Dewey report

- **Priority:** Could — Nice to have: Circulation by Dewey report would provide useful insights but isn't critical.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide a Circulation Count by Dewey report that aggregates circulation by Dewey call number ranges or classifications so subject-area usage can be measured. Acceptance: report groups circulation counts by specified Dewey ranges or call number prefixes and returns totals for the selected period.

### REQ-241 — Circulation by MARC fields report

- **Priority:** Could — Convenience: while valuable for usage analysis, the report is not critical to system operation.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The reporting system shall support Circulation Count by MARC fields so staff can analyze usage based on bibliographic metadata fields (e.g., subject headings or other MARC tags). Acceptance: a user selects one or more MARC fields and a date range and receives aggregated circulation counts keyed by MARC value.

### REQ-242 — Circulation by location and patron county

- **Priority:** Could — Convenience: valuable for geographic analysis but not essential for core functionality.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall produce Circulation Count by Circ Location broken down by Patron County so circulation can be analyzed geographically by patron residence and item location. Acceptance: report accepts circ_location and patron county as grouping axes and returns counts for each combination.

### REQ-243 — Circulation by age demographic report

- **Priority:** Could — Convenience: aids in understanding usage metrics by age but can be managed without it.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide Circulation Count by Age Demographic so circulation metrics can be segmented by patron age ranges. Acceptance: report allows selection of age groups and returns circulation counts per age group for specified date ranges.

### REQ-244 — List items by fines stopped reason

- **Priority:** Could — Convenience: helps in reviewing exceptions but not necessary for system operations.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide a report listing items associated with fines that have been stopped and include the stopped reason so staff can review exception handling. Acceptance: report returns items with stopped fines, their stopped_reason, patron, and related transaction identifiers.

### REQ-245 — Items overdue with patron contact

- **Priority:** Could — Convenience: useful for outreach but not critical to system functions.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide a report of items more than XX days overdue that includes patron contact information (name, phone, email, address) so staff can perform outreach. Acceptance: report accepts an overdue threshold (XX days) and returns items overdue beyond that threshold with associated patron contact fields.

### REQ-246 — Items by total use count

- **Priority:** Could — Convenience: adds value for collection assessment but not essential.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide a report listing items that match a specific total use count (e.g., items used exactly N times) so collection assessment based on usage is possible. Acceptance: report accepts a total use count parameter and returns items with usage equal to that count along with usage history if requested.

### REQ-247 — Items by creation date range

- **Priority:** Could — Convenience: provides valuable insights into item creation dates but not necessary.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The reporting system shall provide a List of Items by Creation Date Range so staff can find items created (cataloged) within a specified date window. Acceptance: report accepts start and end creation dates and returns item identifiers, bib ids, and creation timestamps in that range.

### REQ-248 — Claims returned report

- **Priority:** Could — Convenience: beneficial for claim resolution but can be managed without it.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide a Claims Returned report listing items that have been marked as claimed returned and related circulation/hold history so staff can resolve claim-return cases. Acceptance: report returns items with claimed_returned status and associated transaction dates and patron information.

### REQ-249 — Weeding report with last circulation date

- **Priority:** Could — Convenience: helps in identifying removal candidates but is not a necessity.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide a Weeding report that includes items’ date of last circulation (and related metadata) so collection managers can identify candidates for removal. Acceptance: the report lists items in a call number range or location and includes last_circulation_date for each item.

### REQ-250 — Age of collection by call number

- **Priority:** Could — Convenience: useful for measuring collection currency but not a critical requirement.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide a report that calculates the age-of-collection metrics grouped by call number ranges so collection currency can be measured by subject area. Acceptance: report returns average and distribution of publication dates or age metrics for items grouped by call number bins.

### REQ-251 — Price value by call number

- **Priority:** Could — Convenience: supports investment evaluation by subject but is not essential.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide a report that aggregates collection monetary value (purchase_price or estimated price) by call number so managers can evaluate investment by subject. Acceptance: report aggregates purchase_price (or other price field) by call number groups and returns totals and counts.

### REQ-252 — Bib records edited count

- **Priority:** Could — Convenience: indicates bibliographic activity; however, not essential for core operations.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide a Bib Records Edited Count report to show number of bibliographic records edited in a date range, optionally by editor and library, for bibliographic activity monitoring. Acceptance: report returns counts of bib edits per user and per library for the selected date range.

### REQ-253 — Bib records added by user/library

- **Priority:** Could — Convenience: aids in measuring cataloging productivity but not essential.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide a report counting Bib Records Added by user by library so cataloging productivity can be measured. Acceptance: report accepts date range and returns counts grouped by creating user and home library.

### REQ-254 — Bib records missing MARC fields

- **Priority:** Could — Convenience: helps prioritize data quality but not crucial for system functionality.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide a report that lists bibliographic records missing specified MARC fields so data quality and remediation can be prioritized. Acceptance: a user specifies MARC tags and the report returns bib ids lacking those tags with counts per library or user if requested.

### REQ-255 — Patron count by age demographic

- **Priority:** Could — Convenience: useful for planning but not a critical feature.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide a Patron Count by Age Demographic report to show patron population segmented by age ranges for planning and reporting. Acceptance: report returns patron counts by configurable age buckets and supports filtering by library or patron type.

### REQ-256 — Patron count by county

- **Priority:** Could — Convenience: valuable for summarizing patron distribution but not essential.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide a Patron Count by County report to summarize patron distribution by county of residence. Acceptance: report returns counts of patrons grouped by county and supports export.

### REQ-257 — Patron count by county/city/zip

- **Priority:** Could — Convenience: helps analyze demographic distribution but not a must-have.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide a Patron Count by County, City, & Zip Code report so demographic distribution can be analyzed at multiple geographic granularities. Acceptance: report returns patron counts grouped at the requested geographic level(s) with a configurable drill-down.

### REQ-258 — Voter survey responses report

- **Priority:** Could — Convenience: beneficial for outreach but not critical to the core system.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The reporting system shall include a Voter Survey Responses report to capture and summarize responses from voter-related surveys stored in patron or auxiliary data so outreach and compliance activities can use the data. Acceptance: report returns survey response records aggregated by question and demographic filters when survey data exists.

### REQ-259 — List of inactive patrons

- **Priority:** Could — Convenience: aids in identifying inactive accounts but not essential.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide a report listing patrons with an inactive status so outreach or cleanup processes can identify inactive accounts. Acceptance: report returns patrons flagged inactive with last activity date, home library, and contact fields.

### REQ-260 — Staff password change audit

- **Priority:** Should — High value: supports auditing of staff account activity; workaround is manual tracking.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide a report listing staff accounts with the date of last password change so administrators can audit password recency and enforce policies. Acceptance: report returns staff account identifiers and last_password_change timestamps for the requested date range.

### REQ-261 — Holds purchase alert report

- **Priority:** Could — Convenience: valuable for selectors but not critical for system operation.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall include a Holds Purchase Alert report that identifies holds that meet configured purchase-alert criteria (e.g., hold-to-copy ratios, unmet demand) so selectors can consider purchasing additional copies. Acceptance: report flags bibs or titles meeting the alert thresholds with counts of holds and availability metrics.

### REQ-262 — Unfilled holds report

- **Priority:** Should — High value: essential for prioritizing fulfillment; can be done manually but is cumbersome.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide an Unfilled Holds report listing holds that have not been filled within configurable timeframes so staff can prioritize fulfillment or cancellation. Acceptance: report returns holds with creation dates, hold status, and elapsed time since placement exceeding the configured threshold.

### REQ-263 — Stale holds report

- **Priority:** Should — High value: helps manage and clean stale requests; manual management exists.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide a Stale Holds report that identifies holds with no activity for a configurable period so staff can manage and clean up stale requests. Acceptance: report returns holds inactive for the configured window with details on patron and item and supports filtering by library.

### REQ-264 — Aged debt detailed report

- **Priority:** Could — Convenience: supports financial management but not critical.
- **Derived from:** D14 (evergreen_reference_2009.txt)

The system shall provide an enhanced Aged Debt detailed report that presents owed amounts by age bands, per-patron breakdown, payments, credits, and historical state so finance staff can manage collections. Acceptance: report produces aged debits grouped by age bands (e.g., 0-30, 31-60, 61-90, 90+) and includes per-patron detail and payment history for selected periods.

### REQ-266 — Item transfer utility

- **Priority:** Must — Critical function: essential for staff operations and item management, no workaround.
- **Derived from:** D15 (interview_cataloging_2009-05-08.txt)

Provide a transfer utility that enables staff to move batches of items between locations. The utility must let staff query candidate materials by criteria (for example, items by section and last-circulation age), save and reuse queries for scheduled use, manually select titles from query results, perform batch changes to item location/record to effect transfers, and support mechanisms to revert items back to their original location after a configurable period (for example when a mobile unit returns). Acceptance hints: a saved query can be rerun, staff can select some or all results, a batch location update is applied, and the system can automatically or manually revert locations after the configured time.

### REQ-268 — Weeding reports with configurable criteria

- **Priority:** Should — Valuable feature: staff need to identify materials for removal to manage collection effectively.
- **Derived from:** D15 (interview_cataloging_2009-05-08.txt), D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

The system must provide weeding reports to identify materials for removal based on configurable criteria (usage, age, condition, duplication) to support collection management, and generate automated lists for weeding projects. Acceptance includes staff defining criteria (e.g., items with status 'missing' longer than X months, status 'discard/weed', plus filters such as status, time thresholds, item type, location) and the report listing candidate items with identifiers/metadata based on the selected criteria.

### REQ-270 — Last-copy identification report

- **Priority:** Should — High value: helps prevent loss of last-copy items, but staff could manually check records.
- **Derived from:** D15 (interview_cataloging_2009-05-08.txt)

Provide a last-copy report that identifies items for which the local system holds the final copy (system's last copies). Catalogers need this report before deleting or purging bibliographic items so they can avoid removing the system's last copy and to identify items that may require WorldCat edits. Acceptance hints: report identifies records with only one item/system copy, lists location(s), and can be produced prior to deletion workflows.

### REQ-273 — Shelf space comparison report

- **Priority:** Could — Nice to have: aids decision-making for shelf space but not critical to operations.
- **Derived from:** D15 (interview_cataloging_2009-05-08.txt)

Provide a shelf space report that, for each genre and format, compares percentage of total circulations, percentage of the collection, and percentage of total shelf space. Collection managers need these comparisons to make decisions about allocation of shelf space and resources. Acceptance hints: report groups by genre and format and displays the three percentages side-by-side for comparison.

### REQ-275 — Data quality exception reports

- **Priority:** Must — Data integrity need: cataloging staff require these reports to maintain quality.
- **Derived from:** D15 (interview_cataloging_2009-05-08.txt)

Produce data quality reports that identify records and items with quality problems, including (at minimum) items with invalid item types, items with unusually long call numbers, and bibliographic records that have no associated item records. Cataloging staff require these to maintain data integrity. Acceptance hints: each report lists the offending records with the problematic field(s) highlighted and supports export for batch correction.

### REQ-277 — Deploy on RHEL5 and Solaris10

- **Priority:** Must — Deployment requirement: essential for installation without hardware changes.
- **Derived from:** D16 (interview_sysadmin_2009-05-10.txt)

The system must be deployable and operable on the existing server platforms: Red Hat Enterprise Linux 5 (x86) and Solaris 10 on SPARC. This is required by IT staff to install reporting components at the primary and secondary sites without changing platform hardware; acceptance can be demonstrated by successful installation and operation on a RHEL5 test server and a Solaris10/SPARC test server.

### REQ-282 — Preserve OPAC/circulation responsiveness; no patron-facing functionality in management reporting

- **Priority:** Must — Performance obligation: ensures reporting does not affect OPAC responsiveness.
- **Derived from:** D16 (interview_sysadmin_2009-05-10.txt), D17 (meeting_minutes\meeting_2009-03-15_minutes.txt), D18 (meeting_minutes\meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

Management reporting must not degrade or constrain OPAC and circulation-client responsiveness during normal open hours, remaining responsive even when reports run and meeting agreed performance thresholds/SLA targets under typical reporting load and peak-load tests. The system must not implement patron-facing OPAC search/checkout workflows or circulation client functionality inside the reporting interface; patron-facing activities remain in OPAC/circulation while reporting exposes management-oriented queries only.

### REQ-284 — Section 508 Accessibility Compliance

- **Priority:** Must — Accessibility obligation: compliance with Section 508 is legally required.
- **Derived from:** D16 (interview_sysadmin_2009-05-10.txt)

The system must comply with Section 508 accessibility requirements so staff and patrons with disabilities can use reporting features; this includes producing standards-compliant HTML, proper semantic markup, alt text for images, ARIA labels where appropriate, and ensuring UI controls and outputs are usable with assistive technologies. Acceptance: an accessibility audit confirms Section 508 conformance and users of screen readers/magnifiers can navigate to run reports and read results.

### REQ-285 — Support Assistive Technologies

- **Priority:** Must — Accessibility need: usability with assistive technologies is essential for staff productivity.
- **Derived from:** D16 (interview_sysadmin_2009-05-10.txt)

The system must be usable with common assistive technologies in the environment—specifically screen readers (JAWS, NVDA), screen magnification tools (ZoomText) and similar programs—so blind or low-vision staff can run and read reports. Acceptance: representative tasks (launch report, view results, download) are successfully completed by users employing JAWS, NVDA, and ZoomText in test scenarios.

### REQ-286 — Role-based access control with defined user classes

- **Priority:** Must — Core functionality: critical for role-based access security and permissions management.
- **Derived from:** D16 (interview_sysadmin_2009-05-10.txt), D17 (meeting_minutes\meeting_2009-03-15_minutes.txt), D18 (meeting_minutes\meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

The system shall implement RBAC with defined user classes/roles (Patron, Staff, Local System Administrator, Library Manager, Library Director, Global System Administrator) with appropriate permissions for viewing, creating, configuring, and administering reports. Acceptance requires privilege separation such that users with different roles see different report lists/functions; staff cannot perform global admin functions; and global admins can access consortium-level controls, with tests enforcing expected permissions (e.g., Local Admin can run branch reports but not change global configuration).

### REQ-289 — Separate dev, training, and production environments

- **Priority:** Should — High value: separate environments improve safety but could be managed without them.
- **Derived from:** D16 (interview_sysadmin_2009-05-10.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

The project shall provide distinct development, training, and production environments such that actions in dev/training cannot affect production data or services. Training must be safe for experimentation (isolated or masked data so training operations cannot corrupt production data), and acceptance requires separate instances/DBs or sanitized copies, with demonstrable isolation and no write-through to production.

### REQ-291 — Support Secondary Site/Disaster Recovery

- **Priority:** Must — Disaster readiness: necessary for continuity of reporting during DR events.
- **Derived from:** D16 (interview_sysadmin_2009-05-10.txt)

The reporting system must be deployable and operable at the secondary disaster recovery site so reporting can continue (or be recovered) during DR events; this aligns with existing Solaris10/SPARC DR infrastructure. Acceptance: the system is installed and can run reporting tasks at the secondary site, and failover or DR procedures for reporting are documented and tested.

### REQ-293 — Management Reports and Analysis Tools

- **Priority:** Must — Core functionality: essential for library management decision-making.
- **Derived from:** D17 (meeting_minutes\meeting_2009-03-15_minutes.txt)

The system must provide reporting and analysis tools used by library managers, administrators, and staff for planning, evaluation, and oversight. These tools must enable generation of management-focused reports (not patron-facing OPAC or circulation client functions) so managers can monitor services and make data-driven decisions. Acceptance hints: users in management roles can run, view and export reports summarizing operational metrics for selected time periods and organizational units.

### REQ-294 — Executive Reports Interface

- **Priority:** Must — Core functionality: essential for executive-informed decision-making.
- **Derived from:** D17 (meeting_minutes\meeting_2009-03-15_minutes.txt)

The system must include an Executive Reports Interface that presents a compiled set of executive-level reports intended for library directors and the Library Executive Team. This interface should surface high-level metrics and aggregated views appropriate for executive decision-making. Acceptance hints: a user in a director role can access a dedicated executive dashboard listing the compiled executive reports and open each report without requiring OPAC/circulation client access.

### REQ-297 — Staff Report Authoring

- **Priority:** Should — Valuable: staff report authorship is beneficial but could be done with existing tools.
- **Derived from:** D17 (meeting_minutes\meeting_2009-03-15_minutes.txt)

The system must enable staff users (front-line circulation staff, supervisors, etc.) to author and edit report content and templates because staff are primary content creators for reports. Acceptance hints: a staff user can create a new report or edit an existing template, save drafts, and submit reports for review or publishing according to their permissions.

### REQ-298 — Local Configuration by Administrators

- **Priority:** Must — Local customization: essential for local administrators to meet their unit's needs.
- **Derived from:** D17 (meeting_minutes\meeting_2009-03-15_minutes.txt)

The system must permit local system administrators (branch managers/assistant directors) to configure reporting settings and parameters for their organizational unit so local needs and variations can be supported. Acceptance hints: a local admin can set local defaults (e.g., branch selection, local filters), enable/disable templates for the branch, and run local-only reports without global privileges.

### REQ-299 — Consortium-level Aggregated Reporting

- **Priority:** Must — Core functionality: important for oversight across the consortium.
- **Derived from:** D17 (meeting_minutes\meeting_2009-03-15_minutes.txt)

The system must provide the Global System Administrator the ability to generate statistical reports aggregated across PINES as a whole for consortium-level planning and oversight. Acceptance hints: a global admin can select an aggregation scope covering all libraries and produce consortium-wide metrics and summaries.

### REQ-300 — Collection Use Analysis Reports

- **Priority:** Must — Core functionality: necessary for collection evaluation and development.
- **Derived from:** D17 (meeting_minutes\meeting_2009-03-15_minutes.txt)

The system must provide reports that analyze the library collection and its use by patrons (for example, usage counts, circulation by item/collection) to support collection development and evaluation. Acceptance hints: users can run collection usage reports filtered by collection segment, date range, and branch, producing counts and trends.

### REQ-301 — Branch Capacity and Distribution Analysis

- **Priority:** Must — Core functionality: essential for optimizing resources across branches.
- **Derived from:** D17 (meeting_minutes\meeting_2009-03-15_minutes.txt)

The system must provide reports that analyze branch capacity and the distribution of the collection across branches to assist in optimizing physical holdings and placement. Acceptance hints: users can generate reports showing per-branch capacity metrics and comparative distribution of collection holdings.

### REQ-302 — Patron demographic and interest reporting

- **Priority:** Must — Data privacy: crucial for analyzing patron data while protecting personal information.
- **Derived from:** D17 (meeting_minutes\meeting_2009-03-15_minutes.txt), D20 (survey_results_2009.txt)

The system must produce staff-facing patron reports that analyze patron demographics and stated or inferred interests to inform programming, outreach, and collection decisions while protecting privacy. Aggregate demographic reports must use anonymized counts and exports must not include personally identifiable information. Individual-level outreach reports that require contact information are a separate, explicitly authorized use and must follow the applicable privacy permissions and audit requirements. Reports must support demographic segmentation such as age ranges and geography (e.g., ZIP codes), with privacy-protecting handling of inactive accounts. Where interest data exists, reports must also summarize interest categories. Data sources for demographic fields must be authoritative from the patron table fields (e.g., birth_date for age computation, zip code, county, home branch, patron type, preferred language), ensuring reports reflect the patron table’s canonical values.

### REQ-303 — Staff Productivity and Workflow Reports

- **Priority:** Must — Operational need: necessary for improving staff productivity and workflows.
- **Derived from:** D17 (meeting_minutes\meeting_2009-03-15_minutes.txt)

The system must provide reports that analyze staff productivity and workflow (such as activity counts or workflow step metrics) to support supervision and process improvement. Acceptance hints: supervisors can produce reports showing staff activity levels, task throughput, or workflow bottlenecks for selected time windows and organizational units.

### REQ-304 — Financial Transaction Tracking Reports

- **Priority:** Must — Financial management: critical for tracking and auditing library financial transactions.
- **Derived from:** D17 (meeting_minutes\meeting_2009-03-15_minutes.txt)

The system must provide reports to track and verify financial transactions related to library operations so managers can audit and reconcile financial activity. Acceptance hints: users can generate transaction-level reports with sufficient detail to verify entries and perform reconciliations (date, amount, account/branch, transaction type).

### REQ-305 — Integration with ILS Modules

- **Priority:** Must — Integration requirement: essential for accurate reporting based on comprehensive ILS data.
- **Derived from:** D17 (meeting_minutes\meeting_2009-03-15_minutes.txt)

The reporting system must access and use data from the broader ILS (including acquisitions and cataloging modules under separate specification) to produce management reports that depend on acquisitions, cataloging, and other ILS data. Acceptance hints: reports that require acquisitions or cataloging data return consistent results using the authoritative data from those modules.

### REQ-307 — Report Testing and Staging Workflow

- **Priority:** Must — Quality assurance: required for validating reports before production deployment.
- **Derived from:** D17 (meeting_minutes\meeting_2009-03-15_minutes.txt)

The system must provide a testing/staging workflow or environment where new reports and templates can be reviewed, tested and approved by the Reports Working Group (or designated reviewers) before being deployed to production. Acceptance hints: authors can publish a report to a staging area; reviewers can execute, comment on, and approve or reject staged reports before publication.

### REQ-308 — Prototype Deployment for User Review

- **Priority:** Should — Valuable feedback approach: allows user input on prototypes but not critical.
- **Derived from:** D17 (meeting_minutes\meeting_2009-03-15_minutes.txt)

The system must support deployment of report prototypes to allow iterative, prototype-oriented review by end users so stakeholders have multiple opportunities to review and provide feedback. Acceptance hints: developers or authors can deploy a prototype version of a report to a restricted user group for feedback without affecting production reports.

### REQ-309 — Display-ready Reports for Public Screens

- **Priority:** Should — Convenience: helpful for visual presentation, though indirect patron use not essential.
- **Derived from:** D17 (meeting_minutes\meeting_2009-03-15_minutes.txt)

The system must be able to render or export reports in a form suitable for display on public screens or displays within libraries so patrons may indirectly use certain report outputs. Acceptance hints: users can export or switch a report view into a display mode suitable for public screens (no OPAC functions required).

### REQ-310 — Documentation for Both Audiences

- **Priority:** Should — Workaround exists: Documentation can be created manually until the system documentation is provided.
- **Derived from:** D17 (meeting_minutes\meeting_2009-03-15_minutes.txt)

Project documentation (including the software requirements specification and user documentation for reporting features) must be written to be readable by non-technical library managers and staff while providing sufficient specificity for software project managers and developers. Acceptance hints: documentation includes non-technical descriptions/examples for managers and technical details (data sources, interfaces) for developers.

### REQ-311 — Non-disruptive report processing

- **Priority:** Must — Critical functionality: Non-disruptive processing is essential for maintaining real-time functions during report generation.
- **Derived from:** D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

The system shall provide background processing and queuing for searches and report generation so that report creation can occur during open hours without slowing or disrupting real-time functions such as the circulation client. Branch staff and central operations need report jobs to run without degrading front-end transaction performance. Acceptance hints: queued/background report jobs execute with priority controls and performance tests show circulation transactions maintain required response times while reports run.

### REQ-315 — Dev and training environment migration

- **Priority:** Should — Workaround exists: Manual migration of report templates can be conducted until the system's functionality is implemented.
- **Derived from:** D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

The system shall provide separate development and training environments and support migration/export/import of report templates and configuration from those environments into production. Developers and trainers require the ability to build and test report templates and then deploy them to production reliably. Acceptance hints: documented mechanisms to export/import report templates and configurations and a tested migration procedure.

### REQ-317 — Complete data specifications

- **Priority:** Must — Critical functionality: Complete data specifications are essential for writing accurate queries and reports.
- **Derived from:** D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

The software developer shall provide complete data specifications (data dictionaries) for authority records, bibliographic records, order records, item records, hold/request records, and other records maintained or accessed by the management processes. Report authors and system integrators need these specifications to write accurate queries and reports. Acceptance hints: published data specification documents covering the listed record types and example queries using the documented fields.

### REQ-320 — Enterprise system integration

- **Priority:** Must — Critical functionality: Enterprise system integration is vital for core functionality of the library system.
- **Derived from:** D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

Management processes shall operate as part of an enterprise-level Library Automation System and rely on that infrastructure for core functionality (the PINES environment/Evergreen is the referenced system). Central administrators require reporting to integrate with the enterprise system's data and services. Acceptance hints: documented integration points and successful end-to-end tests within the enterprise LAS environment.

### REQ-322 — Integration with acquisitions and cataloging

- **Priority:** Must — Critical for functionality: Integration with acquisitions and cataloging is necessary for report completeness.
- **Derived from:** D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

The management processes shall rely on and interface with the data structures and functionality of the enterprise system's Acquisitions and Cataloging modules so reports include acquisitions and cataloging data. Report authors require access to acquisitions and cataloging data fields. Acceptance hints: sample reports include acquisitions and cataloging data and interfaces to those modules are documented.

### REQ-323 — Vendor interfaces and standard formats

- **Priority:** Must — Critical functionality: Vendor interfaces are essential for incorporating external vendor data into reporting.
- **Derived from:** D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

The system shall interface with vendor websites using published APIs and/or automated transfer of standard-format data files (examples: USMARC21, EDIFACT) so data from external vendors can be incorporated into reporting. Staff integrating vendor data need standard import/export mechanisms. Acceptance hints: documented adapters or import processes for USMARC21 and EDIFACT and example successful transfers.

### REQ-325 — Pre-defined executive report templates

- **Priority:** Should — Workaround exists: Staff can create reports manually until predefined templates are available.
- **Derived from:** D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

The system shall support creation, storage, and distribution of pre-defined board/executive report templates so directors and board members can obtain standardized executive reports. Directors and report maintainers require ready-made templates for consistent executive reporting. Acceptance hints: ability to create named templates, schedule or run them on demand, and export results in common formats (PDF/CSV).

### REQ-326 — Data quality reporting

- **Priority:** Should — High value: Automated data quality reports would significantly improve staff efficiency, but may be managed manually in the interim.
- **Derived from:** D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

The system shall provide data quality reports that identify issues in bibliographic, item, and patron data so staff can detect and correct data problems. Collections and systems staff need automated reports highlighting data anomalies. Acceptance hints: configurable data quality checks and generated reports listing records failing checks with identifying details.

### REQ-327 — Staff badge-swipe login

- **Priority:** Should — Workaround exists: Manual authentication can occur, but badge-swipe login would streamline the process.
- **Derived from:** D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

The system shall support staff authentication via badge-swipe login so branch staff can authenticate quickly using existing badge-swipe hardware. Branch operations staff need this login method for convenience and workflow integration. Acceptance hints: successful authentication using badge-swipe devices and documented configuration for badge-swipe integration.

### REQ-329 — Missing and damaged item reports by branch

- **Priority:** Must — Critical functionality: Branch-level reporting on missing and damaged items is essential for inventory management.
- **Derived from:** D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

The system shall provide missing and damaged item reports at the branch level so branch managers can track and act on lost or damaged inventory. Acceptance hints: reports that can be filtered by branch and include item identifiers, reported condition, report date, and responsible staff/location.

### REQ-331 — Shelf space utilization reports

- **Priority:** Should — High value: While useful, branch managers can assess space utilization through ad-hoc reports in the absence of this functionality.
- **Derived from:** D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

The system shall provide shelf space utilization reports to help staff analyze physical space usage and support collection planning. Branch managers and collection planners require metrics on item density, shelving gaps, and growth projections. Acceptance hints: reports showing utilization metrics by branch/collection and supporting export for planning.

### REQ-332 — Demographic analysis reports

- **Priority:** Should — High value: Demographic reports offer valuable insights, but current program planning can proceed without them.
- **Derived from:** D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

The system shall provide demographic analysis reports to support program planning, using patron demographic data and geographic/aggregate metrics where permitted. Program planners need demographic insights to tailor services. Acceptance hints: reports that aggregate patron demographics and allow segmentation by geography, age, or other available attributes, with privacy controls documented.

### REQ-333 — Cross-branch comparison reports

- **Priority:** Should — High value: Cross-branch comparison supports performance evaluation but is not critical for operations.
- **Derived from:** D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

The system shall provide cross-branch comparison reports enabling comparison of metrics (circulation, holds, inventory, program attendance) across branches so directors can evaluate relative performance. Acceptance hints: reports that present comparable metrics side-by-side for selected branches and time ranges.

### REQ-334 — Inventory and capacity reports

- **Priority:** Must — Critical functionality: Inventory and capacity reports are essential for daily operations management.
- **Derived from:** D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

The system shall provide inventory and capacity reports (used daily by branch staff) showing item counts, collection sizes, capacity thresholds, and related metrics to support daily operations. Acceptance hints: daily-report generation that includes counts by item type/location and capacity indicators (e.g., percent full) per branch.

### REQ-335 — Financial reporting for directors

- **Priority:** Must — Critical functionality: Financial reporting is necessary for library directors to maintain oversight.
- **Derived from:** D18 (meeting_minutes\meeting_2009-07-20_minutes.txt)

The system shall provide financial reports appropriate for library directors, summarizing expenditures, purchasing, and budget-related metrics derived from acquisitions/order records. Directors need consolidated financial views for oversight. Acceptance hints: director-level financial report templates that aggregate acquisitions/order data and allow export to common formats.

### REQ-336 — PostgreSQL compatibility

- **Priority:** Must — Critical functionality: Compatibility with PostgreSQL is essential for system deployment.
- **Derived from:** D19 (meeting_tech_subcommittee_2009-06-30.txt)

The system shall be compatible with PostgreSQL (the current PINES choice) as a supported backend. PINES operations staff expect the reporting system to operate on the existing PostgreSQL infrastructure. Acceptance: end-to-end deployment and testing on PostgreSQL without schema or query failures; documentation of any PostgreSQL-specific features used.

### REQ-341 — Predefined user roles

- **Priority:** Must — Critical functionality: Predefined user roles are critical for maintaining proper access control.
- **Derived from:** D19 (meeting_tech_subcommittee_2009-06-30.txt)

The system shall provide the following predefined roles with the specified capabilities: Global Admin (full system access); Local Admin (branch-level reporting and configuration); Library Manager (run approved reports, limited template modification); Staff (run reports within assigned permissions); Patron (indirect access via OPAC displays). Library management requires these role semantics for delegation. Acceptance: each role exists and enforces the described scope of capabilities in tests.

### REQ-343 — Data dictionaries and specifications

- **Priority:** Must — Critical functionality: Additional data dictionaries are essential for effective query writing.
- **Derived from:** D19 (meeting_tech_subcommittee_2009-06-30.txt)

The developer shall provide complete data specifications (data dictionaries) for Authority records, Bibliographic records, Order records, Item records, Hold/request records, and other records accessed by Management Processes, including field names, data types and relationships. Staff report writers need these to author effective queries and understand the schema. Acceptance: delivered documentation lists fields, types, relationships and is sufficient for building sample queries that return expected results.

### REQ-346 — Low-level query-specific error feedback

- **Priority:** Should — High value: While precise diagnostics are beneficial, current processes allow troubleshooting without them.
- **Derived from:** D19 (meeting_tech_subcommittee_2009-06-30.txt)

The system shall provide low-level, query-specific diagnostic feedback for administrators when a report fails, including details such as which table, which field, and the error type. Administrators need precise diagnostics to debug failed queries. Acceptance: when an admin-level report fails, the system returns table/field/error-type information sufficient to reproduce and diagnose the problem.

### REQ-347 — Enterprise operating assumptions

- **Priority:** Should — High value: Understanding operational assumptions is valuable for planning, but current operations can proceed without explicit documentation.
- **Derived from:** D19 (meeting_tech_subcommittee_2009-06-30.txt)

The system shall operate as part of an enterprise-level Library Automation System and may rely on enterprise infrastructure features such as redundant servers, backup systems, and network connectivity. Deployment architects need to know this operating environment for capacity and recovery planning. Acceptance: deployment documentation states required infrastructure assumptions and system operates correctly within an environment that provides redundancy, backups and network connectivity.

### REQ-349 — Timely data currency

- **Priority:** Must — Critical functionality: Ensuring data currency is essential for accurate reporting and operational decision-making.
- **Derived from:** D19 (meeting_tech_subcommittee_2009-06-30.txt)

The system shall ensure that data from all locations is complete and current for reporting purposes; reporting must include mechanisms to verify data recency. Central reporting users depend on up-to-date data for operational decisions. Acceptance: documented data latency SLA and verification tests show data freshness meets the SLA for real-time and scheduled reports.

### REQ-350 — Read-only ILS reporting integration

- **Priority:** Must — Legal compliance: Read-only integration is needed to maintain the integrity of acquisitions and cataloging data.
- **Derived from:** D19 (meeting_tech_subcommittee_2009-06-30.txt)

The reporting integration shall access the enterprise ILS (including Acquisitions and Cataloging modules) in a read-only manner and shall not modify acquisitions or cataloging data through reporting functions. Authorized transfer or item-management functions, where provided as separate workflows, may perform the explicitly required item-location changes under their own permissions and audit controls. Acceptance: reporting interfaces use read-only credentials and tests show that reporting functions do not modify ILS data.

### REQ-351 — Vendor data format support

- **Priority:** Must — Critical functionality: Vendor data format support is essential for integrating vendor data into the system.
- **Derived from:** D19 (meeting_tech_subcommittee_2009-06-30.txt)

The system shall interface with vendor systems via published APIs and/or automated import of standard-format data files (examples: USMARC21 and EDIFACT) and be able to process EDI ordering data where present. Integration staff need to ingest vendor-provided data in standard formats. Acceptance: the system successfully ingests sample USMARC21 and EDIFACT files and can call documented vendor APIs to retrieve data; failures due to missing vendor data are handled gracefully.

### REQ-352 — Graceful handling of optional vendor data

- **Priority:** Should — High value: While beneficial for handling optional vendor data, reports can still exist without this functionality.
- **Derived from:** D19 (meeting_tech_subcommittee_2009-06-30.txt)

The system shall operate correctly even when vendor-provided data (e.g., EDI ordering data) is not present at every library, handling missing inputs gracefully. Local libraries vary in vendor support and reporting must not fail due to absent vendor feeds. Acceptance: reports that reference vendor data produce meaningful results or clear indications of missing data when vendor feeds are absent rather than system errors.

### REQ-353 — Read-only OPAC queries

- **Priority:** Should — Workaround exists: staff can manually query OPAC without modifying data.
- **Derived from:** D19 (meeting_tech_subcommittee_2009-06-30.txt)

The system shall interact with the OPAC to query patron-created holds and circulation transactions, but must not modify OPAC data. Reporting staff need access to patron transaction data without affecting the public catalog. Acceptance: OPAC integration is read-only and tests demonstrate retrieval of holds and circulation records without any write operations to the OPAC.

### REQ-354 — Support Excel, CSV, HTML exports

- **Priority:** Should — Workaround exists: reports can be exported in another format if necessary.
- **Derived from:** D19 (meeting_tech_subcommittee_2009-06-30.txt)

The system shall provide report output in Excel, CSV, and HTML formats to meet differing user needs (CSV for reliable export, Excel for pivoting, HTML for web display). Business users and automated processes require these formats. Acceptance: same report can be exported to CSV, XLS/XLSX and HTML and opened in standard tools with correct data and formatting.

### REQ-358 — Filter by survey name resolution

- **Priority:** Could — Convenience: filtering by survey name is user-friendly but not critical.
- **Derived from:** D19 (meeting_tech_subcommittee_2009-06-30.txt)

The system shall allow filtering by survey name (in addition to survey ID) and internally resolve survey names to the corresponding IDs for query execution. Survey analysts want user-friendly filtering without needing numeric IDs. Acceptance: filters entered with survey names produce the same result set as filters using the corresponding survey IDs in test cases.

### REQ-359 — Circulation reports

- **Priority:** Must — Critical for operations: circulation reports are essential for monitoring lending activity.
- **Derived from:** D20 (survey_results_2009.txt)

The system must provide circulation reports for staff users that include checkouts, check-ins and renewals (counts and lists) so library staff can monitor lending activity; acceptance: report types available in UI, selectable time range, exportable to requested formats, and rows/columns include checkout/checkin/renewal indicators.

### REQ-360 — Item inventory reports

- **Priority:** Must — Critical for management: item-level reports are essential for inventory and weeding.
- **Derived from:** D20 (survey_results_2009.txt)

The system must provide item-level reports used for inventory, weeding and missing-item workflows so collection managers can identify items for maintenance or removal; acceptance: reports include item identifiers, current shelving location, status (missing, in-process), and can be filtered and exported.

### REQ-362 — Financial transaction reports

- **Priority:** Must — Critical for finance: financial reports are essential for reconciling transactions.
- **Derived from:** D20 (survey_results_2009.txt)

The system must provide financial reports for fines and payments so finance and circulation staff can reconcile money collected; acceptance: reports list transactions, amounts, dates, payment methods and can be exported to Excel/CSV and grouped by library or patron (anonymized as configured).

### REQ-364 — Custom and on‑demand reports

- **Priority:** Must — Critical for operations: enabling custom reports is essential for local needs.
- **Derived from:** D20 (survey_results_2009.txt)

The system must allow staff users to create, run and maintain custom/on‑demand reports (ad hoc queries) for local needs such as collection development or program attendance; acceptance: interface supports building queries, saving queries, running ad hoc queries and exporting results.

### REQ-371 — Patron behavior statistics

- **Priority:** Must — Critical for planning: patron behavior statistics are essential for program development.
- **Derived from:** D20 (survey_results_2009.txt)

The system must produce statistics used to understand and predict patron behavior (e.g., renewal rates, how quickly items are returned, probability of renewal) so staff can plan acquisitions and programs; acceptance: reports provide computed renewal percentages, average return intervals and trend outputs for selected populations.

### REQ-375 — Save and reuse queries

- **Priority:** Must — Critical for efficiency: saving queries is essential for staff productivity.
- **Derived from:** D20 (survey_results_2009.txt)

The system must allow users to save queries for repeated use and place them in personal or shared folders so staff can reuse frequent searches without rebuilding them; acceptance: saved queries persist, are selectable in UI, and can be run or scheduled.

### REQ-379 — Performance under peak load

- **Priority:** Must — Critical for performance: ensuring acceptable performance during peak load is essential.
- **Derived from:** D20 (survey_results_2009.txt)

The system must run reports with acceptable performance during busy hours so staff are not blocked by long-running reports; acceptance: defined response-time targets for typical reports under peak load and ability to schedule heavy reports off-peak.

### REQ-380 — Export deduplication option

- **Priority:** Must — Critical for data integrity: deduplication option is essential to maintain clean exports.
- **Derived from:** D20 (survey_results_2009.txt)

The system must provide options to avoid duplicate rows in exported data (de-duplication or row grouping) so exports to Excel do not contain redundant rows; acceptance: export settings include de-duplication toggle and exported file shows one row per logical record where requested.

### REQ-382 — Select and consolidate MARC fields

- **Priority:** Must — Critical for cataloging: selecting MARC fields is essential for accurate data extraction.
- **Derived from:** D20 (survey_results_2009.txt)

The system must allow users to select specific MARC fields/subfields for reporting and present them consolidated per bibliographic record (not spread across multiple rows) so catalogers can extract needed MARC data; acceptance: report builder allows selecting MARC fields and output contains one row per bibliographic record with selected MARC content combined as specified.

### REQ-384 — Move items between locations

- **Priority:** Must — Critical for operations: ability to move items between locations is essential for staff.
- **Derived from:** D20 (survey_results_2009.txt)

The system must provide an operation to change item records to move items to a new shelving location or branch so staff can perform collection transfers; acceptance: batch move operation updates shelving location fields and is logged.

### REQ-385 — Revert item location changes

- **Priority:** Must — Critical for operations: reverting item locations is essential for correcting mistakes.
- **Derived from:** D20 (survey_results_2009.txt)

The system must support reverting items to their original location after a move operation so staff can undo mistaken transfers; acceptance: revert operation restores prior location using audit history or undo function and logs the revert.

### REQ-388 — Snapshot bills history

- **Priority:** Must — Critical for auditing: snapshot bills history is essential for maintaining accurate records.
- **Derived from:** D20 (survey_results_2009.txt)

The system must provide a snapshot bills report that can show billing/account information as of historical dates so staff can audit past billing states; acceptance: bills report with historical date parameter reproduces outstanding charges and payments as of that date.

### REQ-389 — Last circulation date on items

- **Priority:** Must — Critical for reporting: last circulation date is essential for managing item checkouts.
- **Derived from:** D20 (survey_results_2009.txt)

The system must include a last circulation date field on item reports so staff can identify items by their most recent circulation; acceptance: item reports contain a last_circulation_date column with correct values or null if never circulated.

### REQ-390 — Exclude renewals from checkin time

- **Priority:** Must — Critical for reporting: checkin timestamps must only reflect physical returns for accuracy.
- **Derived from:** D20 (survey_results_2009.txt)

The system must ensure checkin date/time fields do not include renewal events so checkin timestamps represent physical returns only; acceptance: reports show checkin datetime for return events only and renewal events are recorded separately with their own timestamp/type.

### REQ-392 — Sort in-transit items by due date

- **Priority:** Could — Nice to have: sorting in-transit items improves convenience but isn't critical.
- **Derived from:** D05 (conversations\conv_pines019_020_missing_intransit.eml)

The in-transit items report shall allow front-line staff to sort report results by due date or by transit age so they can prioritize pursuing the oldest or most overdue items. When the user selects sort-by-due-date the list must order items with the earliest due dates (i.e., oldest/most overdue) first; when the user selects sort-by-transit-age the list must order items with the longest time in transit first. The sort control must be available in the report interface and immediately reorder the displayed results when changed. Acceptance hints: choosing either sort option reorders the displayed report accordingly and places the highest-priority (oldest/most overdue or longest-in-transit) items at the top of the list.

### REQ-394 — Staff account expiration reporting

- **Priority:** Should — Workaround exists: accounts can be audited manually without this report, though it is valuable.
- **Derived from:** D10 (early_draft_srs_galecia.txt)

The system shall provide a report of staff accounts that includes each account identifier (e.g., username), the date of last password change, and the account expiration date so Local and Global System Administrators can audit account validity and password recency. Acceptance hints: the report must be producible for a selected scope (single branch, group of branches, or entire system), display the required fields for each staff account, and be exportable or viewable within the reporting interface for administrative review.

## 6. Discarded items (blacklist)

### BL-001 — Proven and tested output

- **Derived from:** D10 (early_draft_srs_galecia.txt)
- **Reason for discarding:** Discarded as nonsensical/out of scope: “Proven” and “reliable” are not defined by measurable acceptance criteria. Regression tests and sample validation cases are useful, but the requirement does not specify a required coverage level or reliability threshold.

Report output must be tested and proven (i.e., reliable and repeatable) to ensure confidence in results for decision-making; acceptance: provide regression-tested report runs with documented test coverage and sample validation cases.

### BL-002 — OPAC functionality non-constraint

- **Derived from:** D10 (early_draft_srs_galecia.txt)
- **Reason for discarding:** Discarded as nonsensical/out of scope: The requirement that management processes must not constrain future OPAC functionality is not objectively testable as written. The acceptance criterion only demonstrates current integration and does not establish that future OPAC changes are unconstrained.

Management Process requirements must not constrain functionality or features of the Online Public Access Catalog (OPAC) module; product owners require separation of concerns so OPAC feature evolution is not restricted by management processes; acceptance: demonstrate management features integrated without requiring OPAC changes beyond documented interfaces.

### BL-003 — Support Appendix A report definitions

- **Derived from:** D10 (early_draft_srs_galecia.txt)
- **Reason for discarding:** Discarded as nonsensical/out of scope: It depends on report definitions in Appendix A, which is not included in the supplied requirements, so the required reports and acceptance criteria cannot be determined.

The system must support the reporting definitions and report types described in Appendix A (circulation, items, bibliographic records, patrons, holds, in-house use, transits, bills) to meet operational and statistical needs; acceptance: demonstrate generation of representative reports from each Appendix A category using sample data.

### BL-004 — Support fine-grained reporting (Appendix B)

- **Derived from:** D10 (early_draft_srs_galecia.txt)
- **Reason for discarding:** Discarded as nonsensical/out of scope: It depends on requirements in Appendix B, which is not included in the supplied requirements, so the required features and acceptance criteria cannot be determined.

The system must support the fine-grained reporting requirements described in Appendix B (detailed attribute selection, scheduling, output formats, etc.) to allow advanced and customized reports; acceptance: demonstrate features called out in Appendix B against sample use cases.

### BL-005 — Open template attribute selection

- **Derived from:** D10 (early_draft_srs_galecia.txt)
- **Reason for discarding:** Discarded as nonsensical/out of scope: “All attributes” across the listed record types is unbounded, and the requirement does not define a complete field set against which coverage can be tested.

Open-template reporting must expose all attributes associated with circulation, patrons, items, bills, and bibs for filtering and the same attributes for display so advanced users can craft bespoke reports; acceptance: demonstrate building a custom report that combines attributes across record types.

### BL-006 — Full field selection access

- **Derived from:** D14 (evergreen_reference_2009.txt)
- **Reason for discarding:** Discarded as nonsensical/out of scope: “A comprehensive set” of fields and “additional previously unavailable fields requested by stakeholders” do not define a bounded, testable field set.

The system shall expose a comprehensive set of database fields for reporting (including fields currently unavailable) across bibliographic_record, item, patron, action_circulation, action_hold, money, and actor record types so report authors can include necessary data elements. Acceptance: documented list of available fields includes the sample fields in the source plus additional previously unavailable fields requested by stakeholders.

### BL-007 — Export/Import Configuration

- **Derived from:** D16 (interview_sysadmin_2009-05-10.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)
- **Reason for discarding:** Discarded as nonsensical/out of scope: “An arbitrary configuration item” is unbounded; the requirement does not identify which configuration types must be exportable and importable.

The system must provide export/import functionality for report templates, permission settings, and other configuration so configurations developed in training/dev can be migrated to production reliably. Acceptance: a report template, a permission configuration, and an arbitrary configuration item can be exported from dev/training and imported to production producing equivalent behavior.

## 7. Generation notes

- Loaded 20 documents from data\corpus
- Extractor: 413 candidate requirements, 0 rejected
- Pre-dedup: +390 new, 0 dropped, pool=390
- Semantic merge: removed 116 duplicates, rejected 0 over-large/invalid groups, 274 left
- Consistency: 1 discarded, 18 edited
- Completeness review (iteration 0): 2 gaps found
- Gap extraction (iteration 1): 5 new candidates
- Pre-dedup: +2 new, 0 dropped, pool=275
- Semantic merge: removed 1 duplicates, rejected 5 over-large/invalid groups, 274 left
- Consistency: 1 discarded, 0 edited
- Completeness review (iteration 1): 2 gaps found
- Gap extraction (iteration 2): 4 new candidates
- Pre-dedup: +2 new, 0 dropped, pool=275
- Semantic merge: removed 1 duplicates, rejected 0 over-large/invalid groups, 274 left
- Consistency: 5 discarded, 0 edited
- Completeness review (iteration 2): 0 gaps found
- Prioritisation done (0 of 269 via fallback)
- Validation passed: unique ids, valid traces, valid priorities.
