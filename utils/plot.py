import talib
from pyecharts import options as opts
from pyecharts.charts import Bar, Kline, Grid, Line, Scatter

class KlineChart:
    def __init__(self,df,point,high_centre,low_centre) -> None:
        self.point = point
        self.df = df
        self.df['macd'], self.df['signal'], self.df['hist'] = talib.MACD(self.df['close'])
        # 从 DataFrame 中获取数据
        self.x_data = self.df.index.tolist()
        self.y_data = self.df[['open', 'close', 'low', 'high']].values.tolist()
        self.volumes = self.df['volume'].tolist()
        self.high_centre = high_centre
        self.low_centre = low_centre
        


    def kline(self):
        # 创建 K 线图
        self._kline = (
            Kline(init_opts=opts.InitOpts(width="100%", height="400px"))
            .add_xaxis(self.x_data)
            .add_yaxis("K线图", self.y_data)
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

        self._line = (
            Line()
            .add_xaxis([i for i in self.point.index.tolist()])
            .add_yaxis(
                "line",
                [i for i in self.point.values.tolist()],
                markline_opts=opts.MarkLineOpts(
                    data=[opts.MarkLineItem(type_="min", name="最小值"),
                        opts.MarkLineItem(type_="max", name="最大值")]
                ),
                label_opts=opts.LabelOpts(is_show=False)
            )
        )
        self._kline.overlap(self._line)

        for i in range(len(self.high_centre)):
            x1, y1 = self.low_centre.index[i], self.low_centre.values.tolist()[i]
            x2, y2 = self.low_centre.index[i], self.high_centre.values.tolist()[i]
            x3, y3 = self.high_centre.index[i], y2
            x4, y4 = x3, y1
            self._scatter= (
                Scatter()
                .add_xaxis([x1, x2, x3, x4])
                .add_yaxis('中枢',[y1, y2, y3, y4],label_opts=opts.LabelOpts(is_show=False))
                    
                )
            self._line = (
                Line()
                .add_xaxis([x1, x2, x3, x4])
                .add_yaxis('中枢',[y1, y2, y3, y4],label_opts=opts.LabelOpts(is_show=False))
                .add_xaxis([x4,x1])
                .add_yaxis('中枢', [y4,y1],label_opts=opts.LabelOpts(is_show=False))
            )


            self._scatter.overlap(self._line)
            self._kline.overlap(self._scatter)

        

    def MACD(self):
        # 创建一个折线图表示MACD
        self._line_macd = (
            Line(init_opts=opts.InitOpts(width="100%", height="200px"))
            .add_xaxis(self.df.index.tolist())
            .add_yaxis("MACD", self.df['macd'].values.tolist(), is_connect_nones=True, label_opts=opts.LabelOpts(is_show=False))
            .add_yaxis("SIGNAL", self.df['signal'].values.tolist(), is_connect_nones=True, label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                legend_opts=opts.LegendOpts(is_show=False)
            )
        )
        macd_hist = self.df['hist'].values.tolist()
        macd_hist_red = [v if v > 0 else 0 for v in macd_hist]
        macd_hist_green = [v if v < 0 else 0 for v in macd_hist]
        # 创建一个柱状图表示MACD Hist
        self._bar = (
            Bar()
            .add_xaxis(self.df.index.tolist())
            .add_yaxis("Hist_Red", macd_hist_red, stack="stack1", color="#c23531", label_opts=opts.LabelOpts(is_show=False))
            .add_yaxis("Hist_Green", macd_hist_green, stack="stack2", color="#008000", label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                legend_opts=opts.LegendOpts(is_show=False),
            )
        )
        self._line_macd.overlap(self._bar)


    def plot(self):
        self.kline()
        self.MACD()
        grid = (
            Grid(
                init_opts=opts.InitOpts(width="100%", height="800px",
                                        animation_opts=opts.AnimationOpts(animation=False))

            )
            .add(self._kline, grid_opts=opts.GridOpts(pos_bottom="30%"))
            .add(self._line_macd, grid_opts=opts.GridOpts(pos_top="75%"))

        )

        return grid.render()

