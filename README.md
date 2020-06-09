# NOMAD Observation Planning Instructions
## Introduction
### Requirements
* SpiceyPy
* Python 3
* Various standard packages (numpy, os, sys, datetime, matplotlib)
* Xlsxwriter and xlrd

All the above are available on crunch7.


### Directories

Within the base directory there are four directories

Directory Name | Description
--- | ---
`cop_patching` | Scripts to generate patches to the COP tables onboard NOMAD.
`nomad_obs` | Scripts to run the observation planning.
`observations` | Input and output files, website pages, etc.
`website` | Temporary website directory


### Scripts

To run the planning with the same settings are the previous MTP, only two scripts must be modified:
Script Name | Description
--- | ---
`run_planning.py` | (Unsurprisingly) this runs the planning. Here the `mtpNumber` must be changed to the current MTP.
`nomad_obs/mtp_inputs.py` | Info about all MTPs run so far. `mtpStart` and `mtpEnd` are the *EXMGEO_TD2N* and *EXMGEO_TD2N* times specified by Bojan or Claudio. `copVersion` is the COP table directory name used for this MTP. After each patch is executed onboard, this must be updated to reflect the new COP rows. If no patching has taken place this is the same as the previous MTP.



In addition, there are five scripts that can be modified if desired.
Script Name | Description
--- | ---
`acs_so_joint_occultations.py` | 
`observation_names.py` | Dictionaries of all user-defined observations, of the form:<br/>*name:[[list of diffraction orders], integration time, rhythm, number of detector lines, channel]*<br/>Where *integration time* is in milliseconds, *rhythm* is in seconds (usually 1 for occultation, 15 for nadir); the *number of detector lines* is usually 16 for occultation and 144 for nadir; and *channel* is 0 for SO and 1 for LNO.<br/>These names are used in the final orbit plan.<br/>Every observation must be included in the COP tables onboard NOMAD.
`observation_weights.py` | Select which observations are run for each observation type (nadir, occultation, etc.) and their weights i.e. the relative number of observations in relation to the other observation types.
`options.py` | Other user-modifiable options. In general do not change.
`regions_of_interest.py` | Add or modify the surface regions of interest defined by the science team for nadir or occultations observations.


There is a final script named `update_orbit_list.py`, which allows the user to override the SPICE geometry calculation for orbits in the MTP. In general this should not be done, except if there is a discrepancy between Bojan or Claudio's calculations and this planning software. This is described later.



### Observation planning general overview

When Bojan and Claudio distribute the MTP overview, the planning can begin. The general steps are outlined here:
1. Analyse geometry and inputs and create orbit plan, populating it with generic observation types e.g. _irIngress_, _irDayside_, etc.
2. Send to OU for iteration.
3. Finalise generic orbit plan and rerun script. This checks the plan is good and makes a list of orbits on which LNO operates. Send these outputs to Bojan and Claudio.
4. Populate the orbit plan with real observation names
5. Generate COP rows, web pages, update SQL database, etc. Generate list of joint ACS-NIR/NOMAD-SO occultation numbers for ESAC.
6. Following step (3), a few days later Bojan or Claudio will distribute the summary files. Check COP rows against these summary files.
7. Manually define solar calibrations.
8. When ready, send COP rows and joint NIR-SO file to Bojan and Claudio

Orbit type definitions can be found on the website: https://nomad.aeronomie.be/index.php/observations/observation-planning-orbit-rules

**All emails must be sent to `nomad.iops@aeronomie.be`**


### Set up paths

To run on crunch7, all the paths are already pointing to the default locations on the servers. If running on Windows, or if you are on Linux and prefer to run the planning in a directory other than the default, modify `nomad_obs/config/paths.py` as required. There are five paths to be specified:


Variable name | Description
--- | ---
`BASE_DIRECTORY` | The working directory, and where new orbit plans will be placed. 
`OBS_DIRECTORY` | Base directory for inputs and outputs. All input files must be placed here, and all output files, webpages and images will be generated here except new orbit plans.
`DEV_DIRECTORY` | Base directory for the website, to be placed on the web dev server. A copy of all images and files will be made here. The BIRA Linux compute servers cannot access the real directory, so they are placed in the temporary directory
`SQL_INI_DIRECTORY` | Directory containing the SQL database ini file (a copy of the inaccessible ini file in the website directory).
`COP_TABLE_DIRECTORY` | Directory containing the COP table directories. This can be temporarily modified to a local folder for testing new cop table patches in the system.
`KERNEL_DIRECTORY` | Directory containing the latest SPICE kernels. The subdirectories contain each type of kernel e.g. `mk`, `ck`, `ik`, etc. inside this directory.

The metakernel name, given by `METAKERNEL_NAME`, should be specified. This should always be `em16_plan.tm` for planning purposes.

