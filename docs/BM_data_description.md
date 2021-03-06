# BMRA Data Description
Each message is composed of three sections:
- timestamp (yyyy:MM:dd:hh:mm:ss:GMT) at which message was received
- subject line, indicating message type and subtype (and possibly also BM Unit and Notification Level)
- message, containing key/value pairs

Each message subtype is listed below along with the expected data within each message

Example lines given below are exactly as seen in raw data file

References:
- https://www.elexon.co.uk/bsc-and-codes/bsc-related-documents/interface-definition-documents/
- https://www.elexon.co.uk/csd/neta-programme-interface-definition-and-design-part-1-interfaces-with-bsc-parties-and-their-agents/
- https://test.bmreports.com/bmrs/?q=help/glossary


# Contents

<!-- TOC depthFrom:2 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [General parameters](#general-parameters)
- [BM Unit Data](#bm-unit-data)
	- [Submissions](#submissions)
		- [FPN / QPN: Final Physical Notification / Quiescent Physical Notification](#fpn-qpn-final-physical-notification-quiescent-physical-notification)
		- [MEL / MIL: Maximum Export Limit / Maximum Import Limit](#mel-mil-maximum-export-limit-maximum-import-limit)
		- [BOD: Bid/Offer Data](#bod-bidoffer-data)
	- [Acceptances](#acceptances)
		- [BOAL: Bid Offer Acceptance Level](#boal-bid-offer-acceptance-level)
		- [BOALF: Bid Offer Acceptance Level Flagged](#boalf-bid-offer-acceptance-level-flagged)
	- [Cashflow and Volume Calculations](#cashflow-and-volume-calculations)
		- [BOAV: Bid-offer Acceptance Volumes](#boav-bid-offer-acceptance-volumes)
		- [EBOCF: Estimated Bid-Offer Cash Flows](#ebocf-estimated-bid-offer-cash-flows)
		- [PTAV: Period Total Bid-Offer Acceptance Volumes](#ptav-period-total-bid-offer-acceptance-volumes)
		- [DISPTAV: Disaggregated Period Total Bid-Offer Acceptance Volumes](#disptav-disaggregated-period-total-bid-offer-acceptance-volumes)
		- [QAS: BM Unit applicable balancing services Volume](#qas-bm-unit-applicable-balancing-services-volume)
- [Dynamic Data](#dynamic-data)
	- [General Parameters](#general-parameters)
	- [Submissions](#submissions)
		- [SIL: Stable Import Limit](#sil-stable-import-limit)
		- [SEL: Stable Export Limit](#sel-stable-export-limit)
		- [MNZT: Minimum Non-zero Time](#mnzt-minimum-non-zero-time)
		- [NDZ: Notice to deviate from zero](#ndz-notice-to-deviate-from-zero)
		- [RURE: Run-up rates export](#rure-run-up-rates-export)
		- [RURI: Run-up rates import](#ruri-run-up-rates-import)
		- [RDRE: Run-down rate Export](#rdre-run-down-rate-export)
		- [RDRI: Run-down rate Import](#rdri-run-down-rate-import)
		- [MDV: Maximum Delivery Volume](#mdv-maximum-delivery-volume)
		- [MDP: Maximum Delivery Period](#mdp-maximum-delivery-period)
		- [MZT: Minimum Zero Time](#mzt-minimum-zero-time)
		- [NTB: Notice to deliver bids](#ntb-notice-to-deliver-bids)
		- [NTO: Notice to deliver offers](#nto-notice-to-deliver-offers)
- [SYSTEM Data](#system-data)
	- [Price Calculation Data](#price-calculation-data)
		- [BSAD: Balancing Services Adjustment Data](#bsad-balancing-services-adjustment-data)
		- [DISBSAD: Balancing Services Adjustment Action Data](#disbsad-balancing-services-adjustment-action-data)
		- [NETBSAD: Balancing Services Adjustment Data](#netbsad-balancing-services-adjustment-data)
		- [MID: Market Index Data](#mid-market-index-data)
		- [EBSP: Estimated buy and sell price](#ebsp-estimated-buy-and-sell-price)
		- [NETEBSP: Estimated Buy and Sell Price](#netebsp-estimated-buy-and-sell-price)
		- [DISEBSP: Disaggregated Estimated Buy and Sell Price](#disebsp-disaggregated-estimated-buy-and-sell-price)
		- [SOSO: SO to SO prices](#soso-so-to-so-prices)
		- [ISPSTACK: Indicative System Price Stack](#ispstack-indicative-system-price-stack)
		- [TBOD: Total Bid Offer Data](#tbod-total-bid-offer-data)
	- [Forecasting Data](#forecasting-data)
		- [DF: Demand Forecast](#df-demand-forecast)
		- [NDF: National Demand Forecast](#ndf-national-demand-forecast)
		- [TSDF: Transmission System Demand Forecast](#tsdf-transmission-system-demand-forecast)
		- [IMBALNGC: Indicated Imbalance](#imbalngc-indicated-imbalance)
		- [INDGEN: Indicated Generation](#indgen-indicated-generation)
		- [MELNGC: Indicated Margin](#melngc-indicated-margin)
		- [INDDEM: Indicated demand](#inddem-indicated-demand)
		- [NDFD: Demand Forecast, 2-14 days ahead](#ndfd-demand-forecast-2-14-days-ahead)
		- [TSDFD: Transmission System Demand Forecast](#tsdfd-transmission-system-demand-forecast)
		- [TSDFW: Transmission System Demand Forecast, 2-52 weeks](#tsdfw-transmission-system-demand-forecast-2-52-weeks)
		- [NDFW: Demand Forecast, 2-52 weeks](#ndfw-demand-forecast-2-52-weeks)
		- [OCNMFW: Surplus forecast 2-52 weeks ahead](#ocnmfw-surplus-forecast-2-52-weeks-ahead)
		- [OCNMFW2: Generating Plant Demand Margin, 2-52 weeks ahead](#ocnmfw2-generating-plant-demand-margin-2-52-weeks-ahead)
		- [WINDFOR: Forecast peak wind generation](#windfor-forecast-peak-wind-generation)
		- [OCNMFD: Surplus forecast 2-14 days ahead](#ocnmfd-surplus-forecast-2-14-days-ahead)
		- [OCNMFD2: Generating Plant margin, 2-14 days ahead](#ocnmfd2-generating-plant-margin-2-14-days-ahead)
		- [FOU2T14D: National Output Usable by Fuel Type, 2-14 Days ahead](#fou2t14d-national-output-usable-by-fuel-type-2-14-days-ahead)
		- [FOU2T52W: National Output Usable by Fuel Type, 2-52 weeks ahead](#fou2t52w-national-output-usable-by-fuel-type-2-52-weeks-ahead)
	- [SO Messages](#so-messages)
		- [SYSWARN: System Warning](#syswarn-system-warning)
		- [SYSMSG: System Message](#sysmsg-system-message)
		- [DCONTROL: Demand Control Instruction Notification](#dcontrol-demand-control-instruction-notification)
	- [Out-turn Data](#out-turn-data)
		- [FREQ: System frequency data](#freq-system-frequency-data)
		- [TEMP: Temperature Data](#temp-temperature-data)
		- [INDO: Initial National Demand Out-Turn](#indo-initial-national-demand-out-turn)
		- [ITSDO: Initial Transmission System Demand Outturn](#itsdo-initial-transmission-system-demand-outturn)
		- [LOLP: Loss of Load Probability and De-rated Margin](#lolp-loss-of-load-probability-and-de-rated-margin)
		- [NONBM: Non-BM STOR Out-Turn](#nonbm-non-bm-stor-out-turn)
		- [INDOD: Daily Energy Volume Data](#indod-daily-energy-volume-data)
		- [FUELINST: Instantaneous Generation by Fuel Type](#fuelinst-instantaneous-generation-by-fuel-type)
		- [FUELHH: Half-hourly system-level generation by fuel type](#fuelhh-half-hourly-system-level-generation-by-fuel-type)
- [Balancing Party-Level Data](#balancing-party-level-data)
	- [Credit Data](#credit-data)
		- [CDN: Credit Default Notice](#cdn-credit-default-notice)
- [INFO type messages](#info-type-messages)
	- [Test Messages](#test-messages)
		- [TEST: Test message](#test-test-message)
		- [MSG: Test message](#msg-test-message)

<!-- /TOC -->

## General parameters

For brevity, these are common fields used by multiple message types, not further described. Where these are used they are listed by fieldname in the individual message indices.

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
| TP | datetime | Publishing time | | The time that the data was originally published by the System Operator,  formatted yyyy:MM:dd:hh:mm:ss:GMT |
| SD | date | Settlement Date | | formatted yyyy:MM:dd:00:00:00:GMT |
| SP | integer(2) | Settlement Period | between 1 and 50 inclusive | |
| TS | datetime | Timestamp of spot point | | formatted yyyy:MM:dd:hh:mm:ss:GMT |
| NP | integer(2) | Number of spot points | | &nbsp; |

## BM Unit Data

### Submissions

#### FPN / QPN: Final Physical Notification / Quiescent Physical Notification

A Physical Notification is the intended export(+ve)/import(-ve) of a BMU nominated ahead of gate closure, and may be amended at any time up to gate closure.

The FPN is the most recent PN submitted when gate closure passes, QPNs are the PNs which have been superceded prior to gate closure.

Message consists of multiple timestamp and power value spot points (usually, but sometimes more than, 2)

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|VP| float|Power value| MW|&nbsp;|

Index: BMU, SD, SP (BMU is indicated in message subject, SD/SP in message body)

Unique FPNs exist for each index, however multiple QPNs may exist for a single BMU/SP, where values have been resubmitted.

Example:

`2017:03:29:00:02:03:GMT: subject=BMRA.BM.T_ABTH9.FPN, message={SD=2017:03:29:00:00:00:GMT,SP=5,NP=2,TS=2017:03:29:01:00:00:GMT,VP=0.0,TS=2017:03:29:01:30:00:GMT,VP=0.0}`

`2017:03:29:00:02:17:GMT: subject=BMRA.BM.E_ABERDARE.QPN, message={SD=2017:03:29:00:00:00:GMT,SP=5,NP=2,TS=2017:03:29:01:00:00:GMT,VP=0.0,TS=2017:03:29:01:30:00:GMT,VP=0.0}`

#### MEL / MIL: Maximum Export Limit / Maximum Import Limit

The MEL is the maximum level at which a BMU may be exporting to the GB Transmission System at the Grid Supply Point, as nominated by the operator.

The MIL is the maximum level at which a BMU may be importing from the GB Transmission System at the Grid Supply Point, as nominated by the operator.

Message consists of multiple timestamp and power value spot points (usually, but sometimes more than, 2)

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|VE| float|(maximum export) power value| MW|&nbsp;|
|VF| float|(maximum import) power value| MW|&nbsp;|

Index: BMU, SD, SP, TS (BMU is indicated in message subject, SD/SP in message body)

Example:

`2017:03:29:00:02:16:GMT: subject=BMRA.BM.T_SIZB-2.MEL, message={SD=2017:03:29:00:00:00:GMT,SP=5,NP=2,TS=2017:03:29:01:00:00:GMT,VE=602.0,TS=2017:03:29:01:30:00:GMT,VE=602.0}`

`2017:03:29:00:01:51:GMT: subject=BMRA.BM.T_DRAXX-1.MIL, message={SD=2017:03:29:00:00:00:GMT,SP=5,NP=2,TS=2017:03:29:01:00:00:GMT,VF=0.0,TS=2017:03:29:01:30:00:GMT,VF=0.0}`

#### BOD: Bid/Offer Data

Message consists of bid/offer spot points (normally, but not always, corresponding to the settlement period start and settlement period end).

BOD pairs may extend from -5 to +5 e.g. up to 10 operating points each with 2 bid/offer pairs.

Bids relate to reductions in export / increases in import

Offers relate to increases in export / reductions in import

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|NN| integer |bid-offer pair number| MW|in range -5 to 5|
|OP| float|offer price| £/MWh|&nbsp;|
|BP| float|bid price| £/MWh|&nbsp;|
|VB| float|bid volume| £/MWh|&nbsp;|

Index: BMU, SD, SP, TS, NN (NN contained in message subject and body)

Example:

`2017:03:29:00:02:02:GMT: subject=BMRA.BM.T_DRAXX-1.BOD.-4, message={SD=2017:03:29:00:00:00:GMT,SP=5,NN=-4,OP=45.0,BP=-250.0,NP=2,TS=2017:03:29:01:00:00:GMT,VB=-645.0,TS=2017:03:29:01:30:00:GMT,VB=-645.0}`

`2017:03:29:00:02:02:GMT: subject=BMRA.BM.T_DRAXX-1.BOD.-3, message={SD=2017:03:29:00:00:00:GMT,SP=5,NN=-3,OP=45.0,BP=-100.0,NP=2,TS=2017:03:29:01:00:00:GMT,VB=-255.0,TS=2017:03:29:01:30:00:GMT,VB=-255.0}`

`2017:03:29:00:02:02:GMT: subject=BMRA.BM.T_DRAXX-1.BOD.-2, message={SD=2017:03:29:00:00:00:GMT,SP=5,NN=-2,OP=45.0,BP=-100.0,NP=2,TS=2017:03:29:01:00:00:GMT,VB=-95.0,TS=2017:03:29:01:30:00:GMT,VB=-95.0}`

`2017:03:29:00:02:02:GMT: subject=BMRA.BM.T_DRAXX-1.BOD.-1, message={SD=2017:03:29:00:00:00:GMT,SP=5,NN=-1,OP=45.0,BP=-100.0,NP=2,TS=2017:03:29:01:00:00:GMT,VB=-95.0,TS=2017:03:29:01:30:00:GMT,VB=-95.0}`

`2017:03:29:00:02:02:GMT: subject=BMRA.BM.T_DRAXX-1.BOD.1, message={SD=2017:03:29:00:00:00:GMT,SP=5,NN=1,OP=150.0,BP=0.0,NP=2,TS=2017:03:29:01:00:00:GMT,VB=645.0,TS=2017:03:29:01:30:00:GMT,VB=645.0}`

`2017:03:29:00:02:02:GMT: subject=BMRA.BM.T_DRAXX-1.BOD.2, message={SD=2017:03:29:00:00:00:GMT,SP=5,NN=2,OP=500.0,BP=0.0,NP=2,TS=2017:03:29:01:00:00:GMT,VB=645.0,TS=2017:03:29:01:30:00:GMT,VB=645.0}`

### Acceptances

#### BOAL: Bid Offer Acceptance Level

Acceptance data for a single BM Unit, for a single acceptance for Settlement Dates before the P217 effective date. The data is published as it is received from the System Operator.

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|NK|integer|Acceptance number||unique ID|
|TA|datetime|Acceptance time|||
|AD|char(1) boolean|Deemed bid-offer flag|'T'/'F'|Indicates whether Bid-Offer was made for an acceptance. Value is 'T' or 'F'. If true, no Bid-Offer was made.|
|VA|float|Acceptance level value|MW|&nbsp;|

Example:

`2009:01:01:00:09:41:GMT: subject=BMRA.BM.T_SHBA-1.BOAL, message={NK=59073,TA=2009:01:01:00:09:00:GMT,AD=F,NP=4,TS=2009:01:01:00:11:00:GMT,VA=597.0,TS=2009:01:01:00:13:00:GMT,VA=560.0,TS=2009:01:01:00:28:00:GMT,VA=560.0,TS=2009:01:01:00:30:00:GMT,VA=498.0}`


#### BOALF: Bid Offer Acceptance Level Flagged

Acceptance data for a single BM Unit, for a single acceptance for Settlement Dates on and after the P217 effective date. The data is published as it is received from the System Operator.

Implemented on 2009-11-09 as part of P217

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|NK|integer|Acceptance number||unique ID|
|TA|datetime|Acceptance time|||
|AD|char(1) boolean|Deemed bid-offer flag|'T'/'F'|Indicates whether Bid-Offer was made for an acceptance. Value is 'T' or 'F'. If true, no Bid-Offer was made.|
|SO|char(1) boolean|SO Flag|'T'/'F'|A value of ‘T’ indicates where an Acceptance or Balancing Services Adjustment Action item should be considered to be potentially impacted by transmission constraints.|
|PF|char(1) boolean|STOR Flag|'T'/'F'|A value of ‘T’ indicates where an Acceptance or Balancing Services Adjustment Action item should be considered being related to a STOR Provider|
|RN|char(1) boolean|RR Instruction Flag|'T'/'F'|A value of ‘T’ indicates where an Acceptance or Balancing Services Adjustment Action item should be considered being related to a Replacement Reserve instruction|
|SC|char(1) boolean|RR Schedule Flag|'T'/'F'|A value of ‘T’ indicates where an Acceptance or Balancing Services Adjustment Action item should be considered being related to a Replacement Reserve schedule|
|VA|float|Acceptance level value|MW|&nbsp;|

Example:

`2017:04:21:00:00:43:GMT: subject=BMRA.BM.T_SCCL-1.BOALF, message={NK=52908,SO=T,PF=F,TA=2017:04:20:23:59:00:GMT,AD=F,NP=4,TS=2017:04:21:00:05:00:GMT,VA=367.0,TS=2017:04:21:00:09:00:GMT,VA=310.0,TS=2017:04:21:00:35:00:GMT,VA=310.0,TS=2017:04:21:00:39:00:GMT,VA=367.0`


### Cashflow and Volume Calculations

#### BOAV: Bid-offer Acceptance Volumes

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|NN|integer|Bid-offer pair number||in range -5 to 5|
|NK|integer|Acceptance number||unique ID|
|BV|float|Bid volume|MWh||
|OV|float|Offer volume|MWh||
|SA|char(1)|Short acceptance flag||'S' or 'L' for short or long|

Example:

`2017:04:21:00:21:54:GMT: subject=BMRA.BM.T_EECL-1.BOAV.1, message={SD=2017:04:21:00:00:00:GMT,SP=2,NN=1,NK=88365,OV=0.0833,BV=0.0,SA=L}`


#### EBOCF: Estimated Bid-Offer Cash Flows

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|NN|integer|Bid-offer pair number||in range -5 to 5|
|BC|float|Bid cashflow|£||
|OC|float|Offer cashflow|£||

Example:

`2017:04:21:00:21:54:GMT: subject=BMRA.BM.T_EECL-1.EBOCF.1, message={SD=2017:04:21:00:00:00:GMT,SP=2,NN=1,OC=4.95,BC=0.0}`

#### PTAV: Period Total Bid-Offer Acceptance Volumes

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|NN|integer|Bid-offer pair number||in range -5 to 5|
|BV|float|Total bid volume accepted for BO pair|MWh||
|OV|float|Total offer volume accepted for BO pair|MWh||

Example:

`2009:01:01:00:20:20:GMT: subject=BMRA.BM.T_DAMC-1.PTAV.-1, message={SD=2008:12:31:00:00:00:GMT,SP=48,NN=-1,OV=1.5833334,BV=-8.333333}`

#### DISPTAV: Disaggregated Period Total Bid-Offer Acceptance Volumes

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|NN|integer|Bid-offer pair number||in range -5 to 5|
|BV|float|Total bid volume accepted for BO pair|MWh||
|OV|float|Total offer volume accepted for BO pair|MWh||
|P1||Tagged element of the Total Offer Volume accepted|||
|P2||Repriced element of the Total Offer Volume accepted|||
|P3||Originally-priced element of the Total Offer Volume accepted|||
|P4||Tagged element of the Total Bid Volume accepted|||
|P5||Repriced element of the Total Bid Volume accepted|||
|P6||Originally-priced element of the Total Bid Volume accepted||&nbsp;|

Example:

`2017:04:21:00:21:54:GMT: subject=BMRA.BM.T_EECL-1.DISPTAV.1, message={SD=2017:04:21:00:00:00:GMT,SP=2,NN=1,OV=0.0833,P1=0.0833,P2=0.0,P3=0.0,BV=0.0,P4=0.0,P5=0.0,P6=0.0}`

#### QAS: BM Unit applicable balancing services Volume

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|SV||Energy Volume for the Settlement Period|MWh|&nbsp;|

Example:

`2017:04:21:07:12:49:GMT: subject=BMRA.BM.T_BAGE-1.QAS, message={SD=2017:04:20:00:00:00:GMT,SP=1,SV=1.621}`



## Dynamic Data

### General Parameters
TE: Time effective from

### Submissions

#### SIL: Stable Import Limit
  Parameters:
    SI: Stable Import Limit (MW)

Example:

`2018:01:02:11:56:15:GMT: subject=BMRA.DYNAMIC.2__MPGEN002.SIL, message={TE=2018:01:02:11:54:00:GMT,SI=0.0}`


#### SEL: Stable Export Limit
  Parameters:
    SE: Stable Export Limit (MW)

Example:

`2017:04:21:01:21:21:GMT: subject=BMRA.DYNAMIC.T_ROCK-1.SEL, message={TE=2017:04:21:01:20:00:GMT,SE=240.0}`

#### MNZT: Minimum Non-zero Time
  Parameters:
    MN: Minimum non-zero time (seconds? minutes?)

Example:

`2017:04:21:01:21:54:GMT: subject=BMRA.DYNAMIC.T_STAY-2.MNZT, message={TE=2017:04:21:01:21:00:GMT,MN=360}`

#### NDZ: Notice to deviate from zero
  Parameters:
    DZ: Notice to deviate from zero time (seconds? minutes?)

Example:

`2017:04:21:01:21:55:GMT: subject=BMRA.DYNAMIC.T_STAY-2.NDZ, message={TE=2017:04:21:01:21:00:GMT,DZ=58}`

#### RURE: Run-up rates export
  Parameters:
    U1: Run up rate 1 (MW/minute)
    UB: Run up elbow 2 (MW)
    U2: Run up rate 2 (MW/minute)
    UC: Run up elbow 3 (MW)
    U3: Run up rate 3 (MW/minute)

Example:

`2017:04:21:01:22:19:GMT: subject=BMRA.DYNAMIC.T_STAY-2.RURE, message={TE=2017:04:21:01:21:00:GMT,U1=8.4,UB=45,U2=0.2,UC=48,U3=17.5}`

#### RURI: Run-up rates import
  Parameters:
    U1: Run up rate 1 (MW/minute)
    UB: Run up elbow 2 (MW)
    U2: Run up rate 2 (MW/minute)
    UC: Run up elbow 3 (MW)
    U3: Run up rate 3 (MW/minute)

Example:

`2002:01:02:17:02:01:GMT: subject=BMRA.DYNAMIC.2__JYELG001.RURI, message={TE=2002:01:02:17:00:00:GMT,U1=900.0,UB=0,U2=0.0,UC=0,U3=0.0}`

#### RDRE: Run-down rate Export
  Parameters:
    R1: Run up rate 1 (MW/minute)
    RB: Run up elbow 2 (MW)
    R2: Run up rate 2 (MW/minute)
    RC: Run up elbow 3 (MW)
    R3: Run up rate 3 (MW/minute)

Example:

`2017:04:21:05:04:39:GMT: subject=BMRA.DYNAMIC.T_ROCK-1.RDRE, message={TE=2017:04:21:05:04:00:GMT,R1=25.0,RB=220,R2=47.5,RC=125,R3=55.0}`

#### RDRI: Run-down rate Import
  Parameters:
    R1: Run up rate 1 (MW/minute)
    RB: Run up elbow 2 (MW)
    R2: Run up rate 2 (MW/minute)
    RC: Run up elbow 3 (MW)
    R3: Run up rate 3 (MW/minute)

Example:

`2002:01:02:17:01:50:GMT: subject=BMRA.DYNAMIC.2__JYELG001.RDRI, message={TE=2002:01:02:17:00:00:GMT,R1=900.0,RB=0,R2=0.0,RC=0,R3=0.0}`

#### MDV: Maximum Delivery Volume
  Parameters:
    DV: Delivery Volume

Example:

`2002:01:02:17:01:13:GMT: subject=BMRA.DYNAMIC.2__JYELG001.MDV, message={TE=2002:01:02:17:00:00:GMT,DV=-44.0}`

#### MDP: Maximum Delivery Period
  Parameters:
    DP: Delivery period

Example:

`2002:01:02:17:01:14:GMT: subject=BMRA.DYNAMIC.2__JYELG001.MDP, message={TE=2002:01:02:17:00:00:GMT,DP=239}`


#### MZT: Minimum Zero Time
  Parameters:
    MZ: Minimum Zero Time (seconds? minutes?)

Example:

`2017:04:21:02:20:27:GMT: subject=BMRA.DYNAMIC.T_FOYE-2.MZT, message={TE=2017:04:21:02:19:00:GMT,MZ=30}`

#### NTB: Notice to deliver bids
  Parameters:
    DB: Notice to deliver bids (minutes)
Example:

`2017:04:21:02:20:44:GMT: subject=BMRA.DYNAMIC.T_FOYE-2.NTB, message={TE=2017:04:21:02:19:00:GMT,DB=2}`

#### NTO: Notice to deliver offers
  Parameters:
    DO: Notice to deliver offers (minutes)
Example:

`2017:04:21:02:20:44:GMT: subject=BMRA.DYNAMIC.T_FOYE-2.NTO, message={TE=2017:04:21:02:19:00:GMT,DO=2}`

## SYSTEM Data

### Price Calculation Data

#### BSAD: Balancing Services Adjustment Data
Ceased on P217 effective date of 2009-11-09, replaced by DISBSAD and NETBSAD

https://www.elexon.co.uk/mod-proposal/p217-revised-tagging-process-and-calculation-of-cash-out-prices/

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
| A1 |decimal(10,2)|Sell price cost Adjustment|£||
| A2 |decimal(10,3)|Sell price volume Adjustment|MWh||
| A3 |decimal(10,3)|Sell price price adjustment|£/MWh||
| A4 |decimal(10,2)|Buy price cost Adjustment|£||
| A5 |decimal(10,3)|Buy price volume Adjustment|MWh||
| A6 |decimal(10,3)|Buy price price adjustment|£/MWh|&nbsp;|

Index: SD, SP

Example:

`2003:01:01:00:08:12:GMT: subject=BMRA.SYSTEM.BSAD, message={SD=2003:01:01:00:00:00:GMT,SP=3,A1=-5248.75,A2=-417.5,A3=0.0,A4=0.0,A5=0.0,A6=3.11}`

#### DISBSAD: Balancing Services Adjustment Action Data
Implemented on 2009-11-09 as part of P217

https://www.elexon.co.uk/mod-proposal/p217-revised-tagging-process-and-calculation-of-cash-out-prices/

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|AI|integer|Adjustment Identifier|Unique integer||
|SO|char(1) boolean|SO Flag|'T'/'F'|A value of ‘T’ indicates where an Acceptance or Balancing Services Adjustment Action item should be considered to be potentially impacted by transmission constraints|
|PF|char(1) boolean|STOR Flag|'T'/'F'|A value of ‘T’ indicates where an Acceptance or Balancing Services Adjustment Action item should be considered being related to a STOR Provider|
|JC|decimal(10,2)|Adjustment cost|£|Blank where zero / null if unpriced|
|JV|decimal(10,3)|Adjustment volume|MWh|&nbsp;|

Index: SD, SP

Example:

`2017:04:21:00:09:12:GMT: subject=BMRA.SYSTEM.DISBSAD, message={SD=2017:04:21:00:00:00:GMT,SP=5,AI=4,SO=T,PF=F,JC=9360.0,JV=120.0}`

#### NETBSAD: Balancing Services Adjustment Data
Implemented on 2009-11-09 as part of P217

https://www.elexon.co.uk/mod-proposal/p217-revised-tagging-process-and-calculation-of-cash-out-prices/

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|A7|decimal(10,2)|Net Energy Sell Price Cost Adjustment (ESCA)|£||
|A8|decimal(10,3)|Net Energy Sell Price Volume Adjustment (ESVA)|MWh||
|A11|decimal(10,3)|Net System Sell Price Volume Adjustment (SSVA)|MWh||
|A3|decimal(10,2)|Sell Price Price Adjustment (SPA)|£||
|A9|decimal(10,2)|Net Energy Buy Price Cost Adjustment (EBCA)|£||
|A10|decimal(10,3)|Net Energy Buy Price Volume Adjustment (EBVA)|MWh||
|A12|decimal(10,3)|Net System Buy Price Volume Adjustment (SBVA)|MWh||
|A6|decimal(10,2)|Buy Price Price Adjustment (BPA)|£|&nbsp;|

Index: SD, SP

Example:

`2017:04:21:00:09:13:GMT: subject=BMRA.SYSTEM.NETBSAD, message={SD=2017:04:21:00:00:00:GMT,SP=5,A7=0.0,A8=0.0,A11=0.0,A3=0.0,A9=0.0,A10=0.0,A12=0.0,A6=0.0}`

#### MID: Market Index Data

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
| MI | text(8)| Market Index Data Provider | | e.g. APXMIDP |
| M1 | decimal(10,2) | Market Index Price | £/MWh | can be null |
| M2 | decimal(10,2) | Market Index Volume | MWh | can be null |

Index: MI, SD, SP

One row per Settlement Period per Market Index Data Provider

Example:

`2017:03:29:00:00:37:GMT: subject=BMRA.SYSTEM.MID, message={MI=APXMIDP,SD=2017:03:29:00:00:00:GMT,SP=2,M1=34.58,M2=223.7}`

#### EBSP: Estimated buy and sell price
Ceased on P217 effective date of 2009-11-09

https://www.elexon.co.uk/mod-proposal/p217-revised-tagging-process-and-calculation-of-cash-out-prices/

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|PB|decimal(10,5)|Buy price - the price that must be paid for electricity which is out of balance|£||
|PS|decimal(10,5)|Sell Price - the price received for electricity which is out of balance|£||
|AO|decimal(10,3)|Total Accepted Offer Volume - System wide total Accepted Offer Volume for the Settlement Period|MWh||
|AB|decimal(10,3)|Total Accepted Bid Volume - System wide total Accepted Bid Volume for the Settlement Period|MWh||
|AP|decimal(10,3)|Total Unpriced Accepted Offer Volume - System wide total Unpriced Accepted Offer Volume for the Settlement Period|MWh||
|AC|decimal(10,3)|Total Unpriced Accepted Bid Volume - System wide total Unpriced Accepted Bid Volume for the Settlement Period|MWh||
|PP|decimal(10,3)|Total Priced Accepted Offer Volume - System wide total Priced Accepted Offer Volume for the Settlement Period|MWh||
|PC|decimal(10,3)|Total Priced Accepted Bid Volume - System wide total Priced Accepted Bid Volume for the Settlement Period|MWh||
|BD|char(1) boolean|BSAD Defaulted|'T'/'F'|If 'T' the following BSAD fields are default values|
|A1|decimal(10,2)|Sell price cost Adjustment|£||
|A2|decimal(10,3)|Sell price volume Adjustment|MWh||
|A3|decimal(10,2)|Sell price price adjustment|£/MWh||
|A4|decimal(10,2)|Buy price cost Adjustment|£||
|A5|decimal(10,3)|Buy price volume Adjustment|MWh||
|A6|decimal(10,2)|Buy price price adjustment|£/MWh|&nbsp;|

Index: SD, SP

Example:

`2003:01:01:00:20:32:GMT: subject=BMRA.SYSTEM.EBSP, message={SD=2002:12:31:00:00:00:GMT,SP=48,PB=15.13,PS=11.10644,AO=307.2657,AB=-686.525,AP=36.6594,AC=0.0,PP=5.0,PC=-420.9187,BD=F,A1=-5248.75,A2=-417.5,A3=0.0,A4=0.0,A5=0.0,A6=0.0}`


#### NETEBSP: Estimated Buy and Sell Price
Derived data concerning system buy and sell prices

Ceased on P217 effective date of 2009-11-09

https://www.elexon.co.uk/mod-proposal/p217-revised-tagging-process-and-calculation-of-cash-out-prices/

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|PB|decimal(10,5)|Buy price - the price that must be paid for electricity which is out of balance|£||
|PS|float|Sell Price - the price received for electricity which is out of balance|£||
|PD|char(2)|Price Derivation Code - A code that describes the way in which SSP and SBP were calculated||Valid values defined in BMRA-I006|
|AO|float|Total Accepted Offer Volume - System wide total Accepted Offer Volume for the Settlement Period|MWh||
|AB|float|Total Accepted Bid Volume - System wide total Accepted Bid Volume for the Settlement Period|MWh||
|AP|float|Total Unpriced Accepted Offer Volume - System wide total Unpriced Accepted Offer Volume for the Settlement Period|MWh||
|AC|float|Total Unpriced Accepted Bid Volume - System wide total Unpriced Accepted Bid Volume for the Settlement Period|MWh||
|PP|float|Total Priced Accepted Offer Volume - System wide total Priced Accepted Offer Volume for the Settlement Period|MWh||
|PC|float|Total Priced Accepted Bid Volume - System wide total Priced Accepted Bid Volume for the Settlement Period|MWh||
|NI|float|Indicative Net Imbalance Volume|MWh||
|BD|char(1) boolean|BSAD Defaulted|'T'/'F'|If 'T' the following BSAD fields are default values|
|A7|float|Net Energy Sell Price Cost Adjustment (ESCA)|£||
|A8|float|Net Energy Sell Price Volume Adjustment (ESVA)|MWh||
|A11|float|Net System Sell Price Volume Adjustment (SSVA)|MWh||
|A3|float|Sell Price Price Adjustment (SPA)|£/MWh||
|A9|float|Net Energy Buy Price Cost Adjustment (EBCA)|£||
|A10|float|Net Energy Buy Price Volume Adjustment (EBVA)|MWh||
|A12|float|Net System Buy Price Volume Adjustment (SBVA)|MWh||
|A6|float|Buy Price Price Adjustment (BPA)|£/MWh|&nbsp;|

Index: SD, SP

Example:

`2009:01:01:00:20:48:GMT: subject=BMRA.SYSTEM.NETEBSP, message={SD=2008:12:31:00:00:00:GMT,SP=48,PB=59.18782,PS=47.9,PD=A,AO=422.9223,AB=-325.8473,AP=0.0,AC=-8.25,PP=96.8589,PC=-0.0,NI=96.8589,BD=F,A7=0.0,A8=0.0,A11=0.0,A3=0.0,A9=0.0,A10=0.0,A12=0.0,A6=0.0}`

#### DISEBSP: Disaggregated Estimated Buy and Sell Price

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|PB|decimal(10,5)|Buy price - the price that must be paid for electricity which is out of balance|£||
|PS|float|Sell Price - the price received for electricity which is out of balance|£||
|PD|char(2)|Price Derivation Code - A code that describes the way in which SSP and SBP were calculated||Valid values defined in BMRA-I006|
|RSP|float|Reserve Scarcity Price| £/MWh |NULL outside of a STOR availability window|
|RP|float|Replacement Price| £/MWh|may be absent|
|RV|float|Replacement Price Calculation Volume| MWh|may be absent|
|BD|float|BSAD Defaulted| |if 'T' following fields are defaulted|
|A3|float|Sell Price Price Adjustment (SPA)|£/MWh||
|A6|float|Buy Price Price Adjustment (BPA)|£/MWh|&nbsp;|
|NI|float|Indicative Net Imbalance Volume|MWh||
|AO|float|Total Accepted Offer Volume - System wide total Accepted Offer Volume for the Settlement Period|MWh||
|AB|float|Total Accepted Bid Volume - System wide total Accepted Bid Volume for the Settlement Period|MWh||
|T1|float|System wide total tagged Accepted Offer Volume for Settlement period|MWh||
|T2|float|System wide total tagged Accepted Bid Volume for Settlement period|MWh||
|PP|float|System wide total priced Accepted Offer Volume for Settlement period|MWh||
|PC|float |System wide total priced Accepted Bid Volume for Settlement period|MWh||
|J1|float |System wide total Adjustment Sell Volume for Settlement period|MWh||
|J2|float |System wide total Adjustment Buy Volume for Settlement period|MWh||
|J3|float |System wide total tagged Adjustment Sell Volume for Settlement period|MWh||
|J4|float |System wide total tagged Adjustment Buy Volume for Settlement period|MWh|&nbsp;|

Index: SD, SP

Example:

`2017:04:21:00:21:54:GMT: subject=BMRA.SYSTEM.DISEBSP, message={SD=2017:04:21:00:00:00:GMT,SP=2,PB=29.83277,PS=29.83277,PD=N,BD=F,A3=0.0,A6=0.0,NI=-18.3724,AO=223.2374,AB=-221.4425,T1=223.2374,T2=-203.0701,PP=222.5202,PC=-80.051,J1=-225.0,J2=205.0,J3=-225.0,J4=205.0}`

#### SOSO: SO to SO prices
Details of prices for trades offered between System Operators

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|TT|Char(10)|SO-SO Trade Type||indicating parties trading as an underscore separated string|
|ST|datetime|Start Time||to nearest minute|
|TD|Char(3)|Trade Direction||Valid values: ‘A01’ (up) or ‘A02’ (down)|
|IC|Char(30)|Contract Identifier|unique string||
|TQ|Decimal(10,3)|Trade Quantity offered|MW||
|PT|Decimal(10,2)|Trade Price offered|£/MWh|Value in unit currency per MWh. The currency used (e.g. EUR or GBP) will potentially be different for different SO-SO Trade Types (i.e. different Interconnectors and products)|

Index: TT, ST

Example:

`2017:04:21:00:10:51:GMT: subject=BMRA.SYSTEM.SOSO, message={TT=EWIC_NG,ST=2017:04:21:02:00:00:GMT,TD=A02,IC=NG_20170421_0200_1,TQ=25.0,PT=39.75}`

#### ISPSTACK: Indicative System Price Stack
Data derived when calculating the System Price. Consists of a number of ordered stack items which can be either BMU Acceptance or Balancing Services Adjustment Action data.

Each message relates to a single item on the Bid or Offer stack for a given Settlement Period.

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|BO|Char(1)|Bid/Offer Indicator||Bid (B) or Offer (O)|
|SN|Integer|Stack Index Number||indicating relative position within the related stack|
|CI|Char(30)|Component Identifier||associated BMU ID, or for Balancing Services Adjustment items the unique ID allocated by the SO, or for Demand Control Volume stack a unique ID from that BSC Agent's system|
|NK|Integer|Acceptance number ||not included for Balancing Services Adjustment items|
|NN|Integer|Bid offer pair Number||for Balancing Services Adjustment Action and Demand Control Volume items this will be NULL|
|CF|Char(1)|CADL Flag|'T'/'F'|A value of 'T' indicates that an Acceptance is considered to be a Short Duration acceptance|
|SO|Char(1)|SO Flag|'T'/'F'|A value of 'T' indicates that an Acceptance or BS Adjustment Action should be considered to be potentially impacted by transmission constraints|
|PF|Char(1)|STOR Provider Flag|'T'/'F'|A value of 'T' Indicates the item relates to a STOR Provider|
|RI|Char(1)|Repriced Indicator|'T'/'F'|'T' indicates the item has been repriced|
|UP|Decimal(10,3)|Bid-offer Original Price|£/MWh|as reported in the original BOD|
|RSP|Decimal(10,3)|Reserve Scarcity Price|£/MWh|absent where the action is outside of a STOR Availability Window|
|IP|Decimal(10,3)|Stack Item Original Price|£/MWh|the original bid-offer price - absent for unpriced items|
|IV|Decimal(10,3)|Stack Item Volume|MWh||
|DA|Decimal(10,3)|DMAT Adjusted Volume|MWh|the volume after DMAT has been applied|
|AV|Decimal(10,3)|Arbitrage Adjusted Volume |MWh|the volume after arbitrage has been applied|
|NIV|Decimal(10,3)|NIV Adjusted Volume |MWh|the volume after NIV has been applied|
|PV|Decimal(10,3)|PAR Adjusted Volume |MWh|the volume after PAR has been applied|
|FP|Decimal(10,3)|Stack Item Final Price |£/MWh||
|TM|Decimal(10,3)|Transmission Loss Multiplier Value |MWh|for associated BM unit|
|TV|Decimal(10,3)|TLM Adjusted Volume|MWh|PAR Adjusted Volume \* TLM|
|TC|Decimal(10,3)|TLM Adjusted Cost|£|PAR Adjusted Volume \* TLM \* Price|

Index: SD, SP, CI, NN

Example:

`2017:04:21:00:21:54:GMT: subject=BMRA.SYSTEM.ISPSTACK, message={SD=2017:04:21:00:00:00:GMT,SP=2,BO=O,SN=1,CI=T_HUMR-1,NK=112149,NN=1,CF=F,SO=F,PF=F,RI=F,UP=49.49,IP=49.49,IV=12.6424,DA=12.6424,AV=12.6424,NV=0.0,PV=0.0,FP=49.49,TM=1.0,TV=0.0,TC=0.0}`

#### TBOD: Total Bid Offer Data

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|OT|Decimal(10,2)|System wide total offer volume|MWh||
|BT|Decimal(10,2)|System wide total bid volume|MWh|&nbsp;|

Index: SD,SP

Example:

`2017:04:21:00:21:54:GMT: subject=BMRA.SYSTEM.TBOD, message={SD=2017:04:21:00:00:00:GMT,SP=2,OT=49472.0,BT=-48434.5}`



### Forecasting Data

#### DF: Demand Forecast
(ceased publication Q1 2009)

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|ZI||Zone Indicator|'B1' through 'B17' or 'N'|also included in message title|
|VD||Demand Value|MW|&nbsp;|

Example:

`2009:01:01:00:16:52:GMT: subject=BMRA.SYSTEM.DF.A, message={ZI=A,NR=58,TP=2008:12:31:23:47:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=1,VD=6177.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=2,VD=6210.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=3,VD=6305.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=4,VD=6318.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=5,VD=6326.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=6,VD=6234.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=7,VD=6007.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=8,VD=5819.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=9,VD=5639.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=10,VD=5520.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=11,VD=5448.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=12,VD=5439.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=13,VD=5310.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=14,VD=5304.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=15,VD=5264.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=16,VD=5132.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=17,VD=4764.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=18,VD=4878.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=19,VD=4974.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=20,VD=5072.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=21,VD=5340.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=22,VD=5643.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=23,VD=5930.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=24,VD=6110.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=25,VD=6366.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=26,VD=6360.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=27,VD=6280.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=28,VD=6243.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=29,VD=6251.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=30,VD=6231.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=31,VD=6216.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=32,VD=6388.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=33,VD=6675.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=34,VD=6971.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=35,VD=7107.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=36,VD=7126.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=37,VD=7043.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=38,VD=6909.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=39,VD=6925.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=40,VD=6800.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=41,VD=6685.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=42,VD=6556.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=43,VD=6410.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=44,VD=6153.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=45,VD=5999.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=46,VD=5765.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=47,VD=5612.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=48,VD=5623.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:02:00:00:00:GMT,SP=1,VD=5767.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:02:00:00:00:GMT,SP=2,VD=5855.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:02:00:00:00:GMT,SP=3,VD=5866.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:02:00:00:00:GMT,SP=4,VD=5678.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:02:00:00:00:GMT,SP=5,VD=5702.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:02:00:00:00:GMT,SP=6,VD=5897.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:02:00:00:00:GMT,SP=7,VD=5916.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:02:00:00:00:GMT,SP=8,VD=5825.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:02:00:00:00:GMT,SP=9,VD=5737.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:02:00:00:00:GMT,SP=10,VD=5729.0}`


#### NDF: National Demand Forecast
The National Demand Forecast values for every half hour period from the start of the current day to the furthest ahead forecast that has so far been received by the BMRA. Every time an updated forecast is received from the System Operator, BMRA publishes the data in this message and additionally includes previously received forecast values from period 1 of the current day onwards. The Publishing Time field is therefore applicable to each period in the forecast and indicates the time that data for a particular period was last received and the data reported is always that most recently received for each period. The records in the message are ordered by Settlement Date and Period.

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|ZI||Zone Indicator|'B1' through 'B17' or 'N'|also included in message title|
|VD||Demand Value|MW|&nbsp;|

Example:

`2017:04:21:00:16:29:GMT: subject=BMRA.SYSTEM.NDF.N, message={ZI=N,NR=58,TP=2017:04:20:22:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=1,VD=23700.0,TP=2017:04:20:23:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=2,VD=22969.0,TP=2017:04:20:23:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=3,VD=23644.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=4,VD=23600.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=5,VD=23347.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=6,VD=23045.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=7,VD=22730.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=8,VD=22467.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=9,VD=22300.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=10,VD=22299.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=11,VD=22994.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=12,VD=23820.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=13,VD=25906.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=14,VD=28202.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=15,VD=31034.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=16,VD=32506.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=17,VD=33300.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=18,VD=33235.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=19,VD=33200.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=20,VD=32808.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=21,VD=32155.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=22,VD=31800.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=23,VD=31388.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=24,VD=31159.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=25,VD=30972.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=26,VD=30570.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=27,VD=29828.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=28,VD=29440.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=29,VD=29081.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=30,VD=28710.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=31,VD=28500.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=32,VD=28920.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=33,VD=29769.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=34,VD=30771.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=35,VD=31738.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=36,VD=32200.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=37,VD=32327.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=38,VD=32283.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=39,VD=32100.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=40,VD=32452.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=41,VD=33155.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=42,VD=33800.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=43,VD=32987.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=44,VD=31570.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=45,VD=29874.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=46,VD=28257.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=47,VD=26412.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=48,VD=24800.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=1,VD=23900.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=2,VD=23300.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=3,VD=23328.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=4,VD=23600.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=5,VD=23052.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=6,VD=22566.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=7,VD=22072.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=8,VD=21644.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=9,VD=21227.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=10,VD=21000.0}`

#### TSDF: Transmission System Demand Forecast
Same as NDF but at Transmission level rather than gross demand

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|ZI||Zone Indicator|'B1' through 'B17' or 'N'|also included in message title|
|VD||Demand Value|MW|&nbsp;|

Example:

`2017:04:21:00:16:40:GMT: subject=BMRA.SYSTEM.TSDF.B1,message={ZI=B1,NR=58,TP=2017:04:20:22:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=1,VD=218.0,TP=2017:04:20:23:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=2,VD=211.0,TP=2017:04:20:23:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=3,VD=217.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=4,VD=217.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=5,VD=215.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=6,VD=212.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=7,VD=209.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=8,VD=207.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=9,VD=205.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=10,VD=205.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=11,VD=211.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=12,VD=219.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=13,VD=238.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=14,VD=258.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=15,VD=284.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=16,VD=297.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=17,VD=304.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=18,VD=304.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=19,VD=303.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=20,VD=300.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=21,VD=294.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=22,VD=291.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=23,VD=287.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=24,VD=285.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=25,VD=283.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=26,VD=280.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=27,VD=273.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=28,VD=269.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=29,VD=266.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=30,VD=263.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=31,VD=261.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=32,VD=265.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=33,VD=272.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=34,VD=281.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=35,VD=290.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=36,VD=294.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=37,VD=295.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=38,VD=295.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=39,VD=293.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=40,VD=297.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=41,VD=303.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=42,VD=309.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=43,VD=301.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=44,VD=289.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=45,VD=273.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=46,VD=259.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=47,VD=242.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=48,VD=228.0,      TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=1,VD=220.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=2,VD=214.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=3,VD=214.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=4,VD=217.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=5,VD=212.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=6,VD=208.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=7,VD=203.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=8,VD=199.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=9,VD=196.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=10,VD=194.0}`

#### IMBALNGC: Indicated Imbalance

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|ZI||Zone Indicator|'B1' through 'B17' or 'N'|also included in message title|
|VI||Imbalance Value|MW|&nbsp;|

Example:

`2017:04:21:00:17:42:GMT: subject=BMRA.SYSTEM.IMBALNGC.B1, message={ZI=B1,NR=58,TP=2017:04:20:22:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=1,VI=636.0,TP=2017:04:20:23:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=2,VI=660.0,TP=2017:04:20:23:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=3,VI=634.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=4,VI=634.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=5,VI=652.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=6,VI=672.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=7,VI=685.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=8,VI=692.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=9,VI=695.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=10,VI=687.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=11,VI=664.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=12,VI=639.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=13,VI=629.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=14,VI=646.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=15,VI=676.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=16,VI=659.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=17,VI=646.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=18,VI=648.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=19,VI=659.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=20,VI=692.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=21,VI=698.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=22,VI=698.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=23,VI=680.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=24,VI=704.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=25,VI=689.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=26,VI=719.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=27,VI=742.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=28,VI=758.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=29,VI=758.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=30,VI=764.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=31,VI=790.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=32,VI=795.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=33,VI=809.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=34,VI=819.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=35,VI=805.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=36,VI=778.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=37,VI=749.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=38,VI=715.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=39,VI=678.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=40,VI=627.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=41,VI=562.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=42,VI=499.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=43,VI=467.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=44,VI=436.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=45,VI=345.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=46,VI=321.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=47,VI=315.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=48,VI=313.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=1,VI=304.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=2,VI=299.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=3,VI=288.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=4,VI=267.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=5,VI=265.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=6,VI=260.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=7,VI=254.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=8,VI=251.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=9,VI=248.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=10,VI=240.0}`

#### INDGEN: Indicated Generation

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|ZI||Zone Indicator|'B1' through 'B17' or 'N'|also included in message title|
|VG||Generation Value|MW|&nbsp;|

  Example entry:
`2017:04:21:00:17:42:GMT: subject=BMRA.SYSTEM.INDGEN.B14, message={ZI=B14,NR=58,TP=2017:04:20:22:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=1,VG=255.0,TP=2017:04:20:23:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=2,VG=255.0,TP=2017:04:20:23:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=3,VG=255.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=4,VG=353.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=5,VG=375.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=6,VG=357.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=7,VG=255.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=8,VG=255.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=9,VG=255.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=10,VG=255.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=11,VG=390.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=12,VG=427.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=13,VG=427.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=14,VG=428.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=15,VG=430.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=16,VG=429.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=17,VG=429.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=18,VG=429.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=19,VG=429.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=20,VG=429.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=21,VG=429.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=22,VG=429.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=23,VG=431.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=24,VG=432.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=25,VG=434.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=26,VG=435.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=27,VG=435.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=28,VG=435.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=29,VG=434.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=30,VG=432.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=31,VG=430.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=32,VG=429.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=33,VG=428.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=34,VG=429.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=35,VG=429.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=36,VG=429.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=37,VG=430.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=38,VG=428.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=39,VG=427.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=40,VG=426.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=41,VG=426.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=42,VG=427.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=43,VG=427.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=44,VG=427.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=45,VG=427.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=46,VG=427.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=47,VG=427.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=48,VG=428.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=1,VG=427.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=2,VG=428.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=3,VG=428.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=4,VG=428.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=5,VG=428.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=6,VG=428.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=7,VG=428.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=8,VG=428.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=9,VG=428.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=10,VG=428.0}`

#### MELNGC: Indicated Margin

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|ZI||Zone Indicator|'B1' through 'B17' or 'N'|also included in message title|
|VM||Sum of MELs within zone|MW|&nbsp;|

Example:

`2017:04:21:00:19:12:GMT: subject=BMRA.SYSTEM.MELNGC.B1, message={ZI=B1,NR=58,TP=2017:04:20:22:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=1,VM=-895.0,TP=2017:04:20:23:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=2,VM=-910.0,TP=2017:04:20:23:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=3,VM=-881.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=4,VM=-896.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=5,VM=-908.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=6,VM=-922.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=7,VM=-933.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=8,VM=-941.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=9,VM=-944.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=10,VM=-939.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=11,VM=-923.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=12,VM=-900.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=13,VM=-872.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=14,VM=-841.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=15,VM=-812.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=16,VM=-796.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=17,VM=-781.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=18,VM=-780.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=19,VM=-784.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=20,VM=-793.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=21,VM=-810.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=22,VM=-826.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=23,VM=-848.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=24,VM=-867.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=25,VM=-885.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=26,VM=-904.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=27,VM=-918.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=28,VM=-921.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=29,VM=-921.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=30,VM=-923.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=31,VM=-923.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=32,VM=-915.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=33,VM=-902.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=34,VM=-883.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=35,VM=-866.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=36,VM=-850.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=37,VM=-831.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=38,VM=-809.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=39,VM=-783.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=40,VM=-745.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=41,VM=-707.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=42,VM=-670.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=43,VM=-647.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=44,VM=-632.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=45,VM=-626.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=46,VM=-624.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=47,VM=-623.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=48,VM=-623.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=1,VM=-618.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=2,VM=-617.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=3,VM=-607.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=4,VM=-601.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=5,VM=-599.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=6,VM=-595.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=7,VM=-591.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=8,VM=-589.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=9,VM=-587.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=10,VM=-580.0}`

#### INDDEM: Indicated demand

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|ZI||Zone Indicator|'B1' through 'B17' or 'N'|also included in message title|
|VD||Sum of demand PNs minus Net Interconnector Export|MW|&nbsp;|

Example:

`2017:04:21:00:20:44:GMT: subject=BMRA.SYSTEM.INDDEM.B1, message={ZI=B1,NR=58,TP=2017:04:20:22:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=1,VD=-99.0,TP=2017:04:20:23:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=2,VD=-98.0,TP=2017:04:20:23:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=3,VD=-100.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=4,VD=-100.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=5,VD=-98.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=6,VD=-101.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=7,VD=-105.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=8,VD=-103.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=9,VD=-94.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=10,VD=-93.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=11,VD=-94.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=12,VD=-97.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=13,VD=-101.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=14,VD=-109.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=15,VD=-121.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=16,VD=-131.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=17,VD=-144.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=18,VD=-149.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=19,VD=-150.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=20,VD=-149.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=21,VD=-150.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=22,VD=-150.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=23,VD=-151.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=24,VD=-152.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=25,VD=-151.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=26,VD=-147.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=27,VD=-145.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=28,VD=-140.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=29,VD=-133.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=30,VD=-131.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=31,VD=-131.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=32,VD=-128.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=33,VD=-129.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=34,VD=-132.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=35,VD=-135.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=36,VD=-130.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=37,VD=-127.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=38,VD=-125.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=39,VD=-125.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=40,VD=-125.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=41,VD=-134.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=42,VD=-131.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=43,VD=-129.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=44,VD=-121.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=45,VD=-120.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=46,VD=-115.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=47,VD=-110.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=48,VD=-107.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=1,VD=-99.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=2,VD=-99.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=3,VD=-100.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=4,VD=-101.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=5,VD=-98.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=6,VD=-99.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=7,VD=-104.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=8,VD=-101.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=9,VD=-94.0,TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=10,VD=-92.0}`


#### NDFD: Demand Forecast, 2-14 days ahead

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|VD||Demand|MW|&nbsp;|

Example:

`2017:04:21:13:45:37:GMT: subject=BMRA.SYSTEM.NDFD, message={TP=2017:04:21:13:45:00:GMT,NR=13,SD=2017:04:23:00:00:00:GMT,SP=3,VD=30950.0,SD=2017:04:24:00:00:00:GMT,SP=3,VD=34400.0,SD=2017:04:25:00:00:00:GMT,SP=3,VD=34700.0,SD=2017:04:26:00:00:00:GMT,SP=3,VD=35690.0,SD=2017:04:27:00:00:00:GMT,SP=3,VD=35700.0,SD=2017:04:28:00:00:00:GMT,SP=3,VD=35330.0,SD=2017:04:29:00:00:00:GMT,SP=3,VD=30090.0,SD=2017:04:30:00:00:00:GMT,SP=3,VD=29400.0,SD=2017:05:01:00:00:00:GMT,SP=3,VD=31410.0,SD=2017:05:02:00:00:00:GMT,SP=3,VD=33770.0,SD=2017:05:03:00:00:00:GMT,SP=3,VD=33500.0,SD=2017:05:04:00:00:00:GMT,SP=3,VD=32710.0,SD=2017:05:05:00:00:00:GMT,SP=3,VD=32360.0}`

#### TSDFD: Transmission System Demand Forecast

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|VD||Demand|MW|&nbsp;|

Example:

`2017:04:21:13:45:53:GMT: subject=BMRA.SYSTEM.TSDFD, message={TP=2017:04:21:13:45:00:GMT,NR=13,SD=2017:04:23:00:00:00:GMT,SP=3,VD=31450.0,SD=2017:04:24:00:00:00:GMT,SP=3,VD=34900.0,SD=2017:04:25:00:00:00:GMT,SP=3,VD=35200.0,SD=2017:04:26:00:00:00:GMT,SP=3,VD=36190.0,SD=2017:04:27:00:00:00:GMT,SP=3,VD=36200.0,SD=2017:04:28:00:00:00:GMT,SP=3,VD=35830.0,SD=2017:04:29:00:00:00:GMT,SP=3,VD=30590.0,SD=2017:04:30:00:00:00:GMT,SP=3,VD=29900.0,SD=2017:05:01:00:00:00:GMT,SP=3,VD=31910.0,SD=2017:05:02:00:00:00:GMT,SP=3,VD=34270.0,SD=2017:05:03:00:00:00:GMT,SP=3,VD=34000.0,SD=2017:05:04:00:00:00:GMT,SP=3,VD=33210.0,SD=2017:05:05:00:00:00:GMT,SP=3,VD=32860.0}`

#### TSDFW: Transmission System Demand Forecast, 2-52 weeks

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|WN|int|Calendar week number|||
|WD|date|Week start date|||
|VD|decimal(10,2)|Demand in MW||&nbsp;|

Example:

`2017:04:27:13:45:44:GMT: subject=BMRA.SYSTEM.TSDFW, message={TP=2017:04:27:13:45:00:GMT,NR=51,WN=19,WD=2017:05:08:00:00:00:GMT,VD=33970.0,WN=20,WD=2017:05:15:00:00:00:GMT,VD=33040.0,WN=21,WD=2017:05:22:00:00:00:GMT,VD=32410.0,WN=22,WD=2017:05:29:00:00:00:GMT,VD=32010.0,WN=23,WD=2017:06:05:00:00:00:GMT,VD=31950.0,WN=24,WD=2017:06:12:00:00:00:GMT,VD=31660.0,WN=25,WD=2017:06:19:00:00:00:GMT,VD=31240.0,WN=26,WD=2017:06:26:00:00:00:GMT,VD=31160.0,WN=27,WD=2017:07:03:00:00:00:GMT,VD=31140.0,WN=28,WD=2017:07:10:00:00:00:GMT,VD=31030.0,WN=29,WD=2017:07:17:00:00:00:GMT,VD=32030.0,WN=30,WD=2017:07:24:00:00:00:GMT,VD=31508.0,WN=31,WD=2017:07:31:00:00:00:GMT,VD=31696.0,WN=32,WD=2017:08:07:00:00:00:GMT,VD=32410.0,WN=33,WD=2017:08:14:00:00:00:GMT,VD=33260.0,WN=34,WD=2017:08:21:00:00:00:GMT,VD=33978.0,WN=35,WD=2017:08:28:00:00:00:GMT,VD=34904.0,WN=36,WD=2017:09:04:00:00:00:GMT,VD=36027.0,WN=37,WD=2017:09:11:00:00:00:GMT,VD=36613.0,WN=38,WD=2017:09:18:00:00:00:GMT,VD=37876.0,WN=39,WD=2017:09:25:00:00:00:GMT,VD=38874.0,WN=40,WD=2017:10:02:00:00:00:GMT,VD=39947.0,WN=41,WD=2017:10:09:00:00:00:GMT,VD=41029.0,WN=42,WD=2017:10:16:00:00:00:GMT,VD=42368.0,WN=43,WD=2017:10:23:00:00:00:GMT,VD=42847.0,WN=44,WD=2017:10:30:00:00:00:GMT,VD=45510.0,WN=45,WD=2017:11:06:00:00:00:GMT,VD=46671.0,WN=46,WD=2017:11:13:00:00:00:GMT,VD=47267.0,WN=47,WD=2017:11:20:00:00:00:GMT,VD=48044.0,WN=48,WD=2017:11:27:00:00:00:GMT,VD=48265.0,WN=49,WD=2017:12:04:00:00:00:GMT,VD=49303.0,WN=50,WD=2017:12:11:00:00:00:GMT,VD=49889.0,WN=51,WD=2017:12:18:00:00:00:GMT,VD=49428.0,WN=52,WD=2017:12:25:00:00:00:GMT,VD=44450.0,WN=1,WD=2018:01:01:00:00:00:GMT,VD=48753.0,WN=2,WD=2018:01:08:00:00:00:GMT,VD=49280.0,WN=3,WD=2018:01:15:00:00:00:GMT,VD=48915.0,WN=4,WD=2018:01:22:00:00:00:GMT,VD=49060.0,WN=5,WD=2018:01:29:00:00:00:GMT,VD=48683.0,WN=6,WD=2018:02:05:00:00:00:GMT,VD=48139.0,WN=7,WD=2018:02:12:00:00:00:GMT,VD=47201.0,WN=8,WD=2018:02:19:00:00:00:GMT,VD=46668.0,WN=9,WD=2018:02:26:00:00:00:GMT,VD=45996.0,WN=10,WD=2018:03:05:00:00:00:GMT,VD=45172.0,WN=11,WD=2018:03:12:00:00:00:GMT,VD=44460.0,WN=12,WD=2018:03:19:00:00:00:GMT,VD=42797.0,WN=13,WD=2018:03:26:00:00:00:GMT,VD=40651.0,WN=14,WD=2018:04:02:00:00:00:GMT,VD=39598.0,WN=15,WD=2018:04:09:00:00:00:GMT,VD=38254.0,WN=16,WD=2018:04:16:00:00:00:GMT,VD=37149.0,WN=17,WD=2018:04:23:00:00:00:GMT,VD=36207.0}`

#### NDFW: Demand Forecast, 2-52 weeks

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|WN|int|Calendar week number|||
|WD|date|Week start date|||
|VD|decimal(10,2)|Demand in MW||&nbsp;|

Example:

`2017:04:27:13:46:00:GMT: subject=BMRA.SYSTEM.NDFW, message={TP=2017:04:27:13:45:00:GMT,NR=51,WN=19,WD=2017:05:08:00:00:00:GMT,VD=33470.0,WN=20,WD=2017:05:15:00:00:00:GMT,VD=32540.0,WN=21,WD=2017:05:22:00:00:00:GMT,VD=31910.0,WN=22,WD=2017:05:29:00:00:00:GMT,VD=31510.0,WN=23,WD=2017:06:05:00:00:00:GMT,VD=31450.0,WN=24,WD=2017:06:12:00:00:00:GMT,VD=31160.0,WN=25,WD=2017:06:19:00:00:00:GMT,VD=30740.0,WN=26,WD=2017:06:26:00:00:00:GMT,VD=30660.0,WN=27,WD=2017:07:03:00:00:00:GMT,VD=30640.0,WN=28,WD=2017:07:10:00:00:00:GMT,VD=30530.0,WN=29,WD=2017:07:17:00:00:00:GMT,VD=31530.0,WN=30,WD=2017:07:24:00:00:00:GMT,VD=31008.0,WN=31,WD=2017:07:31:00:00:00:GMT,VD=31196.0,WN=32,WD=2017:08:07:00:00:00:GMT,VD=31910.0,WN=33,WD=2017:08:14:00:00:00:GMT,VD=32760.0,WN=34,WD=2017:08:21:00:00:00:GMT,VD=33478.0,WN=35,WD=2017:08:28:00:00:00:GMT,VD=34404.0,WN=36,WD=2017:09:04:00:00:00:GMT,VD=35527.0,WN=37,WD=2017:09:11:00:00:00:GMT,VD=36113.0,WN=38,WD=2017:09:18:00:00:00:GMT,VD=37376.0,WN=39,WD=2017:09:25:00:00:00:GMT,VD=38374.0,WN=40,WD=2017:10:02:00:00:00:GMT,VD=39447.0,WN=41,WD=2017:10:09:00:00:00:GMT,VD=40529.0,WN=42,WD=2017:10:16:00:00:00:GMT,VD=41868.0,WN=43,WD=2017:10:23:00:00:00:GMT,VD=42347.0,WN=44,WD=2017:10:30:00:00:00:GMT,VD=45010.0,WN=45,WD=2017:11:06:00:00:00:GMT,VD=46171.0,WN=46,WD=2017:11:13:00:00:00:GMT,VD=46767.0,WN=47,WD=2017:11:20:00:00:00:GMT,VD=47544.0,WN=48,WD=2017:11:27:00:00:00:GMT,VD=47765.0,WN=49,WD=2017:12:04:00:00:00:GMT,VD=48803.0,WN=50,WD=2017:12:11:00:00:00:GMT,VD=49389.0,WN=51,WD=2017:12:18:00:00:00:GMT,VD=48928.0,WN=52,WD=2017:12:25:00:00:00:GMT,VD=43950.0,WN=1,WD=2018:01:01:00:00:00:GMT,VD=48253.0,WN=2,WD=2018:01:08:00:00:00:GMT,VD=48780.0,WN=3,WD=2018:01:15:00:00:00:GMT,VD=48415.0,WN=4,WD=2018:01:22:00:00:00:GMT,VD=48560.0,WN=5,WD=2018:01:29:00:00:00:GMT,VD=48183.0,WN=6,WD=2018:02:05:00:00:00:GMT,VD=47639.0,WN=7,WD=2018:02:12:00:00:00:GMT,VD=46701.0,WN=8,WD=2018:02:19:00:00:00:GMT,VD=46168.0,WN=9,WD=2018:02:26:00:00:00:GMT,VD=45496.0,WN=10,WD=2018:03:05:00:00:00:GMT,VD=44672.0,WN=11,WD=2018:03:12:00:00:00:GMT,VD=43960.0,WN=12,WD=2018:03:19:00:00:00:GMT,VD=42297.0,WN=13,WD=2018:03:26:00:00:00:GMT,VD=40151.0,WN=14,WD=2018:04:02:00:00:00:GMT,VD=39098.0,WN=15,WD=2018:04:09:00:00:00:GMT,VD=37754.0,WN=16,WD=2018:04:16:00:00:00:GMT,VD=36649.0,WN=17,WD=2018:04:23:00:00:00:GMT,VD=35707.0}`

#### OCNMFW: Surplus forecast 2-52 weeks ahead

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|WN|int|Calendar week number|||
|WD|date|Week start date|||
|VM|decimal(10,2)|Surplus|MW|&nbsp;|

Example:

`2018:01:04:13:35:52:GMT: subject=BMRA.SYSTEM.OCNMFW, message={TP=2018:01:04:13:31:00:GMT,NR=51,WN=3,WD=2018:01:15:00:00:00:GMT,VM=10087.0,WN=4,WD=2018:01:22:00:00:00:GMT,VM=9690.0,WN=5,WD=2018:01:29:00:00:00:GMT,VM=9386.0,WN=6,WD=2018:02:05:00:00:00:GMT,VM=10928.0,WN=7,WD=2018:02:12:00:00:00:GMT,VM=12311.0,WN=8,WD=2018:02:19:00:00:00:GMT,VM=14367.0,WN=9,WD=2018:02:26:00:00:00:GMT,VM=13735.0,WN=10,WD=2018:03:05:00:00:00:GMT,VM=12289.0,WN=11,WD=2018:03:12:00:00:00:GMT,VM=13818.0,WN=12,WD=2018:03:19:00:00:00:GMT,VM=15448.0,WN=13,WD=2018:03:26:00:00:00:GMT,VM=16102.0,WN=14,WD=2018:04:02:00:00:00:GMT,VM=11437.0,WN=15,WD=2018:04:09:00:00:00:GMT,VM=12125.0,WN=16,WD=2018:04:16:00:00:00:GMT,VM=12122.0,WN=17,WD=2018:04:23:00:00:00:GMT,VM=13588.0,WN=18,WD=2018:04:30:00:00:00:GMT,VM=13438.0,WN=19,WD=2018:05:07:00:00:00:GMT,VM=12305.0,WN=20,WD=2018:05:14:00:00:00:GMT,VM=14366.0,WN=21,WD=2018:05:21:00:00:00:GMT,VM=14562.0,WN=22,WD=2018:05:28:00:00:00:GMT,VM=17926.0,WN=23,WD=2018:06:04:00:00:00:GMT,VM=13759.0,WN=24,WD=2018:06:11:00:00:00:GMT,VM=13488.0,WN=25,WD=2018:06:18:00:00:00:GMT,VM=13715.0,WN=26,WD=2018:06:25:00:00:00:GMT,VM=12919.0,WN=27,WD=2018:07:02:00:00:00:GMT,VM=11096.0,WN=28,WD=2018:07:09:00:00:00:GMT,VM=9618.0,WN=29,WD=2018:07:16:00:00:00:GMT,VM=12856.0,WN=30,WD=2018:07:23:00:00:00:GMT,VM=14795.0,WN=31,WD=2018:07:30:00:00:00:GMT,VM=15440.0,WN=32,WD=2018:08:06:00:00:00:GMT,VM=15990.0,WN=33,WD=2018:08:13:00:00:00:GMT,VM=15907.0,WN=34,WD=2018:08:20:00:00:00:GMT,VM=15868.0,WN=35,WD=2018:08:27:00:00:00:GMT,VM=16813.0,WN=36,WD=2018:09:03:00:00:00:GMT,VM=15632.0,WN=37,WD=2018:09:10:00:00:00:GMT,VM=12593.0,WN=38,WD=2018:09:17:00:00:00:GMT,VM=12833.0,WN=39,WD=2018:09:24:00:00:00:GMT,VM=13727.0,WN=40,WD=2018:10:01:00:00:00:GMT,VM=12985.0,WN=41,WD=2018:10:08:00:00:00:GMT,VM=11670.0,WN=42,WD=2018:10:15:00:00:00:GMT,VM=10954.0,WN=43,WD=2018:10:22:00:00:00:GMT,VM=10741.0,WN=44,WD=2018:10:29:00:00:00:GMT,VM=9306.0,WN=45,WD=2018:11:05:00:00:00:GMT,VM=8613.0,WN=46,WD=2018:11:12:00:00:00:GMT,VM=8440.0,WN=47,WD=2018:11:19:00:00:00:GMT,VM=7211.0,WN=48,WD=2018:11:26:00:00:00:GMT,VM=7408.0,WN=49,WD=2018:12:03:00:00:00:GMT,VM=6461.0,WN=50,WD=2018:12:10:00:00:00:GMT,VM=6399.0,WN=51,WD=2018:12:17:00:00:00:GMT,VM=5329.0,WN=52,WD=2018:12:24:00:00:00:GMT,VM=11976.0,WN=1,WD=2018:12:31:00:00:00:GMT,VM=7743.0}`

#### OCNMFW2: Generating Plant Demand Margin, 2-52 weeks ahead

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|CY|int|Calendar year|||
|WN|int|Week number|||
|DM|decimal(10,2)|Demand margin|MW|&nbsp;|

Example:

`2018:01:04:13:37:17:GMT: subject=BMRA.SYSTEM.OCNMFW2, message={TP=2018:01:04:13:35:00:GMT,NR=51,WN=3,CY=2018,DM=13753.0,WN=4,CY=2018,DM=13351.0,WN=5,CY=2018,DM=13068.0,WN=6,CY=2018,DM=14611.0,WN=7,CY=2018,DM=16020.0,WN=8,CY=2018,DM=18103.0,WN=9,CY=2018,DM=17484.0,WN=10,CY=2018,DM=16061.0,WN=11,CY=2018,DM=17612.0,WN=12,CY=2018,DM=19269.0,WN=13,CY=2018,DM=19904.0,WN=14,CY=2018,DM=15268.0,WN=15,CY=2018,DM=15988.0,WN=16,CY=2018,DM=16792.0,WN=17,CY=2018,DM=18282.0,WN=18,CY=2018,DM=17764.0,WN=19,CY=2018,DM=16634.0,WN=20,CY=2018,DM=18714.0,WN=21,CY=2018,DM=18944.0,WN=22,CY=2018,DM=22335.0,WN=23,CY=2018,DM=18571.0,WN=24,CY=2018,DM=18305.0,WN=25,CY=2018,DM=18540.0,WN=26,CY=2018,DM=17339.0,WN=27,CY=2018,DM=15684.0,WN=28,CY=2018,DM=14211.0,WN=29,CY=2018,DM=17441.0,WN=30,CY=2018,DM=19378.0,WN=31,CY=2018,DM=20504.0,WN=32,CY=2018,DM=21038.0,WN=33,CY=2018,DM=20934.0,WN=34,CY=2018,DM=20876.0,WN=35,CY=2018,DM=21033.0,WN=36,CY=2018,DM=19809.0,WN=37,CY=2018,DM=17131.0,WN=38,CY=2018,DM=17342.0,WN=39,CY=2018,DM=18612.0,WN=40,CY=2018,DM=17835.0,WN=41,CY=2018,DM=16493.0,WN=42,CY=2018,DM=15740.0,WN=43,CY=2018,DM=15508.0,WN=44,CY=2018,DM=14023.0,WN=45,CY=2018,DM=13305.0,WN=46,CY=2018,DM=13106.0,WN=47,CY=2018,DM=11863.0,WN=48,CY=2018,DM=12052.0,WN=49,CY=2018,DM=11081.0,WN=50,CY=2018,DM=10995.0,WN=51,CY=2018,DM=11229.0,WN=52,CY=2018,DM=18039.0,WN=1,CY=2019,DM=13693.0}`

#### WINDFOR: Forecast peak wind generation

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|VG|decimal(10,2)|Generation|MW||
|TR|decimal(10,2)|Total registered Wind Generation capacity|MW||

Example:

`2017:04:21:04:31:00:GMT: subject=BMRA.SYSTEM.WINDFOR, message={NR=70,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=1,VG=2781.0,TR=9910,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=3,VG=2937.0,TR=9910,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=5,VG=3169.0,TR=9910,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=7,VG=3433.0,TR=9910,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=9,VG=3662.0,TR=9910,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=11,VG=3854.0,TR=9910,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=13,VG=4045.0,TR=9910,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=15,VG=4148.0,TR=9910,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=17,VG=4260.0,TR=9910,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=19,VG=4334.0,TR=9910,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=21,VG=4408.0,TR=9910,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=23,VG=4448.0,TR=9910,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=25,VG=4505.0,TR=9910,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=27,VG=4266.0,TR=9910,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=29,VG=4278.0,TR=9910,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=31,VG=4224.0,TR=9910,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=33,VG=4503.0,TR=9910,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=35,VG=4295.0,TR=9910,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=37,VG=3983.0,TR=9910,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=39,VG=3598.0,TR=9910,TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=41,VG=3191.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=43,VG=2773.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=45,VG=2498.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=47,VG=2368.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=1,VG=2296.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=3,VG=2204.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=5,VG=2149.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=7,VG=2108.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=9,VG=2012.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=11,VG=1868.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=13,VG=1708.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=15,VG=1534.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=17,VG=1426.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=19,VG=1412.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=21,VG=1404.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=23,VG=1495.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=25,VG=1554.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=27,VG=1615.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=29,VG=1765.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=31,VG=1895.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=33,VG=2001.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=35,VG=2104.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=37,VG=2044.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=39,VG=2004.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=41,VG=1707.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=43,VG=1466.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=45,VG=1272.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=47,VG=1060.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=1,VG=902.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=3,VG=779.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=5,VG=756.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=7,VG=745.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=9,VG=748.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=11,VG=777.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=13,VG=808.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=15,VG=840.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=17,VG=903.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=19,VG=984.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=21,VG=1107.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=23,VG=1252.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=25,VG=1431.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=27,VG=1640.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=29,VG=1861.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=31,VG=2097.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=33,VG=2343.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=35,VG=2466.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=37,VG=2597.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=39,VG=2740.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=41,VG=2896.0,TR=9910,TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=43,VG=3087.0,TR=9910}`

#### OCNMFD: Surplus forecast 2-14 days ahead

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|VM|decimal(10,2)|Surplus|MW|&nbsp;|

Example:

`2017:04:21:12:38:37:GMT: subject=BMRA.SYSTEM.OCNMFD, message={TP=2017:04:21:12:37:00:GMT,NR=13,SD=2017:04:23:00:00:00:GMT,SP=3,VM=10910.0,SD=2017:04:24:00:00:00:GMT,SP=3,VM=11422.0,SD=2017:04:25:00:00:00:GMT,SP=3,VM=10520.0,SD=2017:04:26:00:00:00:GMT,SP=3,VM=7643.0,SD=2017:04:27:00:00:00:GMT,SP=3,VM=7239.0,SD=2017:04:28:00:00:00:GMT,SP=3,VM=6933.0,SD=2017:04:29:00:00:00:GMT,SP=3,VM=10730.0,SD=2017:04:30:00:00:00:GMT,SP=3,VM=11714.0,SD=2017:05:01:00:00:00:GMT,SP=3,VM=11903.0,SD=2017:05:02:00:00:00:GMT,SP=3,VM=9834.0,SD=2017:05:03:00:00:00:GMT,SP=3,VM=10329.0,SD=2017:05:04:00:00:00:GMT,SP=3,VM=10910.0,SD=2017:05:05:00:00:00:GMT,SP=3,VM=11699.0}`

#### OCNMFD2: Generating Plant margin, 2-14 days ahead

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|DM|decimal(10,2)|Margin|MW|&nbsp;|

Example:

`2017:04:21:12:39:24:GMT: subject=BMRA.SYSTEM.OCNMFD2, message={TP=2017:04:21:12:38:00:GMT,NR=13,SD=2017:04:23:00:00:00:GMT,DM=15686.0,SD=2017:04:24:00:00:00:GMT,DM=16196.0,SD=2017:04:25:00:00:00:GMT,DM=15291.0,SD=2017:04:26:00:00:00:GMT,DM=11728.0,SD=2017:04:27:00:00:00:GMT,DM=11324.0,SD=2017:04:28:00:00:00:GMT,DM=11028.0,SD=2017:04:29:00:00:00:GMT,DM=14965.0,SD=2017:04:30:00:00:00:GMT,DM=15967.0,SD=2017:05:01:00:00:00:GMT,DM=16103.0,SD=2017:05:02:00:00:00:GMT,DM=13971.0,SD=2017:05:03:00:00:00:GMT,DM=14473.0,SD=2017:05:04:00:00:00:GMT,DM=15075.0,SD=2017:05:05:00:00:00:GMT,DM=15873.0}`


#### FOU2T14D: National Output Usable by Fuel Type, 2-14 Days ahead

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|FT|char(10)|Fuel type|||
|OU|decimal(10,2)|Output usable|MW||

Example:

`2017:04:21:12:39:09:GMT: subject=BMRA.SYSTEM.FOU2T14D, message={TP=2017:04:21:12:38:00:GMT,NR=169,SD=2017:04:23:00:00:00:GMT,FT=WIND,OU=4084.0,SD=2017:04:23:00:00:00:GMT,FT=PS,OU=2408.0,SD=2017:04:23:00:00:00:GMT,FT=OTHER,OU=2065.0,SD=2017:04:23:00:00:00:GMT,FT=OIL,OU=0.0,SD=2017:04:23:00:00:00:GMT,FT=OCGT,OU=728.0,SD=2017:04:23:00:00:00:GMT,FT=NUCLEAR,OU=6898.0,SD=2017:04:23:00:00:00:GMT,FT=NPSHYD,OU=1030.0,SD=2017:04:23:00:00:00:GMT,FT=INTNED,OU=1000.0,SD=2017:04:23:00:00:00:GMT,FT=INTIRL,OU=250.0,SD=2017:04:23:00:00:00:GMT,FT=INTFR,OU=2000.0,SD=2017:04:23:00:00:00:GMT,FT=INTEW,OU=0.0,SD=2017:04:23:00:00:00:GMT,FT=COAL,OU=6831.0,SD=2017:04:23:00:00:00:GMT,FT=CCGT,OU=23092.0,SD=2017:04:24:00:00:00:GMT,FT=WIND,OU=6357.0,SD=2017:04:24:00:00:00:GMT,FT=PS,OU=2408.0,SD=2017:04:24:00:00:00:GMT,FT=OTHER,OU=2065.0,SD=2017:04:24:00:00:00:GMT,FT=OIL,OU=0.0,SD=2017:04:24:00:00:00:GMT,FT=OCGT,OU=700.0,SD=2017:04:24:00:00:00:GMT,FT=NUCLEAR,OU=6898.0,SD=2017:04:24:00:00:00:GMT,FT=NPSHYD,OU=1030.0,SD=2017:04:24:00:00:00:GMT,FT=INTNED,OU=1000.0,SD=2017:04:24:00:00:00:GMT,FT=INTIRL,OU=250.0,SD=2017:04:24:00:00:00:GMT,FT=INTFR,OU=2000.0,SD=2017:04:24:00:00:00:GMT,FT=INTEW,OU=0.0,SD=2017:04:24:00:00:00:GMT,FT=COAL,OU=8121.0,SD=2017:04:24:00:00:00:GMT,FT=CCGT,OU=23517.0,SD=2017:04:25:00:00:00:GMT,FT=WIND,OU=6440.0,SD=2017:04:25:00:00:00:GMT,FT=PS,OU=2408.0,SD=2017:04:25:00:00:00:GMT,FT=OTHER,OU=2065.0,SD=2017:04:25:00:00:00:GMT,FT=OIL,OU=0.0,SD=2017:04:25:00:00:00:GMT,FT=OCGT,OU=728.0,SD=2017:04:25:00:00:00:GMT,FT=NUCLEAR,OU=6658.0,SD=2017:04:25:00:00:00:GMT,FT=NPSHYD,OU=1030.0,SD=2017:04:25:00:00:00:GMT,FT=INTNED,OU=1000.0,SD=2017:04:25:00:00:00:GMT,FT=INTIRL,OU=250.0,SD=2017:04:25:00:00:00:GMT,FT=INTFR,OU=2000.0,SD=2017:04:25:00:00:00:GMT,FT=INTEW,OU=0.0,SD=2017:04:25:00:00:00:GMT,FT=COAL,OU=7621.0,SD=2017:04:25:00:00:00:GMT,FT=CCGT,OU=23541.0,SD=2017:04:26:00:00:00:GMT,FT=WIND,OU=3799.0,SD=2017:04:26:00:00:00:GMT,FT=PS,OU=2408.0,SD=2017:04:26:00:00:00:GMT,FT=OTHER,OU=2065.0,SD=2017:04:26:00:00:00:GMT,FT=OIL,OU=0.0,SD=2017:04:26:00:00:00:GMT,FT=OCGT,OU=728.0,SD=2017:04:26:00:00:00:GMT,FT=NUCLEAR,OU=6750.0,SD=2017:04:26:00:00:00:GMT,FT=NPSHYD,OU=1030.0,SD=2017:04:26:00:00:00:GMT,FT=INTNED,OU=1000.0,SD=2017:04:26:00:00:00:GMT,FT=INTIRL,OU=250.0,SD=2017:04:26:00:00:00:GMT,FT=INTFR,OU=2000.0,SD=2017:04:26:00:00:00:GMT,FT=INTEW,OU=0.0,SD=2017:04:26:00:00:00:GMT,FT=COAL,OU=7129.0,SD=2017:04:26:00:00:00:GMT,FT=CCGT,OU=24009.0,SD=2017:04:27:00:00:00:GMT,FT=WIND,OU=2352.0,SD=2017:04:27:00:00:00:GMT,FT=PS,OU=2408.0,SD=2017:04:27:00:00:00:GMT,FT=OTHER,OU=2063.0,SD=2017:04:27:00:00:00:GMT,FT=OIL,OU=0.0,SD=2017:04:27:00:00:00:GMT,FT=OCGT,OU=728.0,SD=2017:04:27:00:00:00:GMT,FT=NUCLEAR,OU=6809.0,SD=2017:04:27:00:00:00:GMT,FT=NPSHYD,OU=1030.0,SD=2017:04:27:00:00:00:GMT,FT=INTNED,OU=1000.0,SD=2017:04:27:00:00:00:GMT,FT=INTIRL,OU=250.0,SD=2017:04:27:00:00:00:GMT,FT=INTFR,OU=2000.0,SD=2017:04:27:00:00:00:GMT,FT=INTEW,OU=0.0,SD=2017:04:27:00:00:00:GMT,FT=COAL,OU=8121.0,SD=2017:04:27:00:00:00:GMT,FT=CCGT,OU=24013.0,SD=2017:04:28:00:00:00:GMT,FT=WIND,OU=2534.0,SD=2017:04:28:00:00:00:GMT,FT=PS,OU=2408.0,SD=2017:04:28:00:00:00:GMT,FT=OTHER,OU=2115.0,SD=2017:04:28:00:00:00:GMT,FT=OIL,OU=0.0,SD=2017:04:28:00:00:00:GMT,FT=OCGT,OU=728.0,SD=2017:04:28:00:00:00:GMT,FT=NUCLEAR,OU=6781.0,SD=2017:04:28:00:00:00:GMT,FT=NPSHYD,OU=1016.0,SD=2017:04:28:00:00:00:GMT,FT=INTNED,OU=1000.0,SD=2017:04:28:00:00:00:GMT,FT=INTIRL,OU=250.0,SD=2017:04:28:00:00:00:GMT,FT=INTFR,OU=2000.0,SD=2017:04:28:00:00:00:GMT,FT=INTEW,OU=0.0,SD=2017:04:28:00:00:00:GMT,FT=COAL,OU=7716.0,SD=2017:04:28:00:00:00:GMT,FT=CCGT,OU=23560.0,SD=2017:04:29:00:00:00:GMT,FT=WIND,OU=2748.0,SD=2017:04:29:00:00:00:GMT,FT=PS,OU=2408.0,SD=2017:04:29:00:00:00:GMT,FT=OTHER,OU=2115.0,SD=2017:04:29:00:00:00:GMT,FT=OIL,OU=0.0,SD=2017:04:29:00:00:00:GMT,FT=OCGT,OU=728.0,SD=2017:04:29:00:00:00:GMT,FT=NUCLEAR,OU=6624.0,SD=2017:04:29:00:00:00:GMT,FT=NPSHYD,OU=1016.0,SD=2017:04:29:00:00:00:GMT,FT=INTNED,OU=1000.0,SD=2017:04:29:00:00:00:GMT,FT=INTIRL,OU=250.0,SD=2017:04:29:00:00:00:GMT,FT=INTFR,OU=2000.0,SD=2017:04:29:00:00:00:GMT,FT=INTEW,OU=0.0,SD=2017:04:29:00:00:00:GMT,FT=COAL,OU=7216.0,SD=2017:04:29:00:00:00:GMT,FT=CCGT,OU=22700.0,SD=2017:04:30:00:00:00:GMT,FT=WIND,OU=2867.0,SD=2017:04:30:00:00:00:GMT,FT=PS,OU=2408.0,SD=2017:04:30:00:00:00:GMT,FT=OTHER,OU=2115.0,SD=2017:04:30:00:00:00:GMT,FT=OIL,OU=0.0,SD=2017:04:30:00:00:00:GMT,FT=OCGT,OU=728.0,SD=2017:04:30:00:00:00:GMT,FT=NUCLEAR,OU=6914.0,SD=2017:04:30:00:00:00:GMT,FT=NPSHYD,OU=1016.0,SD=2017:04:30:00:00:00:GMT,FT=INTNED,OU=1000.0,SD=2017:04:30:00:00:00:GMT,FT=INTIRL,OU=250.0,SD=2017:04:30:00:00:00:GMT,FT=INTFR,OU=2000.0,SD=2017:04:30:00:00:00:GMT,FT=INTEW,OU=0.0,SD=2017:04:30:00:00:00:GMT,FT=COAL,OU=7216.0,SD=2017:04:30:00:00:00:GMT,FT=CCGT,OU=22603.0,SD=2017:05:01:00:00:00:GMT,FT=WIND,OU=3063.0,SD=2017:05:01:00:00:00:GMT,FT=PS,OU=2408.0,SD=2017:05:01:00:00:00:GMT,FT=OTHER,OU=2115.0,SD=2017:05:01:00:00:00:GMT,FT=OIL,OU=0.0,SD=2017:05:01:00:00:00:GMT,FT=OCGT,OU=728.0,SD=2017:05:01:00:00:00:GMT,FT=NUCLEAR,OU=7179.0,SD=2017:05:01:00:00:00:GMT,FT=NPSHYD,OU=951.0,SD=2017:05:01:00:00:00:GMT,FT=INTNED,OU=1000.0,SD=2017:05:01:00:00:00:GMT,FT=INTIRL,OU=250.0,SD=2017:05:01:00:00:00:GMT,FT=INTFR,OU=2000.0,SD=2017:05:01:00:00:00:GMT,FT=INTEW,OU=0.0,SD=2017:05:01:00:00:00:GMT,FT=COAL,OU=7716.0,SD=2017:05:01:00:00:00:GMT,FT=CCGT,OU=23853.0,SD=2017:05:02:00:00:00:GMT,FT=WIND,OU=2773.0,SD=2017:05:02:00:00:00:GMT,FT=PS,OU=2408.0,SD=2017:05:02:00:00:00:GMT,FT=OTHER,OU=2115.0,SD=2017:05:02:00:00:00:GMT,FT=OIL,OU=0.0,SD=2017:05:02:00:00:00:GMT,FT=OCGT,OU=728.0,SD=2017:05:02:00:00:00:GMT,FT=NUCLEAR,OU=7288.0,SD=2017:05:02:00:00:00:GMT,FT=NPSHYD,OU=965.0,SD=2017:05:02:00:00:00:GMT,FT=INTNED,OU=1000.0,SD=2017:05:02:00:00:00:GMT,FT=INTIRL,OU=250.0,SD=2017:05:02:00:00:00:GMT,FT=INTFR,OU=2000.0,SD=2017:05:02:00:00:00:GMT,FT=INTEW,OU=0.0,SD=2017:05:02:00:00:00:GMT,FT=COAL,OU=7716.0,SD=2017:05:02:00:00:00:GMT,FT=CCGT,OU=24248.0,SD=2017:05:03:00:00:00:GMT,FT=WIND,OU=2857.0,SD=2017:05:03:00:00:00:GMT,FT=PS,OU=2648.0,SD=2017:05:03:00:00:00:GMT,FT=OTHER,OU=2115.0,SD=2017:05:03:00:00:00:GMT,FT=OIL,OU=0.0,SD=2017:05:03:00:00:00:GMT,FT=OCGT,OU=728.0,SD=2017:05:03:00:00:00:GMT,FT=NUCLEAR,OU=7361.0,SD=2017:05:03:00:00:00:GMT,FT=NPSHYD,OU=965.0,SD=2017:05:03:00:00:00:GMT,FT=INTNED,OU=1000.0,SD=2017:05:03:00:00:00:GMT,FT=INTIRL,OU=250.0,SD=2017:05:03:00:00:00:GMT,FT=INTFR,OU=2000.0,SD=2017:05:03:00:00:00:GMT,FT=INTEW,OU=0.0,SD=2017:05:03:00:00:00:GMT,FT=COAL,OU=7716.0,SD=2017:05:03:00:00:00:GMT,FT=CCGT,OU=24083.0,SD=2017:05:04:00:00:00:GMT,FT=WIND,OU=2889.0,SD=2017:05:04:00:00:00:GMT,FT=PS,OU=2648.0,SD=2017:05:04:00:00:00:GMT,FT=OTHER,OU=2115.0,SD=2017:05:04:00:00:00:GMT,FT=OIL,OU=0.0,SD=2017:05:04:00:00:00:GMT,FT=OCGT,OU=728.0,SD=2017:05:04:00:00:00:GMT,FT=NUCLEAR,OU=7361.0,SD=2017:05:04:00:00:00:GMT,FT=NPSHYD,OU=965.0,SD=2017:05:04:00:00:00:GMT,FT=INTNED,OU=1000.0,SD=2017:05:04:00:00:00:GMT,FT=INTIRL,OU=250.0,SD=2017:05:04:00:00:00:GMT,FT=INTFR,OU=2000.0,SD=2017:05:04:00:00:00:GMT,FT=INTEW,OU=0.0,SD=2017:05:04:00:00:00:GMT,FT=COAL,OU=7716.0,SD=2017:05:04:00:00:00:GMT,FT=CCGT,OU=23863.0,SD=2017:05:05:00:00:00:GMT,FT=WIND,OU=4033.0,SD=2017:05:05:00:00:00:GMT,FT=PS,OU=2648.0,SD=2017:05:05:00:00:00:GMT,FT=OTHER,OU=2115.0,SD=2017:05:05:00:00:00:GMT,FT=OIL,OU=0.0,SD=2017:05:05:00:00:00:GMT,FT=OCGT,OU=728.0,SD=2017:05:05:00:00:00:GMT,FT=NUCLEAR,OU=7361.0,SD=2017:05:05:00:00:00:GMT,FT=NPSHYD,OU=965.0,SD=2017:05:05:00:00:00:GMT,FT=INTNED,OU=1000.0,SD=2017:05:05:00:00:00:GMT,FT=INTIRL,OU=250.0,SD=2017:05:05:00:00:00:GMT,FT=INTFR,OU=2000.0,SD=2017:05:05:00:00:00:GMT,FT=INTEW,OU=0.0,SD=2017:05:05:00:00:00:GMT,FT=COAL,OU=7716.0,SD=2017:05:05:00:00:00:GMT,FT=CCGT,OU=23167.0}`

#### FOU2T52W: National Output Usable by Fuel Type, 2-52 weeks ahead

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|CY|int|Calendar year|||
|WN|int|Week number|||
|FT|char(10)|Fuel type|||
|OU|decimal(10,2)|Output usable|MW|&nbsp;|

Example:

`2018:01:04:13:37:11:GMT: subject=BMRA.SYSTEM.FOU2T52W, message={TP=2018:01:04:13:31:00:GMT,NR=679,WN=3,CY=2018,FT=WIND,OU=6447.0,WN=3,CY=2018,FT=PS,OU=2828.0,WN=3,CY=2018,FT=OTHER,OU=6.0,WN=3,CY=2018,FT=OIL,OU=0.0,WN=3,CY=2018,FT=OCGT,OU=837.0,WN=3,CY=2018,FT=NUCLEAR,OU=6990.0,WN=3,CY=2018,FT=NPSHYD,OU=1051.0,WN=3,CY=2018,FT=INTNED,OU=1000.0,WN=3,CY=2018,FT=INTIRL,OU=500.0,WN=3,CY=2018,FT=INTFR,OU=2000.0,WN=3,CY=2018,FT=INTEW,OU=500.0,WN=3,CY=2018,FT=COAL,OU=12786.0,WN=3,CY=2018,FT=CCGT,OU=29578.0,WN=3,CY=2018,FT=BIOMASS,OU=2130.0,WN=4,CY=2018,FT=WIND,OU=6467.0,WN=4,CY=2018,FT=PS,OU=2828.0,WN=4,CY=2018,FT=OTHER,OU=6.0,WN=4,CY=2018,FT=OIL,OU=0.0,WN=4,CY=2018,FT=OCGT,OU=837.0,WN=4,CY=2018,FT=NUCLEAR,OU=6728.0,WN=4,CY=2018,FT=NPSHYD,OU=1051.0,WN=4,CY=2018,FT=INTNED,OU=1000.0,WN=4,CY=2018,FT=INTIRL,OU=500.0,WN=4,CY=2018,FT=INTFR,OU=2000.0,WN=4,CY=2018,FT=INTEW,OU=500.0,WN=4,CY=2018,FT=COAL,OU=12786.0,WN=4,CY=2018,FT=CCGT,OU=29583.0,WN=4,CY=2018,FT=BIOMASS,OU=2165.0,WN=5,CY=2018,FT=WIND,OU=6474.0,WN=5,CY=2018,FT=PS,OU=2828.0,WN=5,CY=2018,FT=OTHER,OU=6.0,WN=5,CY=2018,FT=OIL,OU=0.0,WN=5,CY=2018,FT=OCGT,OU=837.0,WN=5,CY=2018,FT=NUCLEAR,OU=6108.0,WN=5,CY=2018,FT=NPSHYD,OU=1051.0,WN=5,CY=2018,FT=INTNED,OU=1000.0,WN=5,CY=2018,FT=INTIRL,OU=500.0,WN=5,CY=2018,FT=INTFR,OU=2000.0,WN=5,CY=2018,FT=INTEW,OU=500.0,WN=5,CY=2018,FT=COAL,OU=12786.0,WN=5,CY=2018,FT=CCGT,OU=29143.0,WN=5,CY=2018,FT=BIOMASS,OU=2165.0,WN=6,CY=2018,FT=WIND,OU=5923.0,WN=6,CY=2018,FT=PS,OU=2828.0,WN=6,CY=2018,FT=OTHER,OU=6.0,WN=6,CY=2018,FT=OIL,OU=0.0,WN=6,CY=2018,FT=OCGT,OU=837.0,WN=6,CY=2018,FT=NUCLEAR,OU=7271.0,WN=6,CY=2018,FT=NPSHYD,OU=1051.0,WN=6,CY=2018,FT=INTNED,OU=1000.0,WN=6,CY=2018,FT=INTIRL,OU=500.0,WN=6,CY=2018,FT=INTFR,OU=2000.0,WN=6,CY=2018,FT=INTEW,OU=500.0,WN=6,CY=2018,FT=COAL,OU=12786.0,WN=6,CY=2018,FT=CCGT,OU=29912.0,WN=6,CY=2018,FT=BIOMASS,OU=2297.0,WN=7,CY=2018,FT=WIND,OU=5939.0,WN=7,CY=2018,FT=PS,OU=2828.0,WN=7,CY=2018,FT=OTHER,OU=6.0,WN=7,CY=2018,FT=OIL,OU=0.0,WN=7,CY=2018,FT=OCGT,OU=837.0,WN=7,CY=2018,FT=NUCLEAR,OU=7418.0,WN=7,CY=2018,FT=NPSHYD,OU=1051.0,WN=7,CY=2018,FT=INTNED,OU=1000.0,WN=7,CY=2018,FT=INTIRL,OU=500.0,WN=7,CY=2018,FT=INTFR,OU=2000.0,WN=7,CY=2018,FT=INTEW,OU=500.0,WN=7,CY=2018,FT=COAL,OU=12786.0,WN=7,CY=2018,FT=CCGT,OU=30158.0,WN=7,CY=2018,FT=BIOMASS,OU=2297.0,WN=8,CY=2018,FT=WIND,OU=5939.0,WN=8,CY=2018,FT=PS,OU=2828.0,WN=8,CY=2018,FT=OTHER,OU=6.0,WN=8,CY=2018,FT=OIL,OU=0.0,WN=8,CY=2018,FT=OCGT,OU=837.0,WN=8,CY=2018,FT=NUCLEAR,OU=7751.0,WN=8,CY=2018,FT=NPSHYD,OU=1051.0,WN=8,CY=2018,FT=INTNED,OU=1000.0,WN=8,CY=2018,FT=INTIRL,OU=500.0,WN=8,CY=2018,FT=INTFR,OU=2000.0,WN=8,CY=2018,FT=INTEW,OU=500.0,WN=8,CY=2018,FT=COAL,OU=13266.0,WN=8,CY=2018,FT=CCGT,OU=30351.0,WN=8,CY=2018,FT=BIOMASS,OU=2374.0,WN=9,CY=2018,FT=WIND,OU=5955.0,WN=9,CY=2018,FT=PS,OU=2828.0,WN=9,CY=2018,FT=OTHER,OU=6.0,WN=9,CY=2018,FT=OIL,OU=0.0,WN=9,CY=2018,FT=OCGT,OU=837.0,WN=9,CY=2018,FT=NUCLEAR,OU=7708.0,WN=9,CY=2018,FT=NPSHYD,OU=1051.0,WN=9,CY=2018,FT=INTNED,OU=1000.0,WN=9,CY=2018,FT=INTIRL,OU=500.0,WN=9,CY=2018,FT=INTFR,OU=2000.0,WN=9,CY=2018,FT=INTEW,OU=500.0,WN=9,CY=2018,FT=COAL,OU=13266.0,WN=9,CY=2018,FT=CCGT,OU=29204.0,WN=9,CY=2018,FT=BIOMASS,OU=2429.0,WN=10,CY=2018,FT=WIND,OU=4761.0,WN=10,CY=2018,FT=PS,OU=2828.0,WN=10,CY=2018,FT=OTHER,OU=6.0,WN=10,CY=2018,FT=OIL,OU=0.0,WN=10,CY=2018,FT=OCGT,OU=837.0,WN=10,CY=2018,FT=NUCLEAR,OU=7461.0,WN=10,CY=2018,FT=NPSHYD,OU=1051.0,WN=10,CY=2018,FT=INTNED,OU=1000.0,WN=10,CY=2018,FT=INTIRL,OU=500.0,WN=10,CY=2018,FT=INTFR,OU=2000.0,WN=10,CY=2018,FT=INTEW,OU=500.0,WN=10,CY=2018,FT=COAL,OU=13266.0,WN=10,CY=2018,FT=CCGT,OU=28372.0,WN=10,CY=2018,FT=BIOMASS,OU=2429.0,WN=11,CY=2018,FT=WIND,OU=4761.0,WN=11,CY=2018,FT=PS,OU=2628.0,WN=11,CY=2018,FT=OTHER,OU=6.0,WN=11,CY=2018,FT=OIL,OU=0.0,WN=11,CY=2018,FT=OCGT,OU=837.0,WN=11,CY=2018,FT=NUCLEAR,OU=7640.0,WN=11,CY=2018,FT=NPSHYD,OU=1051.0,WN=11,CY=2018,FT=INTNED,OU=1000.0,WN=11,CY=2018,FT=INTIRL,OU=500.0,WN=11,CY=2018,FT=INTFR,OU=2000.0,WN=11,CY=2018,FT=INTEW,OU=500.0,WN=11,CY=2018,FT=COAL,OU=13266.0,WN=11,CY=2018,FT=CCGT,OU=29067.0,WN=11,CY=2018,FT=BIOMASS,OU=2496.0,WN=12,CY=2018,FT=WIND,OU=4761.0,WN=12,CY=2018,FT=PS,OU=2628.0,WN=12,CY=2018,FT=OTHER,OU=6.0,WN=12,CY=2018,FT=OIL,OU=0.0,WN=12,CY=2018,FT=OCGT,OU=837.0,WN=12,CY=2018,FT=NUCLEAR,OU=7462.0,WN=12,CY=2018,FT=NPSHYD,OU=1011.0,WN=12,CY=2018,FT=INTNED,OU=1000.0,WN=12,CY=2018,FT=INTIRL,OU=500.0,WN=12,CY=2018,FT=INTFR,OU=2000.0,WN=12,CY=2018,FT=INTEW,OU=500.0,WN=12,CY=2018,FT=COAL,OU=13266.0,WN=12,CY=2018,FT=CCGT,OU=29942.0,WN=12,CY=2018,FT=BIOMASS,OU=2496.0,WN=13,CY=2018,FT=WIND,OU=4703.0,WN=13,CY=2018,FT=PS,OU=2340.0,WN=13,CY=2018,FT=OTHER,OU=6.0,WN=13,CY=2018,FT=OIL,OU=0.0,WN=13,CY=2018,FT=OCGT,OU=837.0,WN=13,CY=2018,FT=NUCLEAR,OU=7757.0,WN=13,CY=2018,FT=NPSHYD,OU=1011.0,WN=13,CY=2018,FT=INTNED,OU=1000.0,WN=13,CY=2018,FT=INTIRL,OU=500.0,WN=13,CY=2018,FT=INTFR,OU=2000.0,WN=13,CY=2018,FT=INTEW,OU=500.0,WN=13,CY=2018,FT=COAL,OU=13266.0,WN=13,CY=2018,FT=CCGT,OU=28188.0,WN=13,CY=2018,FT=BIOMASS,OU=2496.0,WN=14,CY=2018,FT=WIND,OU=3636.0,WN=14,CY=2018,FT=PS,OU=2052.0,WN=14,CY=2018,FT=OTHER,OU=6.0,WN=14,CY=2018,FT=OIL,OU=0.0,WN=14,CY=2018,FT=OCGT,OU=697.0,WN=14,CY=2018,FT=NUCLEAR,OU=8089.0,WN=14,CY=2018,FT=NPSHYD,OU=891.0,WN=14,CY=2018,FT=INTNED,OU=1000.0,WN=14,CY=2018,FT=INTIRL,OU=500.0,WN=14,CY=2018,FT=INTFR,OU=2000.0,WN=14,CY=2018,FT=INTEW,OU=500.0,WN=14,CY=2018,FT=COAL,OU=11096.0,WN=14,CY=2018,FT=CCGT,OU=25905.0,WN=14,CY=2018,FT=BIOMASS,OU=2496.0,WN=15,CY=2018,FT=WIND,OU=3635.0,WN=15,CY=2018,FT=PS,OU=2052.0,WN=15,CY=2018,FT=OTHER,OU=6.0,WN=15,CY=2018,FT=OIL,OU=0.0,WN=15,CY=2018,FT=OCGT,OU=697.0,WN=15,CY=2018,FT=NUCLEAR,OU=7752.0,WN=15,CY=2018,FT=NPSHYD,OU=899.0,WN=15,CY=2018,FT=INTNED,OU=1000.0,WN=15,CY=2018,FT=INTIRL,OU=500.0,WN=15,CY=2018,FT=INTFR,OU=2000.0,WN=15,CY=2018,FT=INTEW,OU=500.0,WN=15,CY=2018,FT=COAL,OU=10111.0,WN=15,CY=2018,FT=CCGT,OU=26740.0,WN=15,CY=2018,FT=BIOMASS,OU=2496.0,WN=16,CY=2018,FT=WIND,OU=3634.0,WN=16,CY=2018,FT=PS,OU=2052.0,WN=16,CY=2018,FT=OTHER,OU=6.0,WN=16,CY=2018,FT=OIL,OU=0.0,WN=16,CY=2018,FT=OCGT,OU=777.0,WN=16,CY=2018,FT=NUCLEAR,OU=7851.0,WN=16,CY=2018,FT=NPSHYD,OU=899.0,WN=16,CY=2018,FT=INTNED,OU=1000.0,WN=16,CY=2018,FT=INTIRL,OU=500.0,WN=16,CY=2018,FT=INTFR,OU=2000.0,WN=16,CY=2018,FT=INTEW,OU=500.0,WN=16,CY=2018,FT=COAL,OU=10111.0,WN=16,CY=2018,FT=CCGT,OU=26366.0,WN=16,CY=2018,FT=BIOMASS,OU=2496.0,WN=17,CY=2018,FT=WIND,OU=3555.0,WN=17,CY=2018,FT=PS,OU=2152.0,WN=17,CY=2018,FT=OTHER,OU=6.0,WN=17,CY=2018,FT=OIL,OU=0.0,WN=17,CY=2018,FT=OCGT,OU=777.0,WN=17,CY=2018,FT=NUCLEAR,OU=8506.0,WN=17,CY=2018,FT=NPSHYD,OU=921.0,WN=17,CY=2018,FT=INTNED,OU=1000.0,WN=17,CY=2018,FT=INTIRL,OU=500.0,WN=17,CY=2018,FT=INTFR,OU=2000.0,WN=17,CY=2018,FT=INTEW,OU=500.0,WN=17,CY=2018,FT=COAL,OU=10111.0,WN=17,CY=2018,FT=CCGT,OU=26258.0,WN=17,CY=2018,FT=BIOMASS,OU=2496.0,WN=18,CY=2018,FT=WIND,OU=3615.0,WN=18,CY=2018,FT=PS,OU=2002.0,WN=18,CY=2018,FT=OTHER,OU=6.0,WN=18,CY=2018,FT=OIL,OU=0.0,WN=18,CY=2018,FT=OCGT,OU=777.0,WN=18,CY=2018,FT=NUCLEAR,OU=7978.0,WN=18,CY=2018,FT=NPSHYD,OU=921.0,WN=18,CY=2018,FT=INTNED,OU=1000.0,WN=18,CY=2018,FT=INTIRL,OU=500.0,WN=18,CY=2018,FT=INTFR,OU=2000.0,WN=18,CY=2018,FT=INTEW,OU=0.0,WN=18,CY=2018,FT=COAL,OU=9114.0,WN=18,CY=2018,FT=CCGT,OU=26155.0,WN=18,CY=2018,FT=BIOMASS,OU=2496.0,WN=19,CY=2018,FT=WIND,OU=4224.0,WN=19,CY=2018,FT=PS,OU=2002.0,WN=19,CY=2018,FT=OTHER,OU=6.0,WN=19,CY=2018,FT=OCGT,OU=837.0,WN=19,CY=2018,FT=NUCLEAR,OU=6970.0,WN=19,CY=2018,FT=NPSHYD,OU=903.0,WN=19,CY=2018,FT=INTNED,OU=1000.0,WN=19,CY=2018,FT=INTIRL,OU=500.0,WN=19,CY=2018,FT=INTFR,OU=2000.0,WN=19,CY=2018,FT=INTEW,OU=0.0,WN=19,CY=2018,FT=COAL,OU=8634.0,WN=19,CY=2018,FT=CCGT,OU=25762.0,WN=19,CY=2018,FT=BIOMASS,OU=2496.0,WN=20,CY=2018,FT=WIND,OU=4222.0,WN=20,CY=2018,FT=PS,OU=1732.0,WN=20,CY=2018,FT=OTHER,OU=6.0,WN=20,CY=2018,FT=OCGT,OU=837.0,WN=20,CY=2018,FT=NUCLEAR,OU=7248.0,WN=20,CY=2018,FT=NPSHYD,OU=864.0,WN=20,CY=2018,FT=INTNED,OU=0.0,WN=20,CY=2018,FT=INTIRL,OU=500.0,WN=20,CY=2018,FT=INTFR,OU=2000.0,WN=20,CY=2018,FT=INTEW,OU=500.0,WN=20,CY=2018,FT=COAL,OU=8634.0,WN=20,CY=2018,FT=CCGT,OU=27175.0,WN=20,CY=2018,FT=BIOMASS,OU=2496.0,WN=21,CY=2018,FT=WIND,OU=4219.0,WN=21,CY=2018,FT=PS,OU=1732.0,WN=21,CY=2018,FT=OTHER,OU=6.0,WN=21,CY=2018,FT=OCGT,OU=837.0,WN=21,CY=2018,FT=NUCLEAR,OU=7517.0,WN=21,CY=2018,FT=NPSHYD,OU=904.0,WN=21,CY=2018,FT=INTNED,OU=1000.0,WN=21,CY=2018,FT=INTIRL,OU=500.0,WN=21,CY=2018,FT=INTFR,OU=2000.0,WN=21,CY=2018,FT=INTEW,OU=500.0,WN=21,CY=2018,FT=COAL,OU=7627.0,WN=21,CY=2018,FT=CCGT,OU=26806.0,WN=21,CY=2018,FT=BIOMASS,OU=2496.0,WN=22,CY=2018,FT=WIND,OU=4222.0,WN=22,CY=2018,FT=PS,OU=2002.0,WN=22,CY=2018,FT=OTHER,OU=6.0,WN=22,CY=2018,FT=OCGT,OU=837.0,WN=22,CY=2018,FT=NUCLEAR,OU=8024.0,WN=22,CY=2018,FT=NPSHYD,OU=975.0,WN=22,CY=2018,FT=INTNED,OU=1000.0,WN=22,CY=2018,FT=INTIRL,OU=500.0,WN=22,CY=2018,FT=INTFR,OU=2000.0,WN=22,CY=2018,FT=INTEW,OU=500.0,WN=22,CY=2018,FT=COAL,OU=8124.0,WN=22,CY=2018,FT=CCGT,OU=27849.0,WN=22,CY=2018,FT=BIOMASS,OU=2496.0,WN=23,CY=2018,FT=WIND,OU=2355.0,WN=23,CY=2018,FT=PS,OU=2190.0,WN=23,CY=2018,FT=OTHER,OU=6.0,WN=23,CY=2018,FT=OCGT,OU=837.0,WN=23,CY=2018,FT=NUCLEAR,OU=7887.0,WN=23,CY=2018,FT=NPSHYD,OU=950.0,WN=23,CY=2018,FT=INTNED,OU=1000.0,WN=23,CY=2018,FT=INTIRL,OU=500.0,WN=23,CY=2018,FT=INTFR,OU=2000.0,WN=23,CY=2018,FT=INTEW,OU=500.0,WN=23,CY=2018,FT=COAL,OU=8277.0,WN=23,CY=2018,FT=CCGT,OU=26318.0,WN=23,CY=2018,FT=BIOMASS,OU=1851.0,WN=24,CY=2018,FT=WIND,OU=2381.0,WN=24,CY=2018,FT=PS,OU=2340.0,WN=24,CY=2018,FT=OTHER,OU=6.0,WN=24,CY=2018,FT=OCGT,OU=837.0,WN=24,CY=2018,FT=NUCLEAR,OU=7932.0,WN=24,CY=2018,FT=NPSHYD,OU=947.0,WN=24,CY=2018,FT=INTNED,OU=1000.0,WN=24,CY=2018,FT=INTIRL,OU=500.0,WN=24,CY=2018,FT=INTFR,OU=2000.0,WN=24,CY=2018,FT=INTEW,OU=500.0,WN=24,CY=2018,FT=COAL,OU=8604.0,WN=24,CY=2018,FT=CCGT,OU=25317.0,WN=24,CY=2018,FT=BIOMASS,OU=1841.0,WN=25,CY=2018,FT=WIND,OU=2390.0,WN=25,CY=2018,FT=PS,OU=2320.0,WN=25,CY=2018,FT=OTHER,OU=6.0,WN=25,CY=2018,FT=OCGT,OU=837.0,WN=25,CY=2018,FT=NUCLEAR,OU=7827.0,WN=25,CY=2018,FT=NPSHYD,OU=806.0,WN=25,CY=2018,FT=INTNED,OU=1000.0,WN=25,CY=2018,FT=INTIRL,OU=500.0,WN=25,CY=2018,FT=INTFR,OU=1000.0,WN=25,CY=2018,FT=INTEW,OU=500.0,WN=25,CY=2018,FT=COAL,OU=9124.0,WN=25,CY=2018,FT=CCGT,OU=24989.0,WN=25,CY=2018,FT=BIOMASS,OU=1841.0,WN=26,CY=2018,FT=WIND,OU=2393.0,WN=26,CY=2018,FT=PS,OU=2320.0,WN=26,CY=2018,FT=OTHER,OU=6.0,WN=26,CY=2018,FT=OCGT,OU=837.0,WN=26,CY=2018,FT=NUCLEAR,OU=7578.0,WN=26,CY=2018,FT=NPSHYD,OU=780.0,WN=26,CY=2018,FT=INTNED,OU=1000.0,WN=26,CY=2018,FT=INTIRL,OU=500.0,WN=26,CY=2018,FT=INTFR,OU=1000.0,WN=26,CY=2018,FT=INTEW,OU=500.0,WN=26,CY=2018,FT=COAL,OU=8624.0,WN=26,CY=2018,FT=CCGT,OU=24760.0,WN=26,CY=2018,FT=BIOMASS,OU=1841.0,WN=27,CY=2018,FT=WIND,OU=2330.0,WN=27,CY=2018,FT=PS,OU=2440.0,WN=27,CY=2018,FT=OTHER,OU=6.0,WN=27,CY=2018,FT=OCGT,OU=798.0,WN=27,CY=2018,FT=NUCLEAR,OU=7221.0,WN=27,CY=2018,FT=NPSHYD,OU=810.0,WN=27,CY=2018,FT=INTNED,OU=1000.0,WN=27,CY=2018,FT=INTIRL,OU=500.0,WN=27,CY=2018,FT=INTFR,OU=2000.0,WN=27,CY=2018,FT=INTEW,OU=500.0,WN=27,CY=2018,FT=COAL,OU=8124.0,WN=27,CY=2018,FT=CCGT,OU=24014.0,WN=27,CY=2018,FT=BIOMASS,OU=1841.0,WN=28,CY=2018,FT=WIND,OU=2367.0,WN=28,CY=2018,FT=PS,OU=2440.0,WN=28,CY=2018,FT=OTHER,OU=6.0,WN=28,CY=2018,FT=OCGT,OU=798.0,WN=28,CY=2018,FT=NUCLEAR,OU=7311.0,WN=28,CY=2018,FT=NPSHYD,OU=763.0,WN=28,CY=2018,FT=INTNED,OU=1000.0,WN=28,CY=2018,FT=INTIRL,OU=500.0,WN=28,CY=2018,FT=INTFR,OU=2000.0,WN=28,CY=2018,FT=INTEW,OU=500.0,WN=28,CY=2018,FT=COAL,OU=7618.0,WN=28,CY=2018,FT=CCGT,OU=22767.0,WN=28,CY=2018,FT=BIOMASS,OU=1841.0,WN=29,CY=2018,FT=WIND,OU=2368.0,WN=29,CY=2018,FT=PS,OU=2440.0,WN=29,CY=2018,FT=OTHER,OU=6.0,WN=29,CY=2018,FT=OCGT,OU=798.0,WN=29,CY=2018,FT=NUCLEAR,OU=7240.0,WN=29,CY=2018,FT=NPSHYD,OU=763.0,WN=29,CY=2018,FT=INTNED,OU=1000.0,WN=29,CY=2018,FT=INTIRL,OU=500.0,WN=29,CY=2018,FT=INTFR,OU=2000.0,WN=29,CY=2018,FT=INTEW,OU=500.0,WN=29,CY=2018,FT=COAL,OU=8118.0,WN=29,CY=2018,FT=CCGT,OU=25222.0,WN=29,CY=2018,FT=BIOMASS,OU=2486.0,WN=30,CY=2018,FT=WIND,OU=2332.0,WN=30,CY=2018,FT=PS,OU=2440.0,WN=30,CY=2018,FT=OTHER,OU=6.0,WN=30,CY=2018,FT=OCGT,OU=837.0,WN=30,CY=2018,FT=NUCLEAR,OU=7477.0,WN=30,CY=2018,FT=NPSHYD,OU=763.0,WN=30,CY=2018,FT=INTNED,OU=1000.0,WN=30,CY=2018,FT=INTIRL,OU=500.0,WN=30,CY=2018,FT=INTFR,OU=2000.0,WN=30,CY=2018,FT=INTEW,OU=500.0,WN=30,CY=2018,FT=COAL,OU=9103.0,WN=30,CY=2018,FT=CCGT,OU=26044.0,WN=30,CY=2018,FT=BIOMASS,OU=2476.0,WN=31,CY=2018,FT=WIND,OU=2330.0,WN=31,CY=2018,FT=PS,OU=2728.0,WN=31,CY=2018,FT=OTHER,OU=6.0,WN=31,CY=2018,FT=OCGT,OU=837.0,WN=31,CY=2018,FT=NUCLEAR,OU=7919.0,WN=31,CY=2018,FT=NPSHYD,OU=868.0,WN=31,CY=2018,FT=INTNED,OU=1000.0,WN=31,CY=2018,FT=INTIRL,OU=500.0,WN=31,CY=2018,FT=INTFR,OU=2000.0,WN=31,CY=2018,FT=INTEW,OU=500.0,WN=31,CY=2018,FT=COAL,OU=10089.0,WN=31,CY=2018,FT=CCGT,OU=25451.0,WN=31,CY=2018,FT=BIOMASS,OU=2476.0,WN=32,CY=2018,FT=WIND,OU=2887.0,WN=32,CY=2018,FT=PS,OU=2728.0,WN=32,CY=2018,FT=OTHER,OU=6.0,WN=32,CY=2018,FT=OCGT,OU=837.0,WN=32,CY=2018,FT=NUCLEAR,OU=7111.0,WN=32,CY=2018,FT=NPSHYD,OU=931.0,WN=32,CY=2018,FT=INTNED,OU=1000.0,WN=32,CY=2018,FT=INTIRL,OU=500.0,WN=32,CY=2018,FT=INTFR,OU=2000.0,WN=32,CY=2018,FT=INTEW,OU=500.0,WN=32,CY=2018,FT=COAL,OU=10092.0,WN=32,CY=2018,FT=CCGT,OU=26770.0,WN=32,CY=2018,FT=BIOMASS,OU=2476.0,WN=33,CY=2018,FT=WIND,OU=2995.0,WN=33,CY=2018,FT=PS,OU=2728.0,WN=33,CY=2018,FT=OTHER,OU=6.0,WN=33,CY=2018,FT=OCGT,OU=837.0,WN=33,CY=2018,FT=NUCLEAR,OU=6852.0,WN=33,CY=2018,FT=NPSHYD,OU=938.0,WN=33,CY=2018,FT=INTNED,OU=1000.0,WN=33,CY=2018,FT=INTIRL,OU=500.0,WN=33,CY=2018,FT=INTFR,OU=2000.0,WN=33,CY=2018,FT=INTEW,OU=500.0,WN=33,CY=2018,FT=COAL,OU=10092.0,WN=33,CY=2018,FT=CCGT,OU=27610.0,WN=33,CY=2018,FT=BIOMASS,OU=2476.0,WN=34,CY=2018,FT=WIND,OU=2997.0,WN=34,CY=2018,FT=PS,OU=2728.0,WN=34,CY=2018,FT=OTHER,OU=6.0,WN=34,CY=2018,FT=OCGT,OU=837.0,WN=34,CY=2018,FT=NUCLEAR,OU=7157.0,WN=34,CY=2018,FT=NPSHYD,OU=938.0,WN=34,CY=2018,FT=INTNED,OU=1000.0,WN=34,CY=2018,FT=INTIRL,OU=500.0,WN=34,CY=2018,FT=INTFR,OU=2000.0,WN=34,CY=2018,FT=INTEW,OU=500.0,WN=34,CY=2018,FT=COAL,OU=9592.0,WN=34,CY=2018,FT=CCGT,OU=28445.0,WN=34,CY=2018,FT=BIOMASS,OU=2476.0,WN=35,CY=2018,FT=WIND,OU=2988.0,WN=35,CY=2018,FT=PS,OU=2728.0,WN=35,CY=2018,FT=OTHER,OU=6.0,WN=35,CY=2018,FT=OCGT,OU=837.0,WN=35,CY=2018,FT=NUCLEAR,OU=7060.0,WN=35,CY=2018,FT=NPSHYD,OU=938.0,WN=35,CY=2018,FT=INTNED,OU=1000.0,WN=35,CY=2018,FT=INTIRL,OU=500.0,WN=35,CY=2018,FT=INTFR,OU=2000.0,WN=35,CY=2018,FT=INTEW,OU=500.0,WN=35,CY=2018,FT=COAL,OU=11226.0,WN=35,CY=2018,FT=CCGT,OU=27374.0,WN=35,CY=2018,FT=BIOMASS,OU=2476.0,WN=36,CY=2018,FT=WIND,OU=3587.0,WN=36,CY=2018,FT=PS,OU=2728.0,WN=36,CY=2018,FT=OTHER,OU=6.0,WN=36,CY=2018,FT=OCGT,OU=837.0,WN=36,CY=2018,FT=NUCLEAR,OU=7763.0,WN=36,CY=2018,FT=NPSHYD,OU=975.0,WN=36,CY=2018,FT=INTNED,OU=1000.0,WN=36,CY=2018,FT=INTIRL,OU=500.0,WN=36,CY=2018,FT=INTFR,OU=1000.0,WN=36,CY=2018,FT=INTEW,OU=500.0,WN=36,CY=2018,FT=COAL,OU=11226.0,WN=36,CY=2018,FT=CCGT,OU=26411.0,WN=36,CY=2018,FT=BIOMASS,OU=2476.0,WN=37,CY=2018,FT=WIND,OU=3636.0,WN=37,CY=2018,FT=PS,OU=2368.0,WN=37,CY=2018,FT=OTHER,OU=6.0,WN=37,CY=2018,FT=OCGT,OU=837.0,WN=37,CY=2018,FT=NUCLEAR,OU=7144.0,WN=37,CY=2018,FT=NPSHYD,OU=1007.0,WN=37,CY=2018,FT=INTNED,OU=1000.0,WN=37,CY=2018,FT=INTIRL,OU=500.0,WN=37,CY=2018,FT=INTFR,OU=1000.0,WN=37,CY=2018,FT=INTEW,OU=500.0,WN=37,CY=2018,FT=COAL,OU=11726.0,WN=37,CY=2018,FT=CCGT,OU=24831.0,WN=37,CY=2018,FT=BIOMASS,OU=2476.0,WN=38,CY=2018,FT=WIND,OU=3637.0,WN=38,CY=2018,FT=PS,OU=2248.0,WN=38,CY=2018,FT=OTHER,OU=6.0,WN=38,CY=2018,FT=OCGT,OU=837.0,WN=38,CY=2018,FT=NUCLEAR,OU=7110.0,WN=38,CY=2018,FT=NPSHYD,OU=1007.0,WN=38,CY=2018,FT=INTNED,OU=0.0,WN=38,CY=2018,FT=INTIRL,OU=500.0,WN=38,CY=2018,FT=INTFR,OU=2000.0,WN=38,CY=2018,FT=INTEW,OU=500.0,WN=38,CY=2018,FT=COAL,OU=11726.0,WN=38,CY=2018,FT=CCGT,OU=26295.0,WN=38,CY=2018,FT=BIOMASS,OU=2476.0,WN=39,CY=2018,FT=WIND,OU=3626.0,WN=39,CY=2018,FT=PS,OU=2368.0,WN=39,CY=2018,FT=OTHER,OU=6.0,WN=39,CY=2018,FT=OCGT,OU=837.0,WN=39,CY=2018,FT=NUCLEAR,OU=7545.0,WN=39,CY=2018,FT=NPSHYD,OU=1049.0,WN=39,CY=2018,FT=INTNED,OU=1000.0,WN=39,CY=2018,FT=INTIRL,OU=500.0,WN=39,CY=2018,FT=INTFR,OU=2000.0,WN=39,CY=2018,FT=INTEW,OU=500.0,WN=39,CY=2018,FT=COAL,OU=11741.0,WN=39,CY=2018,FT=CCGT,OU=27864.0,WN=39,CY=2018,FT=BIOMASS,OU=2476.0,WN=40,CY=2018,FT=WIND,OU=4850.0,WN=40,CY=2018,FT=PS,OU=2448.0,WN=40,CY=2018,FT=OTHER,OU=6.0,WN=40,CY=2018,FT=OCGT,OU=837.0,WN=40,CY=2018,FT=NUCLEAR,OU=7501.0,WN=40,CY=2018,FT=NPSHYD,OU=1049.0,WN=40,CY=2018,FT=INTNED,OU=1000.0,WN=40,CY=2018,FT=INTIRL,OU=500.0,WN=40,CY=2018,FT=INTFR,OU=2000.0,WN=40,CY=2018,FT=INTEW,OU=500.0,WN=40,CY=2018,FT=COAL,OU=10874.0,WN=40,CY=2018,FT=CCGT,OU=27994.0,WN=40,CY=2018,FT=BIOMASS,OU=2476.0,WN=41,CY=2018,FT=WIND,OU=4858.0,WN=41,CY=2018,FT=PS,OU=2448.0,WN=41,CY=2018,FT=OTHER,OU=6.0,WN=41,CY=2018,FT=OCGT,OU=837.0,WN=41,CY=2018,FT=NUCLEAR,OU=7671.0,WN=41,CY=2018,FT=NPSHYD,OU=1049.0,WN=41,CY=2018,FT=INTNED,OU=1000.0,WN=41,CY=2018,FT=INTIRL,OU=500.0,WN=41,CY=2018,FT=INTFR,OU=2000.0,WN=41,CY=2018,FT=INTEW,OU=500.0,WN=41,CY=2018,FT=COAL,OU=10874.0,WN=41,CY=2018,FT=CCGT,OU=27474.0,WN=41,CY=2018,FT=BIOMASS,OU=2476.0,WN=42,CY=2018,FT=WIND,OU=4849.0,WN=42,CY=2018,FT=PS,OU=2448.0,WN=42,CY=2018,FT=OTHER,OU=6.0,WN=42,CY=2018,FT=OCGT,OU=837.0,WN=42,CY=2018,FT=NUCLEAR,OU=7582.0,WN=42,CY=2018,FT=NPSHYD,OU=1039.0,WN=42,CY=2018,FT=INTNED,OU=1000.0,WN=42,CY=2018,FT=INTIRL,OU=500.0,WN=42,CY=2018,FT=INTFR,OU=2000.0,WN=42,CY=2018,FT=INTEW,OU=500.0,WN=42,CY=2018,FT=COAL,OU=10874.0,WN=42,CY=2018,FT=CCGT,OU=28229.0,WN=42,CY=2018,FT=BIOMASS,OU=2476.0,WN=43,CY=2018,FT=WIND,OU=4827.0,WN=43,CY=2018,FT=PS,OU=2628.0,WN=43,CY=2018,FT=OTHER,OU=6.0,WN=43,CY=2018,FT=OCGT,OU=837.0,WN=43,CY=2018,FT=NUCLEAR,OU=7204.0,WN=43,CY=2018,FT=NPSHYD,OU=1019.0,WN=43,CY=2018,FT=INTNED,OU=1000.0,WN=43,CY=2018,FT=INTIRL,OU=500.0,WN=43,CY=2018,FT=INTFR,OU=2000.0,WN=43,CY=2018,FT=INTEW,OU=500.0,WN=43,CY=2018,FT=COAL,OU=10874.0,WN=43,CY=2018,FT=CCGT,OU=28937.0,WN=43,CY=2018,FT=BIOMASS,OU=2476.0,WN=44,CY=2018,FT=WIND,OU=4717.0,WN=44,CY=2018,FT=PS,OU=2628.0,WN=44,CY=2018,FT=OTHER,OU=6.0,WN=44,CY=2018,FT=OCGT,OU=837.0,WN=44,CY=2018,FT=NUCLEAR,OU=8456.0,WN=44,CY=2018,FT=NPSHYD,OU=1039.0,WN=44,CY=2018,FT=INTNED,OU=1000.0,WN=44,CY=2018,FT=INTIRL,OU=500.0,WN=44,CY=2018,FT=INTFR,OU=2000.0,WN=44,CY=2018,FT=INTEW,OU=500.0,WN=44,CY=2018,FT=COAL,OU=10874.0,WN=44,CY=2018,FT=CCGT,OU=28190.0,WN=44,CY=2018,FT=BIOMASS,OU=2476.0,WN=45,CY=2018,FT=WIND,OU=5317.0,WN=45,CY=2018,FT=PS,OU=2628.0,WN=45,CY=2018,FT=OTHER,OU=6.0,WN=45,CY=2018,FT=OCGT,OU=837.0,WN=45,CY=2018,FT=NUCLEAR,OU=8466.0,WN=45,CY=2018,FT=NPSHYD,OU=1039.0,WN=45,CY=2018,FT=INTNED,OU=1000.0,WN=45,CY=2018,FT=INTIRL,OU=500.0,WN=45,CY=2018,FT=INTFR,OU=2000.0,WN=45,CY=2018,FT=INTEW,OU=500.0,WN=45,CY=2018,FT=COAL,OU=10874.0,WN=45,CY=2018,FT=CCGT,OU=27762.0,WN=45,CY=2018,FT=BIOMASS,OU=2476.0,WN=46,CY=2018,FT=WIND,OU=5317.0,WN=46,CY=2018,FT=PS,OU=2728.0,WN=46,CY=2018,FT=OTHER,OU=6.0,WN=46,CY=2018,FT=OCGT,OU=836.0,WN=46,CY=2018,FT=NUCLEAR,OU=8429.0,WN=46,CY=2018,FT=NPSHYD,OU=1039.0,WN=46,CY=2018,FT=INTNED,OU=1000.0,WN=46,CY=2018,FT=INTIRL,OU=500.0,WN=46,CY=2018,FT=INTFR,OU=2000.0,WN=46,CY=2018,FT=INTEW,OU=500.0,WN=46,CY=2018,FT=COAL,OU=10389.0,WN=46,CY=2018,FT=CCGT,OU=28986.0,WN=46,CY=2018,FT=BIOMASS,OU=2476.0,WN=47,CY=2018,FT=WIND,OU=5317.0,WN=47,CY=2018,FT=PS,OU=2728.0,WN=47,CY=2018,FT=OTHER,OU=6.0,WN=47,CY=2018,FT=OCGT,OU=837.0,WN=47,CY=2018,FT=NUCLEAR,OU=7680.0,WN=47,CY=2018,FT=NPSHYD,OU=1039.0,WN=47,CY=2018,FT=INTNED,OU=1000.0,WN=47,CY=2018,FT=INTIRL,OU=500.0,WN=47,CY=2018,FT=INTFR,OU=2000.0,WN=47,CY=2018,FT=INTEW,OU=500.0,WN=47,CY=2018,FT=COAL,OU=10389.0,WN=47,CY=2018,FT=CCGT,OU=28991.0,WN=47,CY=2018,FT=BIOMASS,OU=2476.0,WN=48,CY=2018,FT=WIND,OU=5317.0,WN=48,CY=2018,FT=PS,OU=2728.0,WN=48,CY=2018,FT=OTHER,OU=6.0,WN=48,CY=2018,FT=OCGT,OU=837.0,WN=48,CY=2018,FT=NUCLEAR,OU=8157.0,WN=48,CY=2018,FT=NPSHYD,OU=1039.0,WN=48,CY=2018,FT=INTNED,OU=1000.0,WN=48,CY=2018,FT=INTIRL,OU=500.0,WN=48,CY=2018,FT=INTFR,OU=2000.0,WN=48,CY=2018,FT=INTEW,OU=500.0,WN=48,CY=2018,FT=COAL,OU=10389.0,WN=48,CY=2018,FT=CCGT,OU=29003.0,WN=48,CY=2018,FT=BIOMASS,OU=2476.0,WN=49,CY=2018,FT=WIND,OU=6483.0,WN=49,CY=2018,FT=PS,OU=2728.0,WN=49,CY=2018,FT=OTHER,OU=6.0,WN=49,CY=2018,FT=OCGT,OU=837.0,WN=49,CY=2018,FT=NUCLEAR,OU=8581.0,WN=49,CY=2018,FT=NPSHYD,OU=1039.0,WN=49,CY=2018,FT=INTNED,OU=1000.0,WN=49,CY=2018,FT=INTIRL,OU=500.0,WN=49,CY=2018,FT=INTFR,OU=2000.0,WN=49,CY=2018,FT=INTEW,OU=500.0,WN=49,CY=2018,FT=COAL,OU=8913.0,WN=49,CY=2018,FT=CCGT,OU=28808.0,WN=49,CY=2018,FT=BIOMASS,OU=2486.0,WN=50,CY=2018,FT=WIND,OU=6483.0,WN=50,CY=2018,FT=PS,OU=2728.0,WN=50,CY=2018,FT=OTHER,OU=6.0,WN=50,CY=2018,FT=OCGT,OU=837.0,WN=50,CY=2018,FT=NUCLEAR,OU=8555.0,WN=50,CY=2018,FT=NPSHYD,OU=1039.0,WN=50,CY=2018,FT=INTNED,OU=1000.0,WN=50,CY=2018,FT=INTIRL,OU=500.0,WN=50,CY=2018,FT=INTFR,OU=2000.0,WN=50,CY=2018,FT=INTEW,OU=500.0,WN=50,CY=2018,FT=COAL,OU=8913.0,WN=50,CY=2018,FT=CCGT,OU=29648.0,WN=50,CY=2018,FT=BIOMASS,OU=2486.0,WN=51,CY=2018,FT=WIND,OU=6483.0,WN=51,CY=2018,FT=PS,OU=2728.0,WN=51,CY=2018,FT=OTHER,OU=6.0,WN=51,CY=2018,FT=OCGT,OU=837.0,WN=51,CY=2018,FT=NUCLEAR,OU=8076.0,WN=51,CY=2018,FT=NPSHYD,OU=1049.0,WN=51,CY=2018,FT=INTNED,OU=1000.0,WN=51,CY=2018,FT=INTIRL,OU=500.0,WN=51,CY=2018,FT=INTFR,OU=2000.0,WN=51,CY=2018,FT=INTEW,OU=500.0,WN=51,CY=2018,FT=COAL,OU=8913.0,WN=51,CY=2018,FT=CCGT,OU=29851.0,WN=51,CY=2018,FT=BIOMASS,OU=2486.0,WN=52,CY=2018,FT=WIND,OU=6483.0,WN=52,CY=2018,FT=PS,OU=2548.0,WN=52,CY=2018,FT=OTHER,OU=6.0,WN=52,CY=2018,FT=OCGT,OU=837.0,WN=52,CY=2018,FT=NUCLEAR,OU=8966.0,WN=52,CY=2018,FT=NPSHYD,OU=1049.0,WN=52,CY=2018,FT=INTNED,OU=1000.0,WN=52,CY=2018,FT=INTIRL,OU=500.0,WN=52,CY=2018,FT=INTFR,OU=2000.0,WN=52,CY=2018,FT=INTEW,OU=500.0,WN=52,CY=2018,FT=COAL,OU=8913.0,WN=52,CY=2018,FT=CCGT,OU=29851.0,WN=52,CY=2018,FT=BIOMASS,OU=2486.0,WN=1,CY=2019,FT=WIND,OU=6458.0,WN=1,CY=2019,FT=PS,OU=2548.0,WN=1,CY=2019,FT=OTHER,OU=0.0,WN=1,CY=2019,FT=OCGT,OU=836.0,WN=1,CY=2019,FT=NUCLEAR,OU=8853.0,WN=1,CY=2019,FT=NPSHYD,OU=1048.0,WN=1,CY=2019,FT=INTNED,OU=1000.0,WN=1,CY=2019,FT=INTIRL,OU=500.0,WN=1,CY=2019,FT=INTFR,OU=2000.0,WN=1,CY=2019,FT=INTEW,OU=500.0,WN=1,CY=2019,FT=COAL,OU=8913.0,WN=1,CY=2019,FT=CCGT,OU=29851.0,WN=1,CY=2019,FT=BIOMASS,OU=2486.0}`

#### UOU2T14D: National Output Usable by Fuel Type and BM Unit, 2-14 Days ahead

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|FT|char(10)|Fuel type|||
|OU|decimal(10,2)|Output usable|MW|&nbsp;|

Index: BMU, SD

Example:

`2017:04:21:12:40:35:GMT: subject=BMRA.SYSTEM.2__PPGEN001.UOU2T14D, message={TP=2017:04:21:12:38:00:GMT,NR=13,SD=2017:04:23:00:00:00:GMT,FT=WIND,OU=12.0,SD=2017:04:24:00:00:00:GMT,FT=WIND,OU=26.0,SD=2017:04:25:00:00:00:GMT,FT=WIND,OU=30.0,SD=2017:04:26:00:00:00:GMT,FT=WIND,OU=8.0,SD=2017:04:27:00:00:00:GMT,FT=WIND,OU=3.0,SD=2017:04:28:00:00:00:GMT,FT=WIND,OU=4.0,SD=2017:04:29:00:00:00:GMT,FT=WIND,OU=5.0,SD=2017:04:30:00:00:00:GMT,FT=WIND,OU=4.0,SD=2017:05:01:00:00:00:GMT,FT=WIND,OU=4.0,SD=2017:05:02:00:00:00:GMT,FT=WIND,OU=5.0,SD=2017:05:03:00:00:00:GMT,FT=WIND,OU=4.0,SD=2017:05:04:00:00:00:GMT,FT=WIND,OU=4.0,SD=2017:05:05:00:00:00:GMT,FT=WIND,OU=18.0}`

#### UOU2T52W: National Output Usable by Fuel Type and BM Unit, 2-52 Weeks ahead

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|CY|int|Calendar year|||
|WN|int|Week number|||
|FT|char(10)|Fuel type|||
|OU|decimal(10,2)|Output usable|MW|&nbsp;|

Index: BMU, CY, WN

Example:

`2018:01:04:13:41:23:GMT: subject=BMRA.SYSTEM.2__PPGEN001.UOU2T52W, message={TP=2018:01:04:13:31:00:GMT,NR=51,WN=3,CY=2018,FT=WIND,OU=28.0,WN=4,CY=2018,FT=WIND,OU=28.0,WN=5,CY=2018,FT=WIND,OU=28.0,WN=6,CY=2018,FT=WIND,OU=26.0,WN=7,CY=2018,FT=WIND,OU=26.0,WN=8,CY=2018,FT=WIND,OU=26.0,WN=9,CY=2018,FT=WIND,OU=26.0,WN=10,CY=2018,FT=WIND,OU=20.0,WN=11,CY=2018,FT=WIND,OU=20.0,WN=12,CY=2018,FT=WIND,OU=20.0,WN=13,CY=2018,FT=WIND,OU=20.0,WN=14,CY=2018,FT=WIND,OU=15.0,WN=15,CY=2018,FT=WIND,OU=15.0,WN=16,CY=2018,FT=WIND,OU=15.0,WN=17,CY=2018,FT=WIND,OU=15.0,WN=18,CY=2018,FT=WIND,OU=15.0,WN=19,CY=2018,FT=WIND,OU=18.0,WN=20,CY=2018,FT=WIND,OU=18.0,WN=21,CY=2018,FT=WIND,OU=18.0,WN=22,CY=2018,FT=WIND,OU=18.0,WN=23,CY=2018,FT=WIND,OU=10.0,WN=24,CY=2018,FT=WIND,OU=10.0,WN=25,CY=2018,FT=WIND,OU=10.0,WN=26,CY=2018,FT=WIND,OU=10.0,WN=27,CY=2018,FT=WIND,OU=10.0,WN=28,CY=2018,FT=WIND,OU=10.0,WN=29,CY=2018,FT=WIND,OU=10.0,WN=30,CY=2018,FT=WIND,OU=10.0,WN=31,CY=2018,FT=WIND,OU=10.0,WN=32,CY=2018,FT=WIND,OU=13.0,WN=33,CY=2018,FT=WIND,OU=13.0,WN=34,CY=2018,FT=WIND,OU=13.0,WN=35,CY=2018,FT=WIND,OU=13.0,WN=36,CY=2018,FT=WIND,OU=15.0,WN=37,CY=2018,FT=WIND,OU=15.0,WN=38,CY=2018,FT=WIND,OU=15.0,WN=39,CY=2018,FT=WIND,OU=15.0,WN=40,CY=2018,FT=WIND,OU=20.0,WN=41,CY=2018,FT=WIND,OU=20.0,WN=42,CY=2018,FT=WIND,OU=20.0,WN=43,CY=2018,FT=WIND,OU=20.0,WN=44,CY=2018,FT=WIND,OU=20.0,WN=45,CY=2018,FT=WIND,OU=23.0,WN=46,CY=2018,FT=WIND,OU=23.0,WN=47,CY=2018,FT=WIND,OU=23.0,WN=48,CY=2018,FT=WIND,OU=23.0,WN=49,CY=2018,FT=WIND,OU=28.0,WN=50,CY=2018,FT=WIND,OU=28.0,WN=51,CY=2018,FT=WIND,OU=28.0,WN=52,CY=2018,FT=WIND,OU=28.0,WN=1,CY=2019,FT=WIND,OU=28.0}`


### SO Messages

#### SYSWARN: System Warning

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|SW|char(unlimited)|System warning message||&nbsp;|

Index: TP

Example:

`2017:04:21:14:28:15:GMT: subject=BMRA.SYSTEM.SYSWARN, message={TP=2017:04:21:14:28:09:GMT,SW=NATIONAL GRID NOTIFICATION of excess energy prices used for settlement outside of BALIT for SO to SO Transactions over the National Grid/RTE  Interconnector.  Prices cover 23:00Hrs Today to 05:00Hrs Tomorrow (UK local time) and are in Euro/MWh. From RTE: Offer 98.69; Bid 1.03 From NGC: Offer 247.38; Bid 0.00  Prices cover 05:00Hrs Tomorrow to 19:00Hrs Tomorrow (UK local time) and are in Euro/MWh. From RTE: Offer 89.05; Bid 0.00 From NGC: Offer 329.84; Bid 17.67  Prices cover 19:00Hrs Tomorrow to 23:00Hrs Tomorrow (UK local time) and are in Euro/MWh. From RTE: Offer 98.69; Bid 1.03 From NGC: Offer 353.40; Bid 23.56}`

#### SYSMSG: System Message

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|SM|char(unlimited)|System warning message|||
|MT|char(6)|Message type|   |&nbsp;|

Example:

`2018:01:02:17:52:56:GMT: subject=BMRA.SYSTEM.SYSMSG, message={MT=MIDNP,TP=2018:01:02:17:51:46:GMT,SM=Market Index Data for Settlement Day 20180102 period 35 from Automated Power Exchange (UK) (APXMIDP) was not received. Price and volume defaulted to 0.}`

#### DCONTROL: Demand Control Instruction Notification

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|DS|char(10)|Affected LDSO|||
|ID|int|Demand Control ID||unique identifier|
|SQ|int|Instruction Sequence No|||
|EV|char(1)|Demand Control Event Flag||'I' indicates instruction by the SO or emergency manual disconnection. 'L' indicates automatic low frequency demand disconnection|
|TF|datetime|Time From|||
|TI|datetime|Time To|||
|VO|decimal(10,2)|Demand Control Level|MW||
|SO|boolean|SO-Flag||True indicates that an instruction should be considered to be potentially impacted by transmission constraints|
|AM|char(3)|Amendment Flag||'ORI' : Original, 'INS' : Insert, 'UPD' : Update|

Example:

`2015:11:30:11:35:59:GMT: subject=BMRA.SYSTEM.DCONTROL, message={TP=2015:11:30:11:32:32:GMT,NR=1,DS=ETCL,ID=00002,SQ=1,EV=I,TF=2015:11:30:00:00:00:GMT,TI=2015:12:02:00:00:00:GMT,VO=34.0,SO=T,AM=ORI}`

### Out-turn Data

#### FREQ: System frequency data

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
| SD | decimal(10,3) | System Frequency | Hz | &nbsp; |

Index: TS

Row generated every 5 minutes

Example:

`2017:03:29:00:00:52:GMT: subject=BMRA.SYSTEM.FREQ, message={TS=2017:03:28:23:58:00:GMT,SF=50.058}`

#### TEMP: Temperature Data

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
| TO | decimal(5,3) | Outturn Temperature | celsius | &nbsp; |
| TN | decimal(5,3) | Normal Reference Temperature | celsius | &nbsp; |
| TL | decimal(5,3) | Low Reference Temperature | celsius | &nbsp; |
| TH | decimal(5,3) | High Reference Temperature | celsius | &nbsp; |

Index: TS

Example:

`2017:04:21:15:45:35:GMT: subject=BMRA.SYSTEM.TEMP, message={TP=2017:04:21:15:45:00:GMT,TS=2017:04:21:11:00:00:GMT,TO=11.2,TN=9.9,TL=7.0,TH=12.5}`

#### INDO: Initial National Demand Out-Turn

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|VD|decimal(10,2)|Demand level|MW|average value of demand for a Settlement Period INCLUDING transmission losses but EXCLUDING station transformer load, pumped storage demand and interconnector demand|

Example:

`2017:03:29:00:01:08:GMT: subject=BMRA.SYSTEM.INDO, message={TP=2017:03:29:00:00:00:GMT,SD=2017:03:29:00:00:00:GMT,SP=2,VD=24016.0}`

#### ITSDO: Initial Transmission System Demand Outturn

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|VD|decimal(10,2)|Demand level|MW|verage megawatt value of demand for a Settlement Period INCLUDING transmission losses, station transformer load, pumped storage demand and interconnector demand. The ITSDO is made available by the System Operator within 15 minutes after a Settlement Period, based on their operational metering. The composition of the Initial Transmission System Demand Out-Turn matches that of the Transmission System Demand Forecast and so ITSDO and TSDF are comparable.|

Example:

`2017:03:29:00:01:09:GMT: subject=BMRA.SYSTEM.ITSDO, message={TP=2017:03:29:00:00:00:GMT,SD=2017:03:29:00:00:00:GMT,SP=2,VD=26085.0}`

#### LOLP: Loss of Load Probability and De-rated Margin

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
| LP  | decimal(10,3)  | Loss of Load Probability  | probability  |  |
| DR  | decimal(10,3)  | De-rated Margin | MW  | &nbsp; |

Example:

`2017:04:21:00:12:37:GMT: subject=BMRA.SYSTEM.LOLP, message={TP=2017:04:21:00:12:31:GMT,NR=4,SD=2017:04:21:00:00:00:GMT,SP=5,LP=0.0,DR=15175.511,SD=2017:04:21:00:00:00:GMT,SP=7,LP=0.0,DR=15777.266,SD=2017:04:21:00:00:00:GMT,SP=11,LP=0.0,DR=14245.876,SD=2017:04:21:00:00:00:GMT,SP=19,LP=0.0,DR=6852.614}`

#### NONBM: Non-BM STOR Out-Turn

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|NB||Non-BM STOR Volume|MWh||

Example:

`2017:03:29:00:01:24:GMT: subject=BMRA.SYSTEM.NONBM, message={TP=2017:03:29:00:00:00:GMT,SD=2017:03:29:00:00:00:GMT,SP=2,NB=0}`

#### INDOD: Daily Energy Volume Data

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|EO||Energy Volume Out-turn|MWh||
|EL||Energy Volume Low Reference|MWh||
|EH||Energy Volume High Reference|MWh||
|EN||Energy Normal Reference Volume|MWh|&nbsp;|

Example:

`2017:04:21:23:15:37:GMT: subject=BMRA.SYSTEM.INDOD, message={TP=2017:04:21:23:15:00:GMT,SD=2017:04:21:00:00:00:GMT,EO=716234,EL=657654,EH=808531,EN=757111}`

#### FUELINST: Instantaneous Generation by Fuel Type

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|FT   | decimal(10,2) | Fuel type  |   |   |
|FG   | decimal(10,2) | Total generation level  |  MW |  &nbsp; |

Example:

`2017:03:29:00:01:10:GMT: subject=BMRA.SYSTEM.FUELINST, message={TP=2017:03:29:00:00:00:GMT,SD=2017:03:29:00:00:00:GMT,SP=2,TS=2017:03:28:23:55:00:GMT,FT=CCGT,FG=10374}`

#### FUELHH: Half-hourly system-level generation by fuel type

| Fieldname | Datatype | Description | Units | Comments |
| --------- | -------- | ----------- | ----- | -------- |
|FT   | decimal(10,2) | Fuel type  |   |   |
|FG   | decimal(10,2) | Total generation level  |  MW |  &nbsp; |

Example:

`2017:03:29:00:01:10:GMT: subject=BMRA.SYSTEM.FUELHH, message={TP=2017:03:29:00:00:00:GMT,SD=2017:03:29:00:00:00:GMT,SP=2,FT=CCGT,FG=10418}`















## Balancing Party-Level Data

### Credit Data

#### CDN: Credit Default Notice
  Parameters:
    DL: Default Level, integer
    ED: Entered Default Settlement Date
    EP: Entered Default Settlement Period
    CD: Cleared Default Settlement Date (optional)
    CP: Cleared Default Settlement Period (optional)
    CT: Cleared Default Text (optional)

Example:

`2017:04:21:23:13:54:GMT: subject=BMRA.BP.GALENA.CDN, message={DL=2,ED=2017:04:22:00:00:00:GMT,EP=3}`


## INFO type messages

### Test Messages

#### TEST: Test message
  Parameters:
    DATA: message data

Example:

`2002:08:14:11:59:48:GMT: subject=BMRA.INFO.TEST, message={DATA=TEST - ignore}`
`2019:03:13:18:20:10:GMT: subject=BMRA.TEST, message={DATA=Test message}`

#### MSG: Test message
  Parameters:
    DATA: message data

Example:

`2002:10:08:16:11:05:GMT: subject=BMRA.INFO.MSG, message={DATA=This is a test message}`
