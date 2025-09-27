from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, GenericAPIView
from .models import *
from .serializers import *
import stripe
from datetime import datetime

stripe.api_key = settings.STRIPE_SECRET_KEY

# --------------------------
# CATEGORY VIEWS
# --------------------------
class CategoryListView(ListAPIView):
    authentication_classes = []
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class LetteringItemCategoryListView(ListAPIView):
    authentication_classes = []
    serializer_class = LetteringItemCategorySerializer
    queryset = LetteringItemCategory.objects.all()


# --------------------------
# PRODUCT VIEWS
# --------------------------
class ProductListView(ListAPIView):
    authentication_classes = []
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductFromCategoryListView(ListAPIView):
    authentication_classes = []
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        category_id = self.kwargs.get(self.lookup_url_kwarg)
        return Product.objects.filter(category__id=category_id)


class ProductColorListView(ListAPIView):
    authentication_classes = []
    serializer_class = ProductColorSerializer
    queryset = ProductColor.objects.all()


class LogoListView(ListAPIView):
    authentication_classes = []
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(category__title='Truck Sign', is_uploaded=False)


class ProductDetail(RetrieveAPIView):
    authentication_classes = []
    serializer_class = ProductSerializer
    lookup_field = 'id'
    queryset = Product.objects.all()


class ProductVariationRetrieveView(RetrieveAPIView):
    authentication_classes = []
    serializer_class = ProductVariationSerializer
    lookup_field = 'id'
    queryset = ProductVariation.objects.all()


# --------------------------
# ORDER VIEWS
# --------------------------
class CreateOrder(GenericAPIView):
    authentication_classes = []
    serializer_class = OrderSerializer

    def post(self, request, id, format=None):
        data = request.data
        product = Product.objects.get(id=id)
        product_variation = ProductVariation(product=product)
        product_variation.save()

        lettering_items = data.get('lettering_items', [])
        for custom_item in lettering_items:
            if custom_item.get('text') and custom_item['text'].strip():
                item_category = LetteringItemCategory.objects.get(title=custom_item['title'])
                lettering_item = LetteringItemVariation(
                    lettering_item_category=item_category,
                    lettering=custom_item['text'],
                    product_variation=product_variation
                )
                lettering_item.save()

        product_color = None
        try:
            product_color = ProductColor.objects.get(id=data['product_color_id'])
        except:
            pass

        product_variation.product_color = product_color
        product_variation.amount = 1
        product_variation.save()

        order_serializer = OrderSerializer(data=data['order'])
        order_serializer.is_valid(raise_exception=True)
        order = order_serializer.save(product=product_variation, payment=None)
        order_serializer = OrderSerializer(order)

        return Response({"Result": order_serializer.data}, status=status.HTTP_200_OK)


class RetrieveOrder(RetrieveAPIView):
    authentication_classes = []
    serializer_class = OrderSerializer
    lookup_field = 'id'
    queryset = Order.objects.all()


class PaymentView(GenericAPIView):
    authentication_classes = []
    serializer_class = PaymentSerializer

    def get(self, request, id, format=None):
        order = Order.objects.get(id=id)
        serializer = OrderSerializer(order)
        return Response({"Order": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, id, format=None):
        try:
            order = Order.objects.get(id=id)
            order_serializer = OrderSerializer(order, data=request.data.get('order', {}), partial=True)
            order_serializer.is_valid(raise_exception=True)
            order = order_serializer.save()

            token = stripe.Token.create(
                card={
                    "number": request.data['card_num'],
                    "exp_month": int(request.data['exp_month']),
                    "exp_year": int(request.data['exp_year']),
                    "cvc": request.data['cvc']
                }
            )

            amount = int(order.get_total_price() * 100)
            charge = stripe.Charge.create(amount=amount, currency="usd", source=token)

            payment = Payment(user_email=order.user_email, stripe_charge_id=charge['id'], amount=amount)
            payment.save()
            order.ordered = True
            order.payment = payment
            order.save()

            return Response({"Result": "Success"}, status=status.HTTP_200_OK)

        except stripe.error.StripeError:
            return Response({"Result": "Stripe payment error"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Result": f"Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


# --------------------------
# COMMENT VIEWS
# --------------------------
class CommentsView(ListAPIView):
    authentication_classes = []
    serializer_class = CommentSerializer
    queryset = Comment.objects.filter(visible=True)


class CommentCreateView(CreateAPIView):
    authentication_classes = []
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


# --------------------------
# UPLOAD CUSTOMER IMAGE
# --------------------------
class UploadCustomerImage(GenericAPIView):
    authentication_classes = []

    def post(self, request, format=None):
        data = request.data
        product_title = f"Customer-Image-{datetime.now()}"
        category = Category.objects.get(title="Truck Sign")
        product = Product(category=category, title=product_title, is_uploaded=True)
        product.save()

        serializer = ProductSerializer(product, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        product.detail_image = product.image
        product.save()
        serializer = ProductSerializer(product)
        return Response({"Result": serializer.data}, status=status.HTTP_200_OK)
