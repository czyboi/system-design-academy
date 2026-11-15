# M00-L02 technical and provenance review

## Technical findings

- **M00-L02-T1 (minor).** The lesson's “Draw the paths and choose a deep dive” and “Trade-offs and failure modes” correctly require a fresh authoritative decision for each read. Make the assumption concrete when discussing a cache: report bytes may be cached behind the application check, while a browser or intermediary serving a cached GET response could bypass that check. Add a test that loads a report, revokes the link, and requests the same URL again through the real client path. [RFC 9110 (2022), §9.3.1](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.3.1) · [RFC 9111 (2022), §5.2.2.5](https://www.rfc-editor.org/rfc/rfc9111.html#section-5.2.2.5)

The worked read-after-revoke trace follows from the stated linearizable status operation and the commit-before-confirmation rule. The lesson bounds concurrent reads, routing, shared-store failure and surviving capacity, and treats the connection-pool diagnosis as hypothetical. The assessment correctly checks evidence before selecting either a pool change or added hosts. No deployment benchmark is claimed. The capacity-planning and evaluation sequence is supported by the cited Google and NASA sections. [Google SRE (2016), Capacity Planning](https://sre.google/sre-book/service-best-practices/#capacity-planning) · [Google SRE, The Four Golden Signals](https://sre.google/sre-book/monitoring-distributed-systems/#xref_monitoring_golden-signals) · [NASA, Systems Design Processes](https://www.nasa.gov/reference/4-0-system-design-processes/) · [NASA, Decision Analysis](https://www.nasa.gov/reference/6-8-decision-analysis/)

## Provenance findings

- **M00-L02-P1 (minor).** The lesson's single RFC 9110 link in “Draw the paths and choose a deep dive” targets the GET section while its label names GET and POST. Give each claim its own section link, as in evidence row D3. [RFC 9110, §9.3.1 GET](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.3.1) · [RFC 9110, §9.3.3 POST](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.3.3)

The evidence ledger scopes NASA guidance to the named handbook revision and Google guidance to the operational methodology. The lesson credits Donne Martin, pins the Primer revision, links the declared CC BY 4.0 license and describes the reorganization. The link-sharing scenario, workload, timebox and assessment are Academy material. No externally sourced asset or substantial excerpt is embedded. [NASA Technical Reports Server, Handbook record](https://ntrs.nasa.gov/citations/20170001761) · [Primer license at the pinned revision](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/LICENSE.txt)

Sources independently checked 2026-11-11. No executable lesson artifact was supplied.

**Verdict: ready-for-human-review.** Technical and provenance checks passed with the minor findings above.
