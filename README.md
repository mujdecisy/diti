
# **diti** - Reduce Your Datetime Operation Pains

## Introduction

**diti** is a powerful and user-friendly Python library that simplifies datetime operations, aiming to reduce your datetime-related headaches. With **diti**, you can perform a wide range of datetime tasks with ease and precision, allowing you to focus on the core functionality of your projects rather than wrestling with date and time intricacies.

## Installation

You can install **diti** using pip:

```bash
pip install diti
```

## Features

### 1. Diti Object > mutable
The **Diti Object** is a powerful feature of the `diti` library that enhances your datetime manipulation capabilities. With the Diti Object, you can:

- **Flexible Constructor** The Diti Object constructor accepts various input formats, including floats, ISO 8601 strings, and standard datetime objects, providing flexibility and compatibility for your specific needs.

``` python
from diti import Diti
from datettime import datetime

dt_now = Diti()
dt1 = Diti("2023-01-01")
dt2 = Diti("2023-01-01T00:00:00.000+0300")
dt3 = Diti(datetime.now())
dt4 = Diti(1697277012)
dt5 = Diti("2023-01-01T00:00:00", timezone="+0300")
dt6 = Diti("2023-01-01T00:00:00", timezone="Europe/Istanbul")
dt7 = Diti("2023-01-01T00:00:00", timezone=180)
```

- **Save Your DateTime Object Mutably** Preserve your datetime object while making changes with ease. `diti` allows you to update the object seamlessly, ensuring your data remains mutable.
```python
from diti import Diti, DitiParts

dt = Diti()
dt.edit().add(DitiParts.HOURS, 1).commit()

another_dt = dt_now().clone()
another_dt.edit().head_of(DitiParts.DAYS)
```

- Elegant Operational Functions: Perform datetime operations elegantly, simplifying complex tasks. `diti` offers a wide array of intuitive methods to modify and manipulate your datetime object effortlessly.
```python
from diti import Diti, DitiParts, DitiTimezone, DitiOps

dt1 = Diti()
(dt1.edit()
    .timezone_change(DitiTimezone.EUROPE__ISTANBUL)
    .tail_of(DitiParts.MONTHS)
    .head_of(DitiParts.WEEK)
    .commit()
)

dt2 = Diti()
dt2.edit_ops([
    DitiOps.TZ_CHANGE(DitiTimezone.EUROPE_ISTANBUL),
    DitiOps.TAIL_OF(DitiParts.MONTHS),
    DitiOps.HEAD_OF(DitiParts.WEEK)
])
```

The Diti Object empowers you to work with datetime data in a manner that is both flexible and user-friendly, reducing the complexities of datetime operations.

### 2. diti_op > immutable
The **diti_op** feature is a versatile component of the `diti` library, designed to make working with datetime objects a breeze. With diti_op, you can:

- **Immutable DateTime Object Support**: Whether you prefer to use immutable `datetime.datetime` objects or mutable ones, **diti_op** provides full functionality. It seamlessly accommodates your choice, ensuring you can work with datetime data as you like.
```python
from datetime import datetime
from diti import diti_op, DitiOps, DitiParts

dt = datetime.now()

tomorrow = diti_op(dt, [
    DitiOps.ADD(DitiParts.DAYS, 1)
])
```

- **Flexible Initialization**: DITI_OP allows you to initialize your datetime objects using a variety of formats, including floats, ISO 8601 strings, or standard datetime objects. This flexibility makes it effortless to create datetime instances that suit your specific requirements.
```python
from datetime import datetime
from diti import diti_op, DitiOps, DitiParts

tomorrow = diti_op(datetime.now(), [
    DitiOps.ADD(DitiParts.DAYS, 1)
])

previous_day = diti_op("2023-01-01T12:34",[
    DitiOps.ADD(DitiParts.DAYS, -1)
])

end_of_week = diti_op(1697277012,[
    DitiOps.TAIL_OF(DitiParts.WEEK)
])
```

- **Effortless Object Updates**: diti_op simplifies the process of modifying your datetime objects. Its intuitive methods enable easy updates, making it convenient to perform various datetime operations without unnecessary complexity.
```python
from datetime import datetime
from diti import diti_op, DitiOps, DitiParts

dt = diti_op(datetime.now(), [
    DitiOps.TZ_UPDATE(DitiTimezone.EUROPE_ISTANBUL),
    DitiOps.TAIL_OF(DitiParts.MONTHS),
    DitiOps.HEAD_OF(DitiParts.WEEK)
])
```


**diti_op** is your trusted companion for datetime management, offering adaptability, ease of use, and efficient datetime object handling.

### 3. diti_interval

The **diti_interval** feature is a powerful addition to the DITI library, built to simplify interval-based datetime operations. With **diti_interval**, you can:

Seamlessly handle a wide range of interval-based datetime operations with ease. **diti_interval** streamlines the process, allowing you to work with date and time intervals in a straightforward manner.

- **Find Closest Datetime**: Quickly identify the closest datetime within a list of datetime instances. This feature is incredibly useful for locating the nearest reference point in your datetime data.
```python
from diti import diti_interval
from datetime import datetime

closest_index = diti_interval.closest_time(
    datetime.fromtimestamp(5),
    [
        datetime.fromtimestamp(1),
        datetime.fromtimestamp(2),
        datetime.fromtimestamp(3),
        datetime.fromtimestamp(6),
        datetime.fromtimestamp(7)
    ]
)
```

- **Divide DateTime Ranges into Slots**: Divide a datetime range into discrete slots, enabling you to categorize and organize your data with precision. This is particularly valuable when dealing with scheduling, time management, or data segmentation.
```python
from diti import diti_interval, DitiParts
from datetime import datetime

time_list = diti_interval.divide_into_timeslots(
    datetime.fromtimestamp(5),
    datetime.fromtimestamp(10),
    DitiParts.SECONDS,
    1
)
```


- **Discover Overlapping Time Slots**: Easily detect overlapping time slots within your data, making it simple to analyze conflicts, schedule intersections, or any scenario where overlapping time intervals need to be managed.
```python
from diti import diti_interval
from datetime import datetime

overlapped_index_list = diti_interval.overlapped_timeslots(
    datetime.fromtimestamp(5),
    [
        (datetime.fromtimestamp(1), datetime.fromtimestamp(5))
        (datetime.fromtimestamp(2), datetime.fromtimestamp(10))
        (datetime.fromtimestamp(4), datetime.fromtimestamp(15))
        (datetime.fromtimestamp(3), None)
        (None, datetime.fromtimestamp(7))
    ]
)
```


**diti_interval** empowers you to work with datetime intervals, providing a set of tools that simplify complex operations and streamline your datetime-based workflows.


## Contact

Have questions, suggestions, or need support? Reach out to me at mujdecisy@gmail.com
