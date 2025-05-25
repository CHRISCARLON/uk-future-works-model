# UK Future Works Profile GeoPackage

A standardised GeoPackage for sharing planned utility works between utility companies and local authorities in the UK.

Version 0.1.1

## Overview

This project generates a standardised GeoPackage containing information about planned utility works and network infrastructure upgrades, enabling effective coordination between organisations for street works and infrastructure planning.

## Features

- Creates a UK Future Works Profile GeoPackage with all necessary tables and relationships
- Populated with sample data for organisations, planned network links, and programmes
- Uses British National Grid (EPSG:27700) as the spatial reference system
- Implements standardised code lists for utility types, work status, etc.
- Includes user-friendly unified view with all data joined in one place

## Key Tables

- **Organisation tables**: organisation, contactdetails
- **Future works tables**: plannedprogramme, networklink
- **Relationship tables**: relationship_organisationtocontactdetails
- **Code list tables**: 16 reference tables with standardised values
- **Unified view**: future_works_unified for easy data access

## Getting Started

1. Ensure GDAL is installed on your system
2. Run `python src/create_uk_future_works_profile.py` to generate an empty GeoPackage
3. Run `python src/populate_uk_future_works_profile.py` to fill it with sample data
4. Open the resulting `uk_future_works_example.gpkg` file in QGIS or other GIS software
5. **Important**: Use the 'future_works_unified' layer for viewing all data in one place

## Requirements

- Python 3.x
- GDAL Python bindings
- Operating system with GDAL libraries installed (required to install GDAL python package)
- e.g. on Mac OS, run `brew install gdal`

## Data Model

The data model is focused on network links representing planned utility works and cycle network development:

- Organisations plan and manage programmes
- Network links represent future utility/cycle infrastructure changes
- Each link includes detailed metadata on timing, location, depth, and installation methods
- USRN (Unique Street Reference Number) links to authoritative identifiers for street locations
- All data is accessible through a unified view joining all related information - this is called the future_works_unified layer
