from datetime import datetime
from textwrap import dedent

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
app.title = 'Synyi'

df = px.data.gapminder()
initial_data = df.loc[df['year'] == 1952]


def create_table(year):
    return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.loc[df['year'] == year].to_dict('records'),
        sort_action="native",
        sort_mode="multi",
        page_action="native",
        page_current=0,
        page_size=10,
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],  # 通过python参数方式控制样式的例子
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
    )  # 复合组件：数据表


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
        
# Step2
修改样式让整体结果更加美观，不同的途径
* 通过提供css, 可以放在assets/styles.css中
* 通过python为组件传入参数

注意：不管是复合组件，还是html组件，最终在浏览器中都会被转化成html标签。

html和css不是这次分享重点，不熟悉忽略即可，不影响对dash的理解。

除此之外，也可替换浏览器的页面图标

# Step3
增加交互效果：
逻辑：监听Input定义的目标，如果发生改变，调用函数，并且升级Output定义的目标
'''


def create_figure(data, year):
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
        id='plot',
        figure=create_figure(initial_data, 1952)
    ),  # Plotly Graph组件
    html.Div('选择时间(暂不生效)'),
    dcc.Slider(
        id='year_slider',
        min=1952,
        max=2007,
        step=5,
        value=1952,
        marks={str(year): str(year) + '年' for year in range(1952, 2012, 5)}
    ),  # 组合组件：slider控件
    html.H2('明细数据'),
    create_table(1952),
])


@app.callback(
    Output('plot', 'figure'),
    [Input('year_slider', 'value')]
)
def update_figure(year):
    data = df.loc[df['year'] == year]
    figure = create_figure(data, year)
    return figure


@app.callback(
    Output('table', 'data'),
    [Input('year_slider', 'value')]
)
def update_table(year):
    return df.loc[df['year'] == year].to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
