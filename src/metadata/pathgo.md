---
layout: ontology_detail
id: pathgo
title: Pathogenesis gene ontology
jobs:
  - id: https://travis-ci.org/rjacak/pathogenesis-gene-ontology
    type: travis-ci
build:
  checkout: git clone https://github.com/rjacak/pathogenesis-gene-ontology.git
  system: git
  path: "."
contact:
  email: cjmungall@lbl.gov
  label: Chris Mungall
description: Pathogenesis gene ontology is an ontology...
domain: stuff
homepage: https://github.com/rjacak/pathogenesis-gene-ontology
products:
  - id: pathgo.owl
  - id: pathgo.obo
dependencies:
 - id: ro
 - id: go
tracker: https://github.com/rjacak/pathogenesis-gene-ontology/issues
license:
  url: http://creativecommons.org/licenses/by/3.0/
  label: CC-BY
---

Enter a detailed description of your ontology here
