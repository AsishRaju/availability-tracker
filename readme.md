# Availability Checker

This script monitors the health and availability of HTTP endpoints specified in a YAML config file. It performs regular checks on each endpoint and reports cumulative availability by domain.

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/AsishRaju/availability-tracker
   cd availability-checker
   ```
2. Set up Python virtual environment
   ```bash
   python -m venv venv
   ```
3. Activate virtual environment
   ```bash
   source venv/bin/activate
   ```
4. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the monitor with a configuration file:

```bash
python improved_monitor.py <path_to_config_file.yaml>
```

Example:

```bash
python improved_monitor.py sample.yaml
```

The monitor will:

- Check all endpoints every 15 seconds
- Calculate and display the cumulative availability percentage for each domain
- Continue running until interrupted (Ctrl+C)

## Configuration File Format

The configuration file should be in YAML format with the following structure:

```yaml
- name: endpoint_name
  url: https://example.com/endpoint
  method: GET # Optional, defaults to GET if not specified
  headers: # Optional
    content-type: application/json
  body: '{"key":"value"}' # Optional, JSON string
```

See [`sample.yaml`](https://github.com/AsishRaju/availability-tracker/blob/main/sample.yaml) for examples.

## Issues Identified and Fix Made

<details>
  <summary>Response Time Check</summary>

<br>

> **Issue:** The original code didn't check if endpoints responded within 500ms as required.

> **Fix:** Added response time measurement and included it in the availability criteria. Endpoints must respond in less than 500ms to be considered "UP". [view code](https://github.com/AsishRaju/availability-tracker/blob/d8643f988a1df8d72a6b241f083f974c22e14a83/lib/monitor.py#L24)

</details>

<details>
  <summary>Default HTTP Method</summary>

<br>

> **Issue:** The original code didn't set GET as the default method when not specified.

> **Fix:** Set GET as the default method when not provided in the configuration. [view code](https://github.com/AsishRaju/availability-tracker/blob/d8643f988a1df8d72a6b241f083f974c22e14a83/lib/monitor.py#L13)

</details>

<details>
  <summary>Port Number Handling</summary>

<br>

> **Issue:** The domain extraction didn't properly ignore port numbers.

> **Fix:** Used simple urllib.parse to extract hostname.[view code](https://github.com/AsishRaju/availability-tracker/blob/d8643f988a1df8d72a6b241f083f974c22e14a83/lib/utils.py#L6)

</details>

<details>
  <summary>Check Cycle Timing</summary>

<br>

**Issue:** The code used a fixed sleep time of 15 seconds, which doesn't account for the time spent processing endpoints.

**Fix:** Calculate the processing time and adjust the sleep duration to maintain a consistent 15-second cycle. [view code](https://github.com/AsishRaju/availability-tracker/blob/d8643f988a1df8d72a6b241f083f974c22e14a83/lib/monitor.py#L61)

</details>

<details>
  <summary>JSON Body Handling</summary>

<br>

**Issue:** The YAML example suggests body may be provided as a JSON string, but the code was passing it directly as a JSON object.

**Fix:** Added parsing of JSON strings to proper objects before sending requests. [view code](https://github.com/AsishRaju/availability-tracker/blob/d8643f988a1df8d72a6b241f083f974c22e14a83/lib/utils.py#L8)

</details>

<details>
  <summary>Availability Percentage Calculation</summary>

<br>

**Issue:** The code was rounding the availability percentage but not dropping decimal points as required.

**Fix:** Changed to integer casting to drop decimal points. [view code](https://github.com/AsishRaju/availability-tracker/blob/d8643f988a1df8d72a6b241f083f974c22e14a83/lib/monitor.py#L55)

</details>

<details>
  <summary>Error Handling Improvements</summary>

<br>

**Issue:** Limited error handling in the original code.

**Fix:** Added better exception handling for various potential issues. [view code](https://github.com/AsishRaju/availability-tracker/blob/main/lib/config.py)

</details>

<details>
  <summary>Improved Logging</summary>

<br>

**Issue:** Basic logging in the original code.

**Fix:** Added timestamps and more detailed information to the logs. [view code](https://github.com/AsishRaju/availability-tracker/blob/main/lib/logging_config.py)

</details>

## Additional Notes

- Availability percentages are displayed as whole numbers with decimals dropped.
- The script adds a 1-second timeout to prevent hanging on unresponsive endpoints.
- Script generates 3 level of logs in `logs/`
  - `logs/debug.log` -> logs debug and info message of the script
  - `logs/error.log` -> logs error related message of the script
  - `logs/monitor.log` -> logs domain wise availability per check cycle
