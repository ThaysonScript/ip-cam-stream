# Appendix: Continuous Movement Parameters

## Direction and Step Length Parameters

| Movement Description                | arg1 | arg2 |
|-------------------------------------|------|------|
| Continuously move left              | < -4 | 0    |
| Continuously move right             | > 4  | 0    |
| Continuously move up                | 0    | > 4  |
| Continuously move down              | 0    | < -4 |
| Continuously move upper-left        | < -4 | > 4  |
| Continuously move upper-right       | > 4  | > 4  |
| Continuously move lower-left        | < -4 | < -4 |
| Continuously move lower-right       | > 4  | < -4 |

**Parameter Notes:**
- Values represent movement speed/step length
- Absolute value indicates speed intensity (higher = faster)
- Negative values indicate left/down direction
- Positive values indicate right/up direction
- Typical operational range is 1-8 for standard speeds
- Values beyond ±4 indicate continuous movement mode