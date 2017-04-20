# EDL SPEC RESOURCES
 - [EDL Specsheet](http://xmil.biz/EDL-X/CMX3600.pdf)
 - [In depth EDL info and usecases](http://www.edlmax.com/maxguide.html)


## notes and xcrrrrps

#[Cleaning EDLs - a Review](http://www.edlmax.com/maxguide.html)

Cleaning edit decision lists is an important part of EDL management. It is usually performed by a computer program external to the editor. It assures that the events in the EDL represent the material recorded on the edit master precisely and are organized in a meaningful way. While the need for cleaning is more obvious in conventional video editing it still has relevance to non-linear systems.

What is EDL "cleaning"?

In conventional video editing, edits are recorded to tape and "events" representing them are recorded in the EDL. As editing progresses it may become necessary to re-record a section of the master. This changes the contents of the tape and adds an event to the EDL, but it does not, generally, update the previously recorded event (or events) at that location of the master. This leaves a "dirty" event (or events) in the list.

Over-records

The first most obvious example of a "dirty" event is the situation where the tail of a previous event is over-recorded:

A previously recorded event:
 001  001   V     C        01:35:11:00 01:35:26:00 01:00:00:00 01:00:15:00
Now the current event "over-records" the tail of it:
 002  002   V     C        02:02:16:22 02:02:18:22 01:00:14:00 01:00:16:00
Note that edit 002 goes in at 01:00:14:00, a second earlier than the out point of edit 001. Pictorially:


An EDL cleaning program would change these edits to:
 001  001   V     C        01:35:11:00 01:35:25:00 01:00:00:00 01:00:14:00

002  002   V     C        02:02:16:22 02:02:18:22 01:00:14:00 01:00:16:00


Note that the source OUT and record OUT of edit 001 have been trimmed 1:00 earlier. The list (only two edits) is now "clean" - the extra frames on the tail of edit 001 are removed and edit 002 follows it exactly.

Inserts

Another slightly more complex example is the situation where an event is "inserted" into a previous event. First, a previous event exists in the list:

 001  001   V     C        01:35:11:00 01:35:26:00 01:00:00:00 01:00:15:00
Now the current event is "inserted" in the middle of it:

 002  002   V     C        02:02:16:22 02:02:21:22 01:00:07:00 01:00:12:00

To clean this situation we need to make a new event. An EDL cleaning program would change these edits to:
 001  001   V     C        01:35:11:00 01:35:16:00 01:00:00:00 01:00:07:00

002  002   V     C        02:02:16:22 02:02:21:22 01:00:07:00 01:00:12:00

100  001   V     C        01:35:24:00 01:35:26:00 01:00:12:00 01:00:15:00


The first edit has been broken in two by the second edit - edit 001s OUT points have been trimmed to match the IN of edit 002, and edit 100 (the third "created" edit) is the remainder of edit 001 (the tail of it).

These two examples illustrate the essence of cleaning EDLs. Needless to say, it becomes rather complex as the subtleties of Video and 4 Audio channels, dissolves, wipes, keys, split edits, etc. are considered.

Why is cleaning important?

A clean list is important for several reasons:

A) A clean list is very much easier for humans to read.
B) A clean list is essential for ON-line assembly.
C) A list must be absolutely clean if the events are sorted.
A "raw" or "dirty" EDL is virtually impossible to read. For any event you may be scrutinizing it is very difficult to see whether another edit somewhere in the list may have altered it. When you are looking for a shot, or using the list for logging purposes, etc. a clean list is a must.

A clean list is critical for ON-line assembly. If the assembly proceeded exactly the way the "raw" list was created, it would work, but it is obviously inefficient to execute all the edits of the Off-line. A strictly "sequential" (A-mode) assembly can be very in-efficient, especially when creative and technical requirements of ON-line are considered. Effects, audio mixing/levels, TBC "painting" all effect the order in which events are selected for execution. With a clean list, the show will fit together no matter the order it is done. If the list is dirty, you have a nightmare.

Sorting EDLs is a useful tool for may purposes, especially optimizing EDLs for assembly. A list must be clean if it is to be sorted. If the list is dirty and the order of the events is changed, the EDL may be wrong. Consider what would happen if the two edits of the "over-record" example, above, were to be reversed in order (edit 002 preceding edit 001). The assembly of those two edits would be entirely incorrect!

# Timecode - A Review

Timecode is an electronic signal which labels video frames on video tape. The ideas for the format were invented by NASA for telemetry tapes tracking space missions. The concept was adopted by EECO in 1967 for video editing, and, after many folks had built similar (but in-compatible) systems, SMPTE created the standard in 1969. The European Broadcasting Union adopted the standard and it is now called SMPTE/EBU (referred to simply as "timecode").

Timecode may be recorded on tape in two ways:

