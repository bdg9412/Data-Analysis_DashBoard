import base64
import io
import datetime
import dash_html_components as html
import dash_table
import pandas as pd


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('euc-kr')))
            df.to_csv('/home/nexen/PycharmProjects/Django_plotly_dash_naive/csv_data/'+datetime.datetime.now().strftime('%Y-%m-%d %H %M')+"uploaded.csv")
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
