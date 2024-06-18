"""
Histogram visualization.
"""

import pandas as pd
import plotly.graph_objects as go

## LE TEMPLATE DE FICHIER A UTILISER POUR LES VISUALISATIONS
## Chaque fichier de visualisation doit contenir la fonction get_figure(data) qui retourne un objet figure de plotly
## Le nom du fichier est : "nom_de_la_visualisation.py"

# data fields are ID,Case Number,Date,Block,IUCR,Primary Type,Description,Location Description,Arrest,Domestic,Beat,District,Ward,Community Area,FBI Code,X Coordinate,Y Coordinate,Year,Updated On,Latitude,Longitude,Location

# load preprocessed data

DATA_FOLDER = "assets/data"
# fields are Time of Day,ARSON,ASSAULT,BATTERY,BURGLARY,CONCEALED CARRY LICENSE VIOLATION,CRIM SEXUAL ASSAULT,CRIMINAL DAMAGE,CRIMINAL SEXUAL ASSAULT,CRIMINAL TRESPASS,DECEPTIVE PRACTICE,DOMESTIC VIOLENCE,GAMBLING,HOMICIDE,HUMAN TRAFFICKING,INTERFERENCE WITH PUBLIC OFFICER,INTIMIDATION,KIDNAPPING,LIQUOR LAW VIOLATION,MOTOR VEHICLE THEFT,NARCOTICS,NON - CRIMINAL,NON-CRIMINAL,NON-CRIMINAL (SUBJECT SPECIFIED),OBSCENITY,OFFENSE INVOLVING CHILDREN,OTHER NARCOTIC VIOLATION,OTHER OFFENSE,PROSTITUTION,PUBLIC INDECENCY,PUBLIC PEACE VIOLATION,RITUALISM,ROBBERY,SEX OFFENSE,STALKING,THEFT,WEAPONS VIOLATION
HISTOGRAM_TIME_OF_DAY_PATH = f"{DATA_FOLDER}/histogram_times_of_day.csv"
# fields are Weekday,ARSON,ASSAULT,BATTERY,BURGLARY,CONCEALED CARRY LICENSE VIOLATION,CRIM SEXUAL ASSAULT,CRIMINAL DAMAGE,CRIMINAL SEXUAL ASSAULT,CRIMINAL TRESPASS,DECEPTIVE PRACTICE,DOMESTIC VIOLENCE,GAMBLING,HOMICIDE,HUMAN TRAFFICKING,INTERFERENCE WITH PUBLIC OFFICER,INTIMIDATION,KIDNAPPING,LIQUOR LAW VIOLATION,MOTOR VEHICLE THEFT,NARCOTICS,NON - CRIMINAL,NON-CRIMINAL,NON-CRIMINAL (SUBJECT SPECIFIED),OBSCENITY,OFFENSE INVOLVING CHILDREN,OTHER NARCOTIC VIOLATION,OTHER OFFENSE,PROSTITUTION,PUBLIC INDECENCY,PUBLIC PEACE VIOLATION,RITUALISM,ROBBERY,SEX OFFENSE,STALKING,THEFT,WEAPONS VIOLATION
HISTOGRAM_DAYS_PATH = f"{DATA_FOLDER}/histogram_days.csv"
# fields are Month,ARSON,ASSAULT,BATTERY,BURGLARY,CONCEALED CARRY LICENSE VIOLATION,CRIM SEXUAL ASSAULT,CRIMINAL DAMAGE,CRIMINAL SEXUAL ASSAULT,CRIMINAL TRESPASS,DECEPTIVE PRACTICE,DOMESTIC VIOLENCE,GAMBLING,HOMICIDE,HUMAN TRAFFICKING,INTERFERENCE WITH PUBLIC OFFICER,INTIMIDATION,KIDNAPPING,LIQUOR LAW VIOLATION,MOTOR VEHICLE THEFT,NARCOTICS,NON - CRIMINAL,NON-CRIMINAL,NON-CRIMINAL (SUBJECT SPECIFIED),OBSCENITY,OFFENSE INVOLVING CHILDREN,OTHER NARCOTIC VIOLATION,OTHER OFFENSE,PROSTITUTION,PUBLIC INDECENCY,PUBLIC PEACE VIOLATION,RITUALISM,ROBBERY,SEX OFFENSE,STALKING,THEFT,WEAPONS VIOLATION
HISTOGRAM_MONTHS_PATH = f"{DATA_FOLDER}/histogram_months.csv"


