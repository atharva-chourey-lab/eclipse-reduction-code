VI/122        The Marginal Zone of the Moon - Watts' Charts    (Watts, 1963)
================================================================================
The Marginal Zone of the Moon
     Watts C.B.
    <Astron. Papers for the preparation of the Nautical Almanach  XVII (1963)>
================================================================================
ADC_Keywords: Solar system ; Occultations

Description:
    The WATTS' charts provide the elevation of the limb of the moon using
    1800 contour maps (step of 0.2deg) that cover all libration ranges of
    the moon. The contours of the maps were digitised by H.M. Nautical
    Almanac Office in the late 1960's, and then converted to a grid format
    by US Naval Observatory in the early 1970's. These charts are present
    in 2 forms: as an ascii file watts.dat (without carriage-return or
    line-feed!), or as a 3-D FITS file watts.fit (transformed from the
    ascii files with the program "make_fit.c"). More details, especially
    about the transformations between the original charts and the files
    stored here, and the special processing of the 36.0{deg} map (map#181), 
    can be found in the "doc.txt" file.

File Summary:
--------------------------------------------------------------------------------
 FileName   Lrecl   Records   Explanations
--------------------------------------------------------------------------------
ReadMe         80         .   This file
doc.txt        75       455   Detailed information concerning the derivation of
                              the file, known errors, and the order of the data
watts.dat       6  13269600   The Watts charts, in grid layout (without CR/LF)
watts.fit    2880     13825   The Watts charts, as a FITS file [91x81x1800]
photos.dat     47       503   List of photographs used in the survey
--------------------------------------------------------------------------------

See also:
    Morrison L.V., Martin R.J., 1971Moon....2..463M

Byte-by-byte Description of bulk file: watts.dat
--------------------------------------------------------------------------------
   Bytes Format  Units   Label   Explanations
--------------------------------------------------------------------------------
   1-  4  I4 0.01arcsec  h       height of the limb, in units of 0.01"
                                 (sign in byte 1)
   5      I1     ---     a       [0,7] Accuracy code a (1)
   6      I1     ---     b       [0,7] Accuracy code b (1)
--------------------------------------------------------------------------------
Note (1): The accuracy code has 2 parts, a and b, each with possible
   values between 0 and 7. The meaning of theses codes is detailed in
   the file "doc.txt", section 3. A simplified reliability code can
   be derived as follows:
   -- Reliable   if: b=0 or b=1; or 1<b<7 and a=0; or b=7 and a=5;
   -- Uncertain  if: 1<b<7 and 0<a<3; or b=7 and a=6;
   -- Unreliable if: b=7 and a<5; or 1<b<7 and a>2; or b=7 and a=7;
                     or h>3.4; or h<-3.4
--------------------------------------------------------------------------------

Byte-by-byte Description of file: photos.dat
--------------------------------------------------------------------------------
   Bytes Format Units   Label     Explanations
--------------------------------------------------------------------------------
   1-  3  I3    ---     Seq       Ordinal sequence in the printed table
   5-  9  I5    ---     ID        Identification number in the printed table
  11- 14  I4    yr      Obs.Y     Year of the photograph
  16- 18  A3   "month"  Obs.M     Month of the photograph
  20- 26  F7.4  d       Obs.D     Day of the photograph
      27  A1    ---     Rem       [#*$] Remark on photograph:
                                   * when used as a 'standard'
                                   # when used to test circularity of 2nd datum
                                   $ for both the above.
  28- 33  F6.2  deg     l         Longitude libration
  34- 39  F6.2  deg     b         Latitude libration
  40- 43  I4    deg     Arc1      Start of measured arc
  44- 47  I4    deg     Arc2      End of measured arc
--------------------------------------------------------------------------------

================================================================================
(End)            Dave Herald [Canberra, Australia]                   24-Mar-2006
