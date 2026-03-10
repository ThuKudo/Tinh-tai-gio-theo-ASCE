# UI Overview

Environment constraints prevented rendering a live screenshot inside the tool session, so this file documents the main screens.

## Main screen

- Top hero banner with:
  - app title `Win Load ASCE`
  - short statement that the app reproduces validated workbook logic
  - two status cards for workbook parity and workflow
- Left panel:
  - grouped form sections for project info, geometry, wind parameters, exposure/internal pressure, and advanced overrides
  - sample load, reset, import JSON, export input, export result, and export HTML report actions
  - inline validation messages under each field
- Right panel:
  - overview cards for design speed, qz, roof angle, mean roof height, Kz, and GCpi(+)
  - table cards for Case A pressures, Case B pressures, line-load labels, and intermediate values
  - calculation breakdown accordion
  - assumptions / notes list

## Interaction states

- Validation errors highlight fields in red and show a concise status banner.
- Successful calculations show a green status banner and update the `Last run` stamp.
- Form values persist in local browser storage so the user can refresh without losing work.

## Exported HTML report

- Printable white-background report with:
  - project header
  - headline metrics
  - full input table
  - Case A and Case B result tables
  - breakdown summary
  - assumptions list
