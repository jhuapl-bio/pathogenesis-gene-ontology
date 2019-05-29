[![Build Status](https://travis-ci.org/rjacak/pathogenesis-gene-ontology.svg?branch=master)](https://travis-ci.org/rjacak/pathogenesis-gene-ontology)
[//]: # ([![DOI](https://zenodo.org/badge/13996/rjacak/pathogenesis-gene-ontology.svg)](https://zenodo.org/badge/latestdoi/13996/rjacak/pathogenesis-gene-ontology))

# PathGO: the Pathogenesis Gene Ontology

| | |
|---|---|
| Authors | Ron Jacak ([rjacak](http://github.com/rjacak)) |
| | Jody Proescher ([jproesch](https://github.com/jproesch)) |

## Description

This ontology contains terms to describe the function of genes and gene products involved in pathogenesis.  Genes that encode toxins, virulence factors, and antimicrobial resistance have functions that are not represented well by the terms contained within the Gene Ontology or any of the other OBO Foundry ontologies.  This ontology will collect and maintain common terms and descriptions of concepts related to pathogenesis, and could help provide more intuitive descriptions of function for these types of sequences.

## Versions

### Stable release versions

The latest version of the ontology can always be found at:

http://purl.obolibrary.org/obo/pathgo.owl

(note this will not show up until the request has been approved by OBO Foundry)

### Editors' version

PathGO would welcome contributions from the community!  Contributors are encouraged to use Protege (https://protege.stanford.edu/) for ontology editing, and a Git-enabled command line environment for version control and to submit changes for integration.  Note, to edit this ontology, contributors should make changes to the "-edit" file, [src/ontology/pathgo-edit.owl](src/ontology/pathgo-edit.owl).

## Editing workflow

For contributors less experienced with Git and command line environments, we recommend a workflow using GitHub Desktop (https://desktop.github.com/).  Individuals should download and install GitHub Desktop, select the option to "Clone a Repository from the Internet...", search for the "pathogenesis_gene_ontology" repository, and clone it.  When prompted, you will be able to choose where the cloned repository files are saved.  **Choose an alternate location or make note of the default location, because you will need this path working with the ontology.**  Our recommended workflow for viewing the ontology and making changes is as follows:

1. From within GitHub Desktop, ensure that the current repository selected is 'pathogenesis_gene_ontology'.
2. Ensure that the "Current Branch" selected is 'master', and click "Fetch origin" to pull down the latest version of the ontology. 
3. Next, under the "Current Branch" menu, click the button to create a "New Branch", and give it a short name indicative of the changes you are making.
4. Click the button in the main window to publish the branch, which will create this branch in the GitHub repository.
5. Download and install Protege if not already available (https://protege.stanford.edu/)
6. From within Protege, open the ontology by navigating to the directory where the repository was cloned, descend into the 'src/ontology' folder, and open the [src/ontology/pathgo-edit.owl](src/ontology/pathgo-edit.owl) file. 
7. Update the settings for "New entities" in Protege (see below)
8. Make desired edits/comments to the ontology in Protege and save the changes.
9. Switch back to the GitHub Desktop application, and review all of the changes present.  Any changes that you don't want to be retained should be removed in Protege.  Alternatively, if you want to start back over with the original version of a file, you can right-click on the file and select "Discard Changes...".
10. Save the changes to your local Git repository by providing a short name and description in the boxes at the bottom left corner, and clicking "Commit to -name of your branch-".  Note, this will only save the changes on your computer.
11. Save the changes to a branch in the GitHub repository by clicking the 'Push origin' button in the main window.
12. Submit a request for the changes to be included into PathGO.  Under the "Current Branch" menu, click the "Pull requests" tab, and click the link at the bottom to "Create a pull request from the current branch".  This action will trigger a notification, i.e. a pull request, to the maintainers of PathGO who will review the changes and incorporate them, if approved.  If not approved, you will have the opportunity to make additional changes, save them in Protege, commit them in GitHub Desktop, push them to the origin, and retry the pull request. 

## Protege Settings

Current best ontology practices include identifying terms/classes with a Uniform Resource Identifier (URI).  PathGO is adopting the conventions that other ontologies within the OBO Foundry use including the use of Permanent URLs (PURLs) with a standard base prefix, as well as short-form identifiers (e.g. PATHGO:0000200) to identify terms.  Users should open the Protege Preferences pane and update the "New entities" tab with the following settings:
![New entity settings pane](static/protege_new_entity_settings.png)

Ensure that under "Auto-generated ID", the Prefix is set to "PATHGO\_", the digit count is 7, and the start is set to the number of last used id.

## Contact

Please use this repository's [Issue tracker](https://github.com/rjacak/pathogenesis-gene-ontology/issues) to request provide feedback, recommend new terms/classes, and/or report errors or specific concerns related to the ontology.  We would love to hear from you!

## Acknowledgements

This ontology repository was created using the [ontology starter kit](https://github.com/INCATools/ontology-starter-kit).  We thank Chris Mungall and any other developers for putting this utility together.

## Disclaimer

All information contained herein is, and remains the property of IARPA and JHUAPL.  Dissemination of this information or reproduction of this material is strictly forbidden unless prior written permission is obtained from IARPA and JHUAPL.