`OFFLINE` should be set to True only if you are operating on a local machine that doesn't have access to the BIRA servers. In this mode, the SQL database is not updated.

---


## Instructions for running

### SPICE kernels

The latest planning kernels will need to be downloaded as follows:

* `cd /bira-iasb/projects/NOMAD/Science/Planning/kernels/`
* `git pull`

This must be done before each MTP.


### Set up MTP and observation parameters

* As a minimum, add `mtpStart`, `mtpEnd` and `copVersion` info to `nomad_obs/mtp_inputs` from the email from the Ops team.
* Update the other files in the `nomad_obs` directory if desired e.g. observations, weights, ACS-SO joint occultation types, regions of interest, etc.
* Copy the SOC event file `LEVF_Mxxx_SOC_PLANNING.EVF` for the MTP into the directory `observations/event_files`. This file can be found in the zip file from Bojan or Claudio.
* Copy the MRO overlap directories into `observations/summary_files/mtpxxx`. There are four: `2deg_latlon_15min_LST`, `2deg_latlon_30min_LST`, `5deg_latlon_15min_LST`, and `5deg_latlon_30min_LST`. From MTP030 onwards, the latter must be present for the pipeline to run.
* (Recommended) copy the solar limb events files `SOLAR_LOS/MARS_IN_UVIS_OCC_FOV.txt` and `SOLAR_LOS/MARS_IN_LNO_OCC_FOV.txt` from the zip file into `observations/summary_files/mtpxxx`. These will be needed later.


### Make generic orbit plan

In run_planning.py, change mtpNumber to the desired value. 

To start the planning script on crunch7 (from hera):

* `ssh -X crunch7`
* `module load 19g/py37` (if python 3 is not already loaded. Note that 18/py36 does not work at present)
* `cd /bira-iasb/projects/NOMAD/Science/Planning/nomad_obs/`
* `python3 run_planning.py`


Then wait a few minutes for the geometry calculations to be completed. The variable `orbitList` will be populated with all the geometric data for the MTP, and the generic orbit plan `nomad_mtpxxx_plan_generic.xlsx` will be placed in the `BASE_DIRECTORY`. 

One line in the orbit plan corresponds to a nightside followed by a dayside i.e. it starts at a day-to-night terminator and ends on the day-to-night terminator. One column in the orbit plan gives the night-to-day terminator crossing time, which is therefore at the mid-point of that orbit. Each orbit is 2 hours long, and so nightside observations will occur in the 1 hour before the night-to-day crossing time; and dayside nadirs/limbs will be measured within the hour after the night-to-day crossing time.


#### Select LNO dayside nadirs

The generic script always includes too many LNO dayside nadirs. Remove some by deleting some of the entries in the LNO dayside column (a blank entry means no observation will be run). Note that:

* The six columns of solar occultation observations should not be modified. 
* If the observation corresponds to a region of interest, the observation type and region will be indicated in the last column in the orbit plan e.g. `&daysideMatch:CURIOSITY;` means that the dayside nadir orbit passes near Gale Crater. It is better to keep most of these observations and remove others nearby; however it is not necessary to keep all. Priority should be given to Curiosity where possible.
* The number of observations to be deleted depends on the TGO orbit characteristics. See Appendix A for approximate duty cycles.
* Do not delete limbs e.g. dayside limb orbit type `28` or nightside limb type `47`.
* Every Saturday afternoon there is an OCM (orbit correction manoeuvre) where observations are not allowed. This is added automatically by the script and the orbit type is set to `14`. The text `&possibleOCM;` will be added to the last column.
* If a row has no occultations or LNO observations, the orbit type in the 1st column must be changed to type `14`:


orbitType | irIngressHigh | irIngressLow | uvisIngress | irEgressHigh | irEgressLow | uvisEgress | irDayside | uvisDayside
--- | --- | --- | --- | --- | --- | --- | --- | ---
14  |     |     |     |     |     |     |     | uvisDayside


==> New constraint for MTP029 onwards: LNO orbits should be preferentially chosen when TGO and MRO orbits overlap, so UVIS and MARCI can perform joint observations. These are given in file `observations/summary_files/mtpxxx/YYYY/TGO_AND_MRO_OVERLAP_IN_ONE_MTP_5deg.txt` where YYYY specifies the observational constraint. `2deg_latlon_15min_LST` contains the tightest (and best) constraints, but there are fewer joint observations as a result. These should be prioritised over `5deg_latlon_30min_LST`, which contains the loosest constraints, however as many should be matched as possible whilst trying the spread out LNO observations evenly between orbits. This is performed manually at present. 

* Orbit type `14` cannot include any LNO observations, so if a dayside nadir is added to a type `14` orbit to satisfy a TGO-MRO overlap, the orbit type must be changed to type `3`:

