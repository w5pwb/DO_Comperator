# DO_Comperator

DO-OMIM project	

Hi Phill,

This project has two parts, which I will describe here.  Part A is programmatically simpler and should be done first, then Part B.  Python 3 is fine for this project.

Part A: DO changes alone (independent of OMIM)

The Disease Ontology file (“do.obo”) is updated periodically.  The DO terms have an ID number and a name - please keep the DOID: in front of the DO numbers in the finished output.

Examples of DO obo files:
DOID.190301.obo -- latest version imported into FlyBase (attached)
DOID.181217.obo -- penultimate version imported into FlyBase (attached)

We need to know the following things:

- new DO terms
- obsoleted DO terms
- merged/split DO terms (not sure could detect these specifically, anyway would overlap with above two categories?)
- renamed DO terms

Since each DO.obo is organized by DO, you can compare the lines under each DO heading and see what the differences are.  If a DO id & name in the old file don’t exactly match an ID & name combo in the new file, that indicates a rename and/or a split and is important. A DO entry existing in one and not the other indicates new or obsoleted terms.

We get new do.obo files every two months or so. 

To do:
Generate a summary file showing a quick list of DOs that are changed, and then the before & after entries for a DO item that changed, with changed lines marked.  This should be a flat file, so the markup needs to both easy to see visually, and not based on color etc. 
We need to be able to run this in-house after each DO update, so please add variables at the top where we can enter the location of our old and new saved .obo files. (This could also be done with interactive variables, but that can get a bit annoying to enter each time, so let’s go with something in the .py text for now.

Part B: DO update comparison for specified diseases with OMIM assignments

We need to be able to efficiently identify new entries that correspond to existing disease models that we care about, i.e. ones with particular OMIM IDs attached.  This relies on what you will have done in Part A, but has the additional wrinkle of OMIM xrefs.

Note some things about OMIM cross-refs in the DO entries:
May be one, many, or no OMIM cross-refs for a given DO entry
We are interested in finding cases for which there is a new term-OMIM association.  These tend to come as one of 2 types:
New single OMIM cross-refs (these may not be new to DO, but are new as single cross-ref association)
Cases for which the new OMIM entry is one of many cross-refs
An issue: sometimes, an OMIM cross-ref appears BOTH as a single entry under a precise term (usually a new term-OMIM association) and as one of many under a more general term (typically not a new term-OMIM association). 

We have been maintaining a list of Human Disease Models (FB identifiers = FBhh numbers) that correspond to a precise OMIM entry, but for which there is no corresponding precise DO entry. In these cases, we annotate to a less precise DO entry, but we want to update that annotation if/when DO adds a precise term.
This list is in spreadsheet format: DO_imprecise_cases.xlsx (attached)
For most of the listed diseases, there is initially no OMIM cross-ref in DO (column G).
For a significant number, there is an OMIM cross-ref, but it is one of many (column F).
For a couple of screwed-up cases there is a single OMIM cross-ref for a general (not precise) DO entry (column E).

The task: 
From the list described above (DO_imprecise_cases.xlsx, attached), query the .obo files using the set of OMIM numbers provided in column D.  You can export those to a flat file first, and have that be one of the input files.
Identify the cases that have a new term-OMIM association between DO version X and DO version Y.  Ways that might happen include:
The OMIM cross-ref is the only OMIM cross-ref for that DO entry (these will usually be new DO term entries).
The new OMIM cross-ref is one of many cross-refs
Keep in mind that there will be some cases where an OMIM cross-ref appears BOTH as a single entry under a new precise term and as one of many under a more general term. This seems to happen commonly when a new precise DO entry is created -- the many-to-one entry is not updated in the same cycle and persists for awhile.
Generate a summary file showing a quick list of DOs and OMIMs that are changed, and then the before & after entries for a DO item that changed, with changed lines marked.
We need to be able to run this in-house after each DO update, so please add variables at the top where we can enter the location of our saved .obo files and the OMIM list.

True positive examples between these two sets:
FBhh0000305	epileptic encephalopathy, early infantile, 34	DOID:0050709	616645
FBhh0000307	epileptic encephalopathy, early infantile, 11	DOID:0050709	613721
FBhh0000318	nephrotic syndrome, type 1	DOID:2590	256300

Part B2: Camcur is interested in knowing this for all OMIM IDs, rather than a subset.  Could you please also make a little script that will isolate all unique OMIM IDs from two do.obo files?  Then they could use that as the input for the Part B script, rather than the trimmed-down list that Harvcur cares about.  If you want to be elegant, you could have this be an optional argument for the script that triggers those processes all in one go.  It will be easier to work on writing and debugging with the short list, so don’t worry about this until you have Part B nailed down.

I’m not sure whether you will have to index the .obos by DOID and by OMIM ID separately to get all the differences, or whether doing just one or the other will get you everything.


Thank you for working on this!  Please don’t hesitate to let me know if you have any questions - this project is a bit more elaborate than the previous ones.

Victoria
