"""Checks for leakage boundaries, data validity, and deterministic preparation."""
import unittest
import numpy as np
import pandas as pd
from src.prepare_data import ROOT, FEATURES, RAW_COLUMNS, prepare, split_ids
from src.load_data import load_split

class PreparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = pd.read_csv(ROOT / "data/raw/energydata_complete.csv")
        cls.df, cls.audit = prepare(cls.raw)

    def test_split_membership(self):
        for method, parts in split_ids(len(self.df)).items():
            sets = [set(ids) for ids in parts.values()]
            self.assertEqual(set.union(*sets), set(range(len(self.df))))
            self.assertFalse(sets[0] & sets[1] or sets[0] & sets[2] or sets[1] & sets[2])
        parts = split_ids(len(self.df))["chronological"]
        self.assertLess(self.df.iloc[parts['train']].date.max(), self.df.iloc[parts['validation']].date.min())
        self.assertLess(self.df.iloc[parts['validation']].date.max(), self.df.iloc[parts['test']].date.min())
        np.testing.assert_array_equal(split_ids(100)['random']['test'], split_ids(100)['random']['test'])

    def test_no_target_or_identifiers_in_features(self):
        self.assertFalse(set(FEATURES) & {'Appliances','date','row_id','lights','rv1','rv2'})
        self.assertTrue(np.isfinite(self.df[FEATURES].to_numpy()).all())
        for method in ('chronological','random'):
            for part in ('train','validation','test'):
                X,y,meta=load_split(method,part)
                self.assertEqual(list(X.columns),FEATURES)
                self.assertEqual(len(X),len(y))
                self.assertEqual(len(X),len(meta))

    def test_duplicates_removed_but_peaks_kept(self):
        doubled = pd.concat([self.raw, self.raw.iloc[[0]]], ignore_index=True)
        clean, audit = prepare(doubled)
        self.assertEqual(len(clean), len(self.df))
        self.assertEqual(audit['exact_duplicate_rows_removed'], 1)
        self.assertEqual(clean.Appliances.max(), self.raw.Appliances.max())

    def test_bad_data_fails(self):
        for column, value in [('T1', None), ('RH_1', 101), ('Appliances', -1), ('date', 'bad-date')]:
            bad=self.raw.copy(); bad.loc[0,column]=value
            with self.assertRaises((ValueError,TypeError)):
                prepare(bad)
        bad=self.raw.copy(); bad.loc[1,'date']=bad.loc[0,'date']
        with self.assertRaises(ValueError): prepare(bad)

    def test_calendar_features(self):
        self.assertTrue((self.df.is_weekend == (self.df.day_of_week >= 5).astype(int)).all())
        np.testing.assert_allclose(self.df.hour_sin**2+self.df.hour_cos**2,1,atol=1e-12)

if __name__ == '__main__': unittest.main()
