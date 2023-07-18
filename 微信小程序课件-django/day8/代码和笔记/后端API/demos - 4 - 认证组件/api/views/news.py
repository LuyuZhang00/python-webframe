from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView,RetrieveAPIView
from rest_framework import status
from api import models

from django.forms import model_to_dict
from django.db.models import F

from utils.auth import GeneralAuthentication

class NewsModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()

    class Meta:
        model = models.News
        fields = ['id', 'cover', 'content', 'topic', "user", 'favor_count']

    def get_user(self, obj):
        return model_to_dict(obj.user, fields=['id', 'nickname', 'avatar'])

    def get_topic(self, obj):
        if not obj.topic:
            return
        return model_to_dict(obj.topic, fields=['id', 'title'])


# ############################# 动态列表 #############################
from utils.filters import MaxFilterBackend, MinFilterBackend
from utils.pagination import OldBoyLimitPagination


class NewsView(ListAPIView):
    serializer_class = NewsModelSerializer
    queryset = models.News.objects.all().order_by('-id')

    pagination_class = OldBoyLimitPagination
    filter_backends = [MinFilterBackend, MaxFilterBackend]


# ############################# 动态详细 #############################

class NewsDetailModelSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    user = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()

    viewer = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()

    class Meta:
        model = models.News
        exclude = ['cover',]

    def get_images(self,obj):
        detail_queryset = models.NewsDetail.objects.filter(news=obj)
        # return [row.cos_path for row in detail_queryset]
        # return [{'id':row.id,'path':row.cos_path} for row in detail_queryset]
        return [model_to_dict(row,['id','cos_path']) for row in detail_queryset]

    def get_user(self, obj):
        return model_to_dict(obj.user, fields=['id', 'nickname', 'avatar'])

    def get_topic(self, obj):
        if not obj.topic:
            return
        return model_to_dict(obj.topic, fields=['id', 'title'])

    def get_viewer(self,obj):
        # 根据新闻的对象 obj(news)
        # viewer_queryset = models.ViewerRecord.objects.filter(news_id=obj.id).order_by('-id')[0:10]
        queryset = models.ViewerRecord.objects.filter(news_id=obj.id)
        viewer_object_list = queryset.order_by('-id')[0:10]
        context = {
            'count':queryset.count(),
            'result': [model_to_dict(row.user,['nickname','avatar']) for row in viewer_object_list]
        }
        return context

    def get_comment(self,obj):
        """
        获取所有的1级评论，再给每个1级评论获取一个耳机评论。
        :param obj:
        :return:
        """

        # 1.获取所有的 一级 评论
        first_queryset = models.CommentRecord.objects.filter(news=obj,depth=1).order_by('id')[0:10].values(
            'id',
            'content',
            'depth',
            'user__nickname',
            'user__avatar',
            'create_date'
        )
        first_id_list = [ item['id'] for item in first_queryset]
        # 2.获取所有的二级评论
        # second_queryset = models.CommentRecord.objects.filter(news=obj,depth=2)
        # 2. 获取所有1级评论下的二级评论
        # second_queryset = models.CommentRecord.objects.filter(news=obj, depth=2,reply_id__in=first_id_list)
        # 2. 获取所有1级评论下的二级评论(每个二级评论只取最新的一条)
        from django.db.models import Max
        result = models.CommentRecord.objects.filter(news=obj, depth=2, reply_id__in=first_id_list).values('reply_id').annotate(max_id=Max('id'))
        second_id_list = [item['max_id'] for item in result] # 5, 8

        second_queryset = models.CommentRecord.objects.filter(id__in=second_id_list).values(
            'id',
            'content',
            'depth',
            'user__nickname',
            'user__avatar',
            'create_date',
            'reply_id',
            'reply__user__nickname'
        )

        import collections
        first_dict = collections.OrderedDict()
        for item in first_queryset:
            item['create_date'] = item['create_date'].strftime('%Y-%m-%d')
            first_dict[item['id']] = item

        for node in second_queryset:
            first_dict[node['reply_id']]['child'] = [node,]

        return first_dict.values()


class NewsDetailView(RetrieveAPIView):
    queryset = models.News.objects
    serializer_class = NewsDetailModelSerializer

    def get(self,request, *args,**kwargs):

        response = super().get(request, *args,**kwargs)
        if not request.user:
            return response
        # 判断当前用户是否有访问此新闻的记录？
        news_object = self.get_object() # models.News.objects.get(pk=pk)
        exists = models.ViewerRecord.objects.filter(user=request.user,news=news_object).exists()
        if exists:
            return response
        models.ViewerRecord.objects.create(user=request.user,news=news_object)
        models.News.objects.filter(id=news_object.id).update(viewer_count=F('viewer_count')+1)

        return response

# ############################# 话题  #############################
class TopicModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topic
        fields = "__all__"


class TopicView(ListAPIView):
    serializer_class = TopicModelSerializer
    queryset = models.Topic.objects.all().order_by('-id')

    pagination_class = OldBoyLimitPagination
    filter_backends = [MinFilterBackend, MaxFilterBackend]


# ############################# 获取所有子评论  #############################
"""
 {
    "id": 5,
    "content": "1-2",
    "user__nickname": "大卫-6",
    "user__avatar": "https://mini-1251317460.cos.ap-chengdu.myqcloud.com/08a9daei1578736867828.png",
    "create_date": "2020-01-15T07:46:35.434290Z",
    "reply_id": 1,
    "reply__user__nickname": "wupeiqi"
}

"""
class CommentModelSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format='%Y-%m-%d')
    user__nickname = serializers.CharField(source='user.nickname')
    user__avatar = serializers.CharField(source='user.avatar')
    reply_id = serializers.CharField(source='reply.id')
    reply__user__nickname = serializers.CharField(source='reply.user.nickname')
    class Meta:
        model = models.CommentRecord
        exclude = ['news','user','reply','root']


class CreateCommentModelSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format='%Y-%m-%d',read_only=True)
    user__nickname = serializers.CharField(source='user.nickname',read_only=True)
    user__avatar = serializers.CharField(source='user.avatar',read_only=True)
    reply_id = serializers.CharField(source='reply.id',read_only=True)
    reply__user__nickname = serializers.CharField(source='reply.user.nickname',read_only=True)

    class Meta:
        model = models.CommentRecord
        # fields = "__all__"
        exclude = ['user','favor_count']

class CommentView(APIView):

    def get(self,request,*args,**kwargs):
        root_id = request.query_params.get('root')
        # 1. 获取这个根评论的所有子孙评论
        node_queryset = models.CommentRecord.objects.filter(root_id=root_id).order_by('id')
        # 2. 序列化
        ser = CommentModelSerializer(instance=node_queryset,many=True)

        return Response(ser.data,status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        # 1. 进行数据校验: news/depth/reply/content/root
        ser = CreateCommentModelSerializer(data=request.data)
        if ser.is_valid():
            # 保存到数据库
            ser.save(user_id=1)
            # 对新增到的数据值进行序列化(数据格式需要调整)
            news_id = ser.data.get('news')
            models.News.objects.filter(id=news_id).update(comment_count=F('comment_count')+1)

            return Response(ser.data,status=status.HTTP_201_CREATED)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
























