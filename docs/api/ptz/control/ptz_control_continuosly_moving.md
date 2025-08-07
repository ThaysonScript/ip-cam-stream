# PTZ Continuously Moving

Start continuously moving the PTZ.

## Request URL
`http://<server>/cgi-bin/ptz.cgi?action=start&code=Continuously`

## Method
`GET`

## Request Params (key=value format in URL)
| Name    | Type     | R/O | Description                                                                 | Example |
|---------|----------|-----|-----------------------------------------------------------------------------|---------|
| channel | int      | R   | The PTZ channel index; starting from 1                                      | 1       |
| code    | char[16] | R   | Must be "Continuously"                                                      | "Continuously" |
| arg1    | int      | O   | Motion direction and step length (see table below)                          | 5       |
| arg2    | int      | O   | Motion direction and step length (see table below)                          | 5       |
| arg3    | int      | O   | Zooming speed; range: [-100, 100]                                           | 5       |
| arg4    | int      | O   | Overtime period (seconds, max 3600). PTZ will auto-stop if no stop command received before timeout | 60      |

## Request Example
`http://192.168.1.108/cgi-bin/ptz.cgi?action=start&code=Continuously&channel=1&arg1=5&arg2=5&arg3=5&arg4=60`

## Response Params
`OK` (in body)

## Response Example
`OK`

## Parameter Details
- **arg1/arg2**: 
  - Positive values indicate right/up movement
  - Negative values indicate left/down movement
  - Absolute value represents step length/speed
- **arg3**:
  - Positive values: zoom in
  - Negative values: zoom out
  - Absolute value represents zoom speed
- **arg4**:
  - Safety timeout in seconds (1-3600)
  - PTZ will automatically stop after this period