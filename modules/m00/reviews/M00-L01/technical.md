# M00-L01 technical and provenance review

## Technical findings

- **M00-L01-T1 (minor).** In the queue-consumer paragraph and evidence row R4, “manually acknowledged delivery” can sound as if the acknowledgement was accepted. The example and Q3 have the correct failure order. Use “unacknowledged delivery in manual acknowledgement mode” and tie requeueing to closure of the delivery channel or connection. [RabbitMQ 4.2, When Consumers Fail or Lose Connection](https://www.rabbitmq.com/docs/4.2/confirms#automatic-requeueing)
- **M00-L01-T2 (minor).** Evidence row R1 says an automatic retry “requires” one of two conditions. The standard gives a **SHOULD NOT** recommendation to clients and a separate **MUST NOT** rule to proxies. Preserve the client recommendation's force in the evidence. The lesson's client advice and stable-key example are compatible with it. [RFC 9110 (2022), §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)

The diagnosis correctly separates the missing HTTP response from database commit, two independent attempts from the transaction's atomicity, and a process-local hash lookup from durable cross-attempt coordination. The receipt exercise places the durable write before the acknowledgement and requires atomic duplicate handling. The study findings concern delayed memory performance in the cited experiments. The lesson scopes the Netflix video-play metric to the historical exercise. [PostgreSQL 18, Transactions](https://www.postgresql.org/docs/18/tutorial-transactions.html) · [Oracle Java SE 21, HashMap class contract](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html) · [Karpicke and Roediger, experiments 1–2](https://learninglab.psych.purdue.edu/downloads/2007/2007_Karpicke_Roediger_JML.pdf) · [Cepeda et al., abstract](https://pubmed.ncbi.nlm.nih.gov/19076480/#abstract) · [Netflix, Chaos Kong](https://netflixtechblog.com/chaos-engineering-upgraded-878d341f15fa)

## Provenance findings

- **M00-L01-P1 (minor).** The Princeton hashing lecture PDF returned HTTP 403 from the review browser. The underlying chained-hash mechanism was corroborated independently in the authors' official sample implementation and the performance qualification in Oracle's API documentation. Add the authors' reachable implementation link as a backup in the hash-lookup paragraph and evidence row R3. No source code is reproduced in the draft. [Authors' SeparateChainingHashST implementation](https://raw.githubusercontent.com/kevin-wayne/algs4/master/src/main/java/edu/princeton/cs/algs4/SeparateChainingHashST.java) · [Oracle Java SE 21, HashMap](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html)

The evidence ledger identifies the external factual references, learning studies, Harvard lecture and historical Netflix report. The lesson links to those resources. The lesson credits Donne Martin, pins the Primer revision, links the declared CC BY 4.0 license and describes the reorganization. The diagnostics, exercise and answer prose use Academy examples. No externally sourced figure, slide, video, code or long quotation is embedded. [Harvard, Scalability](https://cs50.harvard.edu/summer/web/2019/lectures/10/) · [Primer license at the pinned revision](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/LICENSE.txt)

Sources independently checked 2026-11-11. No executable lesson artifact was supplied.

**Verdict: ready-for-human-review.** Technical and provenance checks passed with the minor findings above.
