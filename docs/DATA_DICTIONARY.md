# Data dictionary

Original numeric fields are read as integer or floating-point numbers; date becomes datetime.

| Column | Meaning | Unit / encoding | Use |
|---|---|---|---|
| date | Timestamp | YYYY-MM-DD HH:MM:SS | metadata |
| Appliances | Appliance energy use | Wh | target |
| lights | Light fixture energy use | Wh | excluded from main predictors |
| T1 | Temperature, kitchen | C | predictor |
| RH_1 | Relative humidity, kitchen | % | predictor |
| T2 | Temperature, living room | C | predictor |
| RH_2 | Relative humidity, living room | % | predictor |
| T3 | Temperature, laundry room | C | predictor |
| RH_3 | Relative humidity, laundry room | % | predictor |
| T4 | Temperature, office | C | predictor |
| RH_4 | Relative humidity, office | % | predictor |
| T5 | Temperature, bathroom | C | predictor |
| RH_5 | Relative humidity, bathroom | % | predictor |
| T6 | Temperature, outside north side | C | predictor |
| RH_6 | Relative humidity, outside north side | % | predictor |
| T7 | Temperature, ironing room | C | predictor |
| RH_7 | Relative humidity, ironing room | % | predictor |
| T8 | Temperature, teenager room 2 | C | predictor |
| RH_8 | Relative humidity, teenager room 2 | % | predictor |
| T9 | Temperature, parents room | C | predictor |
| RH_9 | Relative humidity, parents room | % | predictor |
| T_out | Airport station outdoor temperature | C | predictor |
| Press_mm_hg | Station pressure | mm Hg | predictor |
| RH_out | Station relative humidity | % | predictor |
| Windspeed | Wind speed | m/s | predictor |
| Visibility | Visibility | km | predictor |
| Tdewpoint | Dew point | C | predictor |
| rv1 / rv2 | Artificial random controls | unitless | excluded |
| row_id | Stable chronological row identifier | integer | metadata only |
| hour | Hour of day | 0–23 | predictor |
| day_of_week | Monday=0 through Sunday=6 | 0–6 | predictor |
| is_weekend | Saturday/Sunday flag | 0 or 1 | predictor |
| hour_sin / hour_cos | Cyclic time of day including minutes | -1 to 1 | predictors |
| weekday_sin / weekday_cos | Cyclic weekday | -1 to 1 | predictors |

Source: https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction
