# 8.1.3 Get PTZ Capability of Current Protocol

## Request URL
```http://<server>/cgi-bin/ptz.cgi?action=getCurrentProtocolCaps```

## Method
`GET`

## Request Params (key=value format in URL)
| Name    | Type | R/O | Description                          | Example |
|---------|------|-----|--------------------------------------|---------|
| channel | int  | O   | video channel index which starts from 1 | 1       |

## Request Example
`http://192.168.1.108/cgi-bin/ptz.cgi?action=getCurrentProtocolCaps&channel=1`

## Response Params (key=value format in body)
| Name                     | Type             | R/O | Description |
|--------------------------|------------------|-----|-------------|
| caps                     | object           | R   | capabilities |
| +AlarmLen                | uint             | O   | Alarm length in protocol |
| +AuxMax                  | int              | O   | Maximum number for auxiliary functions |
| +AuxMin                  | int              | O   | Minimum number for auxiliary functions |
| +CamAddrMax              | int              | O   | Maximum channel address |
| +CamAddrMin              | int              | O   | Minimum channel address |
| +Flip                    | bool             | O   | True or false, support picture flip or not |
| +Focus                   | bool             | O   | True or false, support focus or not |
| +Iris                    | bool             | O   | True or false, support Iris adjusts or not |
| +Menu                    | bool             | O   | True or false, support internal menu of the PTZ or not |
| +MonAddrMax              | uint             | O   | Maximum monitor address |
| +MonAddrMin              | uint             | O   | Minimum monitor address |
| +Name                    | char[]           | O   | Name of the operation protocol |
| +Pan                     | bool             | O   | True or false, support pan or not |
| +PanSpeedMax             | uint             | O   | Maximum pan speed |
| +PanSpeedMin             | uint             | O   | Minimum pan speed |
| +PatternMax              | uint             | O   | Maximum pattern path number |
| +PatternMin              | uint             | O   | Minimum pattern path number |
| +PresetMax               | uint             | O   | Maximum preset point number |
| +PresetMin               | uint             | O   | Minimum preset point number |
| +Tile                    | bool             | O   | True or false, support tilt or not |
| +Zoom                    | bool             | O   | True or false, support zoom or not |
| +TileSpeedMin            | uint             | O   | Maximum tile speed |
| +TileSpeedMax            | uint             | O   | Minimum tile speed |
| +TourMin                 | uint             | O   | Maximum tour path number |
| +TourMax                 | uint             | O   | Minimum tour path number |
| +Type                    | uint             | O   | Type of PTZ protocol |
| +PtzMotionRange          | object           | O   | range |
| ++HorizontalAngle        | uint[2]          | O   | Horizontal angle range,[0] for minimum angle,[1] for maximum angle it only when Pan was true |
| ++VerticalAngle          | int[2]           | O   | Vertical angle range,[0] for minimum angle,[1] for maximum angle |
| +ZoomMax                 | uint             | O   | Maximum Zoom. it only when Zoom was true |
| +ZoomMin                 | uint             | O   | Minimum Zoom it only when Zoom was true |

## Response Example
```
caps.AlarmLen=0
caps.AuxMax=8
caps.AuxMin=1
caps.CamAddrMax=255
caps.CamAddrMin=1
caps.Flip=false
caps.Focus=false
caps.Interval=200
caps.Iris=false
caps.Menu=false
caps.MonAddrMax=255
caps.MonAddrMin=0
caps.Name=DH-SD1
caps.Pan=false
caps.PanSpeedMax=255
caps.PanSpeedMin=1
caps.PatternMax=5
caps.PatternMin=1
caps.PresetMax=80
caps.PresetMin=1
caps.Tile=false
caps.TileSpeedMax=255
caps.TileSpeedMin=1
caps.TourMax=7
caps.TourMin=0
caps.Type=1
caps.Zoom=false
caps.PtzMotionRange.HorizontalAngle[0]=0
caps.PtzMotionRange.HorizontalAngle[1]=360
caps.PtzMotionRange.VerticalAngle[0]=-20
caps.PtzMotionRange.VerticalAngle[1]=90
caps.ZoomMax=30
caps.ZoomMin=1
```