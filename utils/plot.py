import talib
from pyecharts import options as opts
from pyecharts.charts import Bar, Kline, Grid, Line
df['macd'], df['signal'], df['hist'] = talib.MACD(df['close'])
# 从 DataFrame 中获取数据
x_data = df.index.tolist()
y_data = df[['open', 'close', 'low', 'high']].values.tolist()
volumes = df['volume'].tolist()

# 创建 K 线图
kline = (
    Kline(init_opts=opts.InitOpts(width="100%", height="400px"))
    .add_xaxis(x_data)
    .add_yaxis("K线图", y_data)
    .set_global_opts(
    xaxis_opts=opts.AxisOpts(is_show=False,splitline_opts=opts.SplitLineOpts(is_show=False)),
    datazoom_opts=[
        opts.DataZoomOpts(
            is_show=False,
            type_="slider",
            xaxis_index=[0, 1],
            range_start=0,
            range_end=100,
        ),
        opts.DataZoomOpts(
            is_show=True,
            xaxis_index=[0, 1],
            type_="slider",
            pos_top="90%",
            range_start=0,
            range_end=100,
        ),
    ],
    tooltip_opts=opts.TooltipOpts(
        trigger="axis",
        axis_pointer_type="cross",
        background_color="rgba(245, 245, 245, 0.8)",
        border_width=1,
        border_color="#ccc",
        textstyle_opts=opts.TextStyleOpts(color="#000"),
    ),
    axispointer_opts=opts.AxisPointerOpts(
        is_show=True,
        link=[{"xAxisIndex": "all"}],
        label=opts.LabelOpts(background_color="#777"),
    ),
    brush_opts=opts.BrushOpts(
        x_axis_index="all",
        brush_link="all",
        out_of_brush={"colorAlpha": 0.1},
        brush_type="lineX",
    ),
    )
)

line = (
    Line()
    .add_xaxis([i for i in point.index.tolist()])
    .add_yaxis(
        "line",
        [i for i in point.values.tolist()],
        markline_opts=opts.MarkLineOpts(
            data=[opts.MarkLineItem(type_="min", name="最小值"),
                  opts.MarkLineItem(type_="max", name="最大值")]
        ),
        label_opts=opts.LabelOpts(is_show=False)
    )
)
kline.overlap(line)

# 创建一个折线图表示MACD
line_macd = (
    Line(init_opts=opts.InitOpts(width="100%", height="200px"))
    .add_xaxis(df.index.tolist())
    .add_yaxis("MACD", df['macd'].values.tolist(), is_connect_nones=True, label_opts=opts.LabelOpts(is_show=False))
    .add_yaxis("SIGNAL", df['signal'].values.tolist(), is_connect_nones=True, label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        legend_opts=opts.LegendOpts(is_show=False)
    )
)


# 创建一个柱状图表示MACD Hist
bar = (
    Bar()
    .add_xaxis(df.index.tolist())
    .add_yaxis("Hist", df['hist'].values.tolist(), label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        legend_opts=opts.LegendOpts(is_show=False),
    )
)
bar.overlap(line_macd)

# kline.overlap(bar)
# 组合图，设置全局的标题
grid = (
    Grid(
        init_opts=opts.InitOpts(width="100%", height="800px",
                                animation_opts=opts.AnimationOpts(animation=False))

    )
    .add(kline, grid_opts=opts.GridOpts(pos_bottom="30%"))
    .add(bar, grid_opts=opts.GridOpts(pos_top="75%"))

)

# 在本地生成 html 文件并展示图形
# grid.render("kline_volume.html")
# grid.render_notebook()
grid.render_notebook()
# kline.render_notebook()
