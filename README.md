# DIM Loadout Archiver
*JoshUndefined*

## Purpose

Connect to Player's DIM account to pull raw data for DIM Loadouts, join with data from
D2 Manifest, and export a flat JSON file

## Usage

- Create directory data/
- Manually Save `manifest.db`
- Manually Save `dim-api_loadouts_[date-time].json`
- `python src/main.py`

## Roadmap

- [ ] Authorize with Bungie and DIM
- [ ] Check version and Download Manifest
- [ ] Get DIM Loadouts
- [x] Flatten loadouts with information from Manifest
- [ ] Get InstancedItem data
- [ ] Flatten InstancedItem into Loadouts