"""
UK Future Works Profile GeoPackage
Populates a UK Future Works Profile GeoPackage with sample data
This script is used to populate the GeoPackage with sample data for testing and development purposes.
It is not intended to be used in production.
"""

import os
import sys
from datetime import datetime, timedelta
from osgeo import ogr, osr
from typing import Optional, Any


class UKFutureWorksProfileGeoPackagePopulate:
    def __init__(self, geopackage_path):
        """Initialise the populator with the GeoPackage path"""
        self.geopackage_path = geopackage_path
        self.ds: Optional[Any] = None
        self.srs = None

    def populate_geopackage(self):
        """Main method to populate the GeoPackage with sample data"""
        print(f"Populating UK Future Works Profile GeoPackage: {self.geopackage_path}")

        # Open the GeoPackage
        self.ds = ogr.Open(self.geopackage_path, 1)  # 1 = open in update mode!!
        if self.ds is None:
            raise Exception(f"Failed to open GeoPackage: {self.geopackage_path}")

        # Set up British National Grid (EPSG:27700)
        self.srs = osr.SpatialReference()
        self.srs.ImportFromEPSG(27700)

        try:
            # Populate tables in order
            self._populate_organisations()
            self._populate_contact_details()
            self._populate_organisation_relationships()
            self._populate_planned_programmes()
            self._populate_network_links()

            # Populate the unified table with all joined data
            self._populate_unified_table()

            print("GeoPackage populated successfully!")

        except Exception as e:
            print(f"Error populating GeoPackage: {e}")
            raise
        finally:
            # Close the datasource
            self.ds = None

    def _populate_organisations(self):
        """Populate organisation table with sample utility companies"""
        print("Populating organisations...")
        assert self.ds is not None

        layer = self.ds.GetLayerByName("organisation")

        organisations = [
            {
                "systemid": "org-001",
                "name": "Northern Gas Networks",
                "shortname": "NGN",
                "organisationtype": "utility_company",  
                "swacode": "NGN",
                "websiteurl": "https://www.northerngasnetworks.co.uk",
            },
            {
                "systemid": "org-002",
                "name": "Yorkshire Water Services",
                "shortname": "YWS",
                "organisationtype": "utility_company",  
                "swacode": "YWS",
                "websiteurl": "https://www.yorkshirewater.com",
            },
            {
                "systemid": "org-003",
                "name": "Northern Powergrid",
                "shortname": "NPG",
                "organisationtype": "utility_company",  
                "swacode": "NPG",
                "websiteurl": "https://www.northernpowergrid.com",
            },
            {
                "systemid": "org-004",
                "name": "BT Openreach",
                "shortname": "BTO",
                "organisationtype": "utility_company",  
                "swacode": "BTO",
                "websiteurl": "https://www.openreach.com",
            },
            {
                "systemid": "org-005",
                "name": "Leeds City Council Highways",
                "shortname": "LCC",
                "organisationtype": "highway_authority",  
                "swacode": "LCC",
                "websiteurl": "https://www.leeds.gov.uk",
            },
        ]

        for org_data in organisations:
            feature = ogr.Feature(layer.GetLayerDefn())
            feature.SetField("systemid", org_data["systemid"])
            feature.SetField("lifecyclestatus", "active")  
            feature.SetField("datelastupdated", datetime.now().isoformat())
            feature.SetField("dateoflastlifecyclestatuschange", datetime.now().isoformat())
            feature.SetField("systemloaddate", datetime.now().isoformat())
            feature.SetField("name", org_data["name"])
            feature.SetField("shortname", org_data["shortname"])
            feature.SetField("organisationtype", org_data["organisationtype"])
            feature.SetField("swacode", org_data["swacode"])
            feature.SetField("websiteurl", org_data["websiteurl"])
            layer.CreateFeature(feature)
            feature = None

    def _populate_contact_details(self):
        """Populate contact details for organisations"""
        print("Populating contact details...")
        assert self.ds is not None

        layer = self.ds.GetLayerByName("contactdetails")

        contacts = [
            {
                "systemid": "ctc-001",
                "organisationname": "Northern Gas Networks",
                "contactdetailstype": "planning_coordinator",  
                "departmentname": "Network Planning",
                "emailaddress": "planning@northerngas.co.uk",
                "telephonenumber": "0800 040 7766",
                "dataproviderid_fk": "org-001",
            },
            {
                "systemid": "ctc-002",
                "organisationname": "Yorkshire Water Services",
                "contactdetailstype": "asset_protection",  
                "departmentname": "Asset Management",
                "emailaddress": "assetprotection@yorkshirewater.co.uk",
                "telephonenumber": "0345 124 2424",
                "dataproviderid_fk": "org-002",
            },
            {
                "systemid": "ctc-003",
                "organisationname": "Northern Powergrid",
                "contactdetailstype": "project_manager",  
                "departmentname": "Capital Projects",
                "emailaddress": "projects@northernpowergrid.com",
                "telephonenumber": "0800 011 3332",
                "dataproviderid_fk": "org-003",
            },
            {
                "systemid": "ctc-004",
                "organisationname": "BT Openreach",
                "contactdetailstype": "planning_coordinator",  
                "departmentname": "Network Development",
                "emailaddress": "networkplanning@openreach.co.uk",
                "telephonenumber": "0800 023 2023",
                "dataproviderid_fk": "org-004",
            },
            {
                "systemid": "ctc-005",
                "organisationname": "Leeds City Council Highways",
                "contactdetailstype": "emergency_contact",  
                "departmentname": "Highway Services",
                "emailaddress": "highways@leeds.gov.uk",
                "telephonenumber": "0113 222 4444",
                "dataproviderid_fk": "org-005",
            },
        ]

        for contact_data in contacts:
            feature = ogr.Feature(layer.GetLayerDefn())
            for field, value in contact_data.items():
                feature.SetField(field, value)
            feature.SetField("lifecyclestatus", "active")  
            feature.SetField("datelastupdated", datetime.now().isoformat())
            feature.SetField("dateoflastlifecyclestatuschange", datetime.now().isoformat())
            feature.SetField("systemloaddate", datetime.now().isoformat())
            layer.CreateFeature(feature)
            feature = None

    def _populate_organisation_relationships(self):
        """Populate organisation to contact relationships"""
        print("Populating organisation relationships...")
        assert self.ds is not None

        layer = self.ds.GetLayerByName("relationship_organisationtocontactdetails")

        relationships = [
            ("rel-001", "org-001", "ctc-001", "org-001"),
            ("rel-002", "org-002", "ctc-002", "org-002"),
            ("rel-003", "org-003", "ctc-003", "org-003"),
            ("rel-004", "org-004", "ctc-004", "org-004"),
            ("rel-005", "org-005", "ctc-005", "org-005"),
        ]

        for rel_id, org_id, contact_id, provider_id in relationships:
            feature = ogr.Feature(layer.GetLayerDefn())
            feature.SetField("systemid", rel_id)
            feature.SetField("lifecyclestatus", "active")  
            feature.SetField("datelastupdated", datetime.now().isoformat())
            feature.SetField("dateoflastlifecyclestatuschange", datetime.now().isoformat())
            feature.SetField("systemloaddate", datetime.now().isoformat())
            feature.SetField("linkedorganisationid", org_id)
            feature.SetField("linkedcontactdetailsid", contact_id)
            feature.SetField("dataproviderid_fk", provider_id)
            layer.CreateFeature(feature)
            feature = None

    def _populate_planned_programmes(self):
        """Populate planned programmes"""
        print("Populating planned programmes...")
        assert self.ds is not None

        layer = self.ds.GetLayerByName("plannedprogramme")

        programmes = [
            {
                "systemid": "prg-001",
                "programmename": "Leeds City Centre Gas Main Replacement 2025",
                "programmetype": "asset_replacement",  
                "programmedescription": "Replacement of aging cast iron mains with modern PE pipes in Leeds city centre",
                "plannedstartdate": (datetime.now() + timedelta(days=60)).strftime(
                    "%Y-%m-%d"
                ),
                "plannedenddate": (datetime.now() + timedelta(days=240)).strftime(
                    "%Y-%m-%d"
                ),
                "dataproviderid_fk": "org-001",
                "datasensitivitylevel": "restricted",  
            },
            {
                "systemid": "prg-002",
                "programmename": "Yorkshire Clean Water Investment Programme",
                "programmetype": "capital_investment",  
                "programmedescription": "Major investment to improve water quality and reduce leakage",
                "plannedstartdate": (datetime.now() + timedelta(days=90)).strftime(
                    "%Y-%m-%d"
                ),
                "plannedenddate": (datetime.now() + timedelta(days=365)).strftime(
                    "%Y-%m-%d"
                ),
                "dataproviderid_fk": "org-002",
                "datasensitivitylevel": "public",  
            },
            {
                "systemid": "prg-003",
                "programmename": "Smart Grid Upgrade Programme",
                "programmetype": "network_reinforcement",  
                "programmedescription": "Installation of smart meters and grid monitoring equipment",
                "plannedstartdate": (datetime.now() + timedelta(days=30)).strftime(
                    "%Y-%m-%d"
                ),
                "plannedenddate": (datetime.now() + timedelta(days=180)).strftime(
                    "%Y-%m-%d"
                ),
                "dataproviderid_fk": "org-003",
                "datasensitivitylevel": "restricted",  
            },
            {
                "systemid": "prg-004",
                "programmename": "Fibre to the Premises Rollout - Leeds",
                "programmetype": "network_expansion",  
                "programmedescription": "FTTP deployment to residential and business premises",
                "plannedstartdate": (datetime.now() + timedelta(days=45)).strftime(
                    "%Y-%m-%d"
                ),
                "plannedenddate": (datetime.now() + timedelta(days=300)).strftime(
                    "%Y-%m-%d"
                ),
                "dataproviderid_fk": "org-004",
                "datasensitivitylevel": "public",  
            },
            {
                "systemid": "prg-005",
                "programmename": "Leeds City Centre Cycling Infrastructure Development",
                "programmetype": "cycle_network_development",  
                "programmedescription": "Development of segregated cycle routes in the city center",
                "plannedstartdate": (datetime.now() + timedelta(days=120)).strftime(
                    "%Y-%m-%d"
                ),
                "plannedenddate": (datetime.now() + timedelta(days=365)).strftime(
                    "%Y-%m-%d"
                ),
                "dataproviderid_fk": "org-005",
                "datasensitivitylevel": "public",  
            },
        ]

        for prog_data in programmes:
            feature = ogr.Feature(layer.GetLayerDefn())
            for field, value in prog_data.items():
                feature.SetField(field, value)
            feature.SetField("lifecyclestatus", "active")  
            feature.SetField("datelastupdated", datetime.now().isoformat())
            feature.SetField("dateoflastlifecyclestatuschange", datetime.now().isoformat())
            feature.SetField("systemloaddate", datetime.now().isoformat())
            feature.SetField("certification", "Provisional")
            feature.SetField("dataproviderassigneduniqueid", prog_data["systemid"])
            feature.SetField("dataproviderassigneduniqueidautoassigned", 1)
            layer.CreateFeature(feature)
            feature = None

    def _populate_network_links(self):
        """Populate network links with line geometries and USRN references"""
        print("Populating network links...")
        assert self.ds is not None

        layer = self.ds.GetLayerByName("networklink")

        # Define network links in Leeds area with USRN references
        links = [
            # EXAMPLE 1: Gas main replacement - existing infrastructure being replaced
            {
                "systemid": "nl-001",
                "objectname": "Park Lane Gas Main",
                "description": "315mm PE gas main replacement",
                "utilitytype": "gas",  
                "utilitysubtype": "Medium Pressure",
                "plannedmaterial": "pe (polyethylene)",  
                "plannedinstallationmethod": "open_cut",  
                "planneddepth_depth": 1.2,
                "worktype": "full_replacement",  
                "plannedstartdate": (datetime.now() + timedelta(days=75)).strftime(
                    "%Y-%m-%d"
                ),
                "plannedenddate": (datetime.now() + timedelta(days=90)).strftime(
                    "%Y-%m-%d"
                ),
                "confidencelevel": "confirmed",  
                "usrn": "40701234",
                "operationalstatus": "in_service", 
                "localereference": "Park Lane",
                "localereferencetype": "Street Name",
                "dataproviderid_fk": "org-001",
                "programmeid_fk": "prg-001",
                "conveyancemethod": "medium_pressure",
                "schemestatus": "approved",
                "coords": [(430100, 433875), (430300, 433875)],
            },
            # EXAMPLE 2: New gas main extension - proposed new infrastructure
            {
                "systemid": "nl-002",
                "objectname": "The Headrow Gas Main Extension",
                "description": "New 250mm PE gas main",
                "utilitytype": "gas",  
                "utilitysubtype": "Medium Pressure",
                "plannedmaterial": "pe (polyethylene)",  
                "plannedinstallationmethod": "directional_drilling",  
                "planneddepth_depth": 1.5,
                "worktype": "new_installation",  
                "plannedstartdate": (datetime.now() + timedelta(days=80)).strftime(
                    "%Y-%m-%d"
                ),
                "plannedenddate": (datetime.now() + timedelta(days=95)).strftime(
                    "%Y-%m-%d"
                ),
                "confidencelevel": "highly_likely",  
                "usrn": "40701235",
                "operationalstatus": "proposed",  
                "localereference": "The Headrow",
                "localereferencetype": "Street Name",
                "dataproviderid_fk": "org-001",
                "programmeid_fk": "prg-001",
                "conveyancemethod": "medium_pressure",
                "schemestatus": "approved", 
                "coords": [(430300, 433875), (430500, 433875), (430500, 433925)],
            },
            # EXAMPLE 3: Water main renewal - aging infrastructure scheduled for replacement
            {
                "systemid": "nl-003",
                "objectname": "Kirkstall Road Water Main",
                "description": "300mm ductile iron water main renewal",
                "utilitytype": "water",  
                "utilitysubtype": "Potable Water",
                "plannedmaterial": "ductile iron",  
                "plannedinstallationmethod": "open_cut",  
                "planneddepth_depth": 1.0,
                "worktype": "full_replacement",  
                "plannedstartdate": (datetime.now() + timedelta(days=100)).strftime(
                    "%Y-%m-%d"
                ),
                "plannedenddate": (datetime.now() + timedelta(days=130)).strftime(
                    "%Y-%m-%d"
                ),
                "confidencelevel": "highly_likely",  
                "usrn": "40705678",
                "operationalstatus": "unfit_for_service",  
                "localereference": "Kirkstall Road (A65)",
                "localereferencetype": "Road Name",
                "dataproviderid_fk": "org-002",
                "programmeid_fk": "prg-002",
                "conveyancemethod": "pressure",
                "schemestatus": "in_progress",
                "coords": [(428500, 434175), (428750, 434175), (429000, 434175)],
            },
            # EXAMPLE 4: Infrastructure under construction
            {
                "systemid": "nl-004",
                "objectname": "Commercial Street Water Connection",
                "description": "New 150mm water main for development",
                "utilitytype": "water",  
                "utilitysubtype": "Potable Water",
                "plannedmaterial": "hdpe",  
                "plannedinstallationmethod": "moling",  
                "planneddepth_depth": 0.8,
                "worktype": "new_installation",  
                "plannedstartdate": (datetime.now() + timedelta(days=45)).strftime(
                    "%Y-%m-%d"
                ),
                "plannedenddate": (datetime.now() + timedelta(days=50)).strftime(
                    "%Y-%m-%d"
                ),
                "confidencelevel": "confirmed",  
                "usrn": "40702345",
                "operationalstatus": "under_construction",  
                "localereference": "Commercial Street",
                "localereferencetype": "Street Name",
                "dataproviderid_fk": "org-002",
                "programmeid_fk": "prg-002",
                "conveyancemethod": "pressure",
                "schemestatus": "approved",
                "coords": [(430600, 433500), (430600, 433600)],
            },
            # EXAMPLE 5: Abandoned infrastructure scheduled for removal
            {
                "systemid": "nl-005",
                "objectname": "City Square 11kV Cable",
                "description": "11kV HV cable upgrade",
                "utilitytype": "electricity",  
                "utilitysubtype": "High Voltage",
                "plannedmaterial": "steel", 
                "plannedinstallationmethod": "directional_drilling",  
                "planneddepth_depth": 1.5,
                "worktype": "removal",  
                "plannedstartdate": (datetime.now() + timedelta(days=45)).strftime(
                    "%Y-%m-%d"
                ),
                "plannedenddate": (datetime.now() + timedelta(days=60)).strftime(
                    "%Y-%m-%d"
                ),
                "confidencelevel": "confirmed",  
                "usrn": "40703456",
                "operationalstatus": "abandoned",  
                "localereference": "City Square",
                "localereferencetype": "Named Location",
                "dataproviderid_fk": "org-003",
                "programmeid_fk": "prg-003",
                "conveyancemethod": "high_voltage",
                "schemestatus": "approved",
                "coords": [(430450, 433600), (430450, 433500), (430350, 433500)],
            },
            # Additional network links with proper status values
            {
                "systemid": "nl-006",
                "objectname": "Wellington Street LV Feed",
                "description": "New LV cable for street lighting",
                "utilitytype": "electricity",  
                "utilitysubtype": "Street Lighting",
                "plannedmaterial": "copper",  
                "plannedinstallationmethod": "open_cut",  
                "planneddepth_depth": 0.6,
                "worktype": "new_installation",  
                "plannedstartdate": (datetime.now() + timedelta(days=50)).strftime(
                    "%Y-%m-%d"
                ),
                "plannedenddate": (datetime.now() + timedelta(days=55)).strftime(
                    "%Y-%m-%d"
                ),
                "confidencelevel": "likely",  
                "usrn": "40704567",
                "operationalstatus": "proposed",
                "localereference": "Wellington Street",
                "localereferencetype": "Street Name",
                "dataproviderid_fk": "org-003",
                "programmeid_fk": "prg-003",
                "conveyancemethod": "low_voltage",
                "schemestatus": "proposed",
                "coords": [(430200, 433400), (430300, 433400), (430400, 433400)],
            },
            {
                "systemid": "nl-007",
                "objectname": "Hyde Park Fibre Route",
                "description": "96-fibre optic cable installation",
                "utilitytype": "telecommunications",  
                "utilitysubtype": "Fibre Optic",
                "plannedmaterial": "fibre optic",  
                "plannedinstallationmethod": "moling",  
                "planneddepth_depth": 0.6,
                "worktype": "new_installation",  
                "plannedstartdate": (datetime.now() + timedelta(days=60)).strftime(
                    "%Y-%m-%d"
                ),
                "plannedenddate": (datetime.now() + timedelta(days=75)).strftime(
                    "%Y-%m-%d"
                ),
                "confidencelevel": "likely",  
                "usrn": "40706789",
                "operationalstatus": "proposed",
                "localereference": "Hyde Park Corner",
                "localereferencetype": "Area Name",
                "dataproviderid_fk": "org-004",
                "programmeid_fk": "prg-004",
                "conveyancemethod": "other",
                "schemestatus": "public_consultation",
                "coords": [(429800, 435150), (429900, 435150), (430000, 435150)],
            },
            {
                "systemid": "nl-008",
                "objectname": "Woodhouse Lane Duct Route",
                "description": "Replace existing copper with fibre",
                "utilitytype": "telecommunications",  
                "utilitysubtype": "Fibre Optic",
                "plannedmaterial": "fibre optic",  
                "plannedinstallationmethod": "other",  
                "planneddepth_depth": 0.5,
                "worktype": "full_replacement",  
                "plannedstartdate": (datetime.now() + timedelta(days=65)).strftime(
                    "%Y-%m-%d"
                ),
                "plannedenddate": (datetime.now() + timedelta(days=70)).strftime(
                    "%Y-%m-%d"
                ),
                "confidencelevel": "highly_likely",  
                "usrn": "40707890",
                "operationalstatus": "in_service",
                "localereference": "Woodhouse Lane",
                "localereferencetype": "Street Name",
                "dataproviderid_fk": "org-004",
                "programmeid_fk": "prg-004",
                "conveyancemethod": "other",
                "schemestatus": "funded",
                "coords": [(429700, 435250), (429800, 435250), (429900, 435250)],
            },
            # Cycling infrastructure example
            {
                "systemid": "nl-010",
                "objectname": "The Headrow Cycle Lane",
                "description": "New segregated cycle lane installation",
                "utilitytype": "cycling_infrastructure",  
                "utilitysubtype": "Cycle Lane",
                "plannedmaterial": "asphalt",  
                "plannedinstallationmethod": "open_cut",  
                "planneddepth_depth": 0.3,
                "worktype": "new_installation",  
                "plannedstartdate": (datetime.now() + timedelta(days=120)).strftime(
                    "%Y-%m-%d"
                ),
                "plannedenddate": (datetime.now() + timedelta(days=180)).strftime(
                    "%Y-%m-%d"
                ),
                "confidencelevel": "likely",  
                "usrn": "40701236",
                "operationalstatus": "proposed",
                "localereference": "The Headrow",
                "localereferencetype": "Street Name",
                "dataproviderid_fk": "org-005",
                "programmeid_fk": "prg-005",
                "conveyancemethod": "other",
                "schemestatus": "public_consultation",
                "cycleschemedetails": "2m wide segregated cycle lane with junction improvements and new signaling",
                "coords": [(430350, 433800), (430450, 433800), (430550, 433800)],
            },
            # Multiple utilities - coordination example
            {
                "systemid": "nl-009",
                "objectname": "Otley Road Multi-Utility Corridor",
                "description": "Shared trench for multiple utilities",
                "utilitytype": "other",  
                "utilitysubtype": "Other",
                "plannedmaterial": "other",  
                "plannedinstallationmethod": "open_cut",  
                "planneddepth_depth": 1.0,
                "worktype": "relocation",  
                "plannedstartdate": (datetime.now() + timedelta(days=150)).strftime(
                    "%Y-%m-%d"
                ),
                "plannedenddate": (datetime.now() + timedelta(days=200)).strftime(
                    "%Y-%m-%d"
                ),
                "confidencelevel": "possible",  
                "usrn": "40709012",
                "operationalstatus": "in_service",
                "localereference": "A660/Shaw Lane Junction",
                "localereferencetype": "Junction",
                "dataproviderid_fk": "org-005",
                "programmeid_fk": None,
                "conveyancemethod": "other",
                "schemestatus": "feasibility_study",
                "coords": [(428200, 437400), (428300, 437400), (428400, 437400)],
            },
        ]

        for link_data in links:
            feature = ogr.Feature(layer.GetLayerDefn())

            # Set all fields except geometry
            for field, value in link_data.items():
                if field != "coords" and value is not None:
                    feature.SetField(field, value)
            
            # Set standard fields
            feature.SetField("lifecyclestatus", "active")  
            feature.SetField("datelastupdated", datetime.now().isoformat())
            feature.SetField("dateoflastlifecyclestatuschange", datetime.now().isoformat())
            feature.SetField("systemloaddate", datetime.now().isoformat())
            feature.SetField("planneddepth_unitofmeasure", "metres")  
            feature.SetField("datasensitivitylevel", "public")  
            feature.SetField("featuretype", "NetworkLink")
            feature.SetField("componenttype", link_data["utilitytype"])
            feature.SetField("plannedinstallationdate", link_data["plannedstartdate"])

            # Set data owner to match data provider
            feature.SetField("dataowner", link_data["dataproviderid_fk"])
            feature.SetField("operator", link_data["dataproviderid_fk"])
            feature.SetField("objectowner", link_data["dataproviderid_fk"])

            # Create line geometry
            line = ogr.Geometry(ogr.wkbLineString)
            for coord in link_data["coords"]:
                line.AddPoint(coord[0], coord[1])

            feature.SetGeometry(line)
            layer.CreateFeature(feature)
            feature = None

    def _populate_unified_table(self):
        """Populate the unified future works table with all joined data"""
        print("Creating unified future works table...")
        assert self.ds is not None

        sql = """
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
        WHERE nl.lifecyclestatus = 'active'
        """

        self.ds.ExecuteSQL(sql)
        print("Unified table populated successfully!")

    def generate_summary_report(self):
        """Generate a summary report of the populated data"""
        print("\n" + "=" * 60)
        print("MUDDI NETWORK LINK GEOPACKAGE POPULATION SUMMARY")
        print("=" * 60)

        self.ds = ogr.Open(self.geopackage_path, 0)  

        tables = [
            "organisation",
            "contactdetails",
            "plannedprogramme",
            "networklink",
            "relationship_organisationtocontactdetails",
            "future_works_unified",
        ]

        print(f"\nGeoPackage: {self.geopackage_path}")
        print(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nTable Record Counts:")
        print("-" * 40)

        for table_name in tables:
            layer = self.ds.GetLayerByName(table_name)
            if layer:
                count = layer.GetFeatureCount()
                print(f"{table_name:<40} {count:>5} records")

        print("\nNetwork Link Summary:")
        print("-" * 40)

        # Get network links summary
        layer = self.ds.GetLayerByName("networklink")
        if layer:
            layer.SetAttributeFilter("lifecyclestatus = 'active'")
            active_count = layer.GetFeatureCount()
            print(f"Active network links: {active_count}")

            # Get date range
            layer.ResetReading()
            dates = []
            for feature in layer:
                start_date = feature.GetField("plannedstartdate")
                if start_date:
                    dates.append(start_date)

            if dates:
                print(f"Earliest planned start: {min(dates)}")
                print(f"Latest planned start: {max(dates)}")

            print("\nUtility Type Distribution:")
            print("-" * 40)

            layer.ResetReading()
            layer.SetAttributeFilter(None)  # Remove filter
            utility_counts = {}
            for feature in layer:
                utility_type = feature.GetField("utilitytype")
                utility_counts[utility_type] = utility_counts.get(utility_type, 0) + 1

            for utility_type, count in sorted(utility_counts.items()):
                print(f"{utility_type:<30} {count:>5} links")


            print("\nOperational Status Distribution:")
            print("-" * 40)

            layer.ResetReading()
            status_counts = {}
            for feature in layer:
                operational_status = feature.GetField("operationalstatus")
                status_counts[operational_status] = status_counts.get(operational_status, 0) + 1

            for status, count in sorted(status_counts.items()):
                print(f"{status:<30} {count:>5} links")

            print("\nScheme Status Distribution:")
            print("-" * 40)

            layer.ResetReading()
            scheme_counts = {}
            for feature in layer:
                scheme_status = feature.GetField("schemestatus")
                scheme_counts[scheme_status] = scheme_counts.get(scheme_status, 0) + 1

            for status, count in sorted(scheme_counts.items()):
                print(f"{status:<30} {count:>5} links")

            print("\nConveyance Method Distribution:")
            print("-" * 40)

            layer.ResetReading()
            method_counts = {}
            for feature in layer:
                conveyance_method = feature.GetField("conveyancemethod")
                method_counts[conveyance_method] = method_counts.get(conveyance_method, 0) + 1

            for method, count in sorted(method_counts.items()):
                print(f"{method:<30} {count:>5} links")

            print("\nWork Type Distribution:")
            print("-" * 40)

            layer.ResetReading()
            worktype_counts = {}
            for feature in layer:
                work_type = feature.GetField("worktype")
                worktype_counts[work_type] = worktype_counts.get(work_type, 0) + 1

            for work_type, count in sorted(worktype_counts.items()):
                print(f"{work_type:<30} {count:>5} links")

            print("\nOrganisation Distribution:")
            print("-" * 40)

            layer.ResetReading()
            org_counts = {}
            org_layer = self.ds.GetLayerByName("organisation")

            # Build org lookup
            org_names = {}
            org_layer.ResetReading()
            for feature in org_layer:
                org_names[feature.GetField("systemid")] = feature.GetField("name")

            # Count by organisation
            layer.ResetReading()
            for feature in layer:
                org_id = feature.GetField("dataproviderid_fk")
                org_name = org_names.get(org_id, "Unknown")
                org_counts[org_name] = org_counts.get(org_name, 0) + 1

            for org_name, count in sorted(org_counts.items()):
                print(f"{org_name:<30} {count:>5} links")

            print("\nData Quality Check:")
            print("-" * 40)

            layer.ResetReading()
            missing_operational_status = 0
            missing_scheme_status = 0
            missing_confidence_level = 0
            missing_usrn = 0

            for feature in layer:
                if not feature.GetField("operationalstatus"):
                    missing_operational_status += 1
                if not feature.GetField("schemestatus"):
                    missing_scheme_status += 1
                if not feature.GetField("confidencelevel"):
                    missing_confidence_level += 1
                if not feature.GetField("usrn"):
                    missing_usrn += 1

            print(f"Missing operational status: {missing_operational_status}")
            print(f"Missing scheme status: {missing_scheme_status}")
            print(f"Missing confidence level: {missing_confidence_level}")
            print(f"Missing USRN: {missing_usrn}")

        self.ds = None
        print("\n" + "=" * 60)


def main():
    """Main function"""
    # Default GeoPackage path
    geopackage_path = "uk_future_works_example.gpkg"

    # Check command line arguments
    if len(sys.argv) > 1:
        geopackage_path = sys.argv[1]

    # Check if GeoPackage exists
    if not os.path.exists(geopackage_path):
        print(f"Error: GeoPackage not found: {geopackage_path}")
        print("Please run the create_uk_future_works_profile.py script first.")
        sys.exit(1)

    # Populate the GeoPackage
    populator = UKFutureWorksProfileGeoPackagePopulate(geopackage_path)
    populator.populate_geopackage()

    # Generate summary report
    populator.generate_summary_report()

    print(
        "\nThe GeoPackage has been populated with sample MUDDI-compliant network link data."
    )
    print(
        "You can now open it in QGIS or any GeoPackage-compatible software to view the data."
    )
    print(
        "\nIMPORTANT: Use the 'future_works_unified' layer for viewing all data in one place."
    )
    print(
        "This layer contains all organisation, contact, and programme information joined together."
    )
    print(
        "The GeoPackage now includes proper operational status values for all network links."
    )


if __name__ == "__main__":
    main()