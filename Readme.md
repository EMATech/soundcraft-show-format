Soundcraft Si Session Show file format
--------------------------------------

## Extension
.SSH

Session show? Soundcraft Show?

## Format
Actual format is XML.

Unfortunately it's full of blobs but don't worry!

## XML Sections

### Device

### NODE

### Show
- name: (str) This is a cleartext attribute with the show name! Yay :)

### MHxDFile
- name: (str) Looks like a path and filename.
    - "\._ $SHOWS\Show_0\filename.ext"
- checksum: (int) Undetermined checksum. (Yet!)
- datalength: (int) Size of the uncompressed data blob in bytes. (Except it's wrong for the SS_xxxxx.dat file).
- content: blob

## Blobs
All blobs seem to start with the same header: 'eJz'.

Looks like some kind of data encoding or compression.

Base64? Most likely. The resulting files looks encoded or compressed though…

78 9C header. Doesn't that look like zlib? \o/

### Recipes

#### Decode & Extract
```sh
< "XML MHxDFile entity content in a file" base64 -d | zlib-flate -uncompress > file
```

#### Compress & Encode
```sh
< file zlib-flate -compress | base64 -w0 > "XML MHxDFile entity content in a file"
```

## Files

### ShowHdr.xml
The general show informations as this section is always unique.

#### Show
- Name: (str) The show name.
- activeCueList: (1) The cueListId of the currently active cueList.
- notes: (str) Does not seem to be exposed on the mixing desk!
    - ""
- deskType: (int) I have to find the other types.
    - 12 == Si Compact 16
- versionMajor: (int) The major version number of the firmware.
    - 3
- versionMinor: (int) The minor version number of the firmware.
    - 1
- build: (int) The build version number of the firmware.
    - 9

#### Snapshot
- snapshotId: (int)
- name: (str) "Unamed Snapshot 4" Does not seem to be exposed on the mixing desk!
- notes: (str) Does not seem to be exposed on the mixing desk!
    - ""

#### Cue
- cueId: (int) An ID for the cue.
- snapshotId: (int) Binds the cue to a snapshot.
- name: (str) The name of the cue.
- notes: (str) Does not seem to be exposed on the mixing desk!
    - ""
- midiProgChange: (bool as int) Enables midi program changing on cue recall.
- midiChannel: (int) The MIDI channel onto which sending the program change.
- midiProgNumber: (int) The MIDI program change message number.
- midiRxChannel: (int) The MIDI channel onto which receiving program changes.
- midiRxProgChange: (int?) Enables cue recall on MIDI progam change reception. Oddly, off value is 16.
- midiRxProgNumber: (int) The MIDI program change message number.
- hiQVenueRecall: (bool as int) Enables recalling HiQnet venue on cue recall.
- hiQVenueNumber: (int) The HiQnet venue number to recall.
- cueActive: (bool as int?) Does not seem to be exposed on the mixing desk!
- cueLocked: (bool as int?) Does not seem to be exposed on the mixing desk!
- dmxFadeTime: (int) My desk is not equiped with DMX but the performer model has a DMX port.
- audioRecall: (bool as int?) Certainly for the performer model to allow recalling only audio.
- dmxRecall: (bool as int?) Certainly for the performer model to allow recalling only DMX.

### IOModules.xml
Looks like the routing informations for the Show.

#### IOModuleDatabase

#### PhysicalIODeviceManager

#### PhysicalIODevice
- shortName: (str) The input or output name.
- description (str) Long description.
- serialNo: (int)
    - 39030 on all.
- versionNo: (int)
    - 256 on all.
- position: (int)
    - 255 for internal.
    - 0 for external.
- expansionCardType: (int)
    - O for internal.
    - 2 for my MULTI DIGITAL card.
- moduleType: (int)
    - 1 for internal.
    - 2 for my MULTI DIGITAL card.
- internalModuleType: (int)
    - 0 for my MULTI DIGITAL card.
    - 1 for MIC.
    - 2 for Line and internal Lexicon return.
    - 3 for GRAUX output module.
    - 5 for AES in.
    - 6 for AES out.

#### InternalAudioDevice
- shortName: (str)
    - "" on all.
- description: (str)
    - "" on all.
- serialNo: (int)
    - 4660 on all.
- audioDeviceType: (int)
    - 1 for all internal.
    - 5 for my MULTI DIGITAL card.

#### AudioIOModuleRangeManager

#### AudioIOModuleRange
- logicalStart: (int) The I/O position start.
- logicalEnd: (int) The I/O position end.
- IOmoduleType: (int)
    - 1 for all internal.
    - 2 for my external MULTI DIGITAL card.
- logicalIOType: (int)
    - 1 for MIC inputs.
    - 2 for Line inputs.
    - 3 for Internal Lexicon return.
    - 5 for AES input.
    - 8 for GRAUX output module.
    - 17 for AES output.
    - 4 for external inputs ?
    - 12 for external outputs ?
- discovered: (bool as int?)
    - 1 for all.
- inShow: (bool as int?)
    - 1 for all.
- eAvailable: (bool as int?) Electrically available?
    - 1 for physical I/O.
    - 0 for inexistant I/O (MIC 16 to 63).

#### UnknownExternalAudioDevice
Same as InternalAudioDevice for my MULTI DIGITAL card.

### \*.dat files
Looks like memory dumps. 180kB. Very similar content.

Start with "Snapshot" header.

#### SS_xxxxx.dat
Purpose unknown. Certainly the current state since it's restored on show loading.

#### SS_x.dat
x = snaphotId from ShowHdr.xml

Looks like the cues. The number of sections match the number of cues of the show.
