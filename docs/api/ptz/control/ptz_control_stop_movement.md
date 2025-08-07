# 8.1.5 Stop PTZ Movement

Stop moving the PTZ.

## Request URL
`http://<server>/cgi-bin/ptz.cgi?action=stop`

## Method
`GET`

## Request Params (key=value format in URL)
| Name    | Type     | R/O | Description                              | Example |
|---------|----------|-----|------------------------------------------|---------|
| channel | int      | R   | The PTZ channel index; starting from 1  | 1       |
| code    | char[16] | R   | Operation code for PTZ movement          | "Up"    |
| arg1    | int      | O   | Operation Parameter 1 (reserved)         | 0       |
| arg2    | int      | O   | Operation Parameter 2 (reserved)         | 0       |
| arg3    | int      | O   | Operation Parameter 3 (reserved)         | 0       |

## Request Example
`http://192.168.1.108/cgi-bin/ptz.cgi?action=stop&code=Up&channel=1&arg1=0&arg2=0&arg3=0`

## Response Params
`OK` (in body)

## Response Example
`OK`