# 8.1.5 PTZ Basic Movement

Start moving the PTZ.

## Request URL
`http://<server>/cgi-bin/ptz.cgi?action=start`

## Method
`GET`

## Request Params (key=value format in URL)
| Name    | Type     | R/O | Description                                                                 | Example |
|---------|----------|-----|-----------------------------------------------------------------------------|---------|
| channel | int      | R   | The PTZ channel index; starting from 1                                      | 1       |
| code    | char[16] | R   | Operation codes for PTZ movement (see following table for valid codes)      | "Up"    |
| arg1    | int      | O   | Operation parameter 1 (meaning depends on operation code)                   | 0       |
| arg2    | int      | O   | Operation parameter 2 (meaning depends on operation code)                   | 1       |
| arg3    | int      | O   | Operation parameter 3 (meaning depends on operation code)                   | 0       |

## Request Example
`http://192.168.1.108/cgi-bin/ptz.cgi?action=start&channel=1&code=Up&arg1=0&arg2=1&arg3=0`

## Response Params
`OK` (in body)

## Response Example
`OK`