from GUI import GraphicUserInterface
from GUI import ControlFrame

from FFAPI import FreeFlyerAPI
from STAPI import SpaceTrackAPI

import os

import sys
sys.path.append("C:\\Users\\lucas\\OneDrive\\Documents\\FreeFlyer\\FreeFlyer 7.9.1.11316767 (64-Bit)\\Runtime API\\python\\src")

from aisolutions.freeflyer.runtimeapi.RuntimeApiEngine import RuntimeApiEngine
from aisolutions.freeflyer.runtimeapi.WindowedOutputMode import WindowedOutputMode
from aisolutions.freeflyer.runtimeapi.ConsoleOutputProcessingMethod import ConsoleOutputProcessingMethod

# using with statement to ensure engine is always properly disposed of, even if an exception occurs
with RuntimeApiEngine(os.getenv("FREEFLYER_64_INSTALL_DIRECTORY"), windowedOutputMode=WindowedOutputMode.GenerateOutputWindows, consoleOutputProcessingMethod=ConsoleOutputProcessingMethod.RedirectToRuntimeApi) as engine:
    # variables subject to change
    thrust_plan_path = "C:\\Users\\lucas\\Free Flyer\\Simulate (Thrusters On).MISSIONPLAN"
    collision_plan_path = "C:\\Users\\lucas\\Free Flyer\\Simulate (Thrusters Off).MISSIONPLAN"
    staging_plan_RK89_path = "C:\\Users\\lucas\\Free Flyer\\Simulate (Staging Event RK89).MISSIONPLAN"
    staging_plan_SGP4_path = "C:\\Users\\lucas\\Free Flyer\\Simulate (Staging Event SGP4).MISSIONPLAN"
    other_sats_TLE = "other_sats.tle" # this .tle must be in the same folder as the mission plans
    my_sat_TLE = "my_sat.tle" # this .tle must be in the same folder as the mission plans
    space_track_username = "ljstory@mit.edu"
    space_track_password = "SpacePropulsionLab"
    update_other_3LEs_path = "/basicspacedata/query/class/gp/EPOCH/>now-7/PERIAPSIS/1--500/orderby/EPOCH/format/3le"
    default_NORAD_ID = "25544"  # 25544 is the NORAD_ID for the ISS
    default_thrust_duration = 0.01  # days (must be less than or equal to default_sim_duration)
    default_sim_duration = 0.01 # days
    default_staging_DV = 0.01  # m/s
    default_staging_DM = -0.1  # g
    default_wet_mass = 5.0 # kg
    default_thrust = 2 # micro N (cannot be equal to 0, but can be positive or negative)
    lock_screen = False  # boolean determines whether or not to include a lock screen
    application_password = "KRONOS"
    other_TLE_path = r"C:\Users\lucas\Free Flyer\other_sats.tle"
    my_TLE_path = r"C:\Users\lucas\Free Flyer\my_sat.tle"

    # bootstrapping application
    gui = GraphicUserInterface()
    freeFlyer = FreeFlyerAPI(engine,thrust_plan_path, collision_plan_path, staging_plan_RK89_path, staging_plan_SGP4_path, other_sats_TLE, my_sat_TLE)
    space_track = SpaceTrackAPI(space_track_username, space_track_password, update_other_3LEs_path)
    ControlFrame(gui,freeFlyer,space_track, other_TLE_path, my_TLE_path, default_thrust_duration, default_sim_duration, default_staging_DV, default_staging_DM, default_NORAD_ID, default_wet_mass, default_thrust, lock_screen, application_password)
    gui.mainloop()