orbitType | irIngressHigh | irIngressLow | uvisIngress | irEgressHigh | irEgressLow | uvisEgress | irDayside | uvisDayside
--- | --- | --- | --- | --- | --- | --- | --- | ---
3   |     |     |     |     |     |     | irLongDayside | uvisDayside

* If the orbit type contains occultations, the dayside nadir can be kept or deleted without changing the orbit type. Both of these are valid:

orbitType | irIngressHigh | irIngressLow | uvisIngress | irEgressHigh | irEgressLow | uvisEgress | irDayside | uvisDayside
--- | --- | --- | --- | --- | --- | --- | --- | ---
1   | irIngressHigh | irIngressLow | uvisIngress | irEgressHigh | irEgressLow | uvisEgress | irShortDayside | uvisDayside
1   | irIngressHigh | irIngressLow | uvisIngress | irEgressHigh | irEgressLow | uvisEgress |   | uvisDayside


* There is no distinction between `irShortDayside`, `irDayside`, or `irLongDayside` at present.
* It is highly recommended that the orbits with type `3` and `14` are checked thoroughly (3 = irDayside, 14 = no irDayside), as errors can affect the UVIS observations on those orbits and/or may lead to problems later. Once the summary files are made this cannot be changed. <br/> This can be checked in Excel as follows `=IF(AND(A2=3,H2=""),"Error",0)` and `=IF(AND(A2=14,NOT(H2="")),"Error",0)` however care must be taken to delete all traces of additional columns. Columns `N` and onwards **must** be completely empty.


In general:

* Try to keep LNO on for the targeted observations
* Try to keep LNO on for the MRO overlaps
* LNO should always be switched on the orbit directly after an OCM
* When the solar incidence angle > 60 degrees, swap some H2O / CO observations for Surface Ice observations



**When ready, send `nomad_mtpxxx_plan_generic.xlsx` to `nomad.iops@aeronomie.be` for the OU to add UVIS observations.**


### Finalise generic orbit plan

When the modified version is received from the OU, check for errors - e.g. remove observations that are not allowed, for example UVIS observations scheduled during OCMs (orbital correction manoeuvres) which occur on Saturday afternoons. 



#### Check nightsides

Typically the only modification is to add UVIS nightside nadir observations. To keep the instrument as cool as possible, it is better that LNO dayside nadir observations are removed from the orbit before each UVIS nightside. This is not essential: regions of interest, MRO overlaps, etc. should not be cancelled. Since the LNO duty cycle is now <50%, NOMAD remains cold at all times and so this is less critical. LNO can run with UVIS on the occasional nightside - if so, change the orbit type to `7` and add `irNightside` to the `irNightside` column. Note that all observations on the dayside in the chosen orbit are unaffected, as the dayside observation always comes after the nightside observation. Note that LNO must not measure continuously - if there are LNO dayside measurements on the previous or same orbits, these must be removed (the `irDayside` column must be blank).

Optionally, add `uvisNightside` in the `uvisNightside` column if not present for all UVIS nightsides. 


#### Add LNO limb measurements

Orbits with types `4`, `14` and `3` can be changed to LNO limb orbit type `8`. These should correspond with CaSSIS off-nadir observations where possible, using the list `SOLAR_LOS/MARS_IN_LNO_OCC_FOV.txt` or `SOLAR_LOS/MARS_IN_UVIS_OCC_FOV.txt` provided by Bojan or Claudio. This txt file contains the times when the boresight is pointing closer to the ground than when flying in pure nadir-pointing mode. Each row in the orbit plan contains the night-to-day terminator crossing time - dayside limbs for that orbit will therefore take place within the 1 hour after the crossing time.

There are typically around 5 limb observations per MTP, however during periods without occultations it is possible to run many more (see Appendix A). 

At present, limb observations are added manually: To do this, change the orbit type to `8` and add `irLimb` to the `irDayside` column. 




### Make LNO orbit list file and final orbit plan

When the orbit plan is ready, move it to the directory `orbit_plans/mtpxxx` folder and run entire script again. The file containing the list of orbits where LNO is operating `nomad_mtpxxx_lno_orbits.txt` will be created in the orbit plan directory. **Send this and the generic orbit plan to `nomad.iops@aeronomie.be`.**


When the script is run above to make the joint observation list, the final orbit plan will also be created in the `BASE_DIRECTORY`. Here the table has been filled in with observation names taken from the lists in `observation_names.py` and `observation_weights.py`.


If there are no errors, place the final orbit plan in the `orbit_plans/mtpxxx` folder and run the entire script again. The output COP row files will be generated in `cop_rows/mtpxxx folder`. The joint occultation file `joint_occ_mtpxxx.csv` will also be created for the ACS team. When this is sent to Bojan or Claudio they will 



#### Compare to summary files

