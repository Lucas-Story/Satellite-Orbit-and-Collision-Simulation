import sys
sys.path.append("C:\\Users\\lucas\\OneDrive\\Documents\\FreeFlyer\\FreeFlyer 7.9.1.11316767 (64-Bit)\\Runtime API\\python\\src")

from aisolutions.freeflyer.runtimeapi.RuntimeApiEngine import RuntimeApiEngine

class FreeFlyerAPI:

# can delete the imports and the type hint for engine, as it is only used so VS Code knows the type of engine
# and thus the VS Code linter works and can aid me during development
    def __init__(self, engine: RuntimeApiEngine, thrust_plan_path, collision_plan_path, staging_plan_RK89_path, staging_plan_SGP4_path, other_sats_TLE, my_sat_TLE):
        self.engine = engine
        self.thrust_plan_path = thrust_plan_path
        self.collision_plan_path = collision_plan_path
        self.staging_plan_RK89_path = staging_plan_RK89_path
        self.staging_plan_SPG4_path = staging_plan_SGP4_path
        self.other_sats_TLE = other_sats_TLE
        self.my_sat_TLE = my_sat_TLE

    def prepThrustFireMission(self, thrust_duration, sim_duration, dry_mass, prop_mass, thrust):
        self.engine.loadMissionPlanFromFile(self.thrust_plan_path)
        self.engine.prepareMissionPlan()

        self.engine.assignExpression("numSatellites", f"Satellites.LoadTLE(\"{self.other_sats_TLE}\")")
        self.engine.evaluateExpression(f"mySatellite1.LoadTLE(\"{self.my_sat_TLE}\",0)")
        self.engine.assignExpression("thrustDuration", f"{thrust_duration}")
        self.engine.assignExpression("simDuration", f"{sim_duration}")
        self.engine.assignExpression("mySatellite1.VehicleDryMass", f"{dry_mass}")
        self.engine.assignExpression("(mySatellite1.Tanks[0] AsType ElectricalTank).TankMass", f"{prop_mass}")
        if(thrust<0):
            self.engine.assignExpression("FiniteBurn1.BurnDirection", "{-1,0,0}")
            self.engine.assignExpression("(mySatellite1.Thrusters[0] AsType Thruster).ThrusterC1", f"{-thrust*(10**(-6))}")
        else:
            self.engine.assignExpression("(mySatellite1.Thrusters[0] AsType Thruster).ThrusterC1", f"{thrust*(10**(-6))}")

    def runMission(self):
        self.engine.executeRemainingStatements()

    def closeMission(self):
        self.engine.cleanupMissionPlan()

    def simulateThrusterFiring(self,thrust_duration,sim_duration,dry_mass,prop_mass,thrust):
        self.prepThrustFireMission(thrust_duration,sim_duration,dry_mass,prop_mass,thrust)
        self.runMission()

    def prepPotentialCollision(self, duration):
        self.engine.loadMissionPlanFromFile(self.collision_plan_path)
        self.engine.prepareMissionPlan()

        self.engine.evaluateExpression(f"mySatellite.LoadTLE(\"{self.my_sat_TLE}\",0)")
        self.engine.assignExpression("numSatellites", f"Satellites.LoadTLE(\"{self.other_sats_TLE}\")")
        self.engine.assignExpression("simDuration", f"{duration}")

    def simulatePotentialCollision(self, duration):
        self.prepPotentialCollision(duration)
        self.runMission()

    def prepStagingRK89(self, duration, stagingDV, stagingDM, wetMass):
        self.engine.loadMissionPlanFromFile(self.staging_plan_RK89_path)
        self.engine.prepareMissionPlan()

        self.engine.evaluateExpression(f"mySatellite.LoadTLE(\"{self.my_sat_TLE}\",0)")
        self.engine.assignExpression("numSatellites", f"Satellites.LoadTLE(\"{self.other_sats_TLE}\")")
        self.engine.assignExpression("stagingDV", f"{stagingDV}")
        self.engine.assignExpression("stagingDM", f"{stagingDM}")
        self.engine.assignExpression("simDuration", f"{duration}")
        self.engine.assignExpression("mySatellite.VehicleDryMass", f"{wetMass}")

    def simulateStagingRK89(self, duration, stagingDV, stagingDM, wetMass):
        self.prepStagingRK89(duration, stagingDV, stagingDM, wetMass)
        self.runMission()

    def prepStagingSGP4(self, duration, stagingDV, wetMass):
        self.engine.loadMissionPlanFromFile(self.staging_plan_SPG4_path)
        self.engine.prepareMissionPlan()

        self.engine.evaluateExpression(f"mySatellite.LoadTLE(\"{self.my_sat_TLE}\",0)")
        self.engine.assignExpression("numSatellites", f"Satellites.LoadTLE(\"{self.other_sats_TLE}\")")
        self.engine.assignExpression("stagingDV", f"{stagingDV}")
        self.engine.assignExpression("simDuration", f"{duration}")
        self.engine.assignExpression("mySatellite.VehicleDryMass", f"{wetMass}")

    def simulateStagingSGP4(self, duration, stagingDV,wetMass):
        self.prepStagingSGP4(duration, stagingDV, wetMass)
        self.runMission()


if __name__ == "__main__":
    pass
