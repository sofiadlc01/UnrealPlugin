from unreal import (    # Import necessary modules from the Unreal library
    AssetToolsHelpers, 
    AssetTools, 
    EditorAssetLibrary, 
    Material, 
    MaterialFactoryNew, 
    MaterialProperty, 
    MaterialEditingLibrary, 
    MaterialExpressionTextureSampleParameter2D as TextSampler2D, 
    AssetImportTask, 
    FbxImportUI )
import os  # Import the OS module to interact with the operating system

class UnrealUtility:  # Define a class named UnrealUtility
    def __init__(self):  # Initialize the class with some default properties
        self.substanceRootDir = "/game/Substance/"  # Root directory for Substance assets
        self.baseMaterialName = "M_SubstanceBase"  # Name of the base material
        self.subatanceTempDir = "/game/Substance/Temp/"  # Temporary directory for Substance assets
        self.baseMaterialPath = self.substanceRootDir + self.baseMaterialName  # Path to the base material
        self.baseColorName = "BaseColor"  # Name of the base color parameter
        self.normalName = "Normal"  # Name of the normal parameter
        self.occRoughnessMetallicName = "OcclusionRoughnessMetallic"  # Name of the occlusion, roughness, metallic parameter

    def FindOrCreateBaseMaterial(self):  # Define a method to find or create the base material
        if EditorAssetLibrary.does_asset_exist(self.baseMaterialPath):  # Check if the asset already exists
            return EditorAssetLibrary.load_asset(self.baseMaterialPath)  # If it exists, load and return it
        
        baseMat = AssetToolsHelpers.get_asset_tools().create_asset(  # Create a new material asset
            self.baseMaterialName,  # Name of the material
            self.substanceRootDir,  # Directory to create the material in
            Material,  # Type of asset to create
            MaterialFactoryNew()  # Factory to use for creation
        )
        
        baseColor = MaterialEditingLibrary.create_material_expression(baseMat, TextSampler2D, -800, 0)  # Create a texture sample parameter expression for base color
        baseColor.set_editor_property("parameter_name", self.baseColorName)  # Set the parameter name for base color
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR)  # Connect the base color to the material's base color property
        
        normal = MaterialEditingLibrary.create_material_expression(baseMat, TextSampler2D, -800, 400)  # Create a texture sample parameter expression for normal map
        normal.set_editor_property("parameter_name", self.normalName)  # Set the parameter name for normal map
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal"))  # Set the default normal texture
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL)  # Connect the normal map to the material's normal property
        
        occRoughnessMetalic = MaterialEditingLibrary.create_material_expression(baseMat, TextSampler2D, -800, 800)  # Create a texture sample parameter expression for occlusion, roughness, metallic map
        occRoughnessMetalic.set_editor_property("parameter_name", self.occRoughnessMetallicName)  # Set the parameter name for occlusion, roughness, metallic map
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION)  # Connect the red channel to ambient occlusion
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "G", MaterialProperty.MP_ROUGHNESS)  # Connect the green channel to roughness
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "B", MaterialProperty.MP_METALLIC)  # Connect the blue channel to metallic
        
        EditorAssetLibrary.save_asset(baseMat.get_path_name())  # Save the new material asset
        return baseMat  # Return the created material asset

    def LoadMeshFromPath(self, meshPath):  # Define a method to load a mesh from a given path
        meshName = os.path.split(meshPath)[-1].replace(".fbx", "")  # Extract the mesh name from the file path
        importTask = AssetImportTask()  # Create a new asset import task
        importTask.replace_existing = True  # Set to replace existing assets
        importTask.filename = meshPath  # Set the filename for the import task
        importTask.destination_path = "/game/" + meshName  # Set the destination path for the import task
        importTask.save = True  # Set to save the imported asset
        importTask.automated = True  # Set to run the import task automatically
        
        fbxImportOptions = FbxImportUI()  # Create a new FBX import options UI
        fbxImportOptions.import_mesh = True  # Set to import the mesh
        fbxImportOptions.import_as_skeletal = False  # Set to import as a static mesh (not skeletal)
        fbxImportOptions.import_materials = False  # Set to not import materials
        fbxImportOptions.static_mesh_import_data.combine_meshes = True  # Combine all meshes in the FBX file into one static mesh
        
        importTask.options = fbxImportOptions  # Set the import options for the task
        AssetToolsHelpers.get_asset_tools().import_asset_tasks([importTask])  # Run the asset import task
        return importTask.get_objects()[0]  # Return the first imported object

    def LoadFromDir(self, fileDir):  # Define a method to load all meshes from a directory
        for file in os.listdir(fileDir):  # Loop through all files in the directory
            if ".fbx" in file:  # Check if the file is an FBX file
                self.LoadMeshFromPath(os.path.join(fileDir, file))  # Load the mesh from the file path


