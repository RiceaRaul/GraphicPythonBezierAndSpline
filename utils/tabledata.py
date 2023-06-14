from bokeh.models import (TableColumn, NumberFormatter, NumberEditor)


def getcols() -> list:
    columns = [
        TableColumn(
            field="x",
            title="X",
            editor=NumberEditor(),
            formatter=NumberFormatter(format="0.000"),
        ),
        TableColumn(
            field="y",
            title="Y",
            editor=NumberEditor(),
            formatter=NumberFormatter(format="0.000"),
        ),
    ]

    return columns
