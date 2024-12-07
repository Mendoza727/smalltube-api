from django.urls import path
from .views import *

urlpatterns = [
    # category,
    path('create-category/',  CreateCategorysView.as_view(), name="create-category"),
    path('get-categories-by-id/', GetCategoryByIdsView.as_view(), name="get-categories-by-id"),
    path('get-categorys/', GetCategorysView.as_view(), name="get-categorys"),

    # video,
    path('get-video-by-autor/', getVideosByAutorView.as_view(), name="get-video-by-autor"),
    path('get-all-videos/', getAllVideosView.as_view(), name="get-all-videos"),
    path('video/', VideoRegisterView.as_view(), name="create-video"),
    path('videos-edit/<int:pk>/', VideoUpdateView.as_view(), name='update-video'),
    path('videos-delete/<int:pk>/', VideoDeleteView.as_view(), name='delete-video'),

    # user,
    path('login/', UserLoginApiView.as_view(), name='user-login'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('verify/', VerifyEmailView.as_view(), name="verify"),

    # like,
    path('likes-create/', CreateLikeView.as_view(), name='create-like'),
    path('likes-delete/', DeleteLikeView.as_view(), name='delete-like'),

    # visualitation
    path('visualizations-create/', CreateVisualizationView.as_view(), name='create-visualization'),

    # comments
    path('comments-create/', CreateCommentView.as_view(), name='create_comment'),
    path('get-comments/<int:video_id>/', GetCommentsView.as_view(), name='get_comments'),
    path('comments-edit/<int:id_video>/<int:user_id>/', EditCommentView.as_view(), name='edit_comment'),
    path('comments-delete/<int:comment_id>/', DeleteCommentView.as_view(), name='delete_comment'),


    # video statistics
     path('videos-statistics/<int:video_id>/', GetVideoStatisticsView.as_view(), name='get_video_statistics'),

    

    # notifications
    path('notifications/<int:user_id>/', GetUserNotificationsView.as_view(), name='get_user_notifications'),
    path('notifications/<int:user_id>/mark-all-read/', MarkAllNotificationsReadView.as_view(), name='mark_all_read'),
    path('notifications/<int:user_id>/mark-all-unread/', MarkAllNotificationsUnreadView.as_view(), name='mark_all_unread'),
    path('notifications/<int:notification_id>/mark-read/', MarkNotificationReadByIdView.as_view(), name='mark_notification_read'),
]
