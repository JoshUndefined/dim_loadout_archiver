# DIM Loadout Archiver
*JoshUndefined*

## Purpose

Connect to Player's DIM account to pull raw data for DIM Loadouts, join with data from
D2 Manifest, and export a flat JSON file

In reality, this is actually a project for me to learn how to:

- Link parts of the Destiny API and Manifest
- Navigate and handle JSON with Python
- Just learn more about Python in general

## Usage

- Create directory data/
- Manually Save `manifest.db`
    - https://www.bungie.net/Platform/Destiny2/Manifest/
    - https://www.bungie.net/`{Response.mobileWorldContentPaths.en}`
    - Unzip downloaded file, rename as `data/manifest.db`
- Manually Save `dim-api_loadouts_[date-time].json`
    - In Postman->DIM API:
        - Refresh Bungie access token and save to Collection Vars
        - Refresh DIM access token and save to Collection Vars
        - GET GetLoadouts, save result to `data/` and update `main.py` filepath
- `python src/main.py`

## Roadmap

- [ ] Authorize with Bungie and DIM
    - Bungie auth working in v0.2.0
    [ ] Improve OAuth process with localstorage and auth code capture 
- [ ] Check version and Download Manifest
- [ ] Get DIM Loadouts
    - Currently using a manual download from DIM
- [x] Flatten loadouts with information from Manifest
- [x] Get InstancedItem data
- [x] Flatten InstancedItem into Loadouts