# NOMAD Observation Planning Instructions
## Introduction
### Requirements
* SpiceyPy
* Python 3
* Various standard packages (numpy, os, sys, datetime, matplotlib)
* Xlsxwriter and xlrd

All the above are available on crunch7.



### Scripts

There are four scripts:


Script Name | Description
--- | ---
obs_config.py | Contains hardcoded paths to main directories to find e.g. cop tables, spice kernels, etc. Modify before running program (if required)
obs_functions.py | Contains the functions and calculations that do the obs planning. In general, do not modify unless there is a problem.
obs_inputs.py | Contains the information for all previous mtps and is where new information is to be added by the user for the upcoming mtps. E.g. observation types, mtp start/end times, regions of interest, lists of observation types to be added. Information must be added here before the script is run for a new mtp.
run_planning.py | This is the script to be run. In general, do not modify, except to set the correct MTP number


### Set up paths

If running on Windows, or if you are on Linux and prefer to run the planning in a directory other than the default, modify obs_config.py as required. There are five paths to be specified:


Variable name | Description
--- | ---
BASE_DIRECTORY | This is the directory containing the 4 scripts, and is where new orbit plans will be placed.
OBS_DIRECTORY | This is the base directory for the master version of the website. All input files must be placed here, and all output files, webpages and images will be generated here.
DEV_DIRECTORY | This is the base directory for the website, to be placed on the web dev server. A copy of all images and files will be made here.
COP_TABLE_DIRECTORY | This is the directory containing the cop table directories. Can be temporarily modified to a local folder for testing new cop table patches in the system.
KERNEL_DIRECTORY | This is the base directory containing up to date spice kernels. The subdirectories contain each type of kernel e.g. mk, ck, ik, etc. inside this directory.

The metakernel name, given by METAKERNEL_NAME, should be specified. This should always be em16_plan.tm for planning purposes.

### Linux servers

To run on crunch7, all the paths are already pointing to the default locations on the servers. The latest planning kernels will need to be downloaded as follows:

* cd /bira-iasb/projects/NOMAD/Science/Planning/kernels/
* git pull

This must be done before each MTP.

---

## Instructions for running

### Set up MTP and observation parameters

Add required information to obs_inputs for the mtp to be planned. Minimum required:


Variable Name | Description
--- | ---
mtpStart | This is the EXMGEO_TD2N start time as specified by Bojan or Claudio
mtpEnd | This is the EXMGEO_TD2N end time as specified by Bojan or Claudio
copVersion | This is the cop table folder for this MTP. Remember that after each patch is executed onboard, this must be updated to reflect the new COP rows.



Optional additions - modify the following parameters if desired:


Variable Name | Description
--- | ---
occultationObservationDict<br/>nadirObservationDict | These are the dictionaries of all known observation types, of the form:<br/>name:[[list of diffraction orders], integration time, rhythm, number of detector lines, channel]<br/>Where integration time is in milliseconds, rhythm is in seconds (usually 1 for occultation, 15 for nadir); the number of detector lines is usually 16 for occultation and 144 for nadir; and channel=0 for SO and 1 for LNO.<br/>These names are used in the final orbit plan.<br/>
occultationRegionsOfInterest<br/>nadirRegionsOfInterest | TBD
occultationRegionsObservations<br/>nadirRegionsObservations | TBD
USE_TWO_SCIENCES | TBD
OCCULTATION_KEYS<br>OCCULTATION_MERGED_KEYS<br>OCCULTATION_GRAZING_KEYS<br>NADIR_KEYS<br>NADIR_LIMB_KEYS<br>NADIR_NIGHTSIDE_KEYS | TBD




### Make generic orbit plan

In run_planning.py, change mtpNumber to the desired value. To start the planning script on crunch7:

* ssh -X crunch7
* module load 18/py36
* cd /bira-iasb/projects/NOMAD/Science/Planning/nomad_obs/
* python3 run_planning.py

Then wait a few minutes for the geometry calculations to be completed. 


Step 1 will be initiated, and the orbitList list will be populated with all the geometric data for the MTP
The generic orbit plan nomad_mtpxxx_plan_generic.xlsx will be placed in base directory. The generic script generally includes too many LNO dayside nadirs. Remove some by deleting some of the entries in the LNO dayside column (a blank entry means no observation will be run). Note that:

* If the observation corresponds to a region of interest, this will be indicated in the last column – it is better to keep these observations and remove others before/after to keep to the LNO 50% duty cycle. 
* Do not delete limbs.
* If a row has no SO or LNO observations, the orbit type in the 1st column must be changed to type 14.


LNO on average should have a 50% duty cycle i.e. half of all rows should be of type 4 or 14. See appendix A for more information.
See previous MTPs for examples. Send nomad_mtp015_plan_generic.xlsx to nomad.iops@aeronomie.be


### Finalise generic orbit plan

When the modified version is received from the OU, check for errors - e.g. remove observations that are not allowed, for example UVIS observations scheduled during OCMs. There are two types of UVIS nightsides, which will be highlighted in blue or yellow:

* Those in yellow are UVIS calibration measurements. If desired, LNO can run nightside measurements in these slots (change orbit type to 7 and add “irNightside” to irNightside column)
* Those in blue are UVIS nightside measurements. LNO and UVIS must be switched off on the previous orbit dayside (irDayside and uvisDayside must be blank), and LNO must not run on this nightside (irNightside must be blank). Note that observations on the dayside in the chosen orbit are acceptable.


For all nightsides, add “uvisNightside” to uvisNightside column if not present.




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








