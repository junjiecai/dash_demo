from datetime import datetime
from textwrap import dedent

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px

app = dash.Dash(__name__)

df = px.data.gapminder()
initial_data = df.loc[df['year'] == 1952]


def create_figure(year):
    data = df.loc[df['year'] == year]
    figure = px.scatter(
        data,
        x='gdpPercap',
        y='lifeExp',
        size=data['pop'] ** 0.75,
        size_max=50,
        color='country',
        range_x=[1, 50000],
        range_y=[1, 100],
        title='年代:{}'.format(year)
    )
    return figure


markdown_content = '''
# Step1
ploty的交互图升级成dash后带来的好处：
* 自带webserver，部署后，可以让使用者通过浏览器访问',
* 能添加各种其他组件，例如
    * html组件（[](https://dash.plotly.com/dash-html-components)
    * Dash预封装的复合组件
        * [Dash Core Component](https://dash.plotly.com/dash-core-components)
        * [DataTable](https://dash.plotly.com/dash-core-components)
        * 其他（请在官方文档查询）
'''

# 通过定义app.layout方式，定义Dashboard页面的结构
app.layout = html.Div(children=[
    html.H1(
        'Step 1: Dash极简版本'
    ),  # html组件
    html.H2('描述'),
    html.P(
        '时间:{}'.format(str(datetime.now())[:-7])
    ),
    dcc.Markdown(dedent(
        markdown_content
    )),  # 预封装组件
    html.H2('可视化'),
    dcc.Graph(
        figure=create_figure(1952)
    ),  # Plotly Graph组件
    html.Div('选择时间(暂不生效)'),
    dcc.Slider(
        min=1952,
        max=2007,
        step=5,
        value=1952,
        marks={str(year): str(year) + '年' for year in range(1952, 2012, 5)}
    ),  # 组合组件：slider控件
    html.H2('明细数据'),
    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=initial_data.to_dict('records'),
        sort_action="native",
        sort_mode="multi",
        page_action="native",
        page_current=0,
        page_size=10
    )  # 组合组件：数据表
])

if __name__ == '__main__':
    app.run_server(debug=True)
