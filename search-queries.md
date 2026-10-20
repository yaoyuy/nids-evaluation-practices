# Search queries (executed verbatim)

Source: OpenAlex, endpoint `https://api.openalex.org/works`.
Date executed: 18 October 2026.

Both queries were passed as the `filter` parameter, restricted with the common clause below, and were run over the `title_and_abstract.search` field. Paging used `page=1..N` with `per-page=200`; cursor paging returned HTTP 401 to the author's host and was not used.

## Query Q1 (intrusion detection x deep learning x benchmark dataset names)

```
title_and_abstract.search:
  ("intrusion detection" OR "network intrusion" OR "network anomaly")
  AND ("deep learning" OR LSTM OR CNN OR transformer OR autoencoder OR "neural network" OR "convolutional")
  AND ("NSL-KDD" OR "KDD99" OR "KDD Cup" OR "KDDCup" OR "CICIDS" OR "CIC-IDS"
       OR "UNSW-NB15" OR "Bot-IoT" OR "TON_IoT" OR "CICDDoS" OR "CSE-CIC")
```

Records returned: **2,033**.

## Query Q2 (intrusion detection x deep learning x evaluation vocabulary)

```
title_and_abstract.search:
  ("intrusion detection" OR "network intrusion")
  AND ("deep learning" OR LSTM OR CNN OR transformer OR autoencoder)
  AND ("data leakage" OR "reproducibility" OR "evaluation protocol"
       OR "train-test split" OR "benchmark dataset" OR "experimental setup")
```

Records returned: **413**.

## Common restriction applied to both queries

```
from_publication_date:2019-01-01
to_publication_date:2025-12-31
type:article
language:en
```

After de-duplication of the two result sets by OpenAlex identifier and DOI, the combined candidate set contained **2,241** unique records.

## Fields requested from the API

```
id,doi,title,publication_year,type,language,primary_location,best_oa_location,
open_access,abstract_inverted_index,cited_by_count,authorships
```

## Coverage of the search

The search was run on OpenAlex, which is reachable without institutional authentication. Scopus, Web of Science and IEEE Xplore sit behind institutional subscriptions that were not available to the author, and the Semantic Scholar API returned rate-limit responses throughout the retrieval window. OpenAlex indexes the great majority of the journals those databases cover; its coverage of conference proceedings and of the most recent issues is incomplete. The included set is a structured, reproducible sample of the indexed literature. The citation-snowballing check in `results/snowball-summary.json` quantifies the coverage gap.