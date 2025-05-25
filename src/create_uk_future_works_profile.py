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
        self._add_field(layer, "linkstatus", ogr.OFTString)
        self._add_field(layer, "dataproviderid_fk", ogr.OFTString)
        self._add_field(layer, "programmeid_fk", ogr.OFTString)

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
                ("fw-lcs-001", "Active"),
                ("fw-lcs-002", "Draft"),
                ("fw-lcs-003", "Under Review"),
                ("fw-lcs-004", "Approved"),
                ("fw-lcs-005", "Superseded"),
                ("fw-lcs-006", "Cancelled"),
                ("fw-lcs-007", "Archived"),
            ],
            "organisationtypevalue": [
                ("fw-org-001", "Utility Company"),
                ("fw-org-002", "Local Authority"),
                ("fw-org-003", "Highway Authority"),
                ("fw-org-004", "Contractor"),
                ("fw-org-005", "Consultant"),
                ("fw-org-006", "Regulatory Body"),
                ("fw-org-007", "Other"),
            ],
            "contactdetailstypevalue": [
                ("fw-cdt-001", "Planning Coordinator"),
                ("fw-cdt-002", "Project Manager"),
                ("fw-cdt-003", "Emergency Contact"),
                ("fw-cdt-004", "Asset Protection"),
                ("fw-cdt-005", "General Enquiries"),
                ("fw-cdt-006", "Other"),
            ],
            "plannedworkstatusvalue": [
                ("fw-pws-001", "Proposed"),
                ("fw-pws-002", "Under Consultation"),
                ("fw-pws-003", "Approved"),
                ("fw-pws-004", "Scheduled"),
                ("fw-pws-005", "In Preparation"),
                ("fw-pws-006", "In Progress"),
                ("fw-pws-007", "Completed"),
                ("fw-pws-008", "On Hold"),
                ("fw-pws-009", "Cancelled"),
                ("fw-pws-010", "Deferred"),
            ],
            "programmetypevalue": [
                ("fw-prg-001", "Capital Investment"),
                ("fw-prg-002", "Routine Maintenance"),
                ("fw-prg-003", "Emergency Preparedness"),
                ("fw-prg-004", "Network Expansion"),
                ("fw-prg-005", "Asset Replacement"),
                ("fw-prg-006", "Regulatory Compliance"),
                ("fw-prg-007", "Customer Connection"),
                ("fw-prg-008", "Network Reinforcement"),
                ("fw-prg-009", "Other"),
            ],
            "worktypevalue": [
                ("fw-wkt-001", "New Installation"),
                ("fw-wkt-002", "Full Replacement"),
                ("fw-wkt-003", "Partial Replacement"),
                ("fw-wkt-004", "Upgrade"),
                ("fw-wkt-005", "Repair"),
                ("fw-wkt-006", "Removal"),
                ("fw-wkt-007", "Abandonment"),
                ("fw-wkt-008", "Relocation"),
                ("fw-wkt-009", "Protection Works"),
                ("fw-wkt-010", "Survey/Investigation"),
                ("fw-wkt-011", "Other"),
            ],
            "confidencelevelvalue": [
                ("fw-cnf-001", "Confirmed"),
                ("fw-cnf-002", "Highly Likely"),
                ("fw-cnf-003", "Likely"),
                ("fw-cnf-004", "Possible"),
                ("fw-cnf-005", "Under Review"),
                ("fw-cnf-006", "Tentative"),
            ],
            "utilitytypevalue": [
                ("fw-utl-001", "Electricity"),
                ("fw-utl-002", "Gas"),
                ("fw-utl-003", "Water"),
                ("fw-utl-004", "Sewer"),
                ("fw-utl-005", "Telecommunications"),
                ("fw-utl-006", "District Heating"),
                ("fw-utl-007", "Fuel and Chemicals"),
                ("fw-utl-008", "Transport Signalling"),
                ("fw-utl-009", "Drainage"),
                ("fw-utl-010", "Other"),
            ],
            "materialvalue": [
                ("fw-mat-001", "PE (Polyethylene)"),
                ("fw-mat-002", "PVC"),
                ("fw-mat-003", "Ductile Iron"),
                ("fw-mat-004", "Steel"),
                ("fw-mat-005", "Concrete"),
                ("fw-mat-006", "Clay"),
                ("fw-mat-007", "Copper"),
                ("fw-mat-008", "Fibre Optic"),
                ("fw-mat-009", "Composite"),
                ("fw-mat-010", "HDPE"),
                ("fw-mat-011", "Cast Iron"),
                ("fw-mat-012", "Unknown"),
                ("fw-mat-013", "Other"),
            ],
            "installationmethodvalue": [
                ("fw-ins-001", "Open Cut"),
                ("fw-ins-002", "Directional Drilling"),
                ("fw-ins-003", "Moling"),
                ("fw-ins-004", "Tunnelling"),
                ("fw-ins-005", "Thrust Boring"),
                ("fw-ins-006", "Pipe Jacking"),
                ("fw-ins-007", "Slip Lining"),
                ("fw-ins-008", "Pipe Bursting"),
                ("fw-ins-009", "Trenching"),
                ("fw-ins-010", "Other"),
            ],
            "locationtypevalue": [
                ("fw-loc-001", "Carriageway"),
                ("fw-loc-002", "Footway"),
                ("fw-loc-003", "Verge"),
                ("fw-loc-004", "Cycle Path"),
                ("fw-loc-005", "Private Land"),
                ("fw-loc-006", "Open Space"),
                ("fw-loc-007", "Railway Land"),
                ("fw-loc-008", "Waterway"),
                ("fw-loc-009", "Other"),
            ],
            "dataprovenancevalue": [
                ("fw-dpv-001", "Asset Management System"),
                ("fw-dpv-002", "Planning Application"),
                ("fw-dpv-003", "Capital Programme"),
                ("fw-dpv-004", "Regulatory Submission"),
                ("fw-dpv-005", "Customer Request"),
                ("fw-dpv-006", "Engineering Assessment"),
                ("fw-dpv-007", "Manual Entry"),
                ("fw-dpv-008", "Other"),
            ],
            "measurementunitsvalue": [
                ("fw-mun-001", "Metres"),
                ("fw-mun-002", "Millimetres"),
                ("fw-mun-003", "Kilometres"),
                ("fw-mun-004", "Square Metres"),
                ("fw-mun-005", "Degrees"),
                ("fw-mun-006", "Bar"),
                ("fw-mun-007", "kV"),
                ("fw-mun-008", "Unknown"),
            ],
            "datasensitivitylevelvalue": [
                ("fw-dsl-001", "Public"),
                ("fw-dsl-002", "Official"),
                ("fw-dsl-003", "Official-Sensitive"),
                ("fw-dsl-004", "Restricted"),
                ("fw-dsl-005", "Confidential"),
                ("fw-dsl-006", "Secret"),
                ("fw-dsl-007", "Top Secret"),
            ],
            "linkstatusvalue": [
                ("fw-lks-001", "New"),
                ("fw-lks-002", "Existing"),
                ("fw-lks-003", "Proposed New"),
                ("fw-lks-004", "Existing - To Be Modified"),
                ("fw-lks-005", "Existing - To Be Replaced"),
                ("fw-lks-006", "Existing - To Be Removed"),
            ],
        }

        # Create utilitysubtypevalue separately as it has an extra field
        layer = self.ds.CreateLayer("utilitysubtypevalue", geom_type=ogr.wkbNone)
        self._add_codelist_fields(layer)
        self._add_field(layer, "applicabledomains", ogr.OFTString)

        # Populate utilitysubtypevalue
        utilitysubtypes = [
            ("fw-uts-001", "High Voltage", "Electricity"),
            ("fw-uts-002", "Low Voltage", "Electricity"),
            ("fw-uts-003", "Street Lighting", "Electricity"),
            ("fw-uts-004", "High Pressure", "Gas"),
            ("fw-uts-005", "Medium Pressure", "Gas"),
            ("fw-uts-006", "Low Pressure", "Gas"),
            ("fw-uts-007", "Potable Water", "Water"),
            ("fw-uts-008", "Raw Water", "Water"),
            ("fw-uts-009", "Foul Sewer", "Sewer"),
            ("fw-uts-010", "Surface Water", "Sewer,Drainage"),
            ("fw-uts-011", "Combined Sewer", "Sewer"),
            ("fw-uts-012", "Fibre Optic", "Telecommunications"),
            ("fw-uts-013", "Copper Cable", "Telecommunications"),
            ("fw-uts-014", "Other", "All"),
        ]

        for systemid, value, domains in utilitysubtypes:
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
        self._add_field(layer, "usrn", ogr.OFTString)
        self._add_field(layer, "street_name", ogr.OFTString)
        self._add_field(layer, "link_status", ogr.OFTString)
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

        # Populate the unified table with a SQL insert from joined tables
        sql = """
        INSERT INTO future_works_unified (
            work_id, work_name, description, 
            organisation_name, organisation_shortname, organisation_type, swa_code,
            utility_type, utility_subtype, usrn, street_name, link_status, work_type,
            planned_start_date, planned_end_date, confidence_level,
            material, installation_method, depth_metres,
            programme_name, programme_type,
            contact_name, contact_email, contact_phone,
            last_updated, data_sensitivity, geom
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
            nl.usrn,
            nl.localereference as street_name,
            nl.linkstatus as link_status,
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
            nl.geom
        FROM networklink nl
        LEFT JOIN organisation org ON nl.dataproviderid_fk = org.systemid
        LEFT JOIN plannedprogramme prog ON nl.programmeid_fk = prog.systemid
        LEFT JOIN relationship_organisationtocontactdetails rel ON org.systemid = rel.linkedorganisationid
        LEFT JOIN contactdetails cd ON rel.linkedcontactdetailsid = cd.systemid
        WHERE nl.lifecyclestatus = 'Active'
        """

        # Execute after all tables are populated
        # Note: This SQL will be run by the populate script

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
    print("- Code list tables: 15 reference tables populated with values")
    print("- Unified table: future_works_unified (contains all joined data)")
    print(
        "\nThe main table to use is 'future_works_unified' which contains all information in one place."
    )


if __name__ == "__main__":
    main()
