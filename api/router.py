from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from api.sale.views import SaleAPIView
from api.users.views import UsersAPIViewSwt
from api.uom.views import UomAPIView, UomGroupAPIView
from api.product.views import CategoryAPIView, ProductAPIView, WarehouseProductAPIView

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register(r'user', UsersAPIViewSwt, basename='user')
router.register(r'uom', UomAPIView, basename='uom')
router.register(r'uom-group', UomGroupAPIView, basename='uom-group')
router.register(r'category', CategoryAPIView, basename='category')
router.register(r'product', ProductAPIView, basename='product')
router.register(r'warehouse-product', WarehouseProductAPIView, basename='warehouse-product')
router.register(r'sale', SaleAPIView, basename='sale')
urlpatterns = router.urls
