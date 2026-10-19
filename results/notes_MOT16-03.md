# Notes: MOT16-03 (date: 10/15/2026)

## Target
- ID: 166   
- Description (clothes, where, direction): a female walking with her back, black jacket, dark pant, right side of the video, walking away from the camera
- Clip frames: 352 to 735
- ID Fragmentation: 166 to 270 (from frame 735 to the end)



- ID: 46 
- Description (clothes, where, direction): a business man, walking into the store, left side of the video, walking toward camera,
- Clip frames: 253 to 350
- ID is still same but adding extra ID 144 and 154 with no person (false detection) when he walk near the top lighted cover in the front entrance of the building.




## Target hidden / not detected (frame ranges)
- THere is no miss detection or target hidden. Detector does not target/scan people sitting down or staying stationary. 

## Identity switches / fragmentation seen
| # | Frame(s) | IDs | Type | What happened | Screenshot |
|---|---|---|---|---|---|
| 1 | ~325 | 166 -> 270 | fragmentation | Target walks behind a light pole and is assigned a different ID | ____ |
| 2 | 235-750 | 32, 235, and 263 | fragmentation | Man in the center crosses behind the left pole and returns with a new ID | ____ |
| 3 | 235-355 | 144, 154 | false-positive tracks | Two boxes with no person near the lit cover above the entrance (target ID 46) | ____ |
| 4| many | - | missed detections by design | People sitting are not detected (class 7 - static people - not in training labels) | ____ |
| 5| all | None | ID Switch | No ID switch is seen throughout the video | ____ |

## Frames re-copied from Drive (unreadable-frame fix)
- count: ____   list: ____

## Video link
- URL: ____   viewing permission tested in a private window: yes / no

