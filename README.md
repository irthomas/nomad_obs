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
`nomad_obs/mtp_inputs.py` | Info about all MTPs run so far. `mtpStart` and `mtpEnd` are the EXMGEO_TD2N and EXMGEO_TD2N times specified by Bojan or Claudio. `copVersion` is the COP table directory name used for this MTP. After each patch is executed onboard, this must be updated to reflect the new COP rows. If no patching has taken place this is the same as the previous MTP.



In addition, there are five scripts that can be modified if desired.
Script Name | Description
--- | ---
`acs_so_joint_occultations.py` | 
`observation_names.py` | Dictionaries of all user-defined observations, of the form:<br/>name:[[list of diffraction orders], integration time, rhythm, number of detector lines, channel]<br/>Where integration time is in milliseconds, rhythm is in seconds (usually 1 for occultation, 15 for nadir); the number of detector lines is usually 16 for occultation and 144 for nadir; and channel=0 for SO and 1 for LNO.<br/>These names are used in the final orbit plan.<br/>Every observation must be included in the COP tables onboard NOMAD.
`observation_weights.py` | Select which observations are run for each observation type (nadir, occultation, etc.) and their weights i.e. the relative number of observations in relation to the other observation types.
`options.py` | Other user-modifiable options. In general do not change.
`regions_of_interest.py` | Add or modify the surface regions of interest defined by the science team for nadir or occultations observations.


There is a final script named `update_orbit_list.py`, which allows the user to override the SPICE geometry calculation for orbits in the MTP. In general this should not be done, except if there is a discrepancy between Bojan or Claudio's calculations and this planning software. This is described later.



### Observation planning general overview

When Bojan and Claudio distribute the MTP overview, the planning can begin. The general steps are outlined here:
1. Analyse geometry and inputs and create orbit plan, populating it with generic observation types e.g. _irIngress_, _irDayside_, etc.
2. Send to OU for iteration.
3. Finalise generic orbit plan and send to Bojan and Claudio, along with list of orbits on which LNO operates.
4. Populate the orbit plan with real observation names
5. Generate COP rows, web pages, update SQL database, etc. Generate list of joint ACS-NIR/NOMAD-SO occultation numbers for ESAC.
6. Following step (3), a few days later Bojan or Claudio will distribute the summary files. Check COP rows against these summary files.
7. Manually define solar calibrations.
8. When ready, send COP rows and joint NIR-SO file to Bojan and Claudio

Orbit type definitions can be found on the website: https://nomad.aeronomie.be/index.php/observations/observation-planning-orbit-rules

All emails must be sent to `nomad.iops@aeronomie.be`


### Set up paths

To run on crunch7, all the paths are already pointing to the default locations on the servers. If running on Windows, or if you are on Linux and prefer to run the planning in a directory other than the default, modify `nomad_obs/config/paths.py` as required. There are five paths to be specified:


Variable name | Description
--- | ---
`BASE_DIRECTORY` | The working directory, and where new orbit plans will be placed. 
`OBS_DIRECTORY` | Base directory for inputs and outputs. All input files must be placed here, and all output files, webpages and images will be generated here except new orbit plans.
`DEV_DIRECTORY` | Base directory for the website, to be placed on the web dev server. A copy of all images and files will be made here. The BIRA Linux compute servers cannot access the real directory, so they are placed in the temporary directory
`SQL_INI_DIRECTORY` | Directory containing the SQL database ini file (a copy of the inaccessible ini file in the website directory).
`COP_TABLE_DIRECTORY` | Directory containing the COP table directories. This can be temporarily modified to a local folder for testing new cop table patches in the system.
`KERNEL_DIRECTORY` | Directory containing the latest SPICE kernels. The subdirectories contain each type of kernel e.g. mk, ck, ik, etc. inside this directory.

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

* As a minimum, add `mtpStart`, `mtpEnd` and `copVersion` info to `nomad_obs/mtp_inputs`
* Update the other files in the `nomad_obs` directory if desired e.g. observations, weights, ACS-SO joint occultation types, regions of interest, etc.
* Copy the SOC event file `LEVF_Mxxx_SOC_PLANNING.EVF` for the MTP into the directory `observations/event_files`. This file can be found in the zip file from Bojan or Claudio.
* (Recommended) copy the solar limb events file `MARS_IN_UVIS_OCC_FOV.txt` and MRO joint obs from the zip file into `observations/summary_files/mtpxxx`. These will be needed later.



### Make generic orbit plan

In run_planning.py, change mtpNumber to the desired value. 

To start the planning script on crunch7 (from hera):

* `ssh -X crunch7`
* `module load 18/py36` (if python 3 is not already loaded)
* `cd /bira-iasb/projects/NOMAD/Science/Planning/nomad_obs/`
* `python3 run_planning.py`

