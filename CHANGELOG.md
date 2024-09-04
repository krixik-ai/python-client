# Change Log
All notable changes to this project will be documented in this file.
 
## Version update [1.1.19] 2024-08-30

## Added
- `reset_pipeline` method moved from docs utilities to client, now available through main krixik api.


## 2024-07-10

## Changed

- Messaging for open beta data caps centralized to krixik/utilities/validators/data/__init__.py
- Rounding messaging updated
- open beta messaging for summarizer updated



## Version update [1.1.18] 2024-07-09



### Added

- cap_check api added
- tests for cap_check added

### Changed

- min python version requirement dropped from 3.10 --> 3.8
- messaging for input size failures updated for open beta

### Removed

- audio length check for a/v uploads, and corresponding ffmpeg requirement