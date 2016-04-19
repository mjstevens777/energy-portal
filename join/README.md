# Data Joins

We need a way of establishing relationships between datasets where
there is no one-to-one mapping. For this, we will assign a weight
to mappings from one dataset to another.

The end goal is a table like the following:

| `a_id` | `b_id` | `weight_a_to_b` | `weight_b_to_a` |
|--------|--------|-----------------|-----------------|
|   1    |    2   |      0.75       |        0.6      |
|   1    |    3   |      0.25       |        0.33     |
|   2    |    2   |      0.5        |        0.4      |
|   2    |    3   |      0.5        |        0.66     |
|   3    |    1   |      1.0        |        1.0      |

The goal is that the weights from a to b, grouped by the a key,
sum to 1 (similarly, weights from b to a, grouped by b, should
sum to 1). This can also be interpreted probabilistically in
terms of likelihoods. If this is the case, then the weights have
an additional constraint of obeying Bayes theorem.

For each join, produce a CSV file with this tabular format. If
appropriate, also create a script to load this into the database.

## Sparsity

We want to be careful to make sure we don't build any algorithms that
are O(n squared) on huge datasets. The join matrix should be as sparse
as possible without compromising the data quality.