Then wait a few minutes for the geometry calculations to be completed. The variable `orbitList` will be populated with all the geometric data for the MTP, and the generic orbit plan `nomad_mtpxxx_plan_generic.xlsx` will be placed in the `BASE_DIRECTORY`. 


#### Select LNO dayside nadirs

The generic script always includes too many LNO dayside nadirs. Remove some by deleting some of the entries in the LNO dayside column (a blank entry means no observation will be run). Note that:

* If the observation corresponds to a region of interest, this will be indicated in the last column – it is better to keep most of these observations and remove others before/after to keep to the LNO 50% duty cycle. It is not necessary to keep all.
* Do not delete limbs.
* If a row has no SO or LNO observations, the orbit type in the 1st column must be changed to type 14.


LNO on average should have a 50% duty cycle i.e. half of all rows should be of type 4 or 14. See appendix A for more information.
See previous MTPs for examples. Send nomad_mtp015_plan_generic.xlsx to 


### Finalise generic orbit plan

When the modified version is received from the OU, check for errors - e.g. remove observations that are not allowed, for example UVIS observations scheduled during OCMs. There are two types of UVIS nightsides, which will normally be highlighted in blue or yellow:

* Those in yellow are UVIS calibration measurements. If desired, LNO can run nightside measurements in these slots (change orbit type to 7 and add “irNightside” to irNightside column)
* Those in blue are UVIS nightside measurements. LNO and UVIS must be switched off on the previous orbit dayside (irDayside and uvisDayside must be blank), and LNO must not run on this nightside (irNightside must be blank). Note that observations on the dayside in the chosen orbit are acceptable.


For all nightsides (of both types), add “uvisNightside” to uvisNightside column if not present.




#### Additional LNO limb measurements

Orbits with types 4, 14 and 3 can be changed to LNO limb. These should correspond with CaSSIS off-nadir observations where possible, using the list provided by the ops team. This allows measurements to be made when the boresight is pointing closer to the ground than when flying in pure nadir-pointing mode. To do this, change the orbit type to “8” and add “irLimb” to the irDayside column. Note that nightside limbs are not yet implemented. Remember that LNO should not measure continuously - if there are LNO measurements on previous/next orbits these should be removed (by setting irDayside column blank).



#### Additional LNO nightside measurements

If desired.



#### Targeted observations

Check targeted nadir: 
Curiosity (134/136)
Francesca surface hydration sites (191)
Add more CH4 release sites (134/136)


### Make LNO-UVIS joint observation list

Place the new generic orbit plan file in the orbit_plans/mtpxxx folder and run entire script again. The LNO-UVIS joint observation file will be created in the orbit plan directory. Send this and the generic orbit plan to nomad.iops


### Make final files
If all is ok then place generic orbit plan in the orbit_plans/mtpxxx folder and run entire script again

The final orbit plan will be placed in base directory.
If there are no errors, place the final orbit plan in the orbit_plans/mtpxxx folder and run the entire script again.
The output COP row files will be generated in cop_rows/mtpxxx folder:
This and the other ir cop rows should be checked (compare to summary files from bojan/claudio), particularly timings and number of rows in files
LNO occultations are implemented. In the 5th column, 0 is changed to 1.

The joint occultation file is created for the ACS team. This will be sent by bojan/claudio to the soc.


#### Calibration file
The calibration file must be filled in manually. Use values from solar_calibrations.xlsx file for miniscans/fullscans. See previous mtps for examples.

Send all files in the cop_row/mtpxxx folder to nomad.iops@aeronomie.be

Rerun when UVIS COP rows are ready


#### Update website (not working on crunch)
* Run step5
* Then log in to Tethys, change directory to “/bira-iasb/websites/dev/mars>”
* Then run  “./sync_to_prod.sh”



#### Important things to remember:
* 1st observation after OCM slot should always be LNO+UVIS to keep instrument warm
* Check all orbit type 28 have been added for LNO+UVIS limbs



Remember to check what calibrations there are, and send calibration COP rows separately!



Add manually to comment section where required:
&PDHUMaintenanceSlot


---

## Appendix A: Typical orbit plans
The TGO orbit can be divided, approximately, into 3 categories:

* Periods where there are no occultations (due to high beta angle)
* Periods with short occultations, typically either ingress or egress in one orbit
* Periods with long or multiple occultations in the same orbit
The temperature of NOMAD is lowest in case (1) and highest in case (3) and so this must be offset by running the appropriate number of LNO observations. The script, in general, tends to place too many LNO nadirs during the periods where occultations are prevalent and not enough nadirs when there are no occultations.








