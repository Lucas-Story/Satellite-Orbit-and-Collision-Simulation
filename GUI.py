from FFAPI import FreeFlyerAPI
from STAPI import SpaceTrackAPI
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

PROP_MASS = 0.05


class GraphicUserInterface(tk.Tk):

    def __init__(self):
        super().__init__()

        # sets window size
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()-80
        root_width = int(self.screen_width/2)
        root_height = int(self.screen_height)
        root_x = -8
        root_y = 0
        self.geometry(f"{root_width}x{root_height}+{root_x}+{root_y}")

        self.title("STEP-1 Orbit and Collision Modeling (prototype)")
        self.iconbitmap("./assets/SPLLogo.ico")

    def shrinkWindow(self):
        root_width = 220
        root_height = 440
        root_x = self.screen_width - 230
        root_y = int(self.screen_height/1.5) - 65
        self.geometry(f"{root_width}x{root_height}+{root_x}+{root_y}")

        # essentailly an "update display" command (note: do not use update(), can cause issues)
        # required here because otherwise the window won't update until after the root/source function call is completed,
        # and since this function is called from the same function that later launches FreeFlyer, that will launch and run
        # before the window is updated, so this manual display update here is needed for the Tkinter window to resize first
        self.update_idletasks()

    def growWindow(self):
        root_width = int(self.screen_width/2)
        root_height = int(self.screen_height)
        root_x = -8
        root_y = 0
        self.geometry(f"{root_width}x{root_height}+{root_x}+{root_y}")



# note: ordering of classes does actually matter here, because if ControlFrame is below MainFrame, the type hint in the constructor
# for MainFrame won't recognize that ControlFrame is a class, because it is created below it.
# (for some reason this applies only in the function definition line, as it will be recognized inside the function itself)
class ControlFrame(ttk.Frame):

    def __init__(self,container: GraphicUserInterface, freeflyer: FreeFlyerAPI, space_track: SpaceTrackAPI, other_TLE_path, my_TLE_path, default_thrust_duration, default_sim_duration, default_staging_DV, default_staging_DM, default_NORAD_ID, default_wet_mass, default_thrust, lock_screen, application_password):
        super().__init__(container)

        self.container = container

        self.freeflyer = freeflyer

        self.lock_screen = lock_screen

        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=3, uniform="row")
        self.rowconfigure(1,weight=45, uniform="row")
        self.rowconfigure(2,weight=45, uniform="row")
        self.rowconfigure(3,weight=3, uniform="row")
        self.rowconfigure(4,weight=3, uniform="row")

        # instantiate other frames
        self.cover_frame = CoverFrame(self)
        self.lock_frame = LockFrame(self, application_password)
        self.main_frame = MainFrame(self,freeflyer,space_track, other_TLE_path, my_TLE_path, default_thrust_duration, default_sim_duration, default_staging_DV, default_staging_DM, default_NORAD_ID, default_wet_mass, default_thrust)
        self.title_frame = TitleFrame(self)


        self.close_mission_button = ttk.Button(self,text="Close Simulation", command=self.closeMissionHandler)

        self.return_to_lock_screen_button = ttk.Button(self,text="Return to Lock Screen",command=self.returnToLockScreenHandler)

        if lock_screen:
            self.return_to_lock_screen_button.grid(row=3,column=0)

        self.close_application_button = ttk.Button(self,text="Close Application", command=self.closeApp)
        self.close_application_button.grid(row=4,column=0)

        self.place(relheight=1,relwidth=1,relx=0,rely=0,anchor="nw")

        self.lock_frame.passwordFocus()

        if lock_screen:
            self.lock_frame.tkraise()


    def closeMissionHandler(self):

        # this lowering order is important
        # using lower and not tkraise because ControlFrame's children need to be in a "lowered" state and not a "tkraised" state in order for ControlFrame's widgets to show through their backgrounds
        # when children are tkriased, they raise their backgrounds above their parents widgets, and so they need to then be relowered in order to get the parent's widgets back above their childrens' backgrounds
        self.main_frame.lower()
        self.title_frame.lower()
        self.lock_frame.lower()
        self.cover_frame.lower()

        self.title_frame.showImages()

        self.container.growWindow()
        self.freeflyer.closeMission()
        self.close_application_button.grid_forget()
        self.close_application_button.grid(row=4,column=0)
        self.close_mission_button.grid_forget()
        if self.lock_screen:
            self.return_to_lock_screen_button.grid(row=3,column=0)

    def returnToLockScreenHandler(self):
        self.lock_frame.tkraise()
        self.lock_frame.passwordFocus()

    def shrinkWindow(self):
        # the ordering of lowering is important due to tkinter packing order rules/priorities concerning parents and children as well as their respective widgets and backgrounds
        self.cover_frame.lower()
        self.main_frame.lower()
        self.title_frame.lower()
        self.lock_frame.lower()

        if self.lock_screen:
            self.return_to_lock_screen_button.grid_forget()
        self.close_mission_button.grid(row=1,column=0)
        self.close_application_button.grid_forget()
        self.close_application_button.grid(row=2,column=0)
        self.container.shrinkWindow()

    def closeApp(self):
        self.container.quit()





