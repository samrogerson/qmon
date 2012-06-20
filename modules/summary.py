from collections import defaultdict

def user_status_from_queue_status(d):
    # get our unique list of users
    user_list = []
    for q_info in d.values():
        user_list += q_info.keys()
    user_set = set(user_list)

    user_statuses = defaultdict(dict)
    default_status = {'r':0, 'qw':0, 'o':0}
    for q, user_dict in d.iteritems():
        for user, status_dict in user_dict.iteritems():
            user_statuses[user][q] = status_dict
    return user_statuses

def per_user(analyzer, title=False, pl = None):
    output_format = "{u:<10}"
    per_queue_format = "[{r:>3},{q:>4},{o:>4}] "
    queue_title_format = "{q:<16}"

    output_banner ="{:=^10}".format("")
    output_sub_banner ="{:-^10}".format("")
    queue_banner_base = "=={:=^3}={:=^4}={:=^4}=".format("","","")
    queue_sub_banner_base = "--{:-^3}-{:-^4}-{:-^4}-".format("","","")

    banner = output_banner
    sub_banner = output_sub_banner
    for q in analyzer.queues:
        banner += queue_banner_base
        sub_banner += queue_sub_banner_base

    print banner
    queue_title_str = output_format.format(u="User")
    all_titles = [ queue_title_format.format(q=q) for q in analyzer.queues ]
    queue_title_str += "".join(all_titles)
    print queue_title_str
    print sub_banner

    q_dict = analyzer.get_queue_job_counts()
    user_status = user_status_from_queue_status(q_dict)

    default_statuses = { 'r': 0, 'qw': 0, 'o': 0 }
    for user, job_info in user_status.iteritems():
        u_string = output_format.format(u=user)
        for queue in analyzer.queues:
            r = job_info.get(queue,default_statuses).get('r',0)
            q = job_info.get(queue,default_statuses).get('qw',0)
            o = job_info.get(queue,default_statuses).get('o',0)
            u_string += per_queue_format.format(r=r, q=q, o=o)
        print u_string

    if title :
        print banner

def per_queue(analyzer, output_format = None, pl = None) :
    output_format = "{q:<12} {a:>8} {t:>8}"
    banner_format = "{:=^12}={:=^8}={:=^8}"
    sub_banner_format = "{:-^12}-{:-^8}-{:-^8}"
    banner = banner_format.format("","","")
    sub_banner = sub_banner_format.format("","","")

    q_dict = analyzer.get_queue_status()
    print banner
    print output_format.format(q="Queue", a="Free", t="Total")
    print sub_banner

    for q, cores in q_dict.iteritems() :
        print output_format.format(q=q, a=cores['a'], t=cores['t'])

    print banner
