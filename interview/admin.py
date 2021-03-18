import logging
import csv

from datetime import datetime
from django.contrib import admin, messages
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.utils.safestring import mark_safe


from .tasks import send_dingtalk_message
from interview.models import Candidate
from interview import candidate_fieldset as cf
from jobs.models import Resume

# Register your models here.

logger = logging.getLogger(__name__)

exportable_fields = ('username', 'city', 'phone', 'bachelor_school', 'master_school', 'degree', 'first_result',
                     'first_interviewer_user', 'second_result', 'second_interviewer_user', 'hr_result', 'hr_score',
                     'hr_remark', 'hr_interviewer_user')

# 通知一面面试官面试


def notify_interviewer(modeladmin, request, queryset):
    candidates = ""
    interviewers = ""
    for obj in queryset:
        candidates = obj.username + ";" + candidates
        interviewers = obj.first_interviewer_user.username + ";" + interviewers
    # 这里的消息发送到钉钉， 或者通过 Celery 异步发送到钉钉
    #send ("候选人 %s 进入面试环节，亲爱的面试官，请准备好面试： %s" % (candidates, interviewers) )
    send_dingtalk_message.delay(
        "候选人 %s 进入面试环节，亲爱的面试官: %s 请准备好面试. " % (candidates, interviewers))
    messages.add_message(request, messages.INFO, '已成功发送面试通知')


notify_interviewer.short_description = u'通知一面面试官'


def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    field_list = exportable_fields
    response['Content-Disposition'] = 'attachment; filename=recruitment-candidates-list-%s.csv' % (
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )

    ### 写入表头
    writer = csv.writer(response)
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list]
    )

    for obj in queryset:
        ### 单行的记录（各个字段的值），写入到csv文件
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)

    #logger.error("%s has exported %s candidate records" % (request.user.username, len(queryset)))
    logger.info("%s exported %s candidate records" % (request.user, len(queryset)))

    return response


export_model_as_csv.short_description = u'导出为CSV文件'
export_model_as_csv.allowed_permissions = ('export',)


class CandidateAdmin(admin.ModelAdmin):
    exclude = ('creator', 'created_date', 'modified_date')

    actions = (export_model_as_csv, notify_interviewer,)

    ### 当前用户是否有导出权限
    def has_export_permission(self, request):
        opts = self.opts
        return request.user.has_perm('%s.%s' % (opts.app_label, "export"))

    list_display = (
        'username', 'city', 'bachelor_school', 'get_resume', 'first_score', 'first_result', 'first_interviewer_user',
        'second_result', 'second_interviewer_user', 'hr_score', 'hr_result', 'last_editor')

    # 筛选条件
    list_filter = ('city', 'first_result', 'second_result', 'hr_result', 'first_interviewer_user',
                   'second_interviewer_user', 'hr_interviewer_user')

    # 查询字段
    search_fields = ('username', 'phone', 'email', 'bachelor_school')

    ordering = ('hr_result', 'second_result', 'first_result')

    def get_resume(self, obj):
        if not obj.phone:
            return ""
        resumes = Resume.objects.filter(phone=obj.phone)
        if resumes and len(resumes) > 0:
            return mark_safe(u'<a href="/resume/%s" target="_blank">%s</a>' % (resumes[0].id, "查看简历"))
        return ""
    
    get_resume.short_description = '查看简历'
    get_resume.allow_tags = True

    ### readonly_fields = ('first_interviewer_user', 'second_interviewer_user')

    default_list_editable = ('first_interviewer_user', 'second_interviewer_user')

    def get_list_editable(self, request):
        group_names = self.get_group_names(request.user)

        if request.user.is_superuser or 'hr' in group_names:
            return self.default_list_editable
        return ()

    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin, self).get_changelist_instance(request)

    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        return group_names

    def get_queryset(self, request):
        qs = super(CandidateAdmin, self).get_queryset(request)

        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return qs
        return Candidate.objects.filter(
            Q(first_interviewer_user=request.user) | Q(second_interviewer_user=request.user)
        )

    def get_readonly_fields(self, request, obj):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names:
            logger.info("interviewer is in user's group for %s" % request.user.username)
            return ('first_interviewer_user', 'second_interviewer_user',)
        return ()

    def get_fieldsets(self, request, obj=None):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names and obj.first_interviewer_user == request.user:
            return cf.default_fieldsets_first
        if 'interviewer' in group_names and obj.second_interviewer_user == request.user:
            return cf.default_fieldsets_second
        return cf.default_fieldsets

    def save_model(self, request, obj, form, change):
        obj.last_editor = request.user.username
        if not obj.creator:
            obj.creator = request.user.username
        obj.modified_date = datetime.now()
        obj.save()


admin.site.register(Candidate, CandidateAdmin)
