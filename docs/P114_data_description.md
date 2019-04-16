# P114 input file description

## Source
Based on definitions given in:
- https://www.elexon.co.uk/data-flow/settlement-report-saa-i014-also-known-as-the-s0142
- https://www.elexon.co.uk/wp-content/uploads/2015/04/P114_data-items.xlsx

Other references:
- Balancing and Settlement Code (BSC)

## Contents

<!-- TOC -->

- [P114 input file description](#p114-input-file-description)
  - [Source](#source)
  - [Contents](#contents)
  - [CDCA-I029: Aggregated GSP Group Take Volumes](#cdca-i029-aggregated-gsp-group-take-volumes)
    - [header](#header)
    - [body](#body)
      - [AGV: Aggregated GSP Group Take Volumes](#agv-aggregated-gsp-group-take-volumes)
      - [AGP: Aggregated GSP Group Take - Period](#agp-aggregated-gsp-group-take---period)
    - [footer](#footer)
  - [CDCA-I030: Meter Period Data for Distribution Area](#cdca-i030-meter-period-data-for-distribution-area)
    - [header](#header-1)
    - [body](#body-1)
      - [MPD: Meter Period Data for Distribution Area](#mpd-meter-period-data-for-distribution-area)
      - [GP9: GSP Period Data](#gp9-gsp-period-data)
      - [GMP: Processed Meter Data - Period](#gmp-processed-meter-data---period)
      - [EPD: Interconnector Period Data](#epd-interconnector-period-data)
      - [EMP: Processed Meter Data - Period](#emp-processed-meter-data---period)
      - [IPD: Inter-GSP-Group Connection Period Data](#ipd-inter-gsp-group-connection-period-data)
      - [IMP: Processed Meter Data - Period](#imp-processed-meter-data---period)
    - [Footer](#footer)
  - [CDCA-I042: BM Unit Aggregation Report](#cdca-i042-bm-unit-aggregation-report)
    - [header](#header-2)
    - [body:](#body)
      - [ABV: BM Unit Aggregation Report](#abv-bm-unit-aggregation-report)
      - [ABP: BM Unit Volume - Period](#abp-bm-unit-volume---period)
    - [footer](#footer-1)
  - [SAA-I014: Settlement Report: sub-flow 2](#saa-i014-settlement-report-sub-flow-2)
    - [header](#header-3)
    - [body](#body-2)
      - [SRH: Settlement Report header](#srh-settlement-report-header)

<!-- /TOC -->

## CDCA-I029: Aggregated GSP Group Take Volumes
### header
| Fieldname | Datatype | Comments |
| --------- | -------- | -------- |
|Unknown|||
|Unknown|||
|Unknown|||
|Unknown|||
|Unknown|||

example:
`AAA|C0291002|D|20190325082721|CD|UKDC|PB|PORTAL|351040|OPER|`

### body

#### AGV: Aggregated GSP Group Take Volumes
Single entry per GSP group

| Fieldname | Datatype | Comments |
| --------- | -------- | -------- |
| GSP Group ID | text(2) ||
| Settlement Date | date ||
| Settlement Run Type | text(2) | one of II/SF/R1/R2/R3/RF/DF|
| CDCA Run Number | integer(2) | expected range|
| Date of Aggregation | date ||

example: `AGV|_A|20161128|DF|19|20180116|`

#### AGP: Aggregated GSP Group Take - Period
46/48/50 entries corresponding to previous AGV

| Fieldname | Datatype | Comments |
| --------- | -------- | -------- |
| Settlement Period | integer(2) ||
| Estimate Indicator | boolean (T/F) ||
| Import/Export Indicator: | char (I/E)||
| GSP Group Take Volume | decimal(14,4)||

example: `AGP|1|F|I|1545.2218|`

### footer

| Fieldname | Datatype | Comments |
| --------- | -------- | -------- |
|Unknown|integer(3)||
|Unknown|integer(10)||

example: `ZZZ|688|1916476207|`


## CDCA-I030: Meter Period Data for Distribution Area
### header

| Fieldname | Datatype | Comments |
| --------- | -------- | -------- |
|Unknown|||
|Unknown|||
|Unknown|||
|Unknown|||
|Unknown|||
|Unknown|||
|Unknown|||
|Unknown|||
|Unknown|||

example: `AAA|C0301002|D|20190327074209|CD|UKDC|PB|PORTAL|351293|OPER|`

### body

#### MPD: Meter Period Data for Distribution Area
1 row per GSP Group per Settlement Date

| Fieldname | Datatype | Comments |
| --------- | -------- | -------- |
| GSP Group Id | text(2)||
| Settlement Date | text(8)||
| Settlement Run Type | text(2)||
| CDCA Run Number | integer(2)||
| Date of Aggregation | text(8)||

example: `MPD|_J|20190208|R1|8|20190326|`

#### GP9: GSP Period Data
1 row per GSP Id per Settlement Date

| Fieldname | Datatype | Comments |
| --------- | -------- | -------- |
| GSP Id | text(10) ||

example: `GP9|BEDD_1|`

#### GMP: Processed Meter Data - Period
1 row per GSP Id (given in previous GP9 entry) per Settlement Period

| Fieldname | Datatype | Comments |
| --------- | -------- | -------- |
|  Settlement Period | integer(2)||
|  Estimate Indicator | boolean T/F||
|  Meter Volume | decimal(10,3)||
|  Import/Export Indicator | char I/E||

example: `GMP|1|F|116.845|I|`

#### EPD: Interconnector Period Data
1 row per Interconnector Id

| Fieldname | Datatype | Comments |
| --------- | -------- | -------- |
| Interconnector Id | text(10) ||

example:

#### EMP: Processed Meter Data - Period
1 row per Interconnector Id (given in previous EPD entry) per Settlement Period

| Fieldname | Datatype | Comments |
| --------- | -------- | -------- |
|  Settlement Period | integer(2)||
|  Estimate Indicator | boolean T/F||
|  Meter Volume | decimal(10,3)||
|  Import/Export Indicator | char I/E||

example:

#### IPD: Inter-GSP-Group Connection Period Data

| Fieldname | Datatype | Comments |
| --------- | -------- | -------- |
|  Inter-GSP-Group Id | text(10) ||

example: `IPD|BROMLEY|`

#### IMP: Processed Meter Data - Period

| Fieldname | Datatype | Comments |
| --------- | -------- | -------- |
| Settlement Period | integer(2) ||
| Estimate Indicator | boolean T/F ||
| Meter Volume | decimal(10,3) ||
| Import/Export Indicator | char I/E ||

example: `IMP|1|F|8.692|I|`

### Footer

| Fieldname | Datatype | Comments |
| --------- | -------- | -------- |
| Unknown |||
| Unknown |||

example footer: `ZZZ|787|506868600|`


## CDCA-I042: BM Unit Aggregation Report
### header

| Fieldname | Datatype | Comments |
| --------- | -------- | -------- |
|Unknown|||
|Unknown|||
|Unknown|||
|Unknown|||
|Unknown|||
|Unknown|||
|Unknown|||
|Unknown|||
|Unknown|||

example: `AAA|C0421002|D|20190327075556|CD|UKDC|PB|PORTAL|351297|OPER|`

### body:

#### ABV: BM Unit Aggregation Report
1 per BM Unit per Settlement Date

| Fieldname | Datatype | Comments |
| --------- | -------- | -------- |
| BM Unit Id | text(11) ||
| Settlement Date | date ||
| Settlement Run Type | text(2) ||
| CDCA Run Number | integer(2) ||
| Date of Aggregation | date ||

example: `ABV|T_GANW-11|20190324|II|1|20190326|`

#### ABP: BM Unit Volume - Period
1 per BM Unit (given in previous ABV entry) per Settlement Period

| Fieldname | Datatype | Comments |
| --------- | -------- | -------- |
|  Settlement Period | integer(2) |
|  Estimate Indicator | boolean char T/F |
|  Meter Volume | decimal(10,3) |
|  Import/Export Indicator | char I/E |

example: `ABP|31|F|17.461|E|`

### footer

| Fieldname | Datatype | Comments |
| --------- | -------- | -------- |
|Unknown|||
|Unknown|||

example: `ZZZ|24943|1684565874|`


## SAA-I014: Settlement Report: sub-flow 2



### header

| Fieldname | Datatype | Comments |
| --------- | -------- | -------- |
|Unknown|||
|Unknown|||
|Unknown|||
|Unknown|||
|Unknown|||
|Unknown|||
|Unknown|||
|Unknown|||
|Unknown|||

example: `AAA|S0142008|D|20190110120638|SA|UKDC|PB|PORTAL|21783|OPER|`

### body

#### SRH: Settlement Report header

| Fieldname | Datatype | Comments |
| --------- | -------- | -------- |
|  Settlement Date | text(8) date||
|  SAA Run Number | integer(2)||
|  SAA CDCA Run Number | integer (2)||
|  SVAA CDCA Settlement Date | text(8) date||
|  SVAA CDCA Run Number | integer(2)||
|  SVAA SSR Run Number | integer(2)||
|  BSC Party Id | text(8)||

example: `SRH|20190103|II|1|1|20190103|1|46202|NGC|`
