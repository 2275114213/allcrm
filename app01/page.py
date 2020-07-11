class Pagination(object):

    # 初始化
    def __init__(self,current_page_num,all_acount,request,per_page_num=10,pager_count=11):
        """

        :param current_page_num:  当前页的数字
        :param all_acount:        所有数据的总数
        :param request:
        :param per_page_num:      每页显示的数
        :param pager_count:       最多显示的页码个数
        """
        try:
            current_page_num=int(current_page_num)
        except Exception as e:
            current_page_num = 1
        if current_page_num < 1 :
            current_page_num = 1
        self.current_page_num=current_page_num
        self.all_acount=all_acount
        self.per_page_num=per_page_num
        self.num=(self.current_page_num-1) * (self.per_page_num)



        #实际总页数:
        all_pager,tmp = divmod(all_acount,per_page_num)

        #可以省略几部
        # if tmp :
        #     all_pager=all_pager+1
        # else:
        #     all_pager=all_pager

        if tmp:
            all_pager+=1
        self.all_pager=all_pager

        if current_page_num > self.all_pager:
            self.current_page_num=1

        #限制显示总页数的一半,好前几后几的显示
        self.pager_count=pager_count
        self.pager_count_half = int((pager_count - 1) / 2)



        #保存搜索条件(这是那边把request传过来的原因)
        import copy
        self.params = copy.deepcopy(request.GET)    # 此时是字典形式{"a":"1","b":"2"}





    @property
    def start(self):

        # 注意条件
        return (self.current_page_num-1) * self.per_page_num

    @property
    def end(self):
        # 注意条件
        return  self.current_page_num * self.per_page_num

    # 显示前五后五,最多显示十一页,当前页居中


    #  为了渲染页面
    def page_html(self):
        # 如果页码总数小于11页
        if self.all_pager <= self.pager_count:
            page_start=1
            page_end=self.all_pager+1

        else:

            #限制前面 ,因为1,2,3,4,5 没有前五页
            if self.current_page_num <= self.pager_count_half:
                page_start = 1
                page_end = self.pager_count + 1

            else:

                # 当前页有限制后面,有后五页的时候
                if (self.current_page_num + self.pager_count_half)  <=self.all_pager:
                    page_start = self.current_page_num - self.pager_count_half
                    page_end = self.current_page_num + self.pager_count_half + 1
                else:
                    #当前页没有后五页的时候
                    page_start = self.all_pager - self.pager_count + 1
                    page_end = self.all_pager+1

        page_html_list=[]
        first_page = '<li><a href="?page=%s">首页</a></li>' % (1,)
        page_html_list.append(first_page)
        if self.current_page_num-1 > 0:
            page_html_list.append(' <li ><a href="#">上一页</a></li>')
        else:
            page_html_list.append(' <li class="disabled"><a href="?page=%s">上一页</a></li>' % (self.current_page_num - 1))

        for i in range(page_start,page_end):
            self.params['page'] = i
            if i == self.current_page_num:
                temp = '<li class="active"><a href="?%s">%s</a></li>' % (self.params.urlencode(), i)

            else:
                temp = '<li><a href="?%s">%s</a></li>' % (self.params.urlencode(), i)
            page_html_list.append(temp)
        if self.current_page_num + 1 >=self.all_pager:
            page_html_list.append(' <li class="disabled"><a href="#">下一页</a></li>' )
        else:
            page_html_list.append(' <li ><a href="?page=%s">下一页</a></li>' % (self.current_page_num - 1))

        last_page = '<li><a href="?page=%s">尾页</a></li>' % (self.all_pager)
        page_html_list.append(last_page)

        #     返回列表
        return "".join(page_html_list)