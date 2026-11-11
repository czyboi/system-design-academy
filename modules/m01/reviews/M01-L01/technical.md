# M01-L01 technical and provenance review

Checked 2026-11-11. Reviewed the teaching draft, companion, evidence, and pinned curriculum inputs recorded in the verdict.

## Technical findings

- **L01-T1 · minor · Worked example, final paragraph, and companion EX-1.** The working-set calculation uses every event created in the two-hour interval. The wording about what the set “contains only” can also be read as allowing a subset. State that every event created during the interval is accessed at least once and that no older item is accessed. [Denning, Section 3 definition and Figure 2](https://denninginstitute.com/pjd/PUBS/WSModel_1968.pdf#page=4).

Recalculated the worked example as 10 writes/s and 100 reads/s, 40 and 400 at peak, 77.76 GB retained across three copies, 97.2 GB with 25% added, 6.4 Mbit/s read egress, 0.32 Mbit/s write ingress and 72 MB of working set. The companion's changed inputs correctly yield 5 and 50 average requests/s, 20 and 200 at peak, 97.2 GB with margin, 1.6 Mbit/s read egress and 72 MB of working set. Adding dependent intervals is valid for the stipulated 41 ms and 23 ms individual traces. The lesson scopes percentiles to the end-to-end distribution and labels the timing scale as assumed. HTTP/1.1 pipelining preserves response order and may allow safe requests to be processed concurrently. [NIST, binary and SI comparisons](https://physics.nist.gov/cuu/Units/binary.html) · [RFC 9112 §9.3.2](https://www.rfc-editor.org/rfc/rfc9112.html#section-9.3.2) · [Google SRE, Demand Forecasting and Capacity Planning](https://sre.google/sre-book/introduction/#demand-forecasting-and-capacity-planning).

## Provenance findings

The evidence records source sections and scopes. The timing table and exercises use original hypothetical inputs. The historical comparison and I/O documentation support timing intuition and measurement dimensions. Their figures and code are not reproduced. The Primer attribution includes Donne Martin, pinned revision, CC BY 4.0, and a change statement. No third-party assets or implied endorsement were found. [Patterson, p. 71 and Table 1](https://pages.cs.wisc.edu/~markhill/restricted/cacm2004_latency.pdf) · [fio 3.43-22-gd645, I/O type and latency profile](https://fio.readthedocs.io/en/latest/fio_doc.html) · [Primer license at pinned revision](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/LICENSE.txt).

Verdict: **ready-for-human-review**.
