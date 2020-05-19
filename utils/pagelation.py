from django.http.request import QueryDict

class Pagination:
    """
    page:当前的页码数
    all_count： 总的数据量
    per_num：每页显示的数据量
    max_show：最大显示的页码数
    """

    def __init__(self, page, all_count, params=None, per_num=10, max_show=11):
        try:
            self.page = int(page)
            if self.page <= 0:
                self.page = 1
        except Exception:
            self.page = 1
        # 查询条件
        self.params = params
        if not self.params:
            self.params = QueryDict(mutable=True)
        # 总数据量
        all_count = all_count
        # 每页显示的数据量为10
        # 总页码数
        total_num, more = divmod(all_count, per_num)
        if more:
            total_num = total_num + 1
        # 要显示的页码数
        half_show = max_show // 2

        if total_num <= max_show:
            page_start = 1
            page_end = total_num
        else:
            if self.page - half_show <= 0:
                # 页码起始值
                page_start = 1
                # 页码终止值
                page_end = max_show
            elif self.page + half_show > total_num:
                page_end = total_num
                page_start = total_num - max_show + 1
            else:
                # 页码起始值
                page_start = self.page - half_show
                # 页码终止值
                page_end = self.page + half_show

        self.total_num = total_num
        self.page_start = page_start
        self.page_end = page_end
        self.start = (self.page - 1) * per_num
        self.end = self.page * per_num

    @property
    def page_html(self):
        li_list = []
        if self.page == 1:
            li_list.append(
                '<li class="disabled"><a href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>')
        else:
            self.params['page'] = self.page - 1
            li_list.append(
                '<li><a href="?" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(
                    self.params.urlencode()))
        for i in range(self.page_start, self.page_end + 1):
            self.params['page'] = i
            if i == self.page:
                li_list.append('<li class="active"><a href="{}">{}</a></li>'.format(self.params.urlencode(), i))
            else:
                li_list.append('<li><a href="?{}">{}</a></li>'.format(self.params.urlencode(), i))

        if self.page == self.total_num:
            li_list.append(
                '<li class="disabled"><a href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>')
        else:
            self.params['page'] = self.page + 1
            li_list.append(
                '<li><a href="?{}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                    self.params.urlencode()))

        return ''.join(li_list)