A) Longitudinal Time Code, or LTC, is recorded on an audio channel or a dedicated "address" channel.
B) Vertical Interval Time Code or VITC, is recorded in the vertical interval of the video signal itself.
These two formats are similar as far as the edit information they contain.

Longitudinal Time Code (LTC) is an electronic signal that switches from one voltage to another, forming a string of pulses, or bits. Each one-second long chunk of this signal is "sliced" into 2400 parts (for NTSC) or 2000 parts (for PAL/SECAM). This makes 80 time code bits for each video frame:

NTSC 2400 bits/sec divided by 30 frames/sec = 80 bits/frame PAL/SECAM 2000 bits/sec divided by 25 frames/sec = 80 bits/frame

These 80 bits are given certain assignments according to the standard. There are these important groups of information:

A) The hours/minutes/seconds/frames
B) Drop-frame flag - Whether this timecode is Drop-frame
C) Color-frame Flag - Whether color-framing is intended
D) User bits - "leftover" bits available for user assignment.
E) "Sync word" - Tells an electronic reader where the frame information begins & ends and which direction the tape is moving.
F) "Sync bits" - Help verify (together with the sync word) the position of the data as the tape moves.
VITC (Vertical Interval Time Code) format adds 10 extra bits to each frame label. These add the following to the LTC list, above:

A) Additional "sync" bits between data bit groups.
B) Field bit (allows video-field indexing accuracy).
C) Cyclical Redundancy Check Code (CRC), used for error detection.
The hours/minutes/seconds/frames is the primary information we are interested in. This data is Drop-frame, Non-drop frame or EBU (25 frames/sec, PAL/SECAM) as indicated by the "drop-frame" flag.

The "sync word" and "sync bits" are the heart of how timecode works. As the tape moves, these bits instruct the electronic reader which direction the tape is moving, where the hours/minutes/seconds/frames, drop-frame bit, etc. are located and (if properly aligned on the tape) where the video frames themselves are located with respect to the timecode stream.

All of this is pretty clever, when you think about it. The tape is moving at an unknown speed in either direction as the machine is used, yet the timecode can be read at all times (given a good recording and properly functioning equipment). Note that, at microscopic levels, the tape is jumping and jittering across the reader heads, stopping, reversing direction, going into fast-forward, etc. The sync words and the design of the readers makes it all work! Cool.

NTSC timecode comes in two flavors - Non-drop frame and Drop-frame, and there is only one PAL/SECAM, sometimes called "EBU". These are usually displayed as:

Most sytems:
Non-dropframe: 1:00:00:00 - colon in last position
Dropframe: 1:00:00;00 - semicolon in last position
PAL/SECAM: 1:00:00:00 - colon in last position
SONY:
Non-dropframe: 1:00:00.00 - period in last position
Dropframe: 1:00:00,00 - comma in last position
PAL/SECAM: 1:00:00.00 - period in last position
NTSC - DROP Frame versus NON-DROP, and PAL (EBU)

Non-drop Frame

NTSC video actually runs at 29.97 frames per second, not 30 fps, as is usually implied. If you label all the NTSC frames incrementally, as with NON-DROP FRAME, a 01:00:00:00 label (a colon in the last position indicates non-drop frame) will represent 108,000 video frames (from zero). 108,000 NTSC video frames actually takes 01:00:03:18 to play back. In other words, 01:00:00:00 in NON-DROP frame is not truly 1 hour, but 1 hour and 3 seconds, 18 frames.

This leads to the inconvenient fact that timecode calculations do not represent real-time. 2:00:00:00 minus 1:00:00:00 equals 1:00:00:00 in non-drop frame, BUT the running time of this duration is really 1:00:03:18.

Drop-frame

Many people are very concerned with the actual running time. (Imagine a network making a 3 second & 18 frame error when broadcasting the Superbowl with advertisers paying $33,333 per second! (1995)) The drop-frame labeling scheme was designed to over-come the inaccuracy of non-drop frame labeling, and it is gospel in broadcasting.

The drop-frame format represents the NTSC running time accurately by "dropping out" some of the frame labels - specifically, 2 frame labels at the end of each minute except each 10th minute. This way, a display of drop-frame 01:00:00;00 (semicolon indicates drop-frame) represents 107,892 video frames, or exactly 1 hour of real time from zero.

No actual video frames are "dropped" (where could they go?) - only the timecode labels of the frames. At any point through the labeling sequence the timecode label is very close to the actual elasped time (from zero). Since the labels represent an accurate time-line, adding or subtracting drop-frame timecode results in an accurate calculation - 2:00:00;00 minus 1:00:00;00 equals 1:00:00;00 - one true hour of running time.

PAL/SECAM - EBU

PAL and SECAM video run at precisely 25 frames per second so the DROP frame/NON-DROP frame issue is meaningless. 01:00:00:00 in EBU represents 90,000 PAL video frames- precisely 1 hour of running time.