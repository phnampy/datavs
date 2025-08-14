import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import seaborn as sns
sns.set_style('whitegrid')       

# phnampy@gmail.com
#https://matplotlib.org/stable/users/explain/quick_start.html
# Các thư viện hiển thị biểu đồ nâng cao

def common_chart_kwargs(**kwargs):
    return {
        'figsize': kwargs.get('figsize', (12,5)),
        'title': kwargs.get('title', ''),
        'title_kwargs': kwargs.get('title_kwargs', {'fontsize': 20}),
        'xlabel': kwargs.get('xlabel', ''),
        'xlabel_kwargs': kwargs.get('xlabel_kwargs', {'fontsize': 16}),
        'ylabel': kwargs.get('ylabel', ''),
        'ylabel_kwargs': kwargs.get('ylabel_kwargs', {'fontsize': 16}),
        'vlabel': kwargs.get('vlabel', ''),
        'vlabel_kwargs': kwargs.get('vlabel_kwargs', {'fontsize': 12}),
        'value_fmt': kwargs.get('value_fmt', ',.0f'),
        'glabel_kwargs': kwargs.get('glabel_kwargs', {'fontsize': 12, 'weight': 'bold'}),
        'legend_kwargs': kwargs.get('legend_kwargs', {'fontsize': 16}),
        'prefix1': kwargs.get('prefix1', '#1'),
        'prefix2': kwargs.get('prefix2', '#2'),
    }
    

# Tạo heatmap có thêm cột tổng/trung bình của dòng và cột
def heatmap_agg(data, **kwargs):
    args = common_chart_kwargs(**kwargs)
    
    # Khai báo các cột/dòng tổng hợp
    extra_col = kwargs.get('extra_col', 'sum')
    agg_col = kwargs.get('sum_col', 'Tổng') if (extra_col == 'sum') else \
              kwargs.get('avg_col', 'Trung bình')
    agg_row = agg_col # Dòng tổng hợp giống tên cột tổng hợp

    # Định dạng heatmap
    cbar_v = kwargs.get('cbar_v', False) # hiển thị bảng đo màu của các cell giá trị
    cbar_g = kwargs.get('cbar_g', False) # hiển thị bảng đo màu của dòng/cột tổng hợp
    cmap_v = kwargs.get('cmap', 'Reds')
    cmap_g = kwargs.get('cmap2', 'Blues')
    cbar_kws_v = kwargs.get('cbar_kws_v', {'label': args['vlabel']})
    cbar_kws_g = kwargs.get('cbar_kws_g', {'label': f"{agg_col} {args['vlabel']}" })

    # Xử lý dữ liệu để thêm cột tổng hợp
    df_values = data.copy()
    # Thêm cột tổng hợp
    df_values[agg_col] = df_values.sum(axis = 1) if (extra_col == 'sum') else \
                         df_values.mean(axis = 1) 
    df_values = df_values.sort_values(agg_col, ascending=False) # Sắp xếp dữu liệu giảm dần
    
    # Lấy 2 giá trị biên của cột tổng để gán khoảng giá trị cho heatmap Dữ liệu
    gmin, gmax = df_values[agg_col].min(), df_values[agg_col].max()

    # Thêm dòng tổng hợp
    df_values.loc[agg_row] = df_values.sum(axis = 0) if (extra_col == 'sum') else \
                             df_values.mean(axis = 0) 
   
    df_group = df_values.copy()
    # Đối với bảng dữ liệu, xóa dữ liệu cột/dòng tổng => NAN để không hiển thị
    df_values[agg_col] = float('NAN') 
    df_values.loc[agg_row] = float('NAN')
    # Đối ới bảng tổng hợp => xóa các cell chứa data, để lại cột/dòng tổng hợp
    df_group.iloc[:-1, :-1] = float('NAN')
    
    # Vẽ 2 heatmap chồng lên nhau 
    fig, ax = plt.subplots(figsize=args['figsize'])
    sns.heatmap(ax=ax, data=df_values, annot=True, fmt=args['value_fmt'], annot_kws=args['vlabel_kwargs'], 
                cbar=cbar_v, cmap=cmap_v, cbar_kws=cbar_kws_v)
    sns.heatmap(ax=ax, data=df_group, annot=True, fmt=args['value_fmt'], annot_kws=args['glabel_kwargs'], vmin=gmin, vmax=gmax,
                cbar=cbar_g, cmap=cmap_g, cbar_kws=cbar_kws_g)
    plt.title(args['title'], **dict(args['title_kwargs']))
    plt.xlabel(args['xlabel'], **dict(args['xlabel_kwargs']))
    plt.ylabel(args['ylabel'], **dict(args['ylabel_kwargs']))
    
    # Hiển thị trục x lên phía trên (mặc định)
    if kwargs.get('xaxis', 'top')=='top':
        ax.xaxis.tick_top() # x axis on top
        ax.xaxis.set_label_position('top')
    plt.show()

# Tạo biểu đồ cột xếp chồng của 2 bảng dữ liệu
# Phù hợp so sánh dữ liệu 2 năm (cùng kỳ)
def stacked2(dt1, dt2, **kwargs):
    args = common_chart_kwargs(**kwargs)
    
    # Plot 2 bar stacked
    fig, ax = plt.subplots(figsize=args['figsize'])
    dt1.plot.bar(stacked=True, ax=ax, position=1, width=0.3, hatch='/')
    dt2.plot.bar(stacked=True, ax=ax, position=0, width=0.3)
    plt.title(args['title'], **dict(args['title_kwargs']))
    plt.xlabel(args['xlabel'], **dict(args['xlabel_kwargs']))
    plt.ylabel(args['ylabel'], **dict(args['ylabel_kwargs']))
    legend_items = kwargs['legend_items'] if 'legend_items' in kwargs else \
                   (f"{args['prefix1']} " + dt1.columns).append((f"{args['prefix2']} " + dt2.columns))
    #plt.legend(legend_items, loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=12)
    plt.legend(legend_items, **dict(args['legend_kwargs']))
    
    
# Tạo biểu đồ kết hợp 2 line có 2 trục
def line2(dt1, dt2, **kwargs):
    args = common_chart_kwargs(**kwargs)
    line1_kwargs = kwargs.get('line1_kwargs', {'marker': 's', 'color': 'blue'})
    line2_kwargs = kwargs.get('line2_kwargs', {'marker': 'o', 'color': 'red'})
    ytick_label_color = kwargs.get('ytick_label_color', 'red')

    # Vẽ 2 đường kết hợp bằng twinx
    fig, ax1 = plt.subplots(figsize=args['figsize'])
    ax2 = ax1.twinx()
    fig.suptitle(args['title'], **dict(args['title_kwargs']))

    dt1.plot.line(ax=ax1, **dict(line1_kwargs))
    dt2.plot.line(ax=ax2, **dict(line2_kwargs))
    
    ax1.set_xlabel(args['xlabel'], **dict(args['xlabel_kwargs']))
    ax2.set_ylabel(args['ylabel'], **dict(args['ylabel_kwargs']))
    for label in ax2.get_yticklabels():
        label.set_color(ytick_label_color)
        
    # Tạo ghi chú
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    labels1 = [f"{args['prefix1']} " + sub for sub in labels1]
    labels2 = [f"{args['prefix2']} " + sub for sub in labels2]
    ax2.legend(lines1 + lines2, labels1 + labels2, loc=0)

    
# Tạo biểu đồ bar kết hợp line có 2 trục    
def bar_line(df1, df2, xcol, **kwargs): 
    args = common_chart_kwargs(**kwargs)
    bar_label = kwargs.get('bar_label', '')
    bar_label_kwargs = kwargs.get('bar_label_kwargs', {'fontsize': 18, 'color': 'blue'})
    bar_label_index = kwargs.get('bar_label_index', 1) 
    bar_kwargs = kwargs.get('bar_kwargs', {})

    line_label = kwargs.get('line_label', '')
    line_label_kwargs = kwargs.get('line_label_kwargs', {'fontsize': 18, 'color': 'red'})
    line_kwargs = kwargs.get('line_kwargs', {'color': 'red'})

    ytick_label_color = kwargs.get('ytick_label_color', 'red')
    legends = kwargs.get('legends', []) 
    legend_anchor =  kwargs.get('legend_anchor', (0.35, .75))

    fig, ax1 = plt.subplots(figsize=args['figsize'])
    ax2 = ax1.twinx()
    fig.suptitle(args['title'], **dict(args['title_kwargs']))

    df1.plot.bar(ax=ax1, x=xcol, legend=False, **dict(bar_kwargs))
    df2.plot.line(ax=ax2, x=xcol, legend=False, **dict(line_kwargs))
    
    ax1.set_xlabel(args['xlabel'], **dict(args['xlabel_kwargs']))
    ax1.set_ylabel(bar_label, **dict(bar_label_kwargs))
    ax2.set_ylabel(line_label, **dict(line_label_kwargs))
    for label in ax2.get_yticklabels():
        label.set_color(ytick_label_color)
        
    # Tạo ghi chú
    if len(legends) > 0:
        fig.legend(legends, bbox_to_anchor=legend_anchor)
        
    # Hiển thị giá trị trên các thanh bar
    if kwargs.get("bar_value", True):
        if bar_label_index in range(0, len(ax1.containers)):
            ax1.bar_label(ax1.containers[bar_label_index], label_type='edge', padding=3)

        
# Định dạng chung của Chart
def chart_format(ax, **kwargs):
    if 'title' in kwargs: # Tiêu đề
        ax.set_title(kwargs['title'].get('text', ''), **kwargs['title'].get('kwargs', {}))
    if 'legends' in kwargs: # Ghi chú
        ax.legend(kwargs['legends'].get('text', []), **kwargs['legends'].get('kwargs', {}))
        
    if 'xlabel' in kwargs: # Nhãn trục x - ngang
        plt.xlabel(kwargs['xlabel'].get('text', ''), **kwargs['xlabel'].get('kwargs', {}))
    if 'ylabel' in kwargs: # Nhãn trục y - dọc
        plt.ylabel(kwargs['ylabel'].get('text', ''), **kwargs['ylabel'].get('kwargs', {}))
        
    if 'xticks' in kwargs: # Nhãn trục x
        plt.xticks(**kwargs['xticks'].get('kwargs', {}))
    if 'yticks' in kwargs: # Nhãn trục y
        plt.yticks(**kwargs['yticks'].get('kwargs', {}))
        
# Hiển thị các mục text của mỗi dòng dữ liệu trong bảng df
def draw_bar_texts(ax, df, item_texts):
    for i, row in df.iterrows():
        for item in item_texts:
            value = row[item['col']]
            is_number = isinstance(value, (int, float, complex)) and not isinstance(value, bool)
            number_fmt = item.get('number_fmt', ',.0f') if is_number else ''
            text = f"{value:{number_fmt}}"
            x_pos = item.get('x_margin', 0) + (row[item['x_col']] if 'x_col' in item else 0)
            y_pos = i + item.get('y_margin', 0)
            if text not in ['0', '', None]:
                ax.text(x_pos, y_pos, text, **item.get('kwargs', {}))
                

# Biểu đồ bar ngang nâng cao => tách các cột của bảng df thành nhiều nhóm bar 
# (cho phép stacked riêng từng nhóm bar) => phù hợp bảng kế hoạch
def hbar_group(df, config, **kwargs):
    figsize = kwargs.get('figsize', (12,8))
    fig, ax = plt.subplots(figsize=figsize)
    
    for bar in config['bars']:
        cols = [config['xcol']] + bar['cols']
        df[cols].plot.barh(ax=ax, x=config['xcol'], stacked=True, #width=bar.get('width', 0.2),
                                  position=bar['position'], **bar.get('kwargs', {}))
        
    chart_format(ax, **dict(kwargs))
    
    # Thêm 1/2 dòng trục y ở trên cùng
    y0, y1 = plt.ylim()
    plt.ylim(y0, y1 + 0.5)
    
    # Vẽ các giá trị dữ liệu
    if 'bar_texts' in config:
        draw_bar_texts(ax, df, config['bar_texts'])
        
    # Định dạng số trục x
    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))