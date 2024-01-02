[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/release/myTselection/TotalEnergiesClubCard.svg)](https://github.com/myTselection/TotalEnergiesClubCard/releases)
![GitHub repo size](https://img.shields.io/github/repo-size/myTselection/TotalEnergiesClubCard.svg)

[![GitHub issues](https://img.shields.io/github/issues/myTselection/TotalEnergiesClubCard.svg)](https://github.com/myTselection/TotalEnergiesClubCard/issues)
[![GitHub last commit](https://img.shields.io/github/last-commit/myTselection/TotalEnergiesClubCard.svg)](https://github.com/myTselection/TotalEnergiesClubCard/commits/master)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/myTselection/TotalEnergiesClubCard.svg)](https://github.com/myTselection/TotalEnergiesClubCard/graphs/commit-activity)

# TotalEnergies Club card Home Assistant integration
[TotalEnergies Club card](https://services.totalenergies.be/nl/promoties/de-club-haal-het-meest-uit-uw-bezoek-onze-tankstations) Home Assistant custom component integration for Belgium. This custom component has been built from the ground up to bring TotalEnergies Club card site data into Home Assistant sensors in order to follow up on club card points and free road assist coverage period. This integration is built against the public website provided by TotalEnergies for Belgium and has not been tested for any other countries.

This integration is in no way affiliated with TotalEnergies. **Please don't report issues with this integration to TotalEnergies, they will not be able to support you.**

<p align="center"><img src="https://raw.githubusercontent.com/myTselection/TotalEnergiesClubCard/master/icon.png"/></p>


## Installation
- [HACS](https://hacs.xyz/): add url https://github.com/myTselection/TotalEnergiesClubCard as custom repository (HACS > Integration > option: Custom Repositories)
- Restart Home Assistant
- Add 'TotalEnergies Club Card' integration via HA Settings > 'Devices and Services' > 'Integrations'



## Integration
Device `TotalEnergies Club Card [cardnumber]` should become available with the following sensors:
- <details><summary><code>TotalEnergies Club Card Assistance [cardnr]</code> with indication of number of days the TotalEnergies Assistance is still available</summary>

	| Attribute | Description |
	| --------- | ----------- |
	| State     | Number of days the assistance coverage is valid |
	| `Assistance coverage `   | Date till when the assistance coverage will remain available |
	| `remaining days`   | Same as state |
	| `Card nr`   | Card number |

	</details>
- <details><summary><code>TotalEnergies Club Card Points [cardnr]</code> with number of points available on the TotalEnergies Club Card</summary>

	| Attribute | Description |
	| --------- | ----------- |
	| State     | Nr of points on TotalEngergies Club Card |
	| `Happy fuel card` | Indication of number of cards of 25€ and 15€ can be ordered with number of available points |
	| `Card nr`   | Card number |
	
	</details>
  
- <details><summary><code>TotalEnergies Club Card Transactions [cardnr]</code> with details on the last 10 transactions</summary>

	| Attribute | Description |
	| --------- | ----------- |
	| State     | Date of last transaction executed with the Club card |
	| `Assistance coverage` | Date till when the assistance coverage will remain available |
  | `Last transaction date` | Same a state |
  | `Transactions` | JSON with details of last transactions: date, location, number of points credited or debited |
	| `Card nr`   | Card number |
	
	</details>

## Status
Still some optimisations are planned, see [Issues](https://github.com/myTselection/TotalEnergiesClubCard/issues) section in GitHub.

## Technical pointers
The main logic and API connection related code can be found within source code Carbu.com/custom_components/Carbu.com:
- [sensor.py](https://github.com/myTselection/TotalEnergiesClubCard/blob/master/custom_components/TotalEnergiesClubCard/sensor.py)
- [utils.py](https://github.com/myTselection/TotalEnergiesClubCard/blob/master/custom_components/TotalEnergiesClubCard/utils.py) -> mainly ComponentSession class

All other files just contain boilerplat code for the integration to work wtihin HA or to have some constants/strings/translations.

If you would encounter some issues with this custom component, you can enable extra debug logging by adding below into your `configuration.yaml`:
```
logger:
  default: info
  logs:
     custom_components.totalenergiesclubcard: debug
```

## Example usage

<details><summary>Click to show the Mardown example</summary>

```
type: markdown
  content: >-
    {{states('sensor.totalenergies_club_card_assistance_[cardnr]')}} days
    Total Assistance coverage, till
    {{state_attr('sensor.totalenergies_club_card_assistance_[cardnr]','assistance_coverage')
    | as_timestamp| timestamp_custom("%a %d-%m-%Y")}}

    Points {{states('sensor.totalenergies_club_card_points_[cardnr]')}},
    {{state_attr('sensor.totalenergies_club_card_points_[cardnr]','happy_fuel_card')}}
  
```
</details>
