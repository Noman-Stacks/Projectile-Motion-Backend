# Projectile Motion Calculator — Backend

A small Flask API that calculates ideal projectile motion. It accepts an initial velocity and a launch angle, and returns the horizontal range, the maximum height, the total flight time, and the points along the flight path.

**Live at:** https://projectile-motion-backend.vercel.app

The web page that uses this API lives in a separate repository: [projectile-motion-frontend](https://github.com/itsfarhanpk/projectile-motion-frontend).

## The physics

This is the standard introductory **ideal model**:

- Gravity is constant at **9.81 m/s²**
- There is no air resistance
- The object lands at the same height it was launched from
- The angle is measured upward from the horizontal

Symbols: `v` is the initial velocity in m/s, `θ` is the launch angle in degrees, `g` is 9.81 m/s².

```text
Range          = (v² × sin(2θ)) / g
Maximum height = (v² × sin²(θ)) / (2g)
Flight time    = (2 × v × sin(θ)) / g
```

The path is not a separate formula. It is the position at many times `t`, from launch until landing:

```text
x = v × cos(θ) × t
y = v × sin(θ) × t − (1/2) × g × t²
```

At the special angles:

- `θ = 0°` (flat along the ground): range, height, and time are all 0 in this ground-level model
- `θ = 45°`: the range is as large as this model allows for a given speed, because `sin(2θ)` peaks at `2θ = 90°`
- `θ = 90°` (straight up): range is 0, and the object lands back on the launch point

## Files

```text
backend/
    app.py              Flask API. Validates input and returns JSON.
    physics.py          All projectile formulas. No web code.
    requirements.txt    Python libraries to install.
```

The formulas are deliberately kept out of the Flask route. `physics.py` is plain functions that can be read, checked by hand, or imported from a test without starting a server.

## Installation

You need Python 3.9 or newer.

```bash
pip install -r requirements.txt
```

On Windows, use `py` instead of `python` if `python` is not recognized.

Optional, but cleaner: keep the libraries inside this project with a virtual environment.

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS or Linux:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

The `venv` folder is listed in `.gitignore`.

## How to run

```bash
python app.py
```

The server starts at:

```text
http://127.0.0.1:5000
```

`debug=True` in `app.py` reloads the server when you save a file. That is a local development setting, not a production one.

## API

### `POST /calculate`

Request body:

```json
{
  "velocity": 20,
  "angle": 45
}
```

Successful response, HTTP 200:

```json
{
  "range": 40.77,
  "max_height": 10.19,
  "flight_time": 2.88,
  "trajectory": [
    {"x": 0.0, "y": 0.0}
  ]
}
```

`range`, `max_height`, and `flight_time` are rounded to 2 decimals. `trajectory` is a list of 80 evenly spaced points used for drawing the path; each point has `x` (horizontal distance in meters) and `y` (height in meters).

Try it against the live deployment without a browser:

```bash
curl -X POST https://projectile-motion-backend.vercel.app/calculate -H "Content-Type: application/json" -d "{\"velocity\": 20, \"angle\": 45}"
```

Or against a local server, once it is running:

```bash
curl -X POST http://127.0.0.1:5000/calculate -H "Content-Type: application/json" -d "{\"velocity\": 20, \"angle\": 45}"
```

There is no route at `/`, so opening the base URL in a browser returns 404. That is expected: `/calculate` is the only endpoint, and it only answers POST.

### Validation

Invalid input returns HTTP 400 with a plain message:

| Input | Response |
| --- | --- |
| Velocity `0` or negative | `{"error": "Velocity must be greater than 0."}` |
| Angle below 0 or above 90 | `{"error": "Angle must be between 0 and 90 degrees."}` |
| Missing or non-numeric values | `{"error": "Velocity and angle must be numbers."}` |
| Body that is not JSON | `{"error": "Please send velocity and angle as JSON."}` |

Angles of exactly 0 and 90 are accepted. `NaN` and `Infinity` are rejected, because `float("nan")` does not raise an error in Python.

## Worked example

For 20 m/s at 45°, with `sin 45° ≈ 0.7071` and `sin 90° = 1`:

```text
Range          = (20² × sin 90°) / 9.81 = 400 / 9.81     = 40.77 m
Maximum height = (400 × 0.5) / 19.62                     = 10.19 m
Flight time    = (2 × 20 × 0.7071) / 9.81 = 28.284 / 9.81 = 2.88 s
```

## CORS

The page is served from a different port than this API, so the browser treats them as different origins. `flask-cors` allows that request. There are no passwords or private data in this project.

## Technologies

- Python 3
- Flask
- Flask-CORS

No database, no authentication, no ORM.

## Future improvements

- Add a simple air-resistance model and compare it with the ideal parabola
- Allow a launch height different from the landing height
- Accept other units, such as km/h or feet
- Add automated tests for the three formulas, including 0°, 45°, and 90°
