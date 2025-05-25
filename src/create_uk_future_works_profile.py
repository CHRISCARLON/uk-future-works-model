"""
UK Future Works Profile GeoPackage
Creates a UK Future Works Profile GeoPackage for sharing future works profile data between utility companies and local authorities
"""
import os
import sys
from datetime import datetime
from osgeo import ogr, osr
from typing import Optional, Any

class UKFutureWorksProfileGeoPackage:
    def __init__(self, output_path):
        """Initialise the GeoPackage creator with output path"""
        self.output_path = output_path
        self.driver = ogr.GetDriverByName("GPKG")
        self.ds: Optional[Any] = None
        self.srs = None
        
        if self.driver is None:
            raise Exception("GPKG driver not available. Check GDAL installation.")
    
    def create_geopackage(self):
        """Main method to create the GeoPackage with all tables"""
        print(f"Creating UK Future Works Profile GeoPackage: {self.output_path}")
        
        # Delete existing file if it exists
        if os.path.exists(self.output_path):
            os.remove(self.output_path)
        
        # Create new GeoPackage
        self.ds = self.driver.CreateDataSource(self.output_path)
        if self.ds is None:
            raise Exception(f"Failed to create GeoPackage: {self.output_path}")
        
        # Set up British National Grid (EPSG:27700) as default SRS
        self.srs = osr.SpatialReference()
        self.srs.ImportFromEPSG(27700)
        
        try:
            # Create organisation schema tables
            self._create_organisation_tables()
            
            # Create future works tables
            self._create_future_works_tables()
            
            # Create code list tables
            self._create_codelist_tables()
            
            # Create relationship tables
            self._create_relationship_tables()
            
            # Create views
            self._create_views()
            
            print("GeoPackage created successfully!")
            
        except Exception as e:
            print(f"Error creating GeoPackage: {e}")
            raise
        finally:
            # Close the datasource
            self.ds = None
    
    def _create_organisation_tables(self):
        """Create organisation schema tables"""
        print("Creating organisation tables...")
        assert self.ds is not None
        
        # Create organisation table
        layer = self.ds.CreateLayer("organisation", geom_type=ogr.wkbNone)
        self._add_field(layer, "systemid", ogr.OFTString)
        self._add_field(layer, "lifecyclestatus", ogr.OFTString)
        self._add_field(layer, "datelastupdated", ogr.OFTDateTime)
        self._add_field(layer, "dateoflastlifecyclestatuschange", ogr.OFTDateTime)
        self._add_field(layer, "systemloaddate", ogr.OFTDateTime)
        self._add_field(layer, "name", ogr.OFTString)
        self._add_field(layer, "shortname", ogr.OFTString)
        self._add_field(layer, "organisationtype", ogr.OFTString)
        self._add_field(layer, "swacode", ogr.OFTString)
        self._add_field(layer, "websiteurl", ogr.OFTString)
        
        # Create contactdetails table
        layer = self.ds.CreateLayer("contactdetails", geom_type=ogr.wkbNone)
        self._add_field(layer, "systemid", ogr.OFTString)
        self._add_field(layer, "lifecyclestatus", ogr.OFTString)
        self._add_field(layer, "datelastupdated", ogr.OFTDateTime)
        self._add_field(layer, "dateoflastlifecyclestatuschange", ogr.OFTDateTime)
        self._add_field(layer, "systemloaddate", ogr.OFTDateTime)
        self._add_field(layer, "organisationname", ogr.OFTString)
        self._add_field(layer, "contactdetailstype", ogr.OFTString)
        self._add_field(layer, "departmentname", ogr.OFTString)
        self._add_field(layer, "emailaddress", ogr.OFTString)
        self._add_field(layer, "telephonenumber", ogr.OFTString)
        self._add_field(layer, "dataproviderid_fk", ogr.OFTString)
    
    def _create_future_works_tables(self):
        """Create future works specific tables - network link focused"""
        print("Creating future works tables...")
        assert self.ds is not None
        
        # Create plannedprogramme table
        layer = self.ds.CreateLayer("plannedprogramme", geom_type=ogr.wkbNone)
        self._add_standard_fields(layer)
        self._add_field(layer, "programmename", ogr.OFTString)
        self._add_field(layer, "programmetype", ogr.OFTString)
        self._add_field(layer, "programmedescription", ogr.OFTString)
        self._add_field(layer, "plannedstartdate", ogr.OFTDate)
        self._add_field(layer, "plannedenddate", ogr.OFTDate)
        self._add_field(layer, "dataproviderid_fk", ogr.OFTString)
        
        # Create networklink table with linestring geometry
        layer = self.ds.CreateLayer(
            "networklink", srs=self.srs, geom_type=ogr.wkbLineString
        )
        self._add_standard_fields(layer)
        self._add_field(layer, "description", ogr.OFTString)
        self._add_field(layer, "featuretype", ogr.OFTString)
        self._add_field(layer, "utilitytype", ogr.OFTString)
        self._add_field(layer, "utilitysubtype", ogr.OFTString)
        self._add_field(layer, "plannedinstallationdate", ogr.OFTDate)
        self._add_field(layer, "plannedmaterial", ogr.OFTString)
        self._add_field(layer, "plannedinstallationmethod", ogr.OFTString)
        self._add_field(layer, "planneddepth_depth", ogr.OFTReal)
        self._add_field(layer, "planneddepth_unitofmeasure", ogr.OFTString)
        self._add_field(layer, "componenttype", ogr.OFTString)
        self._add_field(layer, "componentsubtype", ogr.OFTString)
        self._add_field(layer, "worktype", ogr.OFTString)
        self._add_field(layer, "plannedstartdate", ogr.OFTDate)
        self._add_field(layer, "plannedenddate", ogr.OFTDate)
        self._add_field(layer, "confidencelevel", ogr.OFTString)
        self._add_field(layer, "localereference", ogr.OFTString)
        self._add_field(layer, "localereferencetype", ogr.OFTString)
        self._add_field(layer, "objectname", ogr.OFTString)
        self._add_field(layer, "objectowner", ogr.OFTString)
        self._add_field(layer, "operator", ogr.OFTString)
        self._add_field(layer, "usrn", ogr.OFTString)
        self._add_field(layer, "operationalstatus", ogr.OFTString)
        self._add_field(layer, "dataproviderid_fk", ogr.OFTString)
        self._add_field(layer, "programmeid_fk", ogr.OFTString)
        self._add_field(layer, "conveyancemethod", ogr.OFTString)
        self._add_field(layer, "schemestatus", ogr.OFTString)
        self._add_field(layer, "cycleschemedetails", ogr.OFTString)
    
    def _create_relationship_tables(self):
        """Create relationship tables"""
        print("Creating relationship tables...")
        assert self.ds is not None
        
        # Organisation to contact details relationship
        layer = self.ds.CreateLayer(
            "relationship_organisationtocontactdetails", geom_type=ogr.wkbNone
        )
        self._add_field(layer, "systemid", ogr.OFTString)
        self._add_field(layer, "lifecyclestatus", ogr.OFTString)
        self._add_field(layer, "datelastupdated", ogr.OFTDateTime)
        self._add_field(layer, "dateoflastlifecyclestatuschange", ogr.OFTDateTime)
        self._add_field(layer, "systemloaddate", ogr.OFTDateTime)
        self._add_field(layer, "linkedorganisationid", ogr.OFTString)
        self._add_field(layer, "linkedcontactdetailsid", ogr.OFTString)
        self._add_field(layer, "dataproviderid_fk", ogr.OFTString)
    
    def _create_codelist_tables(self):
        """Create and populate code list tables"""
        print("Creating and populating code list tables...")
        assert self.ds is not None
        
        # Define code lists and their values
        codelists = {
            "lifecyclestatusvalue": [
                ("active", "Active"),
                ("draft", "Draft"),
                ("under_review", "Under Review"),
                ("approved", "Approved"),
                ("superseded", "Superseded"),
                ("cancelled", "Cancelled"),
                ("archived", "Archived"),
            ],
            "organisationtypevalue": [
                ("utility_company", "Utility Company"),
                ("local_authority", "Local Authority"),
                ("highway_authority", "Highway Authority"),
                ("contractor", "Contractor"),
                ("consultant", "Consultant"),
                ("regulatory_body", "Regulatory Body"),
                ("other", "Other"),
            ],
            "contactdetailstypevalue": [
                ("planning_coordinator", "Planning Coordinator"),
                ("project_manager", "Project Manager"),
                ("emergency_contact", "Emergency Contact"),
                ("asset_protection", "Asset Protection"),
                ("general_enquiries", "General Enquiries"),
                ("other", "Other"),
            ],
            "plannedworkstatusvalue": [
                ("proposed", "Proposed"),
                ("under_consultation", "Under Consultation"),
                ("approved", "Approved"),
                ("scheduled", "Scheduled"),
                ("in_preparation", "In Preparation"),
                ("in_progress", "In Progress"),
                ("completed", "Completed"),
                ("on_hold", "On Hold"),
                ("cancelled", "Cancelled"),
                ("deferred", "Deferred"),
            ],
            "programmetypevalue": [
                ("capital_investment", "Capital Investment"),
                ("routine_maintenance", "Routine Maintenance"),
                ("emergency_preparedness", "Emergency Preparedness"),
                ("network_expansion", "Network Expansion"),
                ("asset_replacement", "Asset Replacement"),
                ("regulatory_compliance", "Regulatory Compliance"),
                ("customer_connection", "Customer Connection"),
                ("network_reinforcement", "Network Reinforcement"),
                ("cycle_network_development", "Cycle Network Development"),
                ("active_travel_scheme", "Active Travel Scheme"),
                ("other", "Other"),
            ],
            "worktypevalue": [
                ("new_installation", "New Installation"),
                ("full_replacement", "Full Replacement"),
                ("partial_replacement", "Partial Replacement"),
                ("upgrade", "Upgrade"),
                ("repair", "Repair"),
                ("removal", "Removal"),
                ("abandonment", "Abandonment"),
                ("relocation", "Relocation"),
                ("protection_works", "Protection Works"),
                ("survey_investigation", "Survey/Investigation"),
                ("cycle_lane_installation", "Cycle Lane Installation"),
                ("cycle_path_construction", "Cycle Path Construction"),
                ("cycle_crossing_upgrade", "Cycle Crossing Upgrade"),
                ("other", "Other"),
            ],
            "confidencelevelvalue": [
                ("confirmed", "Confirmed"),
                ("highly_likely", "Highly Likely"),
                ("likely", "Likely"),
                ("possible", "Possible"),
                ("under_review", "Under Review"),
                ("tentative", "Tentative"),
            ],
            "utilitytypevalue": [
                ("electricity", "Electricity"),
                ("gas", "Gas"),
                ("water", "Water"),
                ("sewer", "Sewer"),
                ("telecommunications", "Telecommunications"),
                ("district_heating", "District Heating"),
                ("fuel_and_chemicals", "Fuel and Chemicals"),
                ("transport_signalling", "Transport Signalling"),
                ("drainage", "Drainage"),
                ("cycling_infrastructure", "Cycling Infrastructure"),
                ("transport_infrastructure", "Transport Infrastructure"),
                ("other", "Other"),
            ],
            "materialvalue": [
                ("pe (polyethylene)", "PE (Polyethylene)"),
                ("pvc", "PVC"),
                ("ductile iron", "Ductile Iron"),
                ("steel", "Steel"),
                ("concrete", "Concrete"),
                ("clay", "Clay"),
                ("copper", "Copper"),
                ("fibre optic", "Fibre Optic"),
                ("composite", "Composite"),
                ("hdpe", "HDPE"),
                ("cast iron", "Cast Iron"),
                ("unknown", "Unknown"),
                ("other", "Other"),
                ("abs", "ABS"),
                ("asphalt", "Asphalt"),
                ("aluminium", "Aluminium"),
                ("asbestos cement", "Asbestos Cement"),
                ("brick", "Brick"),
                ("ceramic", "Ceramic"),
                ("coated steel", "Coated Steel"),
                ("earthen", "Earthen"),
                ("fiberglass", "Fiberglass"),
                ("galvanised iron", "Galvanised Iron"),
                ("galvanised steel", "Galvanised Steel"),
                ("geotextile", "Geotextile"),
                ("gravel", "Gravel"),
                ("iron", "Iron"),
                ("ldpe", "LDPE"),
                ("mdpe", "MDPE"),
                ("mopc", "MOPC"),
                ("optical fibre", "Optical Fibre"),
                ("pex", "PEX"),
                ("plastic", "Plastic"),
                ("spun iron", "Spun Iron"),
                ("stone", "Stone"),
                ("tile", "Tile"),
                ("transite", "Transite"),
                ("upvc", "uPVC"),
                ("wood", "Wood"),
                ("lead", "Lead"),
                ("pitch fibre", "Pitch Fibre"),
                ("carbon fibre", "Carbon Fibre"),
            ],
            "installationmethodvalue": [
                ("open_cut", "Open Cut"),
                ("directional_drilling", "Directional Drilling"),
                ("moling", "Moling"),
                ("tunnelling", "Tunnelling"),
                ("thrust_boring", "Thrust Boring"),
                ("pipe_jacking", "Pipe Jacking"),
                ("slip_lining", "Slip Lining"),
                ("pipe_bursting", "Pipe Bursting"),
                ("trenching", "Trenching"),
                ("other", "Other"),
            ],
            "locationtypevalue": [
                ("carriageway", "Carriageway"),
                ("footpath", "Footpath"),
                ("verge", "Verge"),
                ("cycle_path", "Cycle Path"),
                ("field", "Field"),
                ("other", "Other"),
            ],
            "dataprovenancevalue": [
                ("asset_management_system", "Asset Management System"),
                ("planning_application", "Planning Application"),
                ("capital_programme", "Capital Programme"),
                ("regulatory_submission", "Regulatory Submission"),
                ("customer_request", "Customer Request"),
                ("engineering_assessment", "Engineering Assessment"),
                ("manual_entry", "Manual Entry"),
                ("other", "Other"),
            ],
            "measurementunitsvalue": [
                ("metres", "Metres"),
                ("millimetres", "Millimetres"),
                ("kilometres", "Kilometres"),
                ("square_metres", "Square Metres"),
                ("degrees", "Degrees"),
                ("bar", "Bar"),
                ("kv", "kV"),
                ("unknown", "Unknown"),
            ],
            "datasensitivitylevelvalue": [
                ("public", "Public"),
                ("restricted", "Restricted"),
            ],
            "operationalstatusvalue": [
                ("abandoned", "Abandoned"),
                ("commissioned", "Commissioned"),
                ("decommissioned", "Decommissioned"),
                ("delete_before_installation", "Delete Before Installation"),
                ("in_service", "In Service"),
                ("installed", "Installed"),
                ("other", "Other"),
                ("out_of_commission", "Out Of Commission"),
                ("pending_abandonment", "Pending Abandonment"),
                ("proposed", "Proposed"),
                ("pending_removal", "Pending Removal"),
                ("removed", "Removed"),
                ("under_construction", "Under Construction"),
                ("unfit_for_service", "Unfit For Service"),
                ("unknown", "Unknown"),
            ],
            "cycleschemestatus": [
                ("proposed", "Proposed"),
                ("feasibility_study", "Feasibility Study"),
                ("public_consultation", "Public Consultation"),
                ("approved", "Approved"),
                ("funded", "Funded"),
                ("planning_granted", "Planning Granted"),
                ("in_progress", "In Progress"),
                ("completed", "Completed"),
                ("canceled", "Canceled"),
            ],
        }
        
        # Create conveyancemethodvalue separately as it has an extra field
        layer = self.ds.CreateLayer("conveyancemethodvalue", geom_type=ogr.wkbNone)
        self._add_codelist_fields(layer)
        self._add_field(layer, "applicabledomains", ogr.OFTString)
        
        # Populate conveyancemethodvalue
        conveyancemethods = [
            ("low_pressure", "Low Pressure", "Fuel And Chemicals,Gas,Water"),
            ("low_voltage", "Low Voltage", "Electricity"),
            ("pressure", "Pressure", "Fuel And Chemicals,Gas,Water"),
            ("gravity", "Gravity", "Drainage,Fuel And Chemicals,Sewer,Thermal,Water"),
            ("high_pressure", "High Pressure", "Fuel And Chemicals,Gas,Water"),
            ("high_voltage", "High Voltage", "Electricity"),
            ("unknown", "Unknown", "All"),
            ("other", "Other", "All"),
            ("syphon", "Syphon", "Drainage,Fuel And Chemicals,Sewer,Thermal,Water"),
            ("vacuum", "Vacuum", "Drainage,Fuel And Chemicals,Sewer,Thermal,Water"),
            ("intermediate_voltage", "Intermediate Voltage", "Electricity"),
            ("medium_voltage", "Medium Voltage", "Electricity"),
            ("intermediate_pressure", "Intermediate Pressure", "Fuel And Chemicals,Gas,Water"),
            ("medium_pressure", "Medium Pressure", "Fuel And Chemicals,Gas"),
            ("pumped", "Pumped", "Drainage,Fuel And Chemicals,Sewer,Thermal,Water"),
            ("regional_intermediate_pressure", "Regional Intermediate Pressure", "Fuel And Chemicals,Gas"),
            ("regional_high_pressure", "Regional High Pressure", "Fuel And Chemicals,Gas"),
            ("extra_high_voltage", "Extra High Voltage", "Electricity"),
            ("national_high_pressure", "National High Pressure", "Fuel And Chemicals,Gas,Water"),
        ]
        
        for systemid, value, domains in conveyancemethods:
            feature = ogr.Feature(layer.GetLayerDefn())
            feature.SetField("systemid", systemid)
            feature.SetField("value", value)
            feature.SetField("applicabledomains", domains)
            feature.SetField("systemloaddate", datetime.now().isoformat())
            feature.SetField("datelastupdated", datetime.now().isoformat())
            layer.CreateFeature(feature)
            feature = None
        
        # Create and populate other code list tables
        for table_name, values in codelists.items():
            layer = self.ds.CreateLayer(table_name, geom_type=ogr.wkbNone)
            self._add_codelist_fields(layer)
            
            # Populate with values
            for systemid, value in values:
                feature = ogr.Feature(layer.GetLayerDefn())
                feature.SetField("systemid", systemid)
                feature.SetField("value", value)
                feature.SetField("systemloaddate", datetime.now().isoformat())
                feature.SetField("datelastupdated", datetime.now().isoformat())
                layer.CreateFeature(feature)
                feature = None
    
    def _create_views(self):
        """Create database views using SQL"""
        print("Creating views...")
        assert self.ds is not None
        
        # Create a unified future works table that combines all necessary data
        # This will be the ONLY table visible to end users
        layer = self.ds.CreateLayer(
            "future_works_unified", srs=self.srs, geom_type=ogr.wkbLineString
        )
        
        # Add all the fields users need to see
        self._add_field(layer, "work_id", ogr.OFTString)
        self._add_field(layer, "work_name", ogr.OFTString)
        self._add_field(layer, "description", ogr.OFTString)
        self._add_field(layer, "organisation_name", ogr.OFTString)
        self._add_field(layer, "organisation_shortname", ogr.OFTString)
        self._add_field(layer, "organisation_type", ogr.OFTString)
        self._add_field(layer, "swa_code", ogr.OFTString)
        self._add_field(layer, "utility_type", ogr.OFTString)
        self._add_field(layer, "utility_subtype", ogr.OFTString)
        self._add_field(layer, "conveyance_method", ogr.OFTString)
        self._add_field(layer, "usrn", ogr.OFTString)
        self._add_field(layer, "street_name", ogr.OFTString)
        self._add_field(layer, "work_type", ogr.OFTString)
        self._add_field(layer, "planned_start_date", ogr.OFTDate)
        self._add_field(layer, "planned_end_date", ogr.OFTDate)
        self._add_field(layer, "confidence_level", ogr.OFTString)
        self._add_field(layer, "material", ogr.OFTString)
        self._add_field(layer, "installation_method", ogr.OFTString)
        self._add_field(layer, "depth_metres", ogr.OFTReal)
        self._add_field(layer, "programme_name", ogr.OFTString)
        self._add_field(layer, "programme_type", ogr.OFTString)
        self._add_field(layer, "contact_name", ogr.OFTString)
        self._add_field(layer, "contact_email", ogr.OFTString)
        self._add_field(layer, "contact_phone", ogr.OFTString)
        self._add_field(layer, "last_updated", ogr.OFTDateTime)
        self._add_field(layer, "data_sensitivity", ogr.OFTString)
        self._add_field(layer, "operational_status", ogr.OFTString)  # Added this field
        self._add_field(layer, "scheme_status", ogr.OFTString)
        self._add_field(layer, "cycle_scheme_details", ogr.OFTString)
        
        # Store the SQL for the populate script to execute
        self.unified_view_sql = """
        INSERT INTO future_works_unified (
            work_id, work_name, description,
            organisation_name, organisation_shortname, organisation_type, swa_code,
            utility_type, utility_subtype, conveyance_method, usrn, street_name, work_type,
            planned_start_date, planned_end_date, confidence_level,
            material, installation_method, depth_metres,
            programme_name, programme_type,
            contact_name, contact_email, contact_phone,
            last_updated, data_sensitivity, operational_status, geom,
            scheme_status, cycle_scheme_details
        )
        SELECT 
            nl.systemid as work_id,
            nl.objectname as work_name,
            nl.description,
            org.name as organisation_name,
            org.shortname as organisation_shortname,
            org.organisationtype as organisation_type,
            org.swacode as swa_code,
            nl.utilitytype as utility_type,
            nl.utilitysubtype as utility_subtype,
            nl.conveyancemethod as conveyance_method,
            nl.usrn,
            nl.localereference as street_name,
            nl.worktype as work_type,
            nl.plannedstartdate as planned_start_date,
            nl.plannedenddate as planned_end_date,
            nl.confidencelevel as confidence_level,
            nl.plannedmaterial as material,
            nl.plannedinstallationmethod as installation_method,
            nl.planneddepth_depth as depth_metres,
            prog.programmename as programme_name,
            prog.programmetype as programme_type,
            cd.contactdetailstype || ' - ' || cd.departmentname as contact_name,
            cd.emailaddress as contact_email,
            cd.telephonenumber as contact_phone,
            nl.datelastupdated as last_updated,
            nl.datasensitivitylevel as data_sensitivity,
            nl.operationalstatus as operational_status,
            nl.geom,
            nl.schemestatus as scheme_status,
            nl.cycleschemedetails as cycle_scheme_details
        FROM networklink nl
        LEFT JOIN organisation org ON nl.dataproviderid_fk = org.systemid
        LEFT JOIN plannedprogramme prog ON nl.programmeid_fk = prog.systemid
        LEFT JOIN relationship_organisationtocontactdetails rel ON org.systemid = rel.linkedorganisationid
        LEFT JOIN contactdetails cd ON rel.linkedcontactdetailsid = cd.systemid
        WHERE nl.lifecyclestatus = 'Active'
        """
        
        # Note: This SQL will be run by the populate script
        print("Note: The unified view SQL has been prepared but needs to be executed after data population.")
        print("SQL stored in self.unified_view_sql for use by the populate script.")
    
    def _add_standard_fields(self, layer):
        """Add standard MUDDI fields to a layer"""
        self._add_field(layer, "systemid", ogr.OFTString)
        self._add_field(layer, "lifecyclestatus", ogr.OFTString)
        self._add_field(layer, "datelastupdated", ogr.OFTDateTime)
        self._add_field(layer, "dateoflastlifecyclestatuschange", ogr.OFTDateTime)
        self._add_field(layer, "systemloaddate", ogr.OFTDateTime)
        self._add_field(layer, "certification", ogr.OFTString)
        self._add_field(layer, "dataproviderassigneduniqueid", ogr.OFTString)
        self._add_field(
            layer, "dataproviderassigneduniqueidautoassigned", ogr.OFTInteger
        )
        self._add_field(layer, "dataowner", ogr.OFTString)
        self._add_field(layer, "dataownerassigneduniqueid", ogr.OFTString)
        self._add_field(layer, "datasensitivitylevel", ogr.OFTString)
    
    def _add_codelist_fields(self, layer):
        """Add standard fields for code list tables"""
        self._add_field(layer, "systemid", ogr.OFTString)
        self._add_field(layer, "systemloaddate", ogr.OFTDateTime)
        self._add_field(layer, "datelastupdated", ogr.OFTDateTime)
        self._add_field(layer, "versionnumber", ogr.OFTString)
        self._add_field(layer, "versiondate", ogr.OFTDateTime)
        self._add_field(layer, "value", ogr.OFTString)
    
    def _add_field(self, layer, name, field_type, width=None):
        """Add a field to a layer"""
        field_defn = ogr.FieldDefn(name, field_type)
        if width:
            field_defn.SetWidth(width)
        layer.CreateField(field_defn)

def main():
    """Main function"""
    # Default output path
    output_path = "uk_future_works_example.gpkg"
    
    # Check command line arguments
    if len(sys.argv) > 1:
        output_path = sys.argv[1]
    
    # Create the GeoPackage
    creator = UKFutureWorksProfileGeoPackage(output_path)
    creator.create_geopackage()
    
    print(f"\nGeoPackage created: {output_path}")
    print("\nTables created:")
    print("- Organisation tables: organisation, contactdetails")
    print("- Future works tables: plannedprogramme, networklink")
    print("- Relationship tables: relationship_organisationtocontactdetails")
    print("- Code list tables: 16 reference tables populated with values")
    print("  Including: operationalstatusvalue, conveyancemethodvalue, materialvalue (expanded)")
    print("- Unified table: future_works_unified (contains all joined data)")
    print(
        "\nThe main table to use is 'future_works_unified' which contains all information in one place."
    )
    print("\nIMPORTANT: The unified view needs to be populated after data is loaded into the base tables.")
    print("The SQL for this is available in the creator.unified_view_sql property.")

if __name__ == "__main__":
    main()