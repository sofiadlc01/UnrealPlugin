import tkinter.filedialog
from unreal import ToolMenuContext, ToolMenus, ToolMenuEntryScript, uclass, ufunction
import sys
import os
import importlib
import tkinter

# Ensure the current directory is in the system path
srcDir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of this script
if srcDir not in sys.path:  # Check if the directory is already in the system path
    sys.path.append(srcDir)  # Add the directory to the system path

# Import UnrealUtilities module and reload it
import UnrealUtilities  # Import the UnrealUtilities module
importlib.reload(UnrealUtilities)  # Reload the UnrealUtilities module to ensure it is the latest version

@uclass()
class LoadFromDirEntryScript(ToolMenuEntryScript):
    @ufunction(override=True)
    def execute(self, context):
        window = tkinter.Tk()  # Create a Tkinter window
        window.withdraw()  # Hide the main Tkinter window
        fileDir = tkinter.filedialog.askdirectory()  # Open a dialog to choose a directory
        window.destroy()  # Destroy the Tkinter window
        UnrealUtilities.UnrealUtility().LoadFromDir(fileDir)  # Call LoadFromDir method from UnrealUtilities

@uclass()
class BuildBaseMaterialEntryScript(ToolMenuEntryScript):
    @ufunction(override=True)
    def execute(self, context: ToolMenuContext) -> None:
        UnrealUtilities.UnrealUtility().FindOrCreateBaseMaterial()  # Call FindOrCreateBaseMaterial method from UnrealUtilities

class UnrealSubstancePlugin:
    def __init__(self):
        self.subMenuName = "SubstancePlugin"  # Set the name of the sub-menu
        self.subMenuLabel = "SubstancePlugin"  # Set the label of the sub-menu
        self.InitUI()  # Initialize the user interface

    def InitUI(self):
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu")  # Get the main menu from the tool menus
        self.subMenu = mainMenu.add_sub_menu(mainMenu.menu_name, "", "SubstancePlugin", "Substance Plugin")  # Add a sub-menu to the main menu
        self.AddEntryScript("BuildBaseMaterial", "Build Base Material", BuildBaseMaterialEntryScript())  # Add "Build Base Material" entry to the sub-menu
        self.AddEntryScript("LoadFromDir", "Load From Directory", LoadFromDirEntryScript())  # Add "Load From Directory" entry to the sub-menu
        ToolMenus.get().refresh_all_widgets()  # Refresh all widgets to reflect changes

    def AddEntryScript(self, name, label, script: ToolMenuEntryScript):
        script.init_entry(self.subMenu.menu_name, self.subMenu.menu_name, "", name, label)  # Initialize the menu entry
        script.register_menu_entry()  # Register the menu entry with the tool menus

# Initialize the UnrealSubstancePlugin
UnrealSubstancePlugin()  # Create an instance of the UnrealSubstancePlugin class




