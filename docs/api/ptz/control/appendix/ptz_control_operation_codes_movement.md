# Appendix: Operation Codes for PTZ Movement

## Movement Control Codes

| Code       | Description                          | arg1 | arg2 | arg3 |
|------------|--------------------------------------|------|------|------|
| Up         | Move up                              | 0    | Vertical motion speed [1-8] | 0 |
| Down       | Move down                            | 0    | Vertical motion speed [1-8] | 0 |
| Left       | Move left                            | 0    | Horizontal motion speed [1-8] | 0 |
| Right      | Move right                           | 0    | Horizontal motion speed [1-8] | 0 |
| LeftUp     | Move in an upper-left direction      | Vertical motion speed [1-8] | Horizontal motion speed [1-8] | 0 |
| RightUp    | Move in an upper-right direction     | Vertical motion speed [1-8] | Horizontal motion speed [1-8] | 0 |
| LeftDown   | Move in an lower-left direction      | Vertical motion speed [1-8] | Horizontal motion speed [1-8] | 0 |
| RightDown  | Move in an lower-right direction     | Vertical motion speed [1-8] | Horizontal motion speed [1-8] | 0 |

## Zoom and Focus Control Codes

| Code       | Description                          | arg1 | arg2 | arg3 |
|------------|--------------------------------------|------|------|------|
| ZoomWide   | Zoom in                              | 0    | 0    | 0    |
| ZoomTele   | Zoom out                             | 0    | 0    | 0    |
| FocusNear  | Focus (near-field)                   | 0    | 0    | 0    |
| FocusFar   | Focus (far-field)                    | 0    | 0    | 0    |
| IrisLarge  | Increase the aperture                | 0    | 0    | 0    |
| IrisSmall  | Decrease the aperture                | 0    | 0    | 0    |

**Note:** 
- For movement commands, speed parameters typically range from 1 (slowest) to 8 (fastest)
- Parameters marked with 0 are typically reserved or unused