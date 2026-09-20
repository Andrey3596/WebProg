from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker
from orders.models import Category, Dish, Order, OrderItem
from django.contrib.auth.models import User
# Create your tests here.
   
        
class CategorysViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
    def test_get_list(self):
        baker.make("orders.Category", 3)
        r = self.client.get('/api/categories/')
        data = r.json()
        print(data)
        assert len(data) == 3
        
    def test_create_category(self):
        r = self.client.post('/api/categories/', {
            'name': 'Новая категория',
        })
        new_id = r.json()['id']

        categories = Category.objects.all()
        assert len(categories) == 1

        new_category = Category.objects.filter(id=new_id).first()
        assert new_category.name == 'Новая категория'    
     
    def test_delete_category(self):
        categories = baker.make("orders.Category", 10)

        r = self.client.get('/api/categories/')
        data = r.json()
        assert len(data) == 10

        category_id_to_delete = categories[3].id
        self.client.delete(f'/api/categories/{category_id_to_delete}/')

        r = self.client.get('/api/categories/')
        data = r.json()
        assert len(data) == 9
        assert category_id_to_delete not in [i['id'] for i in data] 
     
     
    def test_update_category(self):
        categories = baker.make("orders.Category", 3)
        category = categories[1]

        r = self.client.get(f'/api/categories/{category.id}/')
        data = r.json()
        assert data['name'] == category.name

        r = self.client.put(f'/api/categories/{category.id}/', {
            'name': 'Обновлённая категория',
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/categories/{category.id}/')
        data = r.json()
        assert data['name'] == 'Обновлённая категория'

        category.refresh_from_db()
        assert data['name'] == category.name 
     
  
        
class DishsViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
    def test_get_list(self):
        baker.make("orders.Dish", 3)
        r = self.client.get('/api/dishes/')
        data = r.json()
        print(data)
        assert len(data) == 3
        
  
    def test_create_dish(self):
            category = baker.make("orders.Category")
    
            r = self.client.post('/api/dishes/', {
                'name': 'Борщ',
                'description': 'Вкусный суп',
                'price': '250.00',
                'category_id': category.id,
            })
            new_id = r.json()['id']
    
            dishes = Dish.objects.all()
            assert len(dishes) == 1
    
            new_dish = Dish.objects.filter(id=new_id).first()
            assert new_dish.name == 'Борщ'
            assert new_dish.category == category 
         
         
    def test_delete_dish(self):
            dishes = baker.make("orders.Dish", 10)
    
            r = self.client.get('/api/dishes/')
            data = r.json()
            assert len(data) == 10
    
            dish_id_to_delete = dishes[3].id
            self.client.delete(f'/api/dishes/{dish_id_to_delete}/')
    
            r = self.client.get('/api/dishes/')
            data = r.json()
            assert len(data) == 9
            assert dish_id_to_delete not in [i['id'] for i in data]
         
         
    def test_update_dish(self):
            category = baker.make("orders.Category")           
            dishes = baker.make("orders.Dish", 3, category=category)  
            dish = dishes[1]
    
            r = self.client.get(f'/api/dishes/{dish.id}/')
            data = r.json()
            assert data['name'] == dish.name
    
            r = self.client.put(f'/api/dishes/{dish.id}/', {
                'name': 'Обновлённое блюдо',
                'description': 'Новое описание',
                'price': '300.00',
                'category_id': dish.category.id,
            })
            assert r.status_code == 200
    
            r = self.client.get(f'/api/dishes/{dish.id}/')
            data = r.json()
            assert data['name'] == 'Обновлённое блюдо'
    
            dish.refresh_from_db()
            assert data['name'] == dish.name
  
  
class OrdersViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
    def test_get_list(self):
        baker.make("orders.Order", 3)
        r = self.client.get('/api/orders/')
        data = r.json()
        print(data)
        assert len(data) == 3
    
    def test_create_order(self):
        user = baker.make(User)

        r = self.client.post('/api/orders/', {
            'user_id': user.id,
            'status': 'processing',
            'total_amount': '0.00',
        })
        new_id = r.json()['id']

        orders = Order.objects.all()
        assert len(orders) == 1

        new_order = Order.objects.filter(id=new_id).first()
        assert new_order.user == user
        assert new_order.status == 'processing'
  
    def test_delete_order(self):
        orders = baker.make("orders.Order", 10)

        r = self.client.get('/api/orders/')
        data = r.json()
        assert len(data) == 10

        order_id_to_delete = orders[3].id
        self.client.delete(f'/api/orders/{order_id_to_delete}/')

        r = self.client.get('/api/orders/')
        data = r.json()
        assert len(data) == 9
        assert order_id_to_delete not in [i['id'] for i in data]
  
  
    def test_update_order(self):
        orders = baker.make("orders.Order", 3)
        order = orders[1]

        r = self.client.get(f'/api/orders/{order.id}/')
        data = r.json()
        assert data['status'] == order.status

        r = self.client.put(f'/api/orders/{order.id}/', {
            'user_id': order.user.id,
            'status': 'ready',
            'total_amount': '500.00',
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/orders/{order.id}/')
        data = r.json()
        assert data['status'] == 'ready'

        order.refresh_from_db()
        assert data['status'] == order.status
  
  
        
        
class OrderItemsViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
    def test_get_list(self):
        baker.make("orders.OrderItem", 3)
        r = self.client.get('/api/orderitems/')
        data = r.json()
        print(data)
        assert len(data) == 3
    
    def test_create_orderitem(self):
        order = baker.make("orders.Order")
        dish = baker.make("orders.Dish")

        r = self.client.post('/api/orderitems/', {
            'order': order.id,
            'dish_id': dish.id,
            'quantity': 2,
            'price': '250.00',
        })
        new_id = r.json()['id']

        items = OrderItem.objects.all()
        assert len(items) == 1

        new_item = OrderItem.objects.filter(id=new_id).first()
        assert new_item.dish == dish
        assert new_item.order == order
        assert new_item.quantity == 2
        
    def test_delete_orderitem(self):
        items = baker.make("orders.OrderItem", 10)

        r = self.client.get('/api/orderitems/')
        data = r.json()
        assert len(data) == 10

        item_id_to_delete = items[3].id
        self.client.delete(f'/api/orderitems/{item_id_to_delete}/')

        r = self.client.get('/api/orderitems/')
        data = r.json()
        assert len(data) == 9
        assert item_id_to_delete not in [i['id'] for i in data]
        
    
    def test_update_orderitem(self):
        items = baker.make("orders.OrderItem", 3)
        item = items[1]

        r = self.client.get(f'/api/orderitems/{item.id}/')
        data = r.json()
        assert data['quantity'] == item.quantity

        r = self.client.put(f'/api/orderitems/{item.id}/', {
            'order': item.order.id,
            'dish_id': item.dish.id,
            'quantity': 5,
            'price': '999.00',
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/orderitems/{item.id}/')
        data = r.json()
        assert data['quantity'] == 5

        item.refresh_from_db()
        assert data['quantity'] == item.quantity