Once the final orbit plan is sent to Bojan and Claudio, they will generate the summary files, typically within a few days. Place a copy of all the .xlsx or .ods files in the directory `observations\summary_files\mtpxxx`.

The SO/LNO cop rows generated by the script should be compared to the summary files: particularly the number of rows in the file, and the *approximate* start and end times to check that the rows in the file line up correctly. Any rows in orange or red in the summary files should be set to `-1` in the corresponding COP row.

* `NOMAD_dayside_nadir_summary` should be compared to `mtpxxx_ir_dayside_nadir.txt`
* `NOMAD_egress_solar_occulations_summary` should be compared to `mtpxxx_ir_egress_occultations.txt`
* `NOMAD_grazing_solar_occulations_summary` should be compared to `mtpxxx_ir_grazing_occultations.txt`
* `NOMAD_ingress_and_merged_solar_occulations_summary` should be compared to `mtpxxx_ir_ingress_occultations.txt`
* `NOMAD_nightside_nadir_summary` should be compared to `mtpxxx_ir_nightside_nadir.txt`

See Appendix B if the number of COP rows does not match the number in the summary file.






#### Calibration file

The calibration file must be created manually as `cop_row/mtpxxx/mtpxxx_ir_calibrations.txt`. There are two types of solar calibration: *linescan* (to define the boresight vector) and *solar pointing* (to run fullscans or miniscans). 

If the calibration is a boresight linescan, use these values:
```
TC20 FIXED,TC20 PRECOOLING,TC20 SCI1,TC20 SCI2,LNO_OBSERVING (1=YES;0=NO),OBSERVATION NUMBER,OBSERVATION TYPE,APPROX TC START TIME,COMMENTS
1,1,2915,2915,0,-1,NONE,NONE,SO LINE SCAN SO BORESIGHT
```

Otherwise, use values from the `solar_calibrations.xlsx` file for miniscans/fullscans. See previous MTPs for examples. LNO fullscans are useful if it is not clear what to run:

```
TC20 FIXED,TC20 PRECOOLING,TC20 SCI1,TC20 SCI2,LNO_OBSERVING (1=YES;0=NO),OBSERVATION NUMBER,OBSERVATION TYPE,APPROX TC START TIME,COMMENTS
3,1,34,34,1,-1,NONE,NONE,LNO FULLSCAN
```
Note that the number and type (linescan or solar pointing) of calibration observations should match the number of calibrations in the MTP. This is given in the overview email from Bojan and Claudio.


#### COP rows

**Send all files in the `cop_row/mtpxxx` directory, including the `joint_occ_mtpxxx.csv` file to `nomad.iops@aeronomie.be`**. Make a new directory `cop_row/mtpxxx/sent` and copy all the sent files here. This will avoid overwriting the final COP rows if the pipeline is run again and something is changed.

When UVIS COP rows are provided by the OU, place them also in the `cop_row/mtpxxx` directory and rerun the pipeline. This will add the UVIS COP rows to the SQL database.





---

## Appendix

### Appendix A: LNO dayside nadir orbit selection

TGO orbits can be divided, approximately, into 3 categories:

Number of occultations | TGO orbit description | LNO nadir quality
--- | --- | ---
No occultations per orbit | TGO orbit is close to the terminator and does not pass behind the planet | **LNO signal is poor** due to bad solar zenith angle. Ices may be visible if orbit passes near sunrise terminator.
Merged/grazing or two occultations per orbit | TGO orbit is between subsolar point and terminator | **LNO signal is acceptable**, but instrument temperature is the highest.
One occultation per orbit | TGO orbit is close to subsolar/antisolar point | **LNO signal is good**, as solar zenith angle is low.


In general:
* If there are no occultations, LNO should operate on approximately *1 in 4* to *1 in 6* orbits. Approximately 25% of all LNO observations should be limb measurements (orbit type `8`).
* If there are two occultations per orbit, LNO should operate on approximately *1 in 3* or *1 in 4* orbits.
* If there is one occultation per orbit, LNO should operate on approximately *1 in 3* orbits. This happens when the spacecraft musted be flipped each orbit (low beta angle). Note that merged and grazing are counted as 2 orbits.

Note that LNO can also make limb and nightside observations - these must be taken into account when considered the number of LNO observations.


### Appendix B: Bugs and fixes

An error can occur when the occultation types defined by this planning software do not match those defined by Bojan and Claudio. In these cases, Bojan and Claudio's definition is always taken as correct and therefore the `orbitList` must be altered. This is normally clear if the number of rows in the output files `mtpxxx_ir_grazing_occultations.txt` and `mtpxxx_ir_ingress_occultations.txt` do not match the summary files.

Modifying the `orbitList` using the script `nomad_obs/update_orbit_list.py` to manually select the orbit number and occultation type. There are examples in the script already. 