# histogram_days.csv :
# Weekday,ARSON,ASSAULT,BATTERY,BURGLARY,CONCEALED CARRY LICENSE VIOLATION,CRIM SEXUAL ASSAULT,CRIMINAL DAMAGE,CRIMINAL SEXUAL ASSAULT,CRIMINAL TRESPASS,DECEPTIVE PRACTICE,DOMESTIC VIOLENCE,GAMBLING,HOMICIDE,HUMAN TRAFFICKING,INTERFERENCE WITH PUBLIC OFFICER,INTIMIDATION,KIDNAPPING,LIQUOR LAW VIOLATION,MOTOR VEHICLE THEFT,NARCOTICS,NON - CRIMINAL,NON-CRIMINAL,NON-CRIMINAL (SUBJECT SPECIFIED),OBSCENITY,OFFENSE INVOLVING CHILDREN,OTHER NARCOTIC VIOLATION,OTHER OFFENSE,PROSTITUTION,PUBLIC INDECENCY,PUBLIC PEACE VIOLATION,RITUALISM,ROBBERY,SEX OFFENSE,STALKING,THEFT,WEAPONS VIOLATION,Total
# 0,1986.0,76480.0,198660.0,66408.0,180.0,3670.0,127082.0,1174.0,31899.0,57114.0,,2072.0,1797.0,16.0,2680.0,786.0,976.0,1376.0,57379.0,102164.0,3.0,29.0,3.0,132.0,7913.0,16.0,74713.0,6268.0,24.0,7469.0,5.0,43651.0,4723.0,839.0,245682.0,15616.0,1140985.0
# 1,1973.0,78716.0,196767.0,65172.0,128.0,3529.0,123267.0,1085.0,33273.0,56962.0,,2117.0,1675.0,19.0,2643.0,797.0,992.0,1891.0,56094.0,112912.0,6.0,26.0,,141.0,7791.0,26.0,74069.0,12060.0,34.0,7825.0,4.0,42448.0,4836.0,849.0,247161.0,16273.0,1153561.0
# 2,1875.0,79986.0,197486.0,65008.0,167.0,3459.0,124075.0,1116.0,33381.0,56651.0,,2164.0,1630.0,20.0,2670.0,795.0,1025.0,2158.0,57095.0,114787.0,8.0,22.0,2.0,147.0,7859.0,19.0,73850.0,12653.0,24.0,7987.0,,42136.0,4745.0,827.0,248317.0,16055.0,1160199.0
# 3,1776.0,77765.0,197824.0,64538.0,181.0,3574.0,123446.0,1072.0,32149.0,55603.0,1.0,2095.0,1669.0,6.0,2636.0,778.0,971.0,2137.0,56656.0,114894.0,9.0,19.0,4.0,125.0,7970.0,28.0,71665.0,12453.0,35.0,7412.0,1.0,41877.0,4842.0,788.0,245431.0,16153.0,1148583.0
# 4,1821.0,76776.0,206982.0,68088.0,204.0,3832.0,136015.0,1263.0,32089.0,59626.0,,2342.0,1782.0,14.0,2742.0,721.0,1426.0,2944.0,61347.0,116953.0,5.0,46.0,,122.0,9880.0,18.0,73123.0,11815.0,25.0,8304.0,5.0,45107.0,4745.0,779.0,263158.0,17175.0,1211274.0
# 5,2147.0,71595.0,231065.0,53783.0,217.0,4633.0,144093.0,1521.0,29220.0,43628.0,,2001.0,2288.0,17.0,2815.0,514.0,994.0,2703.0,58458.0,102525.0,5.0,21.0,,94.0,8163.0,19.0,67708.0,8741.0,33.0,7108.0,4.0,45352.0,4319.0,597.0,242155.0,17834.0,1156370.0
# 6,2234.0,71170.0,243478.0,49489.0,207.0,4785.0,141598.0,1481.0,27393.0,34851.0,,1847.0,2369.0,15.0,2852.0,496.0,975.0,1901.0,57077.0,89485.0,2.0,22.0,,112.0,8364.0,24.0,66313.0,6062.0,28.0,7168.0,5.0,43602.0,4077.0,665.0,213291.0,16441.0,1099879.0


def create_histogram(_data):
    """
    Button selector to choose the timescale,
    Button selector to choose which crime type
    or all crime types.
    """

    data_time_of_day = pd.read_csv(HISTOGRAM_TIME_OF_DAY_PATH)
    data_days = pd.read_csv(HISTOGRAM_DAYS_PATH)
    data_months = pd.read_csv(HISTOGRAM_MONTHS_PATH)

    # Create the figure
    fig = go.Figure()

    # Add traces
    fig.add_trace(
        go.Bar(
            x=data_time_of_day["Time of Day"],
            y=data_time_of_day["Total"],
            name="Time of Day",
            visible=True,  # Set the trace to be visible by default
        )
    )

    fig.add_trace(
        go.Bar(
            x=data_days["Weekday"],
            y=data_days["Total"],
            name="Days",
            visible=False,  # Set the trace to be invisible by default
        )
    )

    fig.add_trace(
        go.Bar(
            x=data_months["Month"],
            y=data_months["Total"],
            name="Months",
            visible=False,  # Set the trace to be invisible by default
        )
    )

    # Set layout
    fig.update_layout(
        title="Crimes in time",
        xaxis_title="Timescale",
        yaxis_title="Total crimes",
        barmode="group",
        updatemenus=[
            {
                "buttons": [
                    {
                        "label": "Time of Day",
                        "method": "update",
                        "args": [{"visible": [True, False, False]}],
                    },
                    {
                        "label": "Weekdays",
                        "method": "update",
                        "args": [{"visible": [False, True, False]}],
                    },
                    {
                        "label": "Months",
                        "method": "update",
                        "args": [{"visible": [False, False, True]}],
                    },
                ],
                "direction": "down",
                "showactive": True,
            },
            {
                "buttons": [
                    {
                        "label": column,
                        "method": "update",
                        "args": [
                            {
                                "y": [
                                    data_time_of_day[column],
                                    data_days[column],
                                    data_months[column],
                                ]
                            }
                        ],
                    }
                    for column in data_time_of_day.columns[1:]
                ],
                "direction": "down",
                "showactive": True,
                "y": 1.2,
            },
        ],
    )

    return fig


def get_figure(data):
    """
    Returns a plotly figure object

    Args:
        data: The data to display
    Returns:
        The figure to be displayed.
    """
    fig = create_histogram(data)
    return fig


def get_hover_template():
    """
    Returns the hover template for the figure.

    Returns:
        The hover template.
    """
    return "No data to show"
