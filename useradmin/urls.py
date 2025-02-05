from django.urls import path
from useradmin import views

app_name = "useradmin"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("products/", views.products, name="products"),
    path("add_product/", views.add_product, name="add_product"),
    path("edit_product/<pid>/", views.edit_product, name="edit_product"),
    path("delete_product/<pid>/", views.delete_product, name="delete_product"),
    path("manage-users/", views.manage_users_view, name="manage_users"),

    path('fornitore/', views.fornitore_view, name='fornitore-view'),
    path('fornitore/modifica/', views.fornitore_update, name='fornitore-update'),
]