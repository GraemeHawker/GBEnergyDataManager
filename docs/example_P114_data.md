# P114 input file description

## Source
Based on definitions given in:
- https://www.elexon.co.uk/data-flow/settlement-report-saa-i014-also-known-as-the-s0142
- https://www.elexon.co.uk/wp-content/uploads/2015/04/P114_data-items.xlsx

Other references:
- Balancing and Settlement Code (BSC)

## Contents

- [CDCA-I029: Aggregated GSP Group Take Volumes](#cdcai029-aggregated-gsp-group-take-volumes)
- [CDCA-I042: BM Unit Aggregation Report](#cdcai042-bm-unit-aggregation-report)

## CDCA-I029: Aggregated GSP Group Take Volumes
### header
| Fieldname | Datatype | Comments |
| --------- | -------- | -------- |
||||
||||
||||
||||
||||
example:
`AAA|C0291002|D|20190325082721|CD|UKDC|PB|PORTAL|351040|OPER|`

### body

#### AGV: Aggregated GSP Group Take Volumes
Single entry per GSP group
fields:

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
fields:
  Settlement Period: integer(2)
  Estimate Indicator: boolean (T/F)
  Import/Export Indicator: char (I/E)
  GSP Group Take Volume: decimal(14,4)
example:
AGP|1|F|I|1545.2218|

### footer
  :
  :
  :
example:

ZZZ|688|1916476207|


CDCA-I030: Meter Period Data for Distribution Area
header fields:

example header:
AAA|C0301002|D|20190327074209|CD|UKDC|PB|PORTAL|351293|OPER|

body:

MPD: Meter Period Data for Distribution Area
fields:
  GSP Group Id: text(2)
  Settlement Date: text(8)
  Settlement Run Type: text(2)
  CDCA Run Number: integer(2)
  Date of Aggregation: text(8)
example:
MPD|_J|20190208|R1|8|20190326|

GP9: GSP Period Data
fields:
  GSP Id: text(10)
example:
GP9|BEDD_1|

GMP: Processed Meter Data - Period
fields:
  Settlement Period: integer(2)
  Estimate Indicator: boolean T/F
  Meter Volume: decimal(10,3)
  Import/Export Indicator: char I/E
example:
GMP|1|F|116.845|I|

EPD: Interconnector Period Data
fields:
  Interconnector Id: text(10)
example:

EMP: Processed Meter Data - Period
fields:
  Settlement Period: integer(2)
  Estimate Indicator: boolean T/F
  Meter Volume: decimal(10,3)
  Import/Export Indicator: char I/E
example:

IPD: Inter-GSP-Group Connection Period Data
fields:
  Inter-GSP-Group Id: text(10)
example:
IPD|BROMLEY|

IMP: Processed Meter Data - Period
fields:
  Settlement Period: integer(2)
  Estimate Indicator: boolean T/F
  Meter Volume: decimal(10,3)
  Import/Export Indicator: char I/E
example:
IMP|1|F|8.692|I|

example footer:
ZZZ|787|506868600|


## CDCA-I042: BM Unit Aggregation Report
header fields:

example header:
AAA|C0421002|D|20190327075556|CD|UKDC|PB|PORTAL|351297|OPER|

body:

ABV: BM Unit Aggregation Report
fields:
  BM Unit Id: text(11)
  Settlement Date: text(8) date
  Settlement Run Type: text(2)
  CDCA Run Number: integer(2)
  Date of Aggregation: text(8) date
example:
ABV|T_GANW-11|20190324|II|1|20190326|

ABP:
fields:
  Settlement Period: integer(2)
  Estimate Indicator: boolean char T/F
  Meter Volume: decimal(10,3)
  Import/Export Indicator: char I/E
example:
ABP|31|F|17.461|E|

footer fields:

example footer:
ZZZ|24943|1684565874|


SAA-I014: Settlement Report: sub-flow 2
header fields:

example header:
AAA|S0142008|D|20190110120638|SA|UKDC|PB|PORTAL|21783|OPER|
body:

SRH: Settlement Report header
fields:
  Settlement Date: text(8) date
  SAA Run Number: integer(2)
  SAA CDCA Run Number: integer (2)
  SVAA CDCA Settlement Date: text(8) date
  SVAA CDCA Run Number: integer(2)
  SVAA SSR Run Number: integer(2)
  BSC Party Id: text(8)
example:
SRH|20190103|II|1|1|20190103|1|46202|NGC|