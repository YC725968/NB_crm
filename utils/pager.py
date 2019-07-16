from django.utils.safestring import mark_safe
class PageInfo(object):
    def __init__(self,current_page,all_count,base_url,per_page,show_page=11):
        '''

        :param current_page:
        :param all_count: 数据库总行数
        :param per_page:每页显示函数
        '''
        try:
            self.current_page = int(current_page)
            # self.per_page = per_page
        except Exception as e:
            self.current_page = 1
        self.per_page = per_page
        a,b = divmod(all_count,per_page)
        if b:
            a = a+1
        self.all_page = a
        self.show_page =show_page
        self.base_url = base_url
    @property
    def start(self):
        return (self.current_page-1)*self.per_page
    @property
    def end(self):
        return self.current_page*self.per_page
    @property
    def pager(self):
        page_list = []
        half = int((self.show_page-1)/2)
        #如果数据库总页数《11
        if self.all_page < self.show_page:
            begin =1
            stop = self.all_page+1
            #总页数大于11
        else :
            #如果当前页《=5，永远显示1-11
            if self.current_page <= half:
                begin = 1
                stop = self.show_page+1
            else:
                if self.current_page +half > self.all_page:
                    begin = self.all_page -self.show_page+1
                    stop = self.all_page+1
                else:
                    begin = self.current_page - half
                    stop = self.current_page+half+1
        # begin = self.current_page-half
        # stop = self.current_page+half+1
        first_li = '<li><a href="{}?page=1">首页</a></li>'.format(self.base_url)
        page_list.append(first_li)
        if self.current_page <=1:
            prev = "<li><a href='#'><<</a></li>"
        else:
            prev = "<li><a href='{}?page={}'><<</a></li>".format(self.base_url,self.current_page-1)
        page_list.append(prev)
        for i in range(begin,stop):
            if i ==self.current_page:
                temp = "<li class='active'><a href='{}?page={}'>{}</a></li>".format(self.base_url,i,i,)
            else:
                temp = "<li><a href='{}?page={}'>{}</a></li>" .format(self.base_url,i,i,)
            page_list.append(temp)
        if self.current_page >=self.all_page:
            nex = "<li><a href='#'>>></a></li>"
        else:
            nex = "<li><a href='{}?page={}'>>></a></li>" .format(self.base_url,
                        self.current_page +1)
        page_list.append(nex)
        last_li = '<li><a href="{1}?page={0}">尾页</a></li>'.format(self.all_page, self.base_url)
        page_list.append(last_li)
        return mark_safe(''.join(page_list))