# 8.1.5 Relative PTZ Movement

## Request URL
`http://<server>/cgi-bin/ptz.cgi?action=moveRelatively`

## Method
`GET`

## Request Params (key=value format in URL)
| Name    | Type    | R/O | Description                                      | Example |
|---------|---------|-----|--------------------------------------------------|---------|
| channel | int     | R   | The PTZ channel index; starting from 1           | 1       |
| arg1    | double  | O   | Relative horizontal motion; normalized to [-1, 1] | 0.1     |
| arg2    | double  | O   | Relative vertical motion; normalized to [-1, 1]   | 0.1     |
| arg3    | double  | O   | Relative zoom; normalized to [-1, 1]             | 0.5     |

## Request Example
`http://192.168.1.108/cgi-bin/ptz.cgi?action=moveRelatively&channel=1&arg1=0.1&arg2=0.1&arg3=0.5`

## Response Params
`OK` (in body)

## Response Example
`OK`