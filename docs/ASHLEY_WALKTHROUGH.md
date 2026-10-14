# Ashley's code walkthrough

1. `acquire()` downloads the ZIP and preserves the original CSV. Later runs reuse it.
2. `prepare()` checks expected columns and counts blanks/duplicates. Exact duplicates
   are removed, but conflicting records at the same time trigger an error.
3. Dates become datetime objects; measurement columns become numbers. Bad values
   stop execution so a data decision can be documented rather than hidden.
4. Rows are sorted oldest to newest. A row ID lets Jacob match predictions to times.
5. `.dt.hour` extracts hour; `.dt.dayofweek` extracts weekday; weekend is 0 or 1.
6. Sine/cosine features represent a cycle: 23:50 and 00:00 should be close together.
7. The feature list includes 18 sensor columns, six weather columns, seven time columns.
   T6 is the outside north-side sensor; the sensor block is not exclusively indoor.
8. `split_ids()` puts the earliest 70% in training, next 15% in validation, final 15%
   in testing. A seeded shuffle creates a comparison split with the same counts.
9. `run()` saves reusable CSV files, feature configuration, quality report, source
   metadata/checksum. The training-only IQR flag highlights peaks without deleting them.
10. `load_split()` gives teammates predictors X, target y, and separate timestamp/ID
    metadata so the target or identifiers cannot accidentally enter X by default.

## Be ready to explain
- Cleaning does not require changing already-valid data. Checking and documenting
  that no rows need removal is legitimate data-preparation work.
- Random splits can place nearly adjacent measurements in training and testing;
  chronological splits better represent applying the model to later dates.
- Scaling the whole dataset before splitting would expose test-distribution information.
- Unusually high consumption can be real. Automatically deleting it would change
  the question and make high-use performance look better than it is.
- Current measured conditions estimate energy for the same interval. Predicting
  tomorrow needs a different feature-availability design.

Before submitting: run the commands yourself, inspect the report, and edit your
contribution record to reflect what you personally reviewed and changed.
