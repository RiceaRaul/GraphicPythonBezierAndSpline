from bokeh.models import (TableColumn, NumberFormatter, IntEditor)


def getcols() -> list:
    columns = [
        TableColumn(
            field="x",
            title="X",
            editor=IntEditor(),
            formatter=NumberFormatter(format="0.000"),
        ),
        TableColumn(
            field="y",
            title="Y",
            editor=IntEditor(),
            formatter=NumberFormatter(format="0.000"),
        ),
    ]

    return columns
