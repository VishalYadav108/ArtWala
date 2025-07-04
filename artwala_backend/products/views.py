from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category, Product, Cart, CartItem, Order, Wishlist
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    CartSerializer, 
    CartItemSerializer,
    OrderSerializer, 
    WishlistSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_wishlist(self, request, slug=None):
        """
        Add a product to the user's wishlist
        """
        product = self.get_object()
        user = request.user
        
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=user,
            product=product
        )
        
        if created:
            return Response(
                {'message': f'Added {product.title} to your wishlist'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'message': f'This product is already in your wishlist'},
                status=status.HTTP_200_OK
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_from_wishlist(self, request, slug=None):
        """
        Remove a product from the user's wishlist
        """
        product = self.get_object()
        user = request.user
        
        try:
            wishlist_item = Wishlist.objects.get(
                user=user,
                product=product
            )
            wishlist_item.delete()
            
            return Response(
                {'message': f'Removed {product.title} from your wishlist'},
                status=status.HTTP_200_OK
            )
        except Wishlist.DoesNotExist:
            return Response(
                {'error': f'This product is not in your wishlist'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_cart(self, request, slug=None):
        """
        Add a product to the user's cart
        """
        product = self.get_object()
        user = request.user
        quantity = int(request.data.get('quantity', 1))
        
        # Get or create a cart for the user
        cart, _ = Cart.objects.get_or_create(user=user)
        
        # Check if item already in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Update quantity if item already exists
            cart_item.quantity += quantity
            cart_item.save()
        
        serializer = CartItemSerializer(cart_item)
        return Response(
            {
                'message': f'Added {product.title} to your cart',
                'cart_item': serializer.data
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Get the user's cart or create one if it doesn't exist
        """
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """
        Add an item to the cart
        """
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        if not product_id:
            return Response(
                {'error': 'Product ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """
        Remove an item from the cart
        """
        item_id = request.data.get('item_id')
        
        if not item_id:
            return Response(
                {'error': 'Item ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.delete()
            
            return Response(
                {'message': 'Item removed from cart'},
                status=status.HTTP_200_OK
            )
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Cart not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found in cart'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def update_item_quantity(self, request):
        """
        Update the quantity of an item in the cart
        """
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')
        
        if not item_id or not quantity:
            return Response(
                {'error': 'Item ID and quantity are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response(
                    {'error': 'Quantity must be greater than 0'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {'error': 'Quantity must be a number'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.quantity = quantity
            cart_item.save()
            
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Cart not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found in cart'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """
        Clear all items from the cart
        """
        try:
            cart = Cart.objects.get(user=request.user)
            CartItem.objects.filter(cart=cart).delete()
            
            return Response(
                {'message': 'Cart cleared'},
                status=status.HTTP_200_OK
            )
        except Cart.DoesNotExist:
            return Response(
                {'message': 'Cart is already empty'},
                status=status.HTTP_200_OK
            )

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def products(self, request):
        """
        Get all products in the user's wishlist
        """
        wishlist_items = Wishlist.objects.filter(user=request.user)
        products = [item.product for item in wishlist_items]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