class TitleFrame(ttk.Frame):

    def __init__(self,container: ControlFrame):
        super().__init__(container)

        image1 = Image.open("./assets/SPL_Logo.png")
        # 1920x482 is original size
        image2 = image1.resize((1920//4,482//4))
        # must store as instance variable to avoid the grabage collector from destroying the image object which is being referenced by the Label
        self.logo_image = ImageTk.PhotoImage(image2)
        self.logo_image_label = ttk.Label(self, image=self.logo_image)
        self.logo_image_label.pack(pady=10)

        image1 = Image.open("./assets/Main Image for Orbit App.png")
        image2 = image1.resize((900,500))
        self.main_image = ImageTk.PhotoImage(image2)
        self.main_image_label = ttk.Label(self, image=self.main_image)
        self.main_image_label.pack()

        ttk.Label(self,text="STEP-1 Orbit and Collision Modelling",font=("Helvetica", 20)).pack()

        ttk.Label(self,text="Select from the simulation options below and input key values as is necessary.", font=("Helvetica", 10)).pack()

        self.place(relheight=0.64,relwidth=1,relx=0,rely=0,anchor="nw")

    def hideImages(self):
        self.main_image_label.config(image="")
        self.logo_image_label.config(image="")
        self.update_idletasks()

    def showImages(self):
        self.main_image_label.config(image=self.main_image)
        self.logo_image_label.config(image=self.logo_image)



class MainFrame(ttk.Frame):

    def __init__(self,container: ControlFrame,freeflyer: FreeFlyerAPI, space_track: SpaceTrackAPI, other_TLE_path, my_TLE_path, default_thrust_duration, default_sim_duration, default_staging_DV, default_staging_DM, default_NORAD_ID, default_wet_mass, default_thrust):
        super().__init__(container)

        self.thrust_duration = default_thrust_duration
        self.default_thrust_duration = default_thrust_duration

        self.stagingDV = default_staging_DV
        self.default_staging_DV = default_staging_DV

        self.stagingDM = default_staging_DM
        self.default_staging_DM = default_staging_DM

        self.NORAD_ID = default_NORAD_ID
        self.default_NORAD_ID = default_NORAD_ID

        self.container = container

        self.freeflyer = freeflyer

        self.space_track = space_track

        self.sim_duration = default_sim_duration
        self.default_sim_duration = default_sim_duration

        self.wet_mass = default_wet_mass
        self.default_wet_mass = default_wet_mass

        self.thrust = default_thrust
        self.default_thrust = default_thrust


        self.columnconfigure(0, weight=1, uniform="col")
        self.columnconfigure(1, weight=1, uniform="col")
        self.columnconfigure(2, weight=1, uniform="col")
        self.rowconfigure(0, weight=2, uniform="row")
        self.rowconfigure(1, weight=2, uniform="row")
        self.rowconfigure(2, weight=2, uniform="row")
        self.rowconfigure(3, weight=2, uniform="row")
        self.rowconfigure(4, weight=2, uniform="row")
        self.rowconfigure(5, weight=2, uniform="row")
        self.rowconfigure(6, weight=2, uniform="row")
        self.rowconfigure(7, weight=2, uniform="row")
        self.rowconfigure(8, weight=2, uniform="row")
        self.rowconfigure(9, weight=2, uniform="row")

        self.sim_thrust_on = ttk.Button(self, text="Run Simulation", command=self.simThrusterFiringHandler)

        self.TD_input = ttk.Label(self,text="Thrust Duration Input (days)")

        self.TD_success_label = ttk.Label(self,text=" ")
        self.TD_error_label = ttk.Label(self,text=" ")
        TD_text_var = tk.StringVar()
        self.TD_entry = ttk.Entry(self,textvariable=TD_text_var)
        self.TD_entry.bind("<Return>", lambda *args: self.updateThrustDurationHandler(TD_text_var.get()))

        self.sim_thrust_off = ttk.Button(self, text="Run Simulation", command=self.simPotentialCollisionHandler)

        self.sim_staging_RK89 = ttk.Button(self, text="Run Simulation", command=self.simStagingRK89Handler)

        self.sim_staging_SGP4 = ttk.Button(self, text="Run Simulation", command=self.simStagingSGP4Handler)

        self.DV_input = ttk.Label(self,text="STEP-1 Delta V Input (m/s)")

        self.DV_success_label = ttk.Label(self,text=" ")
        self.DV_error_label = ttk.Label(self,text=" ")
        DV_text_var = tk.StringVar()
        self.DV_entry = ttk.Entry(self,textvariable=DV_text_var)
        self.DV_entry.bind("<Return>", lambda *args: self.updateStagingDVHandler(DV_text_var.get()))

        self.DM_input = ttk.Label(self,text="STEP-1 Delta M Input (g)")

        self.DM_success_label = ttk.Label(self,text=" ")
        self.DM_error_label = ttk.Label(self,text=" ")
        DM_text_var = tk.StringVar()
        self.DM_entry = ttk.Entry(self,textvariable=DM_text_var)
        self.DM_entry.bind("<Return>", lambda *args: self.updateStagingDMHandler(DM_text_var.get()))

        self.TLE_success_label = ttk.Label(self,text=" ")
        self.TLE_error_label = ttk.Label(self,text=" ")
        self.update_TLE = ttk.Button(self, text="Update TLEs", command= lambda *args: self.update3LEsHandler(other_TLE_path, my_TLE_path))
        self.update_TLE.grid(row=1,column=2)

        self.ID_input = ttk.Label(self,text="STEP-1 NORAD ID Input")
        self.ID_input.grid(row=2,column=2)

        self.ID_success_label = ttk.Label(self,text=" ")
        self.ID_error_label = ttk.Label(self,text=" ")
        ID_text_var = tk.StringVar()
        self.ID_entry = ttk.Entry(self,textvariable=ID_text_var)
        self.ID_entry.bind("<Return>", lambda *args: self.updateNORADIDHandler(ID_text_var.get()))
        self.ID_entry.grid(row=3,column=2)

        self.SD_input = ttk.Label(self,text="Simulation Duration Input (days)")
        self.SD_input.grid(row=5,column=1)

        self.SD_success_label = ttk.Label(self,text=" ")
        self.SD_error_label = ttk.Label(self,text=" ")
        SD_text_var = tk.StringVar()
        self.SD_entry = ttk.Entry(self,textvariable=SD_text_var)
        self.SD_entry.bind("<Return>", lambda *args: self.updateSimDurationHandler(SD_text_var.get()))
        self.SD_entry.grid(row=6,column=1)

        self.mass_input = ttk.Label(self,text="Wet Mass Input (kg)")
        self.mass_input.grid(row=2,column=1)

        self.mass_success_label = ttk.Label(self,text=" ")
        self.mass_error_label = ttk.Label(self,text=" ")
        mass_text_var = tk.StringVar()
        self.mass_entry = ttk.Entry(self,textvariable=mass_text_var)
        self.mass_entry.bind("<Return>", lambda *args: self.updateWetMassHandler(mass_text_var.get()))
        self.mass_entry.grid(row=3,column=1)

        self.thrust_input = ttk.Label(self,text="Forward Thrust Input (micro N)")

        self.thrust_success_label = ttk.Label(self,text=" ")
        self.thrust_error_label = ttk.Label(self,text=" ")
        thrust_text_var = tk.StringVar()
        self.thrust_entry = ttk.Entry(self,textvariable=thrust_text_var)
        self.thrust_entry.bind("<Return>", lambda *args: self.updateThrustHandler(thrust_text_var.get()))

        dropdown_text_var = tk.StringVar()
        options = ["Thrusters On", "Thrusters Off", "Staging (RK89)", "Staging (SGP4)"]
        ttk.OptionMenu(self,dropdown_text_var, "Select Simulation", *options, command=lambda *args: self.gridingHandler(dropdown_text_var.get())).grid(row=0,column=0)

        ttk.Button(self,text="Reset All Inputs to Default Values", command=lambda *args: self.resetInputsHandler(dropdown_text_var.get())).grid(row=9,column=2)

        self.place(relheight=0.33,relwidth=1,relx=0,rely=0.64,anchor="nw")



    def updateThrustDurationHandler(self, new_thrust_duration):
        self.TD_success_label.grid_forget()
        self.TD_error_label.grid_forget()
        try:
            assert float(new_thrust_duration) <= self.sim_duration
            self.thrust_duration = float(new_thrust_duration)
            self.TD_success_label.config(text=f"Thrust Duration Changed to {self.thrust_duration} days",foreground="green")
            self.TD_success_label.grid(row=7,column=0)
        except:
            self.TD_error_label.config(text=f"xxx Invalid Thrust Duration xxx\n(Must be <= Simulation Duration)",foreground="red")
            self.TD_error_label.grid(row=7,column=0)

    def updateWetMassHandler(self, new_wet_mass):
        self.mass_success_label.grid_forget()
        self.mass_error_label.grid_forget()
        try:
            assert float(new_wet_mass) > PROP_MASS
            assert float(new_wet_mass)*(-1) < self.stagingDM
            self.wet_mass = float(new_wet_mass)
            self.mass_success_label.config(text=f"Wet Mass Changed to {self.wet_mass} kg",foreground="green")
            self.mass_success_label.grid(row=4,column=1)
        except:
            self.mass_error_label.config(text=f"xxx Invalid Wet Mass xxx",foreground="red")
            self.mass_error_label.grid(row=4,column=1)

    def updateThrustHandler(self, new_thrust):
        self.thrust_success_label.grid_forget()
        self.thrust_error_label.grid_forget()
        try:
            assert new_thrust != 0
            self.thrust = float(new_thrust)
            self.thrust_success_label.config(text=f"Thrust Changed to {self.thrust} micro N",foreground="green")
            self.thrust_success_label.grid(row=4,column=0)
        except:
            self.thrust_error_label.config(text=f"xxx Invalid Thrust xxx",foreground="red")
            self.thrust_error_label.grid(row=4,column=0)

    def update3LEsHandler(self, other_TLE_path, my_TLE_path):
        self.TLE_success_label.grid_forget()
        self.TLE_error_label.grid_forget()
        if (self.space_track.update3LEs(other_TLE_path, my_TLE_path, self.NORAD_ID)):
            self.TLE_success_label.config(text=f"TLEs Updated",foreground="green")
            self.TLE_success_label.grid(row=5,column=2)
        else:
            self.TLE_error_label.config(text=f"xxx Error Updating TLEs xxx",foreground="red")
            self.TLE_error_label.grid(row=5,column=2)

    def updateNORADIDHandler(self, new_NORAD_ID):
        self.ID_success_label.grid_forget()
        self.ID_error_label.grid_forget()
        self.TLE_success_label.grid_forget()
        self.TLE_error_label.grid_forget()
        try:
            assert int(new_NORAD_ID) < 100000
            self.NORAD_ID = str(int(new_NORAD_ID))
            self.ID_success_label.config(text=f"NORAD ID Changed to {self.NORAD_ID}\n(update TLEs for change to take effect)",foreground="green")
            self.ID_success_label.grid(row=4, column=2)
        except:
            self.ID_error_label.config(text=f"xxx Invalid NORAD ID xxx",foreground="red")
            self.ID_error_label.grid(row=4,column=2)

    def updateSimDurationHandler(self, new_duration):
        self.SD_success_label.grid_forget()
        self.SD_error_label.grid_forget()
        try:
            assert float(new_duration) >= self.thrust_duration
            self.sim_duration = float(new_duration)
            self.SD_success_label.config(text=f"Simulation Duration Changed to {self.sim_duration} days",foreground="green")
            self.SD_success_label.grid(row=7, column=1)
        except:
            self.SD_error_label.config(text=f"xxx Invalid Simulation Duration xxx\n(Must be >= Thrust Duration)",foreground="red")
            self.SD_error_label.grid(row=7,column=1)

    def updateStagingDVHandler(self, new_staging_DV):
        self.DV_success_label.grid_forget()
        self.DV_error_label.grid_forget()
        try:
            self.stagingDV = float(new_staging_DV)
            self.DV_success_label.config(text=f"STEP-1 Delta V Changed to {self.stagingDV} m/s",foreground="green")
            self.DV_success_label.grid(row=4,column=0)
        except:
            self.DV_error_label.config(text=f"xxx Invalid STEP-1 Delta V xxx",foreground="red")
            self.DV_error_label.grid(row=4,column=0)

    def updateStagingDMHandler(self, new_staging_DM):
        self.DM_success_label.grid_forget()
        self.DM_error_label.grid_forget()
        try:
            assert float(new_staging_DM)/1000 > self.wet_mass*(-1)
            self.stagingDM = float(new_staging_DM)
            self.DM_success_label.config(text=f"STEP-1 Delta M Changed to {self.stagingDM} grams",foreground="green")
            self.DM_success_label.grid(row=7,column=0)
        except:
            self.DM_error_label.config(text=f"xxx Invalid STEP-1 Delta M xxx",foreground="red")
            self.DM_error_label.grid(row=7,column=0)

    def simPotentialCollisionHandler(self):
        self.container.title_frame.hideImages()
        self.container.shrinkWindow()
        self.freeflyer.simulatePotentialCollision(self.sim_duration)

    def simThrusterFiringHandler(self):
        self.container.title_frame.hideImages()
        self.container.shrinkWindow()
        # the splitting of wet mass into dry mass and prop mass is done with 0.05 prop mass to ensure STEP-1 doesn't run out of propellant in the simulation (which would throw an error)
        self.freeflyer.simulateThrusterFiring(self.thrust_duration, self.sim_duration, (self.wet_mass - PROP_MASS), (PROP_MASS), self.thrust)

    def simStagingRK89Handler(self):
        self.container.title_frame.hideImages()
        self.container.shrinkWindow()
        self.freeflyer.simulateStagingRK89(self.sim_duration, self.stagingDV/1000, self.stagingDM/1000, self.wet_mass)

    def simStagingSGP4Handler(self):
        self.container.title_frame.hideImages()
        self.container.shrinkWindow()
        self.freeflyer.simulateStagingSGP4(self.sim_duration, self.stagingDV/1000, self.wet_mass)

    def resetInputsHandler(self, dropdown):

        self.updateNORADIDHandler(self.default_NORAD_ID)
        self.updateStagingDVHandler(self.default_staging_DV)
        self.updateStagingDMHandler(self.default_staging_DM)
        self.updateWetMassHandler(self.default_wet_mass)
        self.updateThrustHandler(self.default_thrust)
        # zeroing here is necessary so reseting to defaults can happen without wrongfully tripping the sim_duration >= thrust_duration assertion
        self.sim_duration = 0
        self.thrust_duration = 0
        self.updateSimDurationHandler(self.default_sim_duration)
        self.updateThrustDurationHandler(self.default_thrust_duration)

        self.ID_entry.delete(0,tk.END)
        self.DV_entry.delete(0,tk.END)
        self.DM_entry.delete(0,tk.END)
        self.TD_entry.delete(0,tk.END)
        self.SD_entry.delete(0,tk.END)
        self.mass_entry.delete(0,tk.END)
        self.thrust_entry.delete(0,tk.END)

        if dropdown == "Thrusters On":
            self.DM_success_label.grid_forget()
            self.DV_success_label.grid_forget()
        elif dropdown == "Staging Event":
            self.TD_success_label.grid_forget()
            self.thrust_success_label.grid_forget()
        else:
            self.DM_success_label.grid_forget()
            self.DV_success_label.grid_forget()
            self.TD_success_label.grid_forget()
            self.thrust_success_label.grid_forget()


    def gridingHandler(self, dropdown):
        self.sim_thrust_on.grid_forget()
        self.sim_thrust_off.grid_forget()
        self.sim_staging_SGP4.grid_forget()
        self.sim_staging_RK89.grid_forget()

        self.thrust_input.grid_forget()
        self.thrust_entry.grid_forget()
        self.thrust_error_label.grid_forget()
        self.thrust_success_label.grid_forget()
        self.TD_input.grid_forget()
        self.TD_entry.grid_forget()
        self.TD_error_label.grid_forget()
        self.TD_success_label.grid_forget()
        self.DV_input.grid_forget()
        self.DV_entry.grid_forget()
        self.DV_error_label.grid_forget()
        self.DV_success_label.grid_forget()
        self.DM_input.grid_forget()
        self.DM_entry.grid_forget()
        self.DM_error_label.grid_forget()
        self.DM_success_label.grid_forget()

        if dropdown == "Thrusters On":
            self.sim_thrust_on.grid(row=1,column=0)
            self.thrust_input.grid(row=2,column=0)
            self.thrust_entry.grid(row=3,column=0)
            self.TD_input.grid(row=5,column=0)
            self.TD_entry.grid(row=6,column=0)
        elif dropdown == "Thrusters Off":
            self.sim_thrust_off.grid(row=1,column=0)
        elif dropdown == "Staging (RK89)":
            self.sim_staging_RK89.grid(row=1,column=0)
            self.DV_input.grid(row=2,column=0)
            self.DV_entry.grid(row=3,column=0)
            self.DM_input.grid(row=5,column=0)
            self.DM_entry.grid(row=6,column=0)
        elif dropdown == "Staging (SGP4)":
            self.sim_staging_SGP4.grid(row=1,column=0)
            self.DV_input.grid(row=2,column=0)
            self.DV_entry.grid(row=3,column=0)


class LockFrame(ttk.Frame):

    def __init__(self,container: ControlFrame, application_password):
        super().__init__(container)

        self.rowconfigure(0,weight=20)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.rowconfigure(3,weight=1)
        self.rowconfigure(4,weight=20)
        self.columnconfigure(0,weight=1)

        self.password = application_password

        ttk.Label(self,text="Password:").grid(column=0, row=1)

        text_var = tk.StringVar()
        self.password_entry = ttk.Entry(self,show="*",textvariable=text_var)
        self.password_entry.focus()
        self.password_entry.bind("<Return>", lambda *args: self.loginHandler(text_var))
        self.password_entry.grid(column=0,row=2)

        ttk.Button(self,text="login", command=lambda: self.loginHandler(text_var)).grid(column=0,row=3)

        self.place(relheight=1,relwidth=1,relx=0,rely=0,anchor="nw")

    def loginHandler(self, text_var: tk.StringVar):
        if text_var.get() == self.password:
            self.password_entry.delete(0, tk.END)
            self.lower()

    def passwordFocus(self):
        self.password_entry.focus()


class CoverFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)

        self.place(relheight=1,relwidth=1,relx=0,rely=0,anchor="nw")



if __name__ == "__main__":
    pass
