# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 09:55:27 2020

@author: iant

set start times for mtps. Note that program will stop if an observation is allowed at the given start time.
Start time must not be in an occultation and must be on nightside, prior to in ingress.
The first observation must be an Ingress (or merged/grazing if beta angle is high).
End time should be 2 orbits later than real MTP end to avoid discontinuties in planning.
First orbit must match with Bojan/Claudio. Don't generate an MTP plan and then delete/add the first line - change the start time instead!
Define a few extra observations and then delete them from the final observation plan.
CHECK START TIMES IN COSMOGRAPHIA OR SOC EVENT FILE

"""


def getMtpConstants(mtpNumber):

    def convertInputTimeStrings(timeString):
        from datetime import datetime, timedelta
        """convert input time strings to SPICE format and add a delta of a few minutes"""
        time = datetime.strptime(timeString, "%Y-%m-%dT%H:%M:%SZ")
        # start time must be a minute after passing from day to night. Bojan will specify which orbit to start on!
        # end time must be a minute after the end of the event file on the nightside
        delta = timedelta(minutes=1)
        newTime = time + delta
        utcString = datetime.strftime(newTime, '%Y %b %d %H:%M:%S')
        return utcString

    forbidden_dayside_orbits = []

    if mtpNumber == 0:
        mtpStart = ""  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = ""  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20180313_091700"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    if mtpNumber == 1:
        mtpStart = "2018-04-21T17:44:23Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2018-05-19T10:22:40Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20180313_091700"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 2:
        mtpStart = "2018-05-19T16:16:34Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2018-06-16T12:18:07Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20180313_091700"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 3:
        mtpStart = "2018-06-16T14:16:00Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2018-07-14T12:59:21Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20180616_110400"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 4:
        mtpStart = "2018-07-14T14:57:14Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2018-08-11T12:54:29Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20180714_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 5:
        mtpStart = "2018-08-11T14:52:26Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2018-09-08T13:13:43Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20180714_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 6:
        mtpStart = "2018-09-08T15:11:38Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2018-10-06T13:02:47Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20180714_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 7:
        mtpStart = "2018-10-06T15:00:39Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2018-11-03T12:01:05Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20181006_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

        """begin new obs planning software"""
    elif mtpNumber == 8:  # 2018-11-03T13:00:13Z (actually started orbit after:2018-11-03T14:58:06Z)     EXMGEO_TN2D - 2018-12-01T12:02:30Z     EXMGEO_TD2N
        mtpStart = "2018-11-03T14:58:06Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2018-12-01T12:02:30Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20181006_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 9:  # 2018-12-01T14:00:32Z EXMGEO_TD2N - 2018-12-29T12:14:53Z EXMGEO_TD2N
        mtpStart = "2018-12-01T14:00:32Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2018-12-29T12:14:53Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20181006_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 10:
        mtpStart = "2018-12-29T14:12:47Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-01-26T12:49:26Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20181229_113000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 11:
        mtpStart = "2019-01-26T14:47:51Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-02-23T12:49:34Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20181229_113000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 12:  # > EXMGEO_TD2N -  > EXMGEO_TD2N
        mtpStart = "2019-02-23T14:47:29Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-03-23T13:13:40Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20181229_113000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 13:
        mtpStart = "2019-03-23T15:11:46Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-04-20T13:16:29Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20190323_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 14:
        mtpStart = "2019-04-20T15:14:22Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-05-18T13:39:12Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20190323_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 15:
        mtpStart = "2019-05-18T15:37:10Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-06-15T11:37:56Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20190323_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 16:
        mtpStart = "2019-06-15T15:33:38Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-07-13T12:48:23Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20190323_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 17:
        mtpStart = "2019-07-13T14:46:20Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-08-10T12:57:59Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20190323_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 18:
        mtpStart = "2019-08-10T14:55:55Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-08-22T12:00:55Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20190323_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 19:
        mtpStart = "2019-09-14T16:36:17Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-10-05T13:48:59Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20190323_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 20:
        mtpStart = "2019-10-05T15:46:51Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-11-02T13:09:33Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20190323_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 21:
        mtpStart = "2019-11-02T15:07:25Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-11-30T13:15:03Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20191102_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 22:
        mtpStart = "2019-11-30T15:12:58Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-12-28T13:50:48Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20191102_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 23:
        mtpStart = "2019-12-28T15:48:47Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-01-25T12:11:37Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20191102_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 24:
        mtpStart = "2020-01-25T14:09:32Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-02-22T13:15:02Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20191102_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 25:
        mtpStart = "2020-02-22T15:12:59Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-03-21T13:26:01Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20200222_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 26:
        mtpStart = "2020-03-21T15:23:55Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-04-18T12:19:28Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20200222_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 27:
        mtpStart = "2020-04-18T14:17:29Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-05-16T12:37:22Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20200222_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 28:
        mtpStart = "2020-05-16T14:35:18Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-06-13T13:19:57Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20200222_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 29:
        mtpStart = "2020-06-13T15:17:54Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-07-11T13:34:20Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20200222_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 30:
        mtpStart = "2020-07-11T15:32:12Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-08-08T12:50:58Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20200222_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 31:
        mtpStart = "2020-08-08T14:48:51Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-09-05T13:02:23Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20200808_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 32:
        mtpStart = "2020-09-05T15:00:18Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-10-03T13:39:32Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20200808_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 33:
        mtpStart = "2020-10-03T15:37:27Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-10-31T13:51:51Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20200808_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 34:
        mtpStart = "2020-10-31T15:49:43Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-11-28T13:04:03Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20200808_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 35:
        mtpStart = "2020-11-28T15:01:57Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-12-26T13:17:21Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20200808_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 36:
        mtpStart = "2020-12-26T15:15:16Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2021-01-23T12:06:45Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20200808_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 37:
        mtpStart = "2021-01-23T14:04:40Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2021-02-20T12:23:57Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20200808_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 38:
        mtpStart = "2021-02-20T14:21:53Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2021-03-20T13:12:16Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20200808_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 39:
        mtpStart = "2021-03-20T15:10:09Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2021-04-17T13:22:21Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20210320_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 40:
        mtpStart = "2021-04-17T15:20:13Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2021-05-15T12:31:34Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20210320_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 41:
        mtpStart = "2021-05-15T14:29:28Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2021-06-12T12:46:38Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20210320_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 42:
        mtpStart = "2021-06-12T14:44:33Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2021-07-10T13:23:35Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20210320_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 43:
        mtpStart = "2021-07-10T15:21:28Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2021-08-07T13:32:59Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20210320_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 44:
        mtpStart = "2021-08-07T15:30:50Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2021-09-04T12:45:06Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20210320_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 45:
        mtpStart = "2021-09-04T14:50:07Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2021-10-01T11:28:57Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20210320_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 46:
        mtpStart = "2021-10-14T12:07:49Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2021-10-30T13:38:12Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20210320_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 47:
        mtpStart = "2021-10-30T15:36:08Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2021-11-27T13:52:44Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20210320_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 48:
        mtpStart = "2021-11-27T15:50:36Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2021-12-25T13:02:21Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20210320_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 49:
        mtpStart = "2021-12-25T15:00:16Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2022-01-22T13:10:17Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20210320_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 50:
        mtpStart = "2022-01-22T15:08:11Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2022-02-19T13:52:23Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20210320_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 51:
        mtpStart = "2022-02-19T15:50:30Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2022-03-19T12:18:00Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20220219_061000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 52:
        mtpStart = "2022-03-19T14:15:58Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2022-04-16T12:50:10Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20220219_061000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 53:
        mtpStart = "2022-04-16T14:48:16Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2022-05-14T13:17:13Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20220219_061000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 54:
        mtpStart = "2022-05-14T15:15:09Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2022-06-11T13:04:43Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20220219_061000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 55:
        mtpStart = "2022-06-11T15:02:07Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2022-07-09T12:40:18Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20220219_061000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 56:
        mtpStart = "2022-07-09T14:38:17Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2022-08-06T13:03:52Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20220219_061000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 57:
        mtpStart = "2022-08-06T15:01:55Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2022-09-03T13:32:29Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20220219_061000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 58:
        mtpStart = "2022-09-03T15:30:27Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2022-10-01T13:36:31Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20220219_061000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 59:
        mtpStart = "2022-10-01T15:34:13Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2022-10-29T12:52:33Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20220219_061000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 60:
        mtpStart = "2022-10-29T14:50:31Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2022-11-26T13:08:23Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20220219_061000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 61:
        mtpStart = "2022-11-26T15:06:26Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2022-12-24T13:54:34Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20220219_061000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 62:
        mtpStart = "2022-12-24T15:52:32Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2023-01-21T12:12:26Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20220219_061000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 63:
        mtpStart = "2023-01-21T14:10:28Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2023-02-18T12:58:24Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20220219_061000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 64:
        mtpStart = "2023-02-18T14:56:24Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2023-03-18T13:08:07Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20230218_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 65:
        mtpStart = "2023-03-18T15:06:04Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2023-04-15T12:20:44Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20230218_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 66:
        mtpStart = "2023-04-15T14:18:38Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2023-05-13T12:29:57Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20230218_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [6, 18, 24, 37, 85, 86, 133, 134, 145, 146, 171, 173, 174, 180, 215, 243, 244,  256, 257, 282, 286, 287, 317, 318, 332, 333]
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 67:
        mtpStart = "2023-05-13T14:27:55Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2023-06-10T13:02:30Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20230218_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [37, 45, 63, 64, 68, 69, 85, 86, 88, 89, 171, 254, 256, 257, 262, 268]  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 68:
        mtpStart = "2023-06-10T15:00:32Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2023-07-08T13:20:26Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20230218_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [85, 86, 134, 158, 171, 183, 210, 222, 234, 256, 257, 261, 284, 292, 331]  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 69:
        mtpStart = "2023-07-08T15:18:23Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2023-08-05T12:54:02Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20230218_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [15, 30, 42, 59, 94, 85, 86, 120, 129, 171,  237, 243,
                                    249, 252, 256, 257, 265, 270, 271, 305, 306, 312]  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 70:
        mtpStart = "2023-08-05T14:51:48Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2023-09-02T12:44:37Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20230218_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [6, 18, 31, 43, 85, 86, 122, 140, 171, 178, 190, 226, 243,
                                    244, 256, 257, 274, 275, 301, 302, 313, 314, 336, 337]  # input these from the email
        required_dayside_orbits = []
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 71:
        mtpStart = "2023-09-02T14:42:32Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2023-09-30T13:07:32Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20230218_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [6, 25, 41, 76, 85, 86, 89, 116, 157, 166, 171, 178, 181, 193, 256, 257]  # input these from the email
        required_dayside_orbits = [204, 241, 254, 266, 267, 278, 279, 303, 306, 307, 316, 332]
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 72:
        mtpStart = "2023-09-30T15:05:34Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2023-10-28T13:38:35Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20230218_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [6, 41, 53, 85, 86, 171, 207, 225, 236, 237, 248, 256, 257, 260, 261, 291, 292, 327]  # input these from the email
        required_dayside_orbits = [37]  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 73:
        mtpStart = "2023-10-28T15:36:31Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2023-11-08T11:03:13Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20231028_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [5, 54, 55, 69, 70, 85, 86, 96, 101, 109]  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 74:
        mtpStart = "2023-11-29T00:28:35Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2023-12-23T12:53:36Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20231028_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [43, 44, 129, 183, 189, 190, 195, 211, 214, 215, 225, 263, 264, 273, 274, 289]  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 600  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 75:
        mtpStart = "2023-12-23T14:51:28Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2024-01-20T13:04:32Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20231028_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [50, 51, 62, 85, 86, 90, 128, 151, 171, 209, 256, 257, 270, 274, 293, 309, 310]  # input these from the email
        required_dayside_orbits = [294, 316, 319, 320]  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 440  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 76:
        mtpStart = "2024-01-20T15:02:28Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2024-02-17T12:03:50Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20231028_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [8, 9, 48, 66, 72, 73, 85, 86, 109, 110, 131, 143, 161, 171, 174, 175,
                                    178, 179, 188, 206, 256, 257, 279, 280, 287, 288, 318, 319, 337]  # input these from the email
        required_dayside_orbits = [12, 62, 74]  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 440  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 77:
        mtpStart = "2024-02-17T14:01:42Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2024-03-16T12:19:06Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20231028_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [6, 7, 31, 32, 46, 47, 51, 52, 55, 56, 85, 86, 107, 108, 138, 139, 144, 145, 162, 163, 169, 170, 171,
                                    179, 180, 185, 186, 200, 201, 231, 232, 249, 250, 256, 257, 288, 289, 294, 295, 305, 306, 319, 320]
        # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 440  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 78:
        mtpStart = "2024-03-16T14:17:01Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2024-04-13T12:59:13Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20231028_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [85, 86, 121, 139, 150, 151, 162, 166, 171, 175, 176, 179, 180, 184,
                                    185, 189, 194, 195, 256, 257, 325, 326, 330, 332, 333, 338, 339]  # input these from the email
        required_dayside_orbits = [6, 7, 43, 47, 81]  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 440  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 79:
        mtpStart = "2024-04-13T14:57:06Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2024-05-11T13:08:36Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20231028_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [6, 23, 45, 57, 75, 85, 86, 99, 100, 111, 118, 119, 169, 170, 171, 173, 174, 188,
                                    225, 231, 232, 243, 244, 249, 256, 257, 262, 301, 302, 305, 306, 336, 337]  # input these from the email
        required_dayside_orbits = [203, 239, 300, 325]  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 440  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 80:
        mtpStart = "2024-05-11T15:06:27Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2024-06-08T12:27:46Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20231028_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [7, 13, 30, 46, 47, 85, 86, 92, 122, 140, 141, 152, 153, 158, 159, 171, 183, 184,
                                    195, 201, 226, 241, 242, 256, 257, 307, 308, 311, 312, 329, 334, 335, 338]  # input these from the email
        required_dayside_orbits = [16, 25, 50, 63, 75, 99, 124]  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 440  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 81:
        mtpStart = "2024-06-08T14:25:37Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2024-07-06T12:37:50Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20231028_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [4, 39, 40, 70, 71, 78,  83, 85, 86, 90, 99, 113, 114, 115, 144, 145,
                                    171, 176, 195, 201, 226, 256, 257, 263, 269, 286, 288, 338]  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 440  # seconds required for precooling
        stp_data_volumes = [43, 43, 43, 43]  # GBit # add if required

    elif mtpNumber == 82:
        mtpStart = "2024-07-06T14:35:44Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2024-08-03T13:15:11Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20231028_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [2, 3, 5, 6, 9, 10, 85, 86, 157, 158, 163, 164, 169, 171, 175, 177, 183, 189, 256, 257]  # input these from the email
        required_dayside_orbits = [7, 20, 57, 82, 94]  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 440  # seconds required for precooling
        stp_data_volumes = [57, 57, 57, 57]  # GBit # add if required

    elif mtpNumber == 83:
        mtpStart = "2024-08-03T15:13:07Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2024-08-31T13:29:30Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20231028_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [21, 22, 26, 42, 65, 85, 86, 88, 99, 111, 127, 157, 171,
                                    176, 189, 246, 252, 256, 257, 263, 268, 280, 298, 337]  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 440  # seconds required for precooling
        stp_data_volumes = [58, 58, 58, 58]  # GBit # add if required

    elif mtpNumber == 84:
        mtpStart = "2024-08-31T15:27:22Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2024-09-28T12:36:19Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20231028_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [33, 34, 85, 86, 138, 139, 114, 120, 148, 160, 171, 183, 195,
                                    207, 213, 225, 255, 256, 271, 272, 283, 289, 295, 331, 332]  # input these from the email
        required_dayside_orbits = [25, 29, 38, 50, 63, 76, 79, 88, 100, 112, 116, 137, 141, 150,
                                   150, 162, 163]  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 440  # seconds required for precooling
        stp_data_volumes = [70, 70, 70, 70]  # GBit # add if required

    elif mtpNumber == 85:
        mtpStart = "2024-09-28T14:34:15Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2024-10-26T12:45:21Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20231028_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [39, 40, 62, 71, 76, 77, 78, 79, 85, 86, 91, 97, 108, 109, 132,
                                    133, 152, 153, 171, 182, 184, 185, 195, 215, 256, 257, 331]  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 440  # seconds required for precooling
        stp_data_volumes = [70, 70, 70, 70]  # GBit # add if required

    elif mtpNumber == 86:
        mtpStart = "2024-10-26T14:43:15Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2024-11-23T13:35:12Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20231028_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [26, 27, 65, 66, 71, 72, 85, 86, 171, 183, 184, 196, 208, 238, 256, 257, 309, 320, 332, 336]  # input these from the email
        required_dayside_orbits = [32, 70, 95, 97, 107, 144, 155, 169, 180, 231]  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 440  # seconds required for precooling
        stp_data_volumes = [70, 0, 70, 70]  # GBit # add if required

    elif mtpNumber == 87:
        mtpStart = "2024-11-23T15:33:14Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2024-12-21T13:52:48Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20231028_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [40, 41, 42, 68, 74,  85, 86, 115, 116, 126, 127, 165, 166, 171, 204,
                                    205, 256, 257, 196, 234, 239, 240, 289, 301, 313, 318, 319]  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 440  # seconds required for precooling
        stp_data_volumes = [70, 70, 70, 70]  # GBit # add if required

    elif mtpNumber == 88:
        mtpStart = "2024-12-21T15:50:43Z"  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2025-01-18T12:28:04Z"  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20231028_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = [46, 47, 58, 59, 70, 82, 83,  85, 86, 95, 96, 114, 115, 134,
                                    170,  248, 249, 252, 253,  255, 256, 280, 305, 327, 338]  # input these from the email
        # add if LNO needs to operate on certain orbits e.g. joint observations
        required_dayside_orbits = [187, 213, 216, 225, 241, 262, 275, 287, 288, 299, 328]
        occultation_precooling = 440  # seconds required for precooling
        stp_data_volumes = [70, 70, 70, 70]  # GBit # add if required

    elif mtpNumber == 89:
        mtpStart = ""  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = ""  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20231028_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 440  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    elif mtpNumber == 90:
        mtpStart = ""  # EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = ""  # EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20231028_120000"  # desired cop table folder - remember to update if patched
        forbidden_dayside_orbits = []  # input these from the email
        required_dayside_orbits = []  # add if LNO needs to operate on certain orbits e.g. joint observations
        occultation_precooling = 440  # seconds required for precooling
        stp_data_volumes = []  # GBit # add if required

    # add corrections for certain changes in planning since beginning of mission
    mappsEventFilename = "LEVF_M%03d_SOC_PLANNING.EVF" % mtpNumber
    if mtpNumber < 13:
        acsStartAltitude = 250  # km
    else:
        acsStartAltitude = 200  # km

    if mtpNumber == 2:
        soCentreDetectorLine = 130  # boresight corrected by moving detector readout region
    elif mtpNumber in [3, 4]:
        soCentreDetectorLine = 131  # detector readout region improved
    else:
        soCentreDetectorLine = 128  # boresight corrected from MTP005 onwards

    # convert input times if given, if not leave blank and throw error in main script asking for inputs
    if mtpStart != "":
        utcstringStart = convertInputTimeStrings(mtpStart)
    else:
        utcstringStart = ""

    if mtpEnd != "":
        utcstringEnd = convertInputTimeStrings(mtpEnd)
    else:
        utcstringEnd = ""

    mtpConstantsDict = {"mtpNumber": mtpNumber,
                        "utcStringStart": utcstringStart,
                        "utcStringEnd": utcstringEnd,
                        "copVersion": copVersion,
                        "mappsEventFilename": mappsEventFilename,
                        "soCentreDetectorLine": soCentreDetectorLine,
                        "acsStartAltitude": acsStartAltitude,
                        "forbidden_dayside_orbits": forbidden_dayside_orbits,
                        "required_dayside_orbits": required_dayside_orbits,
                        "occultation_precooling": occultation_precooling,
                        "stp_data_volumes": stp_data_volumes,
                        }

    return mtpConstantsDict